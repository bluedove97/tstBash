👉 핵심:

> **BM25 Function은 “데이터 INSERT 시 자동 생성”이지, “검색 시 자동 변환”이 아니다.**

---

## 🔥 에러 설명

구조:

* insert 시 → `"text"` 넣음 → BM25 Function이 자동으로 `"text_sparse"` 생성 ✅
* search 시 → `"text_sparse"`에 `"문자열"` 넣음 ❌

여기서 착각 포인트👇

### ❌ 잘못된 기대

> “문자열 넣으면 Milvus가 BM25로 변환해주겠지?”

👉 **안 해줌. 절대 안 해줌.**

---

## 📌 공식 문서 문장의 진짜 의미

> “스파스 벡터를 수동으로 제공할 필요가 없습니다”

이 말은:

👉 **INSERT할 때만 해당**

* 데이터 넣을 때: text → 자동 변환 ✅
* 검색할 때: ❌ 자동 변환 없음

---

## 🧠 구조를 그림처럼 보면

```
[INSERT]
"text" ──(BM25 function)──> "text_sparse" 저장됨

[SEARCH]
❌ "text_sparse" ← "문자열" (안됨)
✅ "text_sparse" ← "sparse vector" (맞음)
```

---

## ✅ 해결 방법 

### 직접 BM25 encoder 사용 (추천)

Milvus에서 제공하는 BM25 embedding 사용:

```python
from pymilvus import BM25EmbeddingFunction

bm25_ef = BM25EmbeddingFunction()

query_sparse = bm25_ef.encode_queries([query_text])

search_param_2 = {
    "data": query_sparse,
    "anns_field": "text_sparse",
    "limit": 2
}
```

---

## 🔥 최종 정리

👉 수정:

```python
"data": [query_text]   ❌
"data": query_sparse   ✅
```

## 💬 한마디로 정리하면

> BM25 Function은 “저장 시 자동화”일 뿐,
> 검색 쿼리는 **직접 sparse vector로 만들어야 한다.**


---


> **`client.hybrid_search()` + `AnnSearchRequest` 조합에서는
> 문자열 → BM25 변환이 자동으로 안 된다.**

코드에서 이 부분:

```python
"data": [query_text]
```

👉 **이건 2.6.x에서도 여전히 에러 나는 게 정상**

---

## 🔥 왜 이런 일이 생기냐 (핵심 구조)

Milvus 2.6.x의 기능을 분리해서 보면:

### 1️⃣ BM25 Function

* INSERT 시: 자동 실행 ✅
* SEARCH 시: ❌ hybrid_search에서는 자동 실행 안 됨

---

### 2️⃣ `hybrid_search()`

이건 내부적으로:

> 👉 “여러 개의 **ANN 요청**을 합쳐서 랭킹하는 API”

즉:

```text
dense ANN + sparse ANN → 결과 합치기
```

👉 포인트는 **ANN = vector 기반**이라는 것

---

## 💥 그래서 발생하는 정확한 문제 흐름

```text
query_text (string)
   ↓
AnnSearchRequest 전달
   ↓
Milvus 입장:
"이건 sparse vector 필드인데 왜 string이지?"
   ↓
❌ type mismatch 에러
```


---

## ✅ 정답 (실전에서 무조건 이걸 써야 함)

너 구조에서는 무조건 이렇게 가야 한다:

```python
from pymilvus import BM25EmbeddingFunction

bm25 = BM25EmbeddingFunction()

query_sparse = bm25.encode_queries([query_text])

search_param_2 = {
    "data": query_sparse,   # ✅ 반드시 vector
    "anns_field": "text_sparse",
    "limit": 2
}
```

---


