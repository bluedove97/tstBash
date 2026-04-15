"""
MD → Qdrant 인제스트 파이프라인

실행: python md_qdrant_ingest.py

흐름:
  1. 사용자 입력 → collection 이름
  2. Qdrant에 collection 생성 (size=1024, COSINE)
  3. ./data 하위 .md 파일 재귀 탐색
  4. 각 파일을 마크다운 헤더 기준으로 의미 단위 chunking
  5. 각 chunk를 bge-m3로 embedding
  6. Qdrant에 upsert
"""

import os
import uuid
from pathlib import Path

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
QDRANT_URL      = "http://192.168.219.184:6333"
OLLAMA_URL      = "http://localhost:11434/v1"
EMBEDDING_MODEL = "bge-m3"
DATA_DIR        = "./data"
VECTOR_SIZE     = 1024
CHUNK_SIZE      = 800   # 헤더 분할 후 2차 분할 크기
CHUNK_OVERLAP   = 100

# ─────────────────────────────────────────────
# Embedding (embedding.py 패턴 그대로)
# ─────────────────────────────────────────────
_openai_client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")

def get_embedding(text: str, model: str = EMBEDDING_MODEL) -> list:
    return _openai_client.embeddings.create(input=[text], model=model).data[0].embedding


# ─────────────────────────────────────────────
# Step 1 — Collection 생성 (qdrant_create_collection.py 패턴)
# ─────────────────────────────────────────────
def create_collection(client: QdrantClient, collection_name: str) -> None:
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    print(f"[완료] Collection '{collection_name}' 생성")


# ─────────────────────────────────────────────
# Step 2 — .md 파일 탐색
# ─────────────────────────────────────────────
def find_markdown_files(data_dir: str) -> list:
    """data 디렉터리 하위의 모든 .md 파일을 재귀 탐색해서 반환."""
    return sorted(Path(data_dir).rglob("*.md"))


# ─────────────────────────────────────────────
# Step 3 — 마크다운 Chunking
# ─────────────────────────────────────────────
def chunk_markdown(text: str, source: str) -> list:
    """
    1차: 마크다운 헤더(#~####) 기준으로 의미 단위 분할
    2차: 분할된 섹션이 CHUNK_SIZE 초과 시 RecursiveCharacterTextSplitter로 추가 분할
    """
    headers_to_split_on = [
        ("#",    "h1"),
        ("##",   "h2"),
        ("###",  "h3"),
        ("####", "h4"),
    ]
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False,   # 헤더 텍스트를 청크에 포함해서 문맥 유지
    )
    header_docs = header_splitter.split_text(text)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = []
    for doc in header_docs:
        content = doc.page_content.strip()
        if not content:
            continue

        # 섹션이 CHUNK_SIZE보다 길면 추가 분할
        if len(content) > CHUNK_SIZE:
            sub_texts = text_splitter.split_text(content)
        else:
            sub_texts = [content]

        # 헤더 계층 정보를 payload에 담을 메타데이터로 정리
        section_info = " > ".join(
            v for k, v in sorted(doc.metadata.items()) if v
        )

        for sub in sub_texts:
            if sub.strip():
                chunks.append({
                    "text":    sub.strip(),
                    "source":  source,
                    "section": section_info,
                })

    return chunks


# ─────────────────────────────────────────────
# Step 4 — 파일 단위 Embed & Upsert (qdrant_embed_chucking.py 패턴)
# ─────────────────────────────────────────────
def ingest_file(client: QdrantClient, collection_name: str, md_file: Path) -> int:
    text = md_file.read_text(encoding="utf-8")
    chunks = chunk_markdown(text, str(md_file))

    if not chunks:
        print(f"  [skip] 청크 없음: {md_file}")
        return 0

    points = []
    for chunk in chunks:
        vector = get_embedding(chunk["text"])
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text":    chunk["text"],
                    "source":  chunk["source"],
                    "section": chunk["section"],
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

    # 2. Qdrant 연결 & Collection 생성
    qdrant = QdrantClient(url=QDRANT_URL)
    create_collection(qdrant, collection_name)

    # 3. 마크다운 파일 탐색
    md_files = find_markdown_files(DATA_DIR)
    if not md_files:
        print(f"[오류] '{DATA_DIR}' 하위에 마크다운 파일이 없습니다.")
        return

    print(f"\n총 {len(md_files)}개 마크다운 파일 발견\n")

    # 4. 파일별 파이프라인 실행
    total_points = 0
    for idx, md_file in enumerate(md_files, 1):
        rel = md_file.relative_to(DATA_DIR) if md_file.is_relative_to(DATA_DIR) else md_file
        print(f"[{idx}/{len(md_files)}] {rel}")
        try:
            count = ingest_file(qdrant, collection_name, md_file)
            print(f"         → {count}개 포인트 입력")
            total_points += count
        except Exception as e:
            print(f"         [오류] {e}")

    print(f"\n파이프라인 완료: 총 {total_points}개 포인트 → '{collection_name}'")


if __name__ == "__main__":
    run_pipeline()
