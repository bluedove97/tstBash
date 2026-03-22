
import traceback

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from embedding import get_embedding
import uuid


# ----------------------
# 0. Ollama(OpenAI 호환)
# ----------------------
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key=""
)

# ----------------------
# 1. embedding 함수 (기존 그대로)
# ----------------------
def get_embedding(text, model="bge-m3"):
    return client.embeddings.create(
        input=[text],
        model=model
    ).data[0].embedding

# ----------------------
# 2. Qdrant 연결
# ----------------------
qdrant = QdrantClient(url="http://192.168.219.184:6333")
collection_name = "chunk001"

# ----------------------
# 3. 검색 함수
# ----------------------
def retrieve(query, top_k=3):
    query_vector = get_embedding(query)

    results = qdrant.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k
    )

    #contexts = [r.payload["text"] for r in results]
    contexts = []
    for p in results.points:
        contexts.append({
            "text": p.payload["text"],
            "score": p.score
        })
    return contexts

# ----------------------
# 4. 프롬프트 생성
# ----------------------
def build_prompt(query, contexts):
    #''.join(map(str, int_list))
    context_text = "\n\n".join(map(str,contexts))

    prompt = f"""
당신은 회원약관에 대한 질의응답 도우미입니다.
주어진 context만을 기반으로 한글로 답변하세요.
모르면 모른다고 답하세요.

[context]
{context_text}

[question]
{query}
"""
    return prompt

# ----------------------
# 5. LLM 호출
# ----------------------
def ask_llm(prompt, model="gemma3:4b"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

# ----------------------
# 6. 전체 파이프라인
# ----------------------
def rag_ask(query):
    contexts = retrieve(query)
    print(contexts)
    prompt = build_prompt(query, contexts)
    answer = ask_llm(prompt)
    return answer

# ----------------------
# 7. 실행
# ----------------------
if __name__ == "__main__":
    question = "넌 어떤 정보를 가지고 있어?"
    result = rag_ask(question)

    print("\n💬 질문:", question)
    print("\n🤖 답변:\n", result)