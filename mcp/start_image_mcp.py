from mcp_server import mcp

if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=5000)
    