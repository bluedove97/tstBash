"""AG-UI server example."""

import os

from agent_framework import Agent
#from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.openai import OpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
#from azure.identity import AzureCliCredential
from fastapi import FastAPI

# Read required configuration
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT") or "http://localhost:11434/v1"
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME") or "qwen3:8b"

if not endpoint:
    raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
if not deployment_name:
    raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME environment variable is required")

chat_client = OpenAIChatClient(
    model_id="qwen3:8b",
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # Ollama는 실제 키 필요 없음
)

# Create the AI agent
agent = Agent(
    name="AGUIAssistant",
    instructions="You are a helpful assistant. Do not use emoji. You must speak in english.",
    client=chat_client,
)

# Create FastAPI app
app = FastAPI(title="AG-UI Server")

# Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8888)