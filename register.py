import streamlit as st
def show_register_page(auth_service):
    st.title("CoreAxis AI")
    st.subheader("Create your account")
    st.write(
        "Create an account to start using the CoreAxis AI Assistant."
    )
    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password"
    )
    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Re-enter your password"
    )
    if st.button(
        "Create Account",
        use_container_width=True
    ):
        if not email or not password or not confirm_password:
            st.error(
                "Please fill in all fields."
            )
            return
        if password != confirm_password:
            st.error(
                "Passwords do not match."
            )
            return
        result = auth_service.register_user(
            email,
            password
        )
        if result["success"]:
            st.success(
                "Account created successfully."
            )
            st.info(
                "You can now log in with your new account."
            )
            if st.button(
                "Go to Login",
                use_container_width=True
            ):
                st.session_state.page = "login"
                st.rerun()
        else:
            st.error(
                result["message"]
            )
    st.divider()
    st.write(
        "Already have an account?"
    )
    if st.button(
        "Back to Login",
        use_container_width=True
    ):
        st.session_state.page = "login"
        st.rerun()