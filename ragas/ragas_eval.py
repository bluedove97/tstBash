"""
RAGAS 평가 파이프라인
- ground_truth 있음: Faithfulness + AnswerRelevancy + ContextRecall + ContextPrecision
- ground_truth 없음: Faithfulness + AnswerRelevancy
GROUND_TRUTHS 리스트를 [None, None, None]으로 바꾸면 ground_truth 없음 모드로 실행됩니다.
"""

from openai import AsyncOpenAI
from ragas.metrics.collections import Faithfulness, AnswerRelevancy, ContextRecall, ContextPrecision
from ragas.llms import llm_factory
from ragas.embeddings import OpenAIEmbeddings

from qdrant_pipeline import retrieve, rag_ask

# ─────────────────────────────────────
# 설정값
# ─────────────────────────────────────
OLLAMA_URL  = "http://localhost:11434/v1"
LLM_MODEL   = "ingu627/exaone4.0:1.2b"
EMBED_MODEL = "bge-m3"

TEST_QUESTIONS = [
    "본인 결혼시 휴가는 몇일인가요?",
    "입사시 필요 서류",
    "수습기간은 어떻게 되나요?",
]

# ground_truth 없이 실행하려면 아래를 [None, None, None]으로 교체
GROUND_TRUTHS = [
    "본인 결혼 시 7일의 유급휴가를 받을 수 있으며, 경조금 300,000원과 화환도 제공됩니다. (제33조 경조휴가 표 ①)",
    "입사 시 필요 서류: ① 입사지원서(이력서, 자기소개서) 1부 ② 주민등록등본 1부 ③ 건강보험자격득실확인서 또는 고용보험자격이력내역서 1부 ④ 경력증명서(해당자) ⑤ 최종학교 졸업(예정)증명서 1부 ⑥ 최종학교 성적증명서 1부 ⑦ 급여통장 사본 1부 ⑧ 전 직장 원천징수영수증·원천징수부 각 1부(해당자) ⑨ 보유 자격증 사본(해당자) ⑩ 기타 회사 요청 서류. ①을 제외한 나머지는 최종 합격 후 15일 이내 제출. (제5조)",
    "신입사원에 한하여 최초 근무 개시일부터 3개월의 수습(시용)기간이 있습니다. 경력자나 자격 소지자는 면제하거나 기간 단축/연장 가능. 수습기간 평가 결과 부적당하면 근로계약 종료 가능. 정식 채용 시 수습기간은 근속연수에 포함. (제3조, 제8조)",
]

# ─────────────────────────────────────
# RAGAS용 Ollama 어댑터 (OpenAI 호환)
# ─────────────────────────────────────
_openai_client = AsyncOpenAI(base_url=OLLAMA_URL, api_key="ollama")

ragas_llm = llm_factory(LLM_MODEL, client=_openai_client)
ragas_embeddings = OpenAIEmbeddings(client=_openai_client, model=EMBED_MODEL)

# 각 메트릭의 ascore()가 요구하는 입력 필드 목록
_METRIC_FIELDS = {
    "faithfulness":       ["user_input", "response", "retrieved_contexts"],
    "answer_relevancy":   ["user_input", "response"],
    "context_recall":     ["user_input", "retrieved_contexts", "reference"],
    "context_precision":  ["user_input", "reference", "retrieved_contexts"],
}


# ─────────────────────────────────────
# 샘플 빌드 (plain dict 형태)
# ─────────────────────────────────────
def build_samples(questions, ground_truths):
    samples = []
    for i, (q, gt) in enumerate(zip(questions, ground_truths), 1):
        print(f"  [{i}/{len(questions)}] RAG 실행 중: {q}")
        answer   = rag_ask(q)
        contexts = [r["text"] for r in retrieve(q)]

        sample = {"user_input": q, "response": answer, "retrieved_contexts": contexts}
        if gt is not None:
            sample["reference"] = gt
        samples.append(sample)
    return samples


# ─────────────────────────────────────
# 메트릭 선택
# ─────────────────────────────────────
def select_metrics(has_ground_truth: bool):
    metrics = [
        Faithfulness(llm=ragas_llm),
        AnswerRelevancy(llm=ragas_llm, embeddings=ragas_embeddings),
    ]
    if has_ground_truth:
        metrics += [
            ContextRecall(llm=ragas_llm),
            ContextPrecision(llm=ragas_llm),
        ]
    return metrics


# ─────────────────────────────────────
# 평가 실행 (evaluate() 대신 batch_score() 직접 호출)
# ─────────────────────────────────────
def run_evaluation(questions, ground_truths):
    has_gt = all(gt is not None for gt in ground_truths)

    print("\n=== RAGAS 평가 시작 ===")
    print(f"평가 모드: {'ground_truth 있음 (4개 지표)' if has_gt else 'ground_truth 없음 (2개 지표)'}")
    print(f"평가 질문 수: {len(questions)}\n")

    print("[ RAG 파이프라인 실행 중... ]")
    samples = build_samples(questions, ground_truths)

    metrics = select_metrics(has_gt)

    print("\n[ RAGAS 평가 중... (시간이 걸릴 수 있습니다) ]")
    results = {}
    for metric in metrics:
        print(f"  - {metric.name} 평가 중...")
        fields = _METRIC_FIELDS[metric.name]
        inputs = [{k: s[k] for k in fields} for s in samples]
        scores = metric.batch_score(inputs)
        results[metric.name] = [r.value for r in scores]

    return results, has_gt


# ─────────────────────────────────────
# 결과 출력
# ─────────────────────────────────────
def print_results(results, has_gt, questions):
    print("\n" + "=" * 60)
    print("  RAGAS 평가 결과")
    print("=" * 60)

    metric_cols = ["faithfulness", "answer_relevancy"]
    if has_gt:
        metric_cols += ["context_recall", "context_precision"]

    col_width = 30
    header = f"{'질문':<{col_width}}" + "".join(f"  {c[:12]:>14}" for c in metric_cols)
    print(f"\n[ 질문별 점수 ]")
    print(header)
    print("-" * len(header))

    for i, q in enumerate(questions):
        q_short = q[:col_width - 1] if len(q) > col_width - 1 else q
        scores = ""
        for c in metric_cols:
            vals = results.get(c, [])
            v = vals[i] if i < len(vals) else None
            scores += f"  {v:>14.4f}" if v is not None else f"  {'N/A':>14}"
        print(f"{q_short:<{col_width}}{scores}")

    print(f"\n[ 지표별 평균 점수 ]")
    for c in metric_cols:
        vals = results.get(c, [])
        if vals:
            avg = sum(vals) / len(vals)
            label = c.replace("_", " ").title()
            print(f"  {label:<25}: {avg:.4f}")

    print("=" * 60)


# ─────────────────────────────────────
# 진입점
# ─────────────────────────────────────
if __name__ == "__main__":
    results, has_gt = run_evaluation(TEST_QUESTIONS, GROUND_TRUTHS)
    print_results(results, has_gt, TEST_QUESTIONS)
