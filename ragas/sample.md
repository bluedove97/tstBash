> user input → Qdrant 검색 → context → LLM 답변


---

# 🧠 전체 구조 (실무형)

1. 질문 리스트 준비
2. 각 질문에 대해:

   * Qdrant에서 context retrieval
   * LLM으로 answer 생성

3. 결과를 dataset 형태로 변환
4. Ragas로 평가

---

# ⚙️ Python 예제

## 📦 필요 패키지

```bash
pip install ragas datasets langchain openai qdrant-client
```

---

## 🧩 전체 코드

```python
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

from qdrant_client import QdrantClient
from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

# -----------------------------
# 1. 설정
# -----------------------------
QDRANT_HOST = "localhost"
QDRANT_COLLECTION = "your_collection"

llm = ChatOpenAI(model="gpt-4o-mini")  # 평가용 LLM
embedding = OpenAIEmbeddings()

qdrant = QdrantClient(host=QDRANT_HOST, port=6333)

# -----------------------------
# 2. retrieval 함수
# -----------------------------
def retrieve_context(query, top_k=3):
    query_vector = embedding.embed_query(query)

    hits = qdrant.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_vector,
        limit=top_k
    )

    contexts = [hit.payload["text"] for hit in hits]
    return contexts


# -----------------------------
# 3. LLM 답변 생성
# -----------------------------
def generate_answer(query, contexts):
    context_text = "\n".join(contexts)

    prompt = f"""
    다음 context를 기반으로 질문에 답하세요.

    context:
    {context_text}

    질문:
    {query}
    """

    response = llm.invoke(prompt)
    return response.content


# -----------------------------
# 4. 데이터셋 생성
# -----------------------------
def build_dataset(questions):
    data = {
        "question": [],
        "answer": [],
        "contexts": [],
    }

    for q in questions:
        contexts = retrieve_context(q)
        answer = generate_answer(q, contexts)

        data["question"].append(q)
        data["answer"].append(answer)
        data["contexts"].append(contexts)

    return Dataset.from_dict(data)


# -----------------------------
# 5. 평가 실행
# -----------------------------
def run_evaluation(dataset):
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall
        ],
    )
    return result


# -----------------------------
# 6. 실행
# -----------------------------
if __name__ == "__main__":
    questions = [
        "A 회사는 언제 설립되었나요?",
        "서비스의 주요 기능은 무엇인가요?",
        "이 시스템의 아키텍처를 설명해주세요"
    ]

    dataset = build_dataset(questions)

    result = run_evaluation(dataset)

    print(result)
```

---

# 🔍 코드 핵심 포인트

## 1. ground_truth 없음

👉 이 상태에서도 평가 가능
(Ragas의 장점)

---

## 2. contexts 구조 중요

```python
"contexts": [["doc1", "doc2", "doc3"]]
```

👉 반드시 **list of list 형태**

---

## 3. metric 선택

* faithfulness → hallucination 체크
* answer_relevancy → 질문 적합성
* context_* → retrieval 품질

---

# 💡 실무에서 꼭 추가해야 하는 것

## 1. ground_truth 넣기 (가능하면)

```python
"ground_truth": [...]
```

👉 answer_correctness까지 평가 가능

---

## 2. 로그 저장

```python
dataset.to_pandas().to_csv("eval_log.csv")
```

---

## 3. 질문 다양화

* 쉬운 질문
* tricky 질문
* ambiguous 질문


---

# ⚠️ 주의 (중요)

## 1. 평가용 LLM = 고정

* 항상 같은 모델 써야 비교 가능

## 2. 비용

* 질문 100개 → LLM 호출 수백 번

---

# 🔥 한 줄 요약

> Qdrant + LLM 파이프라인 결과를 dataset으로 만들고 Ragas에 넣으면 끝

