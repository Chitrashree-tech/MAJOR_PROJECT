import streamlit as st
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GitHub Activity | WorkFlow AI",
    page_icon="🐙",
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


# ============================================================
# LOGIN CHECK
# ============================================================

if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .page-title {
        font-size: 32px;
        font-weight: 700;
    }

    .subtitle {
        color: #94A3B8;
        margin-bottom: 20px;
    }

    .connection-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
    }

    .event-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .event-title {
        font-size: 16px;
        font-weight: 600;
    }

    .muted {
        color: #94A3B8;
        font-size: 13px;
    }

    .github-name {
        font-size: 20px;
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
    '<div class="page-title">🐙 GitHub Activity</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Track GitHub activity and automatically connect it with your tasks.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# GITHUB CONNECTION CARD
# ============================================================

st.subheader("GitHub Connection")

connection_col1, connection_col2 = st.columns([7, 2])

with connection_col1:

    if st.session_state.github_connected:

        st.markdown(
            """
            <div class="connection-card">

            🟢 <strong>GitHub Connected</strong>

            <br><br>

            <span class="github-name">
                @arjun-dev
            </span>

            <br>

            <span class="muted">
                Last synced: 5 minutes ago
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="connection-card">

            🔴 <strong>GitHub Not Connected</strong>

            <br><br>

            <span class="muted">
                Connect your GitHub account to automatically
                track commits, pull requests and issues.
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )


with connection_col2:

    if st.session_state.github_connected:

        if st.button(
            "🔄 Sync Now",
            type="primary",
            use_container_width=True
        ):

            with st.spinner("Syncing GitHub activity..."):

                import time
                time.sleep(1)

            st.success(
                "GitHub activity synced!"
            )

        if st.button(
            "Disconnect",
            use_container_width=True
        ):

            st.session_state.github_connected = False
            st.rerun()

    else:

        if st.button(
            "🔗 Connect GitHub",
            type="primary",
            use_container_width=True
        ):

            st.session_state.github_connected = True

            st.success(
                "GitHub account connected!"
            )

            st.rerun()


# ============================================================
# FILTER
# ============================================================

st.divider()

st.subheader("Activity")

filter_type = st.radio(
    "Filter events",
    [
        "All Events",
        "Commits Only",
        "PRs Only",
        "Issues Only"
    ],
    horizontal=True
)


# ============================================================
# DUMMY GITHUB EVENTS
# ============================================================

events = [

    {
        "type": "Commit",
        "icon": "🟢",
        "description": "fixed null pointer exception in AuthService.java",
        "task": "Fix authentication bug",
        "repository": "workflow-api",
        "time": "3 mins ago",
        "progress": 40
    },

    {
        "type": "PR",
        "icon": "🟣",
        "description": "feature/user-profile-endpoint",
        "task": "Build user dashboard API",
        "repository": "workflow-api",
        "time": "1 hour ago",
        "progress": 80
    },

    {
        "type": "Issue",
        "icon": "🔵",
        "description": "database connection timeout fix",
        "task": "Fix authentication bug",
        "repository": "workflow-api",
        "time": "2 hours ago",
        "progress": 100
    },

    {
        "type": "Commit",
        "icon": "🟢",
        "description": "added unit test for login controller",
        "task": "Write unit tests",
        "repository": "workflow-api",
        "time": "3 hours ago",
        "progress": 30
    },

    {
        "type": "Commit",
        "icon": "🟢",
        "description": "updated README with API documentation",
        "task": "Update project documentation",
        "repository": "workflow-api",
        "time": "5 hours ago",
        "progress": 20
    }
]


# ============================================================
# FILTER EVENTS
# ============================================================

if filter_type == "Commits Only":

    filtered_events = [
        event
        for event in events
        if event["type"] == "Commit"
    ]

elif filter_type == "PRs Only":

    filtered_events = [
        event
        for event in events
        if event["type"] == "PR"
    ]

elif filter_type == "Issues Only":

    filtered_events = [
        event
        for event in events
        if event["type"] == "Issue"
    ]

else:

    filtered_events = events


# ============================================================
# ACTIVITY TIMELINE
# ============================================================

for event in filtered_events:

    st.markdown(
        f"""
        <div class="event-card">

        <div class="event-title">
            {event["icon"]}
            {event["type"]}: {event["description"]}
        </div>

        <br>

        <span class="muted">
            Repository:
        </span>

        <strong>
            {event["repository"]}
        </strong>

        &nbsp;&nbsp;•&nbsp;&nbsp;

        <span class="muted">
            {event["time"]}
        </span>

        <br><br>

        <span class="muted">
            Linked task:
        </span>

        <strong>
            {event["task"]}
        </strong>

        <br><br>

        <span class="muted">
            Progress contribution
        </span>

        <div style="margin-top:8px;">
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        event["progress"] / 100
    )

    st.caption(
        f"Activity contribution: {event['progress']}%"
    )


# ============================================================
# UNMAPPED ACTIVITY
# ============================================================

st.divider()

st.subheader("🔍 Activity Not Linked to Any Task")

st.caption(
    "These GitHub activities could not automatically be matched "
    "with an existing task."
)


unmapped = [
    {
        "description": "refactor database connection pool",
        "repository": "workflow-api",
        "time": "6 hours ago"
    },
    {
        "description": "update CI/CD workflow",
        "repository": "workflow-infrastructure",
        "time": "Yesterday"
    }
]


for index, activity in enumerate(unmapped):

    col1, col2, col3 = st.columns(
        [5, 2, 2]
    )

    with col1:

        st.write(
            f"🟢 **{activity['description']}**"
        )

        st.caption(
            f"{activity['repository']} • {activity['time']}"
        )

    with col2:

        selected_task = st.selectbox(
            "Link to task",
            [
                "Select task...",
                "Fix authentication bug",
                "Build user dashboard API",
                "Write unit tests",
                "Update project documentation",
                "Review pull request"
            ],
            key=f"link_task_{index}"
        )

    with col3:

        if st.button(
            "Link Activity",
            key=f"link_{index}",
            use_container_width=True
        ):

            if selected_task != "Select task...":

                st.success(
                    f"Linked to {selected_task}"
                )

            else:

                st.warning(
                    "Select a task first."
                )


# ============================================================
# GITHUB STATISTICS
# ============================================================

st.divider()

st.subheader("📈 GitHub Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Commits",
        "18",
        "+4"
    )

with c2:
    st.metric(
        "PRs Merged",
        "5",
        "+2"
    )

with c3:
    st.metric(
        "Issues Closed",
        "8",
        "+3"
    )

with c4:
    st.metric(
        "Activity → Tasks",
        "82%",
        "+7%"
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
        "⚙️ Settings",
        use_container_width=True
    ):
        st.switch_page(
            "pages/6_Settings.py"
        )