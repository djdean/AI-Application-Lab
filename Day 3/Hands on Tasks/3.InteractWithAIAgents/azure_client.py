"""
Azure AI Foundry Client for workshop tasks.
This module contains the main client class and supporting data structures.
"""
import asyncio
import logging
from typing import Optional, List, Dict
from dataclasses import dataclass
from enum import Enum
from azure.ai.projects import AIProjectClient
from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import MessageRole
from azure.identity import DefaultAzureCredential

logger = logging.getLogger(__name__)


class ListSortOrder(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


@dataclass
class ChatMessage:
    """Represents a chat message."""
    role: MessageRole
    content: str
    timestamp: Optional[str] = None


@dataclass
class AgentResponse:
    """Represents a response from the AI agent."""
    message: str = None
    charts: Optional[List[Dict]] = None
    error: Optional[str] = None


@dataclass
class AzureAIConfig:
    """Configuration for Azure AI Foundry connection."""
    endpoint: str
    agent_id: Optional[str] = None


class AzureAIFoundryClient:
    """Client for interacting with Azure AI Foundry Agent Service using the Azure AI Projects SDK."""

    def __init__(self, config: AzureAIConfig, credential: Optional[DefaultAzureCredential] = None):
        self.config = config
        self.client: Optional[AIProjectClient] = None
        self.credential: Optional[DefaultAzureCredential] = credential or None
        self.thread_id: Optional[str] = None
        self._create_client()

    def _create_client(self):
        """Create the AIProjectClient and DefaultAzureCredential."""
        try:
            if not self.credential:
                self.credential = DefaultAzureCredential()
            self.client = AIProjectClient(
                endpoint=self.config.endpoint, credential=self.credential
            )
            self.agents_client = AgentsClient(
                endpoint=self.config.endpoint, credential=self.credential
            )
            logger.info("Successfully created Azure AI Projects client")
        except Exception as e:
            logger.error(f"Failed to create Azure AI Projects client: {e}")
            self.client = None
            self.credential = None
    def test_connection(self) -> bool:
        """Test connection to Azure AI Foundry by attempting to create a thread."""
        if not self.client:
            logger.error("Client not initialized")
            return False
        return True
    async def start_conversation(self) -> bool:
        """Start a new conversation thread with the agent."""
        if not self.client:
            logger.error("Client not initialized")
            return False

        try:

            thread = await self.agents_client.threads.create()
            self.thread_id = thread.id
            logger.info(f"Conversation started with thread ID: {self.thread_id}")
            return True

        except Exception as e:
            logger.error(f"Error starting conversation: {e}")
            return False

    async def send_message(
        self, message: str, attachments: Optional[List[Dict]] = None
    ) -> Optional[AgentResponse]:
        """Send a message to the agent and get response."""
        if not self.client:
            return AgentResponse(
                message="Client not initialized",
                error="Azure AI Projects client is not available",
            )

        if not self.thread_id:
            if not await self.start_conversation():
                return AgentResponse(
                    message="Failed to start conversation",
                    error="Could not initialize thread with agent",
                )

        try:
            # Create message in thread
            await self.agents_client.messages.create(
                thread_id=self.thread_id, role=MessageRole.USER, content=message
            )

            # Create and process a run
            run = await self.agents_client.runs.create_and_process(
                thread_id=self.thread_id, agent_id=self.config.agent_id
            )

            messages = self.agents_client.messages.list(
                thread_id=self.thread_id, order=ListSortOrder.ASCENDING.value
            )
            return await self._process_messages_response(messages, run.id)

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return AgentResponse(
                message="An error occurred while communicating with the agent",
                error=str(e),
            )

    async def _process_messages_response(self, messages, run_id: str) -> AgentResponse:
        """Process the messages response from the agent."""
        try:
            # Find the assistant message from this run
            assistant_message = None

            # Collect all messages
            all_messages = []
            async for message in messages:
                all_messages.append(message)

            # Look for assistant message from this specific run
            for message in reversed(all_messages):
                if (
                    message.role == MessageRole.AGENT
                    and getattr(message, "run_id", None) == run_id
                ):
                    assistant_message = message
                    break

            # If no message found for this run, get the most recent assistant message
            if not assistant_message:
                for message in reversed(all_messages):
                    if message.role == MessageRole.AGENT:
                        assistant_message = message
                        break

            if not assistant_message:
                return AgentResponse(
                    message="No response from assistant",
                    error="No assistant message found in response",
                )

            # Extract message content
            message_text = ""
            if hasattr(assistant_message, "text_messages") and assistant_message.text_messages:
                last_text = assistant_message.text_messages[-1]
                message_text = last_text.text.value if hasattr(last_text, "text") else str(last_text)

            # Handle image contents if present
            charts = []
            if (
                hasattr(assistant_message, "image_contents")
                and assistant_message.image_contents
            ):
                for i, image_content in enumerate(assistant_message.image_contents):
                    file_id = None
                    if hasattr(image_content, "file_id"):
                        file_id = image_content.file_id
                    elif hasattr(image_content, "image_file") and hasattr(
                        image_content.image_file, "file_id"
                    ):
                        file_id = image_content.image_file.file_id

                    if file_id:
                        charts.append(
                            {
                                "type": "image",
                                "file_id": file_id,
                                "filename": f"chart_{i}.png",
                            }
                        )

            return AgentResponse(
                message=message_text or "Response received",
                charts=charts if charts else None,
            )

        except Exception as e:
            logger.error(f"Error processing messages response: {e}")
            return AgentResponse(
                message="Error processing agent response", error=str(e)
            )

    async def get_conversation_history(self, thread_id=None) -> List[ChatMessage]:
        """Get the conversation history."""
        if not self.client or (not self.thread_id and not thread_id):
            return []
        if thread_id:
            self.thread_id = thread_id

        try:
            messages = self.agents_client.messages.list(
                thread_id=self.thread_id, order=ListSortOrder.ASCENDING.value
            )

            chat_messages = []
            async for message in messages:
                # Use the SDK MessageRole directly
                role = message.role

                # Extract content using SDK pattern
                content = ""
                if hasattr(message, "text_messages") and message.text_messages:
                    last_text = message.text_messages[-1]
                    content = last_text.text.value if hasattr(last_text, "text") else str(last_text)

                timestamp = str(message.created_at) if hasattr(message, "created_at") and message.created_at else None

                chat_messages.append(
                    ChatMessage(role=role, content=content, timestamp=timestamp)
                )

            return chat_messages

        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []

    async def get_file_content(self, file_id: str) -> Optional[bytes]:
        """Get file content by file ID."""
        if not self.client:
            return None

        try:
            # Use the Azure AI Projects SDK method to get file content
            result = await self.agents_client.files.get_content(file_id)
            return await self._process_file_result(result)

        except Exception as e:
            logger.error(f"Error getting file content: {e}")
            return None

    async def _process_file_result(self, result) -> Optional[bytes]:
        """Process file download result regardless of return type."""
        try:
            if hasattr(result, "__aiter__"):
                # It's an async generator, collect the chunks
                chunks = []
                async for chunk in result:
                    if isinstance(chunk, (bytes, bytearray)):
                        chunks.append(chunk)
                return b"".join(chunks)
            elif isinstance(result, bytes):
                return result
            else:
                # Try to convert other types
                return result
        except Exception as e:
            logger.error(f"Error processing file result: {e}")
            return None

    async def create_agent(
        self, 
        model: str = "gpt-4o",
        name: str = "my-agent",
        instructions: str = "You are a helpful AI assistant.",
        tools: Optional[list] = None
    ) -> Optional[str]:
        """Create a new agent and return its ID."""
        if not self.client:
            logger.error("Client not initialized")
            return None

        try:
            # Create agent with specified configuration
            agent = await self.agents_client.create_agent(
                model=model,
                name=name,
                instructions=instructions,
            )
            
            logger.info(f"Successfully created agent: {agent.id}")
            logger.info(f"  Name: {agent.name}")
            logger.info(f"  Model: {agent.model}")
            logger.info(f"  Instructions: {agent.instructions}")

            return agent.id

        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            return None

    async def get_agent(self, agent_id: str):
        """Retrieve agent details by ID."""
        if not self.client:
            logger.error("Client not initialized")
            return None

        try:
            agent = await self.agents_client.get_agent(agent_id)
            
            logger.info(f"Agent details:")
            logger.info(f"  ID: {agent.id}")
            logger.info(f"  Name: {agent.name}")
            logger.info(f"  Model: {agent.model}")
            logger.info(f"  Instructions: {agent.instructions}")
            logger.info(f"  Created at: {agent.created_at}")
            
            return agent

        except Exception as e:
            logger.error(f"Error retrieving agent: {e}")
            return None

    async def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent by ID."""
        if not self.client:
            logger.error("Client not initialized")
            return False

        try:
            await self.agents_client.delete_agent(agent_id)
            logger.info(f"Successfully deleted agent: {agent_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting agent: {e}")
            return False
