import streamlit as st

st.set_page_config(
    page_title="WorkFlow AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = "Arjun"

if "onboarding_complete" not in st.session_state:
    st.session_state.onboarding_complete = False

if "checkin_done" not in st.session_state:
    st.session_state.checkin_done = False

if "github_connected" not in st.session_state:
    st.session_state.github_connected = False

if "capacity_score" not in st.session_state:
    st.session_state.capacity_score = 0.74

if "effective_hours" not in st.session_state:
    st.session_state.effective_hours = 5.9

if "selected_project" not in st.session_state:
    st.session_state.selected_project = None

if "today_tasks" not in st.session_state:
    st.session_state.today_tasks = []


# -----------------------------
# Login
# -----------------------------
st.markdown(
    """
    <style>
    .login-card {
        background: #1E293B;
        padding: 40px;
        border-radius: 16px;
        max-width: 500px;
        margin: 80px auto;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
    }

    .subtitle {
        text-align: center;
        color: #94A3B8;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if not st.session_state.logged_in:

    st.markdown(
        '<div class="title">⚡ WorkFlow AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-powered dynamic workload allocation</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Welcome back")

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    col1, col2 = st.columns(2)

    with col1:
        login = st.button(
            "Login",
            use_container_width=True,
            type="primary"
        )

    with col2:
        signup = st.button(
            "Sign Up",
            use_container_width=True
        )

    if login:

        if email == "admin@test.com" and password == "admin123":

            st.session_state.logged_in = True
            st.session_state.user_name = "Arjun"

            st.success("Login successful!")

            st.switch_page("pages/7_Onboarding.py")

        else:
            st.error(
                "Invalid credentials. Use admin@test.com / admin123"
            )

    st.divider()

    if st.button(
        "🔗 Connect with GitHub",
        use_container_width=True
    ):
        st.info("GitHub OAuth will be connected here later.")

    st.caption(
        "Demo credentials: admin@test.com / admin123"
    )

else:

    st.title("⚡ WorkFlow AI")

    st.success(
        f"Welcome back, {st.session_state.user_name}!"
    )

    st.write(
        "Your AI-powered productivity optimization system."
    )

    if st.button("Open Dashboard", type="primary"):
        st.switch_page("pages/1_Dashboard.py")