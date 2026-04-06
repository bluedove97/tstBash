from fastmcp import Client
import asyncio

#client = Client("stdio://mcp_server.py")
#client = Client("http://localhost:5000")
#async with Client("https://gofastmcp.com/mcp") as client:



# async def main():
#     tools = await client.list_tools()
#     print("Available tools:", tools)

#     result = await client.call_tool(
#         "search_docs",
#         {"query": "회원 가입은 어떻게 합니까?"}
#     )

#     print(result)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())


# mcp_host.py에다가는 이런식으로
def mcpHost():
    print("-")
    # tools = await client.list_tools()

    # response = llm.chat(
    #     messages=[{"role": "user", "content": "qdrant 설명해줘"}],
    #     tools=tools
    # )



async def main():
    async with Client("http://localhost:5000/mcp") as client:
        tools = await client.list_tools()
        print("Available tools:", tools)
        print("-------------------------------")
        # result = await client.call_tool(
        #     name="search_docs",
        #     arguments={"query": "회원 가입은 어떻게 합니까?"}
        # )

        result = await client.call_tool(
            name="get_image_info",
            arguments={"image_path": "C:/Users/bluedove/Pictures/icon_me.png"}
        )

        # result = await client.call_tool(
        #     name="get_weather",
        #     arguments={"city": "AnYang"}
        # )
    print(result)

asyncio.run(main())


