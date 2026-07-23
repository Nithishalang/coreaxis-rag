import streamlit as st
from main import CoreAxisRAG
from src.database.conversation_repository import ConversationRepository
@st.cache_resource
def load_assistant():
    return CoreAxisRAG()

@st.cache_resource
def load_conversation_repository():
    return ConversationRepository()
def show_chat():
    assistant = load_assistant()
    conversation_repo = load_conversation_repository()
    if "user_id" not in st.session_state:
        st.error(
            "Please login first."
        )
        st.stop()
    user_id = st.session_state.user_id
    if "conversation_id" not in st.session_state:
        conversation_id = conversation_repo.create_conversation(
            user_id=user_id,
            title="New Conversation"
        )
        st.session_state.conversation_id = conversation_id
    conversation_id = st.session_state.conversation_id
    st.title(
        "🤖 CoreAxis AI Assistant"
    )
    st.caption(
        "Ask questions about CoreAxis Technologies."
    )
    if "messages_loaded" not in st.session_state:
        stored_messages = conversation_repo.get_messages(
            conversation_id
        )
        st.session_state.messages = []
        for message in stored_messages:
            st.session_state.messages.append(
                {
                    "role": message["role"],
                    "content": message["content"],
                    "source": message.get(
                        "source"
                    )
                }
            )
        st.session_state.messages_loaded = True
    for message in st.session_state.messages:
        with st.chat_message(
            message["role"]
        ):
            st.markdown(
                message["content"]
            )
            if (
                message["role"] == "assistant"
                and message.get("source")
            ):
                if message["source"] == "documents":
                    st.caption(
                        "📄 Source: Company Documents"
                    )
                elif message["source"] == "web":
                    st.caption(
                        "🌐 Source: Web Search"
                    )
    question = st.chat_input(
        "Ask a question..."
    )
    if question:
        conversation_repo.save_message(
            conversation_id=conversation_id,
            role="user",
            content=question,
            source=None
        )
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
                "source": None
            }
        )
        with st.chat_message(
            "user"
        ):
            st.markdown(
                question
            )
        with st.chat_message(
            "assistant"
        ):
            status = st.empty()
            status.info(

                "📄 Searching company documents..."
            )
            result = assistant.ask(
                question
            )
            if result["source"] == "documents":
                status.success(
                    "📄 Answer found in company documents."
                )
            else:
                status.info(
                    "🌐 Company documents were insufficient. "
                    "Searching the web..."
                )
                status.success(
                    "🌐 Answer retrieved from the web."
                )
            answer = result["answer"]
            st.markdown(
                answer
            )
            conversation_repo.save_message(
                conversation_id=conversation_id,
                role="assistant",
                content=answer,
                source=result["source"]
            )
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "source": result["source"]
            }
        )