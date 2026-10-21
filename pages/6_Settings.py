import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Settings | WorkFlow AI",
    page_icon="⚙️",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = "Arjun"

if "github_connected" not in st.session_state:
    st.session_state.github_connected = False


if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("⚙️ Settings")

st.caption(
    "Manage your profile, integrations, notifications and preferences."
)

st.divider()


# ============================================================
# PROFILE
# ============================================================

st.header("👤 Profile")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Name",
        value=st.session_state.user_name
    )

    email = st.text_input(
        "Email",
        value="admin@test.com"
    )

with col2:

    role = st.selectbox(
        "Role",
        [
            "Developer",
            "Student",
            "Freelancer"
        ]
    )

    experience = st.selectbox(
        "Experience Level",
        [
            "Junior",
            "Mid",
            "Senior"
        ]
    )


if st.button(
    "Save Profile",
    type="primary"
):

    st.session_state.user_name = name

    st.success(
        "Profile saved successfully."
    )


# ============================================================
# GITHUB
# ============================================================

st.divider()

st.header("🐙 GitHub Integration")

if st.session_state.github_connected:

    st.success(
        "🟢 GitHub account connected"
    )

    st.write(
        "**Connected account:** @arjun-dev"
    )

    st.write(
        "**Webhook:** 🟢 Active"
    )

    if st.button(
        "Disconnect GitHub"
    ):

        st.session_state.github_connected = False

        st.success(
            "GitHub disconnected."
        )

        st.rerun()

else:

    st.warning(
        "GitHub account is not connected."
    )

    if st.button(
        "Connect GitHub",
        type="primary"
    ):

        st.session_state.github_connected = True

        st.success(
            "GitHub connected!"
        )

        st.rerun()


# ============================================================
# NOTIFICATIONS
# ============================================================

st.divider()

st.header("🔔 Notification Preferences")

daily_reminder = st.toggle(
    "Daily morning reminder",
    value=True
)

deadline_alerts = st.toggle(
    "Deadline alerts",
    value=True
)

progress_updates = st.toggle(
    "Progress updates",
    value=True
)

weekly_report = st.toggle(
    "Weekly analytics report",
    value=True
)


# ============================================================
# WORK PREFERENCES
# ============================================================

st.divider()

st.header("💼 Work Preferences")

work_hours = st.slider(
    "Reference work hours",
    min_value=4,
    max_value=12,
    value=8
)

task_load = st.selectbox(
    "Preferred task load",
    [
        "Light (3-4 tasks)",
        "Moderate (4-6 tasks)",
        "Heavy (6-8 tasks)"
    ]
)

task_types = st.multiselect(
    "Preferred task types",
    [
        "Bug Fix",
        "Feature",
        "Research",
        "Documentation",
        "Testing"
    ],
    default=[
        "Feature",
        "Bug Fix"
    ]
)


if st.button(
    "Save Work Preferences"
):

    st.success(
        "Work preferences saved."
    )


# ============================================================
# DATA & PRIVACY
# ============================================================

st.divider()

st.header("🔐 Data & Privacy")

st.write(
    "Your productivity data is currently stored locally "
    "while the application is in development."
)

if st.button(
    "📥 Export My Data"
):

    export_data = f"""
WorkFlow AI User Data

Name: {st.session_state.user_name}
Email: {email}
Role: {role}
Experience: {experience}
Reference Work Hours: {work_hours}
Preferred Task Load: {task_load}
"""

    st.download_button(
        "Download Data",
        data=export_data,
        file_name="workflow_ai_user_data.txt",
        mime="text/plain"
    )


if st.button(
    "🗑️ Clear History"
):

    st.warning(
        "History clearing will be connected to the database later."
    )


# ============================================================
# DANGER ZONE
# ============================================================

st.divider()

st.header("⚠️ Danger Zone")

st.error(
    "Deleting your account is permanent."
)

delete_confirm = st.checkbox(
    "I understand that this action cannot be undone."
)

if st.button(
    "Delete Account"
):

    if delete_confirm:

        st.session_state.clear()

        st.success(
            "Account deleted."
        )

        st.rerun()

    else:

        st.warning(
            "Please confirm account deletion first."
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚡ WorkFlow AI")

    st.caption(
        f"Logged in as {st.session_state.user_name}"
    )

    st.divider()

    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):
        st.switch_page(
            "pages/1_Dashboard.py"
        )

    if st.button(
        "☀️ Morning Check-in",
        use_container_width=True
    ):
        st.switch_page(
            "pages/2_Morning_Checkin.py"
        )

    if st.button(
        "📋 Projects & Tasks",
        use_container_width=True
    ):
        st.switch_page(
            "pages/3_Projects_and_Tasks.py"
        )

    if st.button(
        "📊 Analytics",
        use_container_width=True
    ):
        st.switch_page(
            "pages/4_Analytics.py"
        )

    if st.button(
        "🐙 GitHub Activity",
        use_container_width=True
    ):
        st.switch_page(
            "pages/5_GitHub_Activity.py"
        )