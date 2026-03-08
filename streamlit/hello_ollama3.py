from openai import OpenAI

async def chatFunction(input) -> None:
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    response = client.chat.completions.create(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": "당신은 여행객을 안내하는 가이드입니다. 여행, 장소, 음식, 문화와 관련이 없는 정보라면 '저는 여행 전문 챗봇입니다. 관련없는 정보는 말씀드리기 어려워요' 라고 친절하게 답하세요."},
            {"role": "user", "content": input}
        ]
    )

    return response.choices[0].message.content


# client = OpenAI(
#     base_url="http://localhost:11434/v1",
#     api_key="ollama"
# )

# response = client.responses.create(
#     model="qwen3:8b",
#     input="한국의 수도는 어디야?"
# )

# print(response.output[1].content[0].text)


# class SimpleAgent:
#     def __init__(self):
#         self.client = OpenAI(
#             base_url="http://localhost:11434/v1",
#             api_key="ollama"
#         )
#         self.model = "qwen3:8b"

#     def run(self, prompt):
#         response = self.client.responses.create(
#             model=self.model,
#             input=prompt
#         )
#         return response.output[1].content[0].text


# agent = SimpleAgent()

# result = agent.run("한국의 수도는 어디야?")

# print(result)