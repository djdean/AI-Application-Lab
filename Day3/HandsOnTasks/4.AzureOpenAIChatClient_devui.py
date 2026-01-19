"""Azure OpenAI agent with DevUI."""

import asyncio
import os
import sys
from dotenv import load_dotenv

from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.devui import serve
from azure.identity import AzureCliCredential

# Get the workspace root directory (Pfizer-AI-labs)
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(workspace_root, '.env')

# Load .env from workspace root if it exists
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"📁 Loaded .env from: {dotenv_path}")
else:
    print(f"⚠️  No .env file found at: {dotenv_path}")


class JokeAgent:
    """Joke-telling agent using Azure OpenAI."""
    
    name = "azure-joke-agent"
    description = "Tells jokes using Azure OpenAI"
    
    def __init__(self):
        try:
            # Use Azure OpenAI endpoint with API key
            client = AzureOpenAIChatClient(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o")
            )
            self.agent = client.as_agent(
                instructions="You are a friendly joke teller.",
                name="Joker"
            )
        except Exception as e:
            print(f"❌ Azure OpenAI initialization failed: {e}")
            print("💡 Please check your .env file has:")
            print("   - AZURE_OPENAI_ENDPOINT")
            print("   - AZURE_OPENAI_API_KEY")
            print("   - AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
            raise
    
    def run_stream(self, input_data, **kwargs):
        prompt = str(input_data.text if hasattr(input_data, 'text') else input_data)
        return self.agent.run_stream(prompt)
    
    async def run(self, input_data, **kwargs):
        prompt = str(input_data.text if hasattr(input_data, 'text') else input_data)
        result = await self.agent.run(prompt)
        return result.text if hasattr(result, 'text') else str(result)


async def test_direct():
    """Test agent directly."""
    try:
        client = AzureOpenAIChatClient(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o")
        )
        agent = client.as_agent(
            instructions="You are a joke teller.",
            name="Joker"
        )
        result = await agent.run("Tell me a joke.")
        print(f"Result: {result.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        asyncio.run(test_direct())
    else:
        print("🎭 Starting Azure OpenAI Joke Agent...")
        print("📍 http://localhost:8082")
        try:
            serve(entities=[JokeAgent()], port=8082, auto_open=True)
        except Exception as e:
            print(f"❌ Failed to start DevUI: {e}")
            print("💡 Please check your Azure authentication:")
            print("   - Run: az login")
            print("   - Or set AZURE_OPENAI_API_KEY in .env")


if __name__ == "__main__":
    main()