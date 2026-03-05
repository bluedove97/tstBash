import asyncio
from agent_framework.openai import OpenAIChatClient
from agent_framework import Agent

async def main() -> None:
    # Ollama 연결
    client = OpenAIChatClient(
        model_id="qwen3:8b",
        base_url="http://localhost:11434/v1",
        api_key="ollama"   # Ollama는 실제 키 필요 없음
    )

    # Agent 생성
    agent = Agent(
        name="assistant-agent",
        instructions="당신은 여행객을 안내하는 가이드입니다.",
        client=client
    )

    print("Agent started. 종료하려면 exit 입력")

    while True:
        user_input = input("\nUser > ")

        if user_input.lower() in ["exit", "quit"]:
            print("Agent 종료")
            break

        result = await agent.run(user_input)
        print(f"Agent: {result}")

        print("Agent (streaming): ", end="", flush=True)
        async for chunk in agent.run(user_input, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()
    

if __name__ == "__main__":
    asyncio.run(main())