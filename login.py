import streamlit as st
def show_login_page(auth_service):
    st.title("CoreAxis AI")
    st.subheader("Welcome back")
    st.write("Sign in to continue to your AI assistant.")
    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )
    if st.button(
        "Login",
        use_container_width=True
    ):
        if not email or not password:
            st.error(
                "Please enter your email and password."
            )
            return
        result = auth_service.login_user(
            email,
            password
        )
        if result["success"]:
            st.session_state.logged_in = True
            st.session_state.user_id = result["user_id"]
            st.session_state.user_email = email
            st.session_state.page = "chat"
            st.success(
                "Login successful."
            )
            st.rerun()
        else:
            st.error(
                result["message"]
            )
    st.divider()
    st.write(
        "Don't have an account?"
    )
    if st.button(
        "Create an account",
        use_container_width=True
    ):
        st.session_state.page = "register"
        st.rerun()