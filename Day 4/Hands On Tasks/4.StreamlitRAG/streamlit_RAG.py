import streamlit as st
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import KnowledgeBaseRetrievalRequest, KnowledgeBaseMessage, KnowledgeBaseMessageTextContent, SearchIndexKnowledgeSourceParams, KnowledgeRetrievalLowReasoningEffort
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="AI Chat Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize session state variables."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.messages = get_message()
        st.session_state.loading = False

    if "search_client" not in st.session_state:
        st.session_state.search_client = KnowledgeBaseRetrievalClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            knowledge_base_name=os.getenv("KNOWLEDGE_BASE_NAME"),
            credential=DefaultAzureCredential()
        )


def get_message():
    instructions = """
    A Q&A agent that can answer questions.
    If you don't have the answer, respond with "I don't know".
    """
    return [{"role": "system", "content": instructions}]


def _collect_response_text(result):
    response_parts = []
    for resp in getattr(result, "response", []) or []:
        for content in getattr(resp, "content", []) or []:
            if getattr(content, "text", None):
                response_parts.append(content.text)
    return "\n\n".join(response_parts) if response_parts else "No response found."


def _collect_reference_items(result):
    references = []
    for resp in getattr(result, "response", []) or []:
        for reference in getattr(resp, "references", []) or []:
            source_data = getattr(reference, "source_data", None)
            references.append(
                {
                    "title": getattr(reference, "title", None) or getattr(reference, "id", None) or "Reference",
                    "snippet": getattr(reference, "content", None),
                    "source": str(source_data) if source_data else None,
                }
            )
    return references


def _collect_activity_items(result):
    activities = []
    for activity in getattr(result, "activity", []) or []:
        activities.append(str(activity))
    return activities


def run_search():
    req = KnowledgeBaseRetrievalRequest(
        messages=[
            KnowledgeBaseMessage(
                role=m["role"],
                content=[KnowledgeBaseMessageTextContent(text=m["content"])]
            )
            for m in st.session_state.messages
            if m["role"] != "system"
        ],
        knowledge_source_params=[
            SearchIndexKnowledgeSourceParams(
                knowledge_source_name=os.getenv("KNOWLEDGE_SOURCE_NAME"),
                include_references=True,
                include_reference_source_data=True,
                always_query_source=True,
            )
        ],
        include_activity=True,
        retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort,
    )

    with st.spinner("Searching knowledge base..."):
        result = st.session_state.search_client.retrieve(retrieval_request=req)

    response_content = _collect_response_text(result)
    reference_items = _collect_reference_items(result)
    activity_items = _collect_activity_items(result)

    st.markdown("### Answer")
    st.markdown(response_content)

    if reference_items:
        with st.expander(f"Sources ({len(reference_items)})", expanded=False):
            for index, item in enumerate(reference_items, start=1):
                st.markdown(f"**{index}. {item['title']}**")
                if item["snippet"]:
                    st.caption(item["snippet"])
                if item["source"]:
                    st.text(item["source"])
                if index < len(reference_items):
                    st.divider()

    if activity_items:
        with st.expander("Retrieval details", expanded=False):
            for item in activity_items:
                st.text(item)


def main():
    initialize_session_state()

    st.title("🤖 AI Chat Assistant")
    st.markdown("Welcome to your Streamlit AI Chat Assistant!")

    question = st.text_input("Ask a question when ready...")
    if st.button("Submit Question"):
        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            run_search()
        else:
            st.warning("Please enter a question before submitting.")


if __name__ == "__main__":
    main()
