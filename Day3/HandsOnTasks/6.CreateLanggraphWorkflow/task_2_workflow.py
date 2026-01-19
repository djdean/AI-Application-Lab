"""
Extended LangGraph workflow with a summarizer node.

This example demonstrates how to:
1. Chain multiple nodes in a LangGraph
2. Add conversation summarization after each agent reply
3. Maintain both conversation history and a running summary

Example usage: "Plan a 3-step checklist for brewing coffee"
The agent responds, then a second node generates a concise summary.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List

# Optional: Load environment variables from .env file
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# Azure AI Agents SDK for interacting with Azure AI Foundry
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import MessageRole, RunStatus
from azure.identity import DefaultAzureCredential

# LangGraph for building stateful, multi-step workflows
from langgraph.graph import END, StateGraph

if load_dotenv:
    load_dotenv()

# ============================================================================
# CONFIGURATION: Load Azure AI Foundry connection details from environment
# ============================================================================
AGENT_ID = os.environ.get("AZURE_OPENAI_AGENT_ID")  # Your agent's unique identifier
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")  # Your Azure AI Foundry endpoint

if not AGENT_ID:
    raise RuntimeError("Set AZURE_OPENAI_AGENT_ID in your environment.")
if not ENDPOINT:
    raise RuntimeError("Set AZURE_OPENAI_ENDPOINT in your environment.")


def build_client() -> AgentsClient:
    """Create an authenticated Azure AI Agents client.
    
    Supports two authentication methods:
    1. API Key (set AZURE_OPENAI_API_KEY)
    2. DefaultAzureCredential (uses Azure AD/managed identity)
    """
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    if api_key:
        return AgentsClient(endpoint=ENDPOINT, api_key=api_key)
    credential = DefaultAzureCredential()
    return AgentsClient(endpoint=ENDPOINT, credential=credential)


# Initialize the global client once at startup
CLIENT = build_client()


# ============================================================================
# STATE DEFINITION: Tracks conversation history, thread context, and summary
# ============================================================================
@dataclass
class ChatState:
    """State passed between LangGraph nodes.
    
    Attributes:
        history: List of message dictionaries with 'role' and 'content' keys
                 Example: [{'role': 'user', 'content': 'Plan a 3-step checklist...'}]
        thread_id: Azure AI thread ID for maintaining conversation context
        summary: Optional summary of the conversation (updated after each turn)
    """
    history: List[Dict[str, Any]] = field(default_factory=list)
    thread_id: str | None = None
    summary: str | None = None


# ============================================================================
# HELPER FUNCTION: Format conversation history for summarization
# ============================================================================
def format_history(history: List[Dict[str, Any]]) -> str:
    """Format conversation history into a readable string for summarization.
    
    Example output:
        user: Plan a 3-step checklist for brewing coffee
        assistant: 1. Grind coffee beans\n2. Heat water to 200°F\n3. Pour and brew for 4 minutes
    """
    lines = []
    for turn in history:
        role = turn.get("role", "unknown")
        content = turn.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


# ============================================================================
# GRAPH NODE 1: Sends user input to Azure AI Agent and retrieves response
# ============================================================================
def call_agent(state: ChatState) -> ChatState:
    """LangGraph node that processes one conversation turn with the agent.
    
    Flow:
    1. Create or reuse a thread (conversation container)
    2. Add the user's latest message to the thread
    3. Run the agent and poll until completion
    4. Extract the agent's response
    5. Return updated state with agent reply added to history
    """
    
    # STEP 1: Get or create a conversation thread
    # Threads maintain context across multiple turns (like a chat session)
    thread_id = state.thread_id
    if not thread_id:
        thread = CLIENT.threads.create()
        thread_id = thread.id
        # First turn: thread created. Subsequent turns will reuse this ID.

    # STEP 2: Add the user's message to the thread
    # Example: "Plan a 3-step checklist for brewing coffee"
    last_turn = state.history[-1] if state.history else None
    if last_turn and last_turn["role"] == "user":
        CLIENT.messages.create(
            thread_id=thread_id,
            role=MessageRole.USER,
            content=last_turn["content"],
        )

    # STEP 3: Start the agent run
    # The agent will process the user's message using its configured model and instructions
    run = CLIENT.runs.create(thread_id=thread_id, agent_id=AGENT_ID)

    # STEP 4: Poll until the run completes
    # The agent may take time to generate a response, especially for complex requests
    while run.status in {RunStatus.QUEUED, RunStatus.IN_PROGRESS, RunStatus.REQUIRES_ACTION}:
        time.sleep(1)  # Wait 1 second between polls
        run = CLIENT.runs.get(thread_id=thread_id, run_id=run.id)

    # STEP 5: Check if the run completed successfully
    if run.status != RunStatus.COMPLETED:
        # If run failed, capture error details for debugging
        err = getattr(run, "last_error", None)
        err_text = ""
        if err:
            parts = [str(getattr(err, "code", "")), str(getattr(err, "message", ""))]
            err_text = " ".join(p for p in parts if p).strip()
        new_history = list(state.history)
        new_history.append(
            {
                "role": "assistant",
                "content": f"Run finished with status {run.status}. {('Error: ' + err_text) if err_text else 'Check agent config or logs.'} (run_id={run.id})",
            }
        )
        return ChatState(history=new_history, thread_id=thread_id, summary=state.summary)

    # STEP 6: Retrieve all messages from the thread
    messages = list(CLIENT.messages.list(thread_id=thread_id, order="asc"))
    
    # STEP 7: Filter for agent (assistant) messages
    assistant_msgs = [m for m in messages if m.role == MessageRole.AGENT]

    # Helper function to extract text from various content formats
    def _extract_text(content_item: Any) -> str:
        """Handle different SDK content structures to get plain text."""
        if hasattr(content_item, "text"):
            text_val = content_item.text
            if hasattr(text_val, "value"):
                return str(text_val.value)
            return str(text_val)
        if hasattr(content_item, "content"):
            return str(content_item.content)
        return str(content_item)

    # STEP 8: Extract the most recent agent response
    # Example response: "1. Grind coffee beans\n2. Heat water to 200°F\n3. Pour and brew for 4 minutes"
    if assistant_msgs and assistant_msgs[-1].content:
        latest = assistant_msgs[-1].content[0]
        assistant_text = _extract_text(latest)
    else:
        assistant_text = "(no reply)"

    # STEP 9: Update conversation history with agent's response
    new_history = list(state.history)
    new_history.append({"role": "assistant", "content": assistant_text})
    
    # Return new state with updated history and preserved thread_id (summary unchanged)
    return ChatState(history=new_history, thread_id=thread_id, summary=state.summary)


# ============================================================================
# GRAPH NODE 2: Summarizes the conversation after each agent reply
# ============================================================================
def summarize(state: ChatState) -> ChatState:
    """LangGraph node that generates a summary of the conversation so far.
    
    Flow:
    1. Format the conversation history into a readable string
    2. Create a prompt asking for a 3-bullet summary
    3. Create a new thread (separate from main conversation)
    4. Run the agent to generate the summary
    5. Extract and store the summary
    
    Example summary for coffee brewing conversation:
        • User requested a 3-step coffee brewing checklist
        • Agent provided steps: grind beans, heat water, pour and brew
        • Conversation focused on basic coffee preparation methodology
    """
    
    # STEP 1: Format conversation history
    formatted = format_history(state.history)
    
    # STEP 2: Build summarization prompt
    # The same agent that handles user queries can also summarize when prompted
    prompt = f"Summarize the following conversation in 3 concise bullet points:\n\n{formatted}"
    
    # STEP 3: Create a fresh thread for summarization (keeps main thread clean)
    summary_thread = CLIENT.threads.create()
    
    # STEP 4: Add the summarization request to the new thread
    CLIENT.messages.create(
        thread_id=summary_thread.id,
        role=MessageRole.USER,
        content=prompt,
    )
    
    # STEP 5: Run the agent to generate summary
    run = CLIENT.runs.create(thread_id=summary_thread.id, agent_id=AGENT_ID)
    
    # STEP 6: Poll until summary generation completes
    while run.status in {RunStatus.QUEUED, RunStatus.IN_PROGRESS, RunStatus.REQUIRES_ACTION}:
        time.sleep(1)
        run = CLIENT.runs.get(thread_id=summary_thread.id, run_id=run.id)
    
    # STEP 7: Extract the summary from the agent's response
    summary_text = "(summary unavailable)"
    if run.status == RunStatus.COMPLETED:
        messages = list(CLIENT.messages.list(thread_id=summary_thread.id, order="asc"))
        assistant_msgs = [m for m in messages if m.role == MessageRole.AGENT]
        
        if assistant_msgs and assistant_msgs[-1].content:
            latest = assistant_msgs[-1].content[0]
            if hasattr(latest, "text"):
                text_val = latest.text
                if hasattr(text_val, "value"):
                    summary_text = str(text_val.value)
                else:
                    summary_text = str(text_val)
            else:
                summary_text = str(latest)
    
    # STEP 8: Return state with updated summary (history and thread_id unchanged)
    return ChatState(history=state.history, thread_id=state.thread_id, summary=summary_text)


# ============================================================================
# GRAPH CONSTRUCTION: Build the two-node LangGraph workflow
# ============================================================================
# Create a StateGraph that manages ChatState
builder = StateGraph(ChatState)

# Add both nodes to the graph
builder.add_node("agent_turn", call_agent)      # First: handle user request
builder.add_node("summarize", summarize)        # Second: generate summary

# Set the entry point (where the graph starts)
builder.set_entry_point("agent_turn")

# Chain the nodes: agent_turn → summarize → END
builder.add_edge("agent_turn", "summarize")
builder.add_edge("summarize", END)

# Compile into an executable graph
GRAPH = builder.compile()


# ============================================================================
# CLI INTERFACE: Interactive chat loop with summary display
# ============================================================================
def main() -> None:
    """Run an interactive command-line chat session with the agent and summarizer.
    
    Example conversation:
        You: Plan a 3-step checklist for brewing coffee
        Agent: 1. Grind coffee beans
                2. Heat water to 200°F
                3. Pour and brew for 4 minutes
        
        Summary:
        • User requested a 3-step coffee brewing checklist
        • Agent provided steps: grind beans, heat water, pour and brew
        • Conversation focused on basic coffee preparation methodology
    """
    # Initialize empty state (no history, no thread, no summary yet)
    state = ChatState()
    print("Type 'exit' or 'quit' to stop.")
    print("After each response, you'll see a conversation summary.\n")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        
        # Add user message to history
        state.history.append({"role": "user", "content": user_input})
        
        # Invoke the graph (runs agent_turn, then summarize)
        result = GRAPH.invoke(state)
        
        # Normalize result back to ChatState (LangGraph may return a dict)
        state = ChatState(**result) if isinstance(result, dict) else result
        
        # Display agent's response
        print(f"\nAgent: {state.history[-1]['content']}")
        
        # Display the conversation summary
        if state.summary:
            print(f"\n📝 Summary:\n{state.summary}\n")
        else:
            print("\n📝 Summary: (not available)\n")
    
    print("Session ended.")


if __name__ == "__main__":
    main()
