"""
YAML → Qdrant 인제스트 파이프라인

실행: python yaml_qdrant_ingest.py

흐름:
  1. 사용자 입력 → collection 이름
  2. Qdrant에 collection 생성 (size=1024, COSINE) — 이미 있으면 그대로 사용
  3. ./data 하위 .yaml / .yml 파일 재귀 탐색
  4. 각 파일을 의미 단위로 chunking
       - --- 구분자로 다중 문서 분리
       - 각 문서에서 identity(apiVersion/kind/metadata) + 섹션(spec, data 등) 분리
       - 섹션이 클 경우 RecursiveCharacterTextSplitter로 추가 분할
  5. 각 chunk를 bge-m3로 embedding
  6. Qdrant에 upsert (payload: text, source, section, kind, name, namespace)
"""

import re
import uuid
from pathlib import Path

import yaml
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
QDRANT_URL      = "http://192.168.219.184:6333"
OLLAMA_URL      = "http://localhost:11434/v1"
EMBEDDING_MODEL = "bge-m3"
DATA_DIR        = "./data"
VECTOR_SIZE     = 1024
CHUNK_SIZE      = 800
CHUNK_OVERLAP   = 100

# ─────────────────────────────────────────────
# Embedding (embedding.py 패턴)
# ─────────────────────────────────────────────
_openai_client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")

def get_embedding(text: str, model: str = EMBEDDING_MODEL) -> list:
    return _openai_client.embeddings.create(input=[text], model=model).data[0].embedding


# ─────────────────────────────────────────────
# Step 1 — Collection 생성 또는 재사용
# ─────────────────────────────────────────────
def get_or_create_collection(client: QdrantClient, collection_name: str) -> None:
    existing = [c.name for c in client.get_collections().collections]
    if collection_name in existing:
        print(f"[재사용] Collection '{collection_name}' 이미 존재 → 그대로 사용")
    else:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print(f"[완료] Collection '{collection_name}' 생성")


# ─────────────────────────────────────────────
# Step 2 — YAML 파일 탐색
# ─────────────────────────────────────────────
def find_yaml_files(data_dir: str) -> list:
    """data 디렉터리 하위의 모든 .yaml / .yml 파일을 재귀 탐색."""
    path = Path(data_dir)
    yaml_files = sorted(path.rglob("*.yaml")) + sorted(path.rglob("*.yml"))
    # 중복 제거 후 정렬
    return sorted(set(yaml_files))


# ─────────────────────────────────────────────
# Step 3 — YAML Chunking
# ─────────────────────────────────────────────
def _extract_identity(doc: dict) -> dict:
    """YAML 문서에서 리소스 식별 정보를 추출."""
    metadata = doc.get("metadata", {}) or {}
    return {
        "kind":       doc.get("kind", ""),
        "api_version": doc.get("apiVersion", ""),
        "name":       metadata.get("name", "") if isinstance(metadata, dict) else "",
        "namespace":  metadata.get("namespace", "") if isinstance(metadata, dict) else "",
    }


def _identity_label(identity: dict) -> str:
    label = identity["kind"]
    if identity["name"]:
        label += f"/{identity['name']}"
    if identity["namespace"]:
        label += f" ({identity['namespace']})"
    return label or "unknown"


def _split_if_large(text: str, splitter: RecursiveCharacterTextSplitter) -> list:
    if len(text) > CHUNK_SIZE:
        return splitter.split_text(text)
    return [text]


def chunk_yaml(text: str, source: str) -> list:
    """
    YAML 파일을 의미 단위 청크 리스트로 변환.

    전략:
    - --- 구분자로 다중 문서 분리
    - 각 문서: identity 섹션(apiVersion/kind/metadata) + 나머지 top-level 섹션(spec, data, …)
    - identity를 각 청크 앞에 붙여 단독으로 꺼내도 문맥 파악 가능하게 함
    - 섹션이 CHUNK_SIZE 초과 시 RecursiveCharacterTextSplitter로 추가 분할
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " "],
    )

    chunks = []
    raw_docs = re.split(r"^---\s*$", text, flags=re.MULTILINE)

    for raw_doc in raw_docs:
        raw_doc = raw_doc.strip()
        if not raw_doc:
            continue

        # YAML 파싱 실패 시 텍스트 전체를 단일 청크로
        try:
            doc = yaml.safe_load(raw_doc)
        except yaml.YAMLError as e:
            chunks.append({
                "text":    raw_doc,
                "source":  source,
                "section": "raw(parse_error)",
                "kind": "", "name": "", "namespace": "",
            })
            continue

        if not isinstance(doc, dict):
            # 스칼라·리스트 문서는 그대로 단일 청크
            chunks.append({
                "text":    raw_doc,
                "source":  source,
                "section": "raw",
                "kind": "", "name": "", "namespace": "",
            })
            continue

        identity   = _extract_identity(doc)
        id_label   = _identity_label(identity)

        # identity 섹션 (apiVersion + kind + metadata)
        id_keys    = ["apiVersion", "kind", "metadata"]
        id_data    = {k: doc[k] for k in id_keys if k in doc}
        id_text    = yaml.dump(id_data, allow_unicode=True, default_flow_style=False)
        id_header  = f"# {id_label}\n\n"

        for sub in _split_if_large(id_header + id_text, splitter):
            if sub.strip():
                chunks.append({
                    "text":    sub,
                    "source":  source,
                    "section": f"{id_label} > identity",
                    **identity,
                })

        # 나머지 top-level 섹션 (spec, data, rules, status, …)
        for key, value in doc.items():
            if key in id_keys:
                continue

            section_yaml = yaml.dump({key: value}, allow_unicode=True, default_flow_style=False)
            full_text    = f"# {id_label} > {key}\n\n{section_yaml}"

            for sub in _split_if_large(full_text, splitter):
                if sub.strip():
                    chunks.append({
                        "text":    sub,
                        "source":  source,
                        "section": f"{id_label} > {key}",
                        **identity,
                    })

    return chunks


# ─────────────────────────────────────────────
# Step 4 — 파일 단위 Embed & Upsert (qdrant_embed_chucking.py 패턴)
# ─────────────────────────────────────────────
def ingest_file(client: QdrantClient, collection_name: str, yaml_file: Path) -> int:
    text   = yaml_file.read_text(encoding="utf-8")
    chunks = chunk_yaml(text, str(yaml_file))

    if not chunks:
        print(f"  [skip] 청크 없음: {yaml_file}")
        return 0

    points = []
    for chunk in chunks:
        vector = get_embedding(chunk["text"])
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text":      chunk["text"],
                    "source":    chunk["source"],
                    "section":   chunk["section"],
                    "kind":      chunk.get("kind", ""),
                    "name":      chunk.get("name", ""),
                    "namespace": chunk.get("namespace", ""),
                },
            )
        )

    client.upsert(collection_name=collection_name, points=points)
    return len(points)


# ─────────────────────────────────────────────
# 파이프라인 진입점
# ─────────────────────────────────────────────
def run_pipeline() -> None:
    # 1. Collection 이름 입력
    collection_name = input("Collection 이름을 입력하세요: ").strip()
    if not collection_name:
        print("[오류] Collection 이름이 없습니다.")
        return

    # 2. Qdrant 연결 & Collection 생성 or 재사용
    qdrant = QdrantClient(url=QDRANT_URL)
    get_or_create_collection(qdrant, collection_name)

    # 3. YAML 파일 탐색
    yaml_files = find_yaml_files(DATA_DIR)
    if not yaml_files:
        print(f"[오류] '{DATA_DIR}' 하위에 YAML 파일이 없습니다.")
        return

    print(f"\n총 {len(yaml_files)}개 YAML 파일 발견\n")

    # 4. 파일별 파이프라인 실행
    total_points = 0
    for idx, yaml_file in enumerate(yaml_files, 1):
        try:
            rel = yaml_file.relative_to(DATA_DIR)
        except ValueError:
            rel = yaml_file
        print(f"[{idx}/{len(yaml_files)}] {rel}")
        try:
            count = ingest_file(qdrant, collection_name, yaml_file)
            print(f"         → {count}개 포인트 입력")
            total_points += count
        except Exception as e:
            print(f"         [오류] {e}")

    print(f"\n파이프라인 완료: 총 {total_points}개 포인트 → '{collection_name}'")


if __name__ == "__main__":
    run_pipeline()
