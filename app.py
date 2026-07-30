import streamlit as st
from main import CoreAxisRAG

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="CoreAxis Knowledge Assistant",
    page_icon="📘",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1000px;
}

h1{
    font-weight:700;
}

div[data-testid="stChatMessage"]{
    padding-bottom:0.8rem;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("📘 CoreAxis")

    st.markdown("### Knowledge Assistant")

    st.divider()

    st.markdown("""
Ask questions about:

- 👨‍💼 Human Resources
- 💰 Finance
- 💻 Software Engineering
- 🤖 AI & Machine Learning
- 🔒 Information Security
- 🖥️ Information Technology
""")

    st.divider()

    st.markdown("### System")

    st.caption("Hybrid Retrieval")
    st.caption("• Vector Search")
    st.caption("• BM25 Search")
    st.caption("• Cross-Encoder Reranker")
    st.caption("• Web Search Fallback")

    st.divider()

    if st.button("🗑️ New Chat"):

        st.session_state.messages = []
        st.rerun()

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("CoreAxis Knowledge Assistant")

st.caption(
    "Ask questions about company policies, procedures and internal handbooks."
)

# --------------------------------------------------
# Load Assistant
# --------------------------------------------------

@st.cache_resource
def load_assistant():
    return CoreAxisRAG()

if "assistant" not in st.session_state:

    with st.spinner("Loading Assistant..."):
        st.session_state.assistant = load_assistant()

assistant = st.session_state.assistant

# --------------------------------------------------
# Chat History
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            if message.get("source") == "documents":
                st.caption("📄 Company Handbook")

            elif message.get("source") == "web":
                st.caption("🌐 Web Search")

# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input("Ask a question...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            result = assistant.ask(question)

        with st.container(border=True):

            st.markdown(result["answer"])

        if result["source"] == "documents":

            st.caption("📄 Company Handbook")

        else:

            st.caption("🌐 Web Search")

    st.session_state.messages.append({

        "role": "assistant",

        "content": result["answer"],

        "source": result["source"]

    })
