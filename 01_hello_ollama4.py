import asyncio
import os
from openai import OpenAI

async def main() -> None:
    class SimpleAgent:
        def __init__(self):
            self.client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama"
            )
            self.model = "qwen3:8b"

        def run(self, prompt):
            response = self.client.responses.create(
                model=self.model,
                input=prompt
            )
            return response.output[1].content[0].text


    agent = SimpleAgent()

    result = agent.run("한국의 수도는 어디야?")
    print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(main())