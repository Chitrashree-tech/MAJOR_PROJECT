import streamlit as st
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Onboarding | WorkFlow AI",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = "Arjun"

if "onboarding_complete" not in st.session_state:
    st.session_state.onboarding_complete = False

if "github_connected" not in st.session_state:
    st.session_state.github_connected = False

if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 1


if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()


# ============================================================
# IF ALREADY COMPLETED
# ============================================================

if st.session_state.onboarding_complete:

    st.success("Your onboarding is already complete.")

    st.title("🚀 Welcome back!")

    st.write(
        "Your WorkFlow AI profile has already been configured."
    )

    if st.button(
        "Go to Dashboard",
        type="primary"
    ):
        st.switch_page(
            "pages/1_Dashboard.py"
        )

    st.stop()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .onboarding-title {
        text-align: center;
        font-size: 34px;
        font-weight: 700;
    }

    .onboarding-subtitle {
        text-align: center;
        color: #94A3B8;
        margin-bottom: 30px;
    }

    .step-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 25px;
        margin-top: 20px;
    }

    .step-number {
        color: #60A5FA;
        font-size: 14px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="onboarding-title">🚀 Welcome to WorkFlow AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="onboarding-subtitle">'
    'Let\'s personalize your productivity system.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PROGRESS
# ============================================================

step = st.session_state.onboarding_step

st.progress(
    step / 4
)

st.caption(
    f"Step {step} of 4"
)


# ============================================================
# STEP 1 — BASIC INFORMATION
# ============================================================

if step == 1:

    st.markdown(
        """
        <div class="step-card">

        <div class="step-number">
        STEP 1
        </div>

        <h2>👤 Basic Information</h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    name = st.text_input(
        "What should we call you?",
        value=st.session_state.user_name
    )

    role = st.selectbox(
        "What best describes you?",
        [
            "Developer",
            "Student",
            "Freelancer"
        ]
    )

    experience = st.selectbox(
        "Experience level",
        [
            "Junior",
            "Mid",
            "Senior"
        ]
    )

    st.write("")

    if st.button(
        "Continue →",
        type="primary",
        use_container_width=True
    ):

        if not name.strip():

            st.error(
                "Please enter your name."
            )

        else:

            st.session_state.user_name = name
            st.session_state.role = role
            st.session_state.experience = experience
            st.session_state.onboarding_step = 2

            st.rerun()


# ============================================================
# STEP 2 — WORK PREFERENCES
# ============================================================

elif step == 2:

    st.markdown(
        """
        <div class="step-card">

        <div class="step-number">
        STEP 2
        </div>

        <h2>💼 Work Preferences</h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    work_hours = st.slider(
        "Typical work hours per day",
        min_value=4,
        max_value=12,
        value=8
    )

    start_time = st.selectbox(
        "Preferred start time",
        [
            "6:00 AM",
            "7:00 AM",
            "8:00 AM",
            "9:00 AM",
            "10:00 AM",
            "11:00 AM"
        ]
    )

    work_style = st.selectbox(
        "Work style",
        [
            "Focused",
            "Multitasker",
            "Flexible"
        ]
    )

    st.info(
        f"You prefer around {work_hours} hours of work "
        f"starting at {start_time}."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Back",
            use_container_width=True
        ):

            st.session_state.onboarding_step = 1
            st.rerun()

    with col2:

        if st.button(
            "Continue →",
            type="primary",
            use_container_width=True
        ):

            st.session_state.work_hours = work_hours
            st.session_state.start_time = start_time
            st.session_state.work_style = work_style

            st.session_state.onboarding_step = 3

            st.rerun()


# ============================================================
# STEP 3 — GITHUB
# ============================================================

elif step == 3:

    st.markdown(
        """
        <div class="step-card">

        <div class="step-number">
        STEP 3
        </div>

        <h2>🐙 Connect GitHub</h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Connect GitHub so WorkFlow AI can track commits, "
        "pull requests and issues related to your tasks."
    )

    st.info(
        "Real GitHub OAuth will be connected later. "
        "For now this button simulates the connection."
    )

    if not st.session_state.github_connected:

        if st.button(
            "🔗 Connect GitHub Account",
            type="primary",
            use_container_width=True
        ):

            st.session_state.github_connected = True

            st.success(
                "GitHub account connected successfully!"
            )

            st.rerun()

    else:

        st.success(
            "🟢 GitHub connected as @arjun-dev"
        )

        if st.button(
            "Disconnect GitHub"
        ):

            st.session_state.github_connected = False
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Back",
            use_container_width=True
        ):

            st.session_state.onboarding_step = 2
            st.rerun()

    with col2:

        if st.button(
            "Continue →",
            type="primary",
            use_container_width=True
        ):

            st.session_state.onboarding_step = 4
            st.rerun()


# ============================================================
# STEP 4 — BEHAVIORAL BASELINE
# ============================================================

elif step == 4:

    st.markdown(
        """
        <div class="step-card">

        <div class="step-number">
        STEP 4
        </div>

        <h2>🧠 Behavioral Baseline</h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "These values give the system an initial understanding "
        "of your normal work capacity."
    )

    sleep = st.slider(
        "Average sleep hours",
        min_value=3.0,
        max_value=12.0,
        value=7.0,
        step=0.5
    )

    stress = st.slider(
        "Typical stress level",
        min_value=1,
        max_value=10,
        value=5
    )

    energy = st.slider(
        "Average energy level",
        min_value=1,
        max_value=10,
        value=7
    )

    # Initial baseline capacity
    baseline_capacity = (
        (sleep / 10 * 0.35)
        + ((10 - stress) / 10 * 0.25)
        + (energy / 10 * 0.40)
    )

    st.divider()

    st.metric(
        "Initial Capacity Estimate",
        f"{baseline_capacity:.2f}"
    )

    st.progress(
        baseline_capacity
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Back",
            use_container_width=True
        ):

            st.session_state.onboarding_step = 3
            st.rerun()

    with col2:

        if st.button(
            "🚀 Complete Setup",
            type="primary",
            use_container_width=True
        ):

            st.session_state.average_sleep = sleep
            st.session_state.typical_stress = stress
            st.session_state.average_energy = energy

            st.session_state.capacity_score = round(
                baseline_capacity,
                2
            )

            st.session_state.effective_hours = round(
                baseline_capacity * st.session_state.get(
                    "work_hours",
                    8
                ),
                1
            )

            st.session_state.onboarding_complete = True

            st.success(
                "Your WorkFlow AI profile is ready!"
            )

            st.switch_page(
                "pages/1_Dashboard.py"
            )