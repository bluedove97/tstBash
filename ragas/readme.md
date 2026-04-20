Ragas는 RAG(Retrieval-Augmented Generation) 기반 LLM 시스템을 평가하기 위해 만들어진 오픈소스 프레임워크.

단순 정확도 평가가 아니라, “검색 + 생성” 전체 파이프라인 품질을 정량적으로 측정.

---

# 🔍 Ragas가 왜 필요한가

기존 LLM 평가는 보통 이런 식이다.

* 정답(label)과 비교 → accuracy, F1 등

근데 RAG는 구조가 다르다.

1. 문서 검색 (retrieval)
2. 답변 생성 (generation)

👉 문제

* 답이 틀린 이유가 **검색 때문인지 / 생성 때문인지** 구분이 어려움
* 정답 데이터셋 만들기도 어려움

👉 그래서 Ragas 등장
→ LLM 자체를 평가자로 활용해서 품질을 측정

---

# 핵심 개념 (중요)

Ragas는 “Reference 없이도 평가 가능”하다는 게 핵심 포인트.

즉,

* 사람이 만든 정답 없이도 평가 가능
* 또는 정답이 있으면 더 정밀하게 평가 가능

---

# 📊 주요 평가 지표들

## 1. Faithfulness (충실성)

👉 답변이 실제 문서(context)에 기반했는가

* hallucination 탐지
* context에 없는 내용을 말하면 점수 ↓

예:

* 문서: “A는 2020년에 설립”
* 답변: “A는 2018년에 설립”
  → ❌ 낮은 점수

---

## 2. Answer Relevancy (답변 관련성)

👉 질문에 제대로 답했는가

* 질문과 답변의 semantic alignment 평가
* 엉뚱한 답변 걸러냄

---

## 3. Context Precision

👉 검색된 문서가 얼마나 “쓸모 있는 정보”였는가

* 불필요한 문서 많으면 점수 ↓

---

## 4. Context Recall

👉 필요한 정보가 제대로 검색됐는가

* 중요한 정보 빠지면 점수 ↓

---

## 5. Answer Correctness (정답 기반)

👉 정답이 있을 경우 정확도 평가

---

# ⚙️ 평가 흐름

Ragas는 보통 이런 데이터셋을 사용한다

```json
{
  "question": "...",
  "contexts": ["retrieved doc1", "doc2"],
  "answer": "LLM output",
  "ground_truth": "optional"
}
```

그리고 내부적으로 LLM을 사용해서

* 질문 vs 답변 비교
* 답변 vs context 비교
* context 품질 평가

평가를 처리한다.

---

# 🧪 데이터셋 생성도 지원함

Ragas의 강력한 기능 중 하나는

👉 문서만 넣으면 자동으로:

* 질문 생성
* 답변 생성
* 평가용 데이터셋 생성

즉:

> “RAG 테스트용 데이터셋을 자동 생성”

이게 실무에서 꽤 큰 장점임

---

# 🧩 실제 사용 예 (Python)

```python
from ragas import evaluate
from datasets import Dataset

data = {
    "question": ["A 회사는 언제 설립되었나요?"],
    "answer": ["A 회사는 2020년에 설립되었습니다."],
    "contexts": [["A 회사는 2020년에 설립되었습니다."]],
}

dataset = Dataset.from_dict(data)

result = evaluate(dataset)
print(result)
```

---

# 💡 어디에 쓰면 좋냐

## 1. 사내 LLM / RAG 검증

* MCP / Agent / 사내 검색 시스템 평가
* “이거 진짜 잘 찾고 잘 답하냐?” 수치화 가능

## 2. 모델 비교

* GPT vs 사내 LLM vs 오픈소스 모델
* 같은 질문으로 점수 비교

## 3. 프롬프트 튜닝

* prompt 바꾸고 점수 변화 확인

## 4. 검색엔진 개선

* embedding / vector DB 성능 평가

---

# ⚠️ 한계도 있음 (중요)

## 1. LLM이 평가자라서 완벽하지 않음

* 평가 자체도 모델에 의존
* bias 가능(편향) --> “평가 결과가 객관적 진실이 아니라, 평가에 사용된 LLM의 성향에 영향을 받는다”는 뜻

## 2. 비용 발생

* 평가할 때도 LLM 호출함

## 3. 절대적인 점수 X

* 상대 비교 용도로 더 적합

---

# 🧠 핵심 요약

* Ragas = **RAG 시스템 평가 프레임워크**
* 특징:

  * 정답 없이도 평가 가능
  * 검색 + 생성을 동시에 평가
* 주요 지표:

  * Faithfulness (환각 방지)
  * Relevancy (질문 적합성)
  * Context Precision/Recall (검색 품질)
* 활용:

  * 사내 LLM 검증
  * 모델 비교
  * 데이터셋 자동 생성

---

# 🔥 한 줄 정리

👉 **“RAG가 잘 작동하는지 숫자로 보여주는 도구”**
