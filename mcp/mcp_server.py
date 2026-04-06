from fastmcp import FastMCP
from image_info import getImageInfo
from qdrant_pipeline import rag_ask


#mcp_server.py는 tools.py의 함수들을 MCP 도구로 등록하는 파일

mcp = FastMCP("mcp-processor")


@mcp.tool()
def get_image_info(image_path: str) -> dict:
    print(image_path)
    """Get information about an image file.
    
    Args:
        image_path: Absolute path to the image file.
    """
    return getImageInfo(image_path)

@mcp.tool()
def search_docs(query: str) -> str:
    """
    Qdrant에서 문서를 검색해서 반환
    """
    result = rag_ask(query)
    return result


@mcp.tool()
def get_weather(city: str) -> str:
    """Get weather information for a given city."""

    return f"The weather in {city} is clear and the temperature is 20 degrees."
