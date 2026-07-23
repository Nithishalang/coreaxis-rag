import streamlit as st
from src.auth.auth_service import AuthService
from src.ui.login import show_login_page
from src.ui.register import show_register_page
from src.ui.chat import show_chat
st.set_page_config(
    page_title="CoreAxis AI Assistant",
    page_icon="🤖",
    layout="wide"
)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "page" not in st.session_state:
    st.session_state.page = "login"
@st.cache_resource
def load_auth_service():
    return AuthService()
auth_service = load_auth_service()
if st.session_state.logged_in:
    show_chat()
else:
    if st.session_state.page == "login":
        show_login_page(
            auth_service
        )
        st.divider()
        if st.button(
            "Create a new account"
        ):
            st.session_state.page = "register"
            st.rerun()
    elif st.session_state.page == "register":
        show_register_page(
            auth_service
        )
        st.divider()
        if st.button(
            "Already have an account? Login"
        ):
            st.session_state.page = "login"
            st.rerun()