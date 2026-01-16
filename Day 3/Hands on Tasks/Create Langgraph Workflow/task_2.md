# Task 2 (Optional): Add a Summarizer Node

## Objective
Extend the graph with a second node that summarizes the conversation after each assistant reply. This shows how to chain multiple runs and attach extra data to state.

## Suggested Plan
1. Extend `ChatState` with a `summary: str | None` field.
2. Add a helper to format history (e.g., `"user: ...\nassistant: ..."`).
3. Create `summarize(state)` that:
   - Builds a prompt like `"Summarize the conversation in 3 bullet points"` plus the formatted history
   - Creates a fresh thread, posts that prompt, runs the same Agent, and grabs the assistant reply as the summary
   - Returns state with `summary` set
4. Wire the graph: entry -> `agent_turn` -> `summarize` -> `END`.
5. In the CLI loop, print both the assistant reply and the latest summary.

## Notes
- Using a separate thread for summarization keeps the main chat thread clean.
- You can reuse the same Agent ID; the prompt steers the summarization behavior.
- If you prefer, route both nodes through the same thread, but be aware it will mix messages.

## Challenge
- Add a tool to the Agent (for example, a weather function) in Azure AI Foundry, then re-run Task 1 to watch tool calls execute through the graph.
