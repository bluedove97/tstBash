from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="qwen3:8b",
    messages=[
        {"role": "system", "content": "markdown 형태로 답변해."},
        {"role": "user", "content": "한국의 수도는 어디야?"}
    ]
)

print(response.choices[0].message.content)


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