from openai import OpenAI # !pip install openai





text = "파이썬 기초 문법"
def get_embedding(text, model="bge-m3"):
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    return client.embeddings.create(input = [text], model=model).data[0].embedding

result = get_embedding(text) # 숫자 리스트 1개

print(f"len(result)={len(result)}")

#print(f"result={result}")