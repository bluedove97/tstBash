```
           _                 _    
  __ _  __| |_ __ __ _ _ __ | |_  
 / _` |/ _` | '__/ _` | '_ \| __| 
| (_| | (_| | | | (_| | | | | |_  
 \__, |\__,_|_|  \__,_|_| |_|\__| 
    |_|
```

## qdrant 사용하기

d:\work\maf\qdrant


가상환경 세팅
python -m venv venv
source venv/Scripts/activate

가상환경 종료
deactivate


pip install qdrant-client
pip install qdrant-client langchain sentence-transformers pypdf beautifulsoup4 langchain-community langchain_qdrant openai



bge-m3






* langchain_text_splitters
https://velog.io/@wclee7/ragrerank-ollama-llama3-qdrant



* 배포관련
https://www.sktenterprise.com/bizInsight/blogDetail/dev/12607

* qudrant 장점
https://skywork.ai/skypage/ko/qdrant-ai-vector-database-analysis/1982633553159098368

-------------------------------------------------------------------
👉 Quadrant 발음
Qdrant는 사실상 Quadrant(사분면)에서 온 이름이라서
“쿼드런트(kwah-drant)”가 가장 자연스럽고 공식에 가까운 발음이야.
영어 발음도 거의 그대로 따라가면 됨

실무에서는 그냥
👉 “큐드란트”라고 해도 다 알아듣긴 함ㅋㅋ

-------------------------------------------------------------------
## Chroma vs Qdrant

Chroma → 빠르게 만들고 실험하기 좋은 “개발자 친화형”
Qdrant → 대규모/실서비스용 “프로덕션 지향형”


### 핵심 구조 비교
| 항목 | Chroma | Qdrant |
| :--- | :---: | ---: |
| 아키텍처 | In-process / 로컬 중심 | 서버형 (REST/gRPC) |
| 언어 | Python 중심 | Rust 기반 |
| 목표 | 프로토타이핑, RAG 실험 | 대규모 서비스, 고성능 |
| 확장성 | 제한적 | 수평 확장 지원 |
| 필터링 | 기본 제공 | 매우 강력 (index-level) |
| 하이브리드검색 | 제한적 / 수동 구현 | 네이티브 지원 |


Chroma = “개발 속도”
Qdrant = “검색 품질 + 운영 안정성”


“Chroma로 개발 → Qdrant/Pinecone로 이전”

### Qdrant 장단점
✅ 장점
1) 강력한 필터링 (핵심)
HNSW + 필터를 검색 과정에서 같이 처리

👉 크로마 DB:
vector 검색 → 필터

👉 Qdrant:
검색하면서 필터 적용

2) 네이티브 하이브리드 검색
- keyword + vector 결합 지원
- sparse + dense 통합 검색 가능

3) 프로덕션 준비 완료
Rust 기반 고성능

4) 대규모 데이터 처리
- 수백만~수억 벡터 대응
- 메모리 효율, quantization 지원

❌ 단점
- 설정, 운영 필요
- Chroma 대비 개발 속도 느림
- 생태계는 상대적으로 작음


### 하이브리드 검색이란?
- Vector (semantic) + Keyword (BM25 등) 결합
- 👉 더 정확한 검색 결과

#### 한 번에 처리 (Single-stage)
- vector + keyword + filter → 한 번에 실행
- 👉 latency 감소
- 👉 정확도 증가


#### 👉 Chroma 쓰는 경우
- RAG 처음 만든다
- PoC / 실험 / 데모
- 로컬 개발 위주
- infra 없이 빠르게
- 👉 “혼자 개발 / 스타트업 초기”

#### 👉 Qdrant 쓰는 경우
- 사용자 트래픽 있음
- 필터 조건 많음 (권한, 날짜 등)
- hybrid search 필요
- 성능 중요
- 👉 “서비스 운영 / SaaS / 검색 품질 중요”

-------------------------------------------------------------------

## Qdrant vs Milvus

👉 Milvus = 초대규모 / 분산 / 고처리량
엄청 많이 처리하는 DB” (high throughput + scale)
대규모 데이터 처리
👉 Qdrant = 저지연 / 필터링 / 실시간 검색
빠르고 똑똑하게 찾는 DB” (low latency + filtering)
실시간 검색 최적화


Qdrant:
* 더 낮은 지연시간 (빠른 응답)
* 실시간 API에 유리

Milvus:
* 더 높은 처리량 (QPS, ingest)
* 대량 데이터 처리에 강함


| 성능 항목 | 우위 | 
| :--- | :---: |
| 응답속도 | Qdrant |
| 대량 처리 | Milvus |
| 실시간성 | Qdrant |
| 배치 처리 | Milvus |


🚀확장성
* Milvus (압도적)
* 수억~수십억 벡터
* 클러스터 기반
* GPU 지원
* “빅테크급” 100M+

Qdrant
* 수백만~수천만까지 안정적
* 초대규모에서는 한계 가능


-------------------------------------------------------------------

## Qdrant + BGE-M3 + Dense/Sparse/Hybrid 샘플코드

1. Dense
- 의미 기반 (semantic)
- 문장이 달라도 잘 찾음
- 키워드 정확도는 약함

2. Sparse
- 키워드 기반 (BM25)
- exact match 강함
- 의미 이해는 약함

3. Hybrid
- 둘의 장점 결합
- 실제 서비스에서 사용

#### Collection 생성 (Dense + Sparse)

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, SparseVectorParams

client = QdrantClient(url="http://localhost:6333")

collection_name = "hybrid_demo"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config={
        "dense": VectorParams(
            size=1024,   # bge-m3 dense dimension
            distance=Distance.COSINE
        )
    },
    sparse_vectors_config={
        "sparse": SparseVectorParams()
    }
)

```

#### BGE-M3 Embedding 함수 (Dense + Sparse)

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")


def embed(texts):
    # Dense
    dense_vectors = model.encode(texts, normalize_embeddings=True)

    # Sparse (BM25-like)
    sparse_embeddings = model.encode(
        texts,
        output_value="token_embeddings",
        normalize_embeddings=False
    )

    sparse_vectors = []
    for emb in sparse_embeddings:
        indices = []
        values = []

        for idx, val in enumerate(emb):
            if val != 0:
                indices.append(idx)
                values.append(float(val))

        sparse_vectors.append({
            "indices": indices,
            "values": values
        })

    return dense_vectors, sparse_vectors
```

#### 데이터 삽입

```python
from qdrant_client.models import PointStruct

docs = [
    "Qdrant is a vector database",
    "Hybrid search combines dense and sparse vectors",
    "BM25 is a sparse retrieval method",
    "BGE-M3 supports hybrid embeddings",
    "Vector search is useful for semantic retrieval"
]

dense_vecs, sparse_vecs = embed(docs)

points = []
for i, (d, s, text) in enumerate(zip(dense_vecs, sparse_vecs, docs)):
    points.append(
        PointStruct(
            id=i,
            vector={
                "dense": d.tolist(),
                "sparse": s
            },
            payload={"text": text}
        )
    )

client.upsert(
    collection_name=collection_name,
    points=points
)
```


#### Dense 검색

```python
query = "What is hybrid search?"

dense_q, sparse_q = embed([query])

dense_result = client.query_points(
    collection_name=collection_name,
    query={
        "vector": dense_q[0],
        "using": "dense"
    },
    limit=3
)

print("\n=== Dense Search ===")
for r in dense_result.points:
    print(r.payload["text"], r.score)

```

#### Sparse 검색

```python
sparse_result = client.query_points(
    collection_name=collection_name,
    query={
        "vector": sparse_q[0],
        "using": "sparse"
    },
    limit=3
)

print("\n=== Sparse Search ===")
for r in sparse_result.points:
    print(r.payload["text"], r.score)
```

#### Hybrid 검색

```python
hybrid_result = client.query_points(
    collection_name=collection_name,
    query={
        "vector": {
            "dense": dense_q[0],
            "sparse": sparse_q[0]
        }
    },
    limit=3
)

print("\n=== Hybrid Search ===")
for r in hybrid_result.points:
    print(r.payload["text"], r.score)
```


#### 결과 비교

```python
def print_results(title, results):
    print(f"\n=== {title} ===")
    for r in results.points:
        print(f"{r.payload['text']} | score={r.score:.4f}")

print_results("Dense", dense_result)
print_results("Sparse", sparse_result)
print_results("Hybrid", hybrid_result)
```

#### 가중치 튜닝

```python
hybrid_result = client.query_points(
    collection_name=collection_name,
    query={
        "vector": {
            "dense": dense_q[0],
            "sparse": sparse_q[0]
        },
        "weights": {
            "dense": 0.7,
            "sparse": 0.3
        }
    },
    limit=3
)
```
