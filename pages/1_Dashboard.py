import streamlit as st
from datetime import datetime

from utils.api_client import check_backend, api_get


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Dashboard | WorkFlow AI",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = "User"

if "checkin_done" not in st.session_state:
    st.session_state.checkin_done = False

if "capacity_score" not in st.session_state:
    st.session_state.capacity_score = 0.74

if "effective_hours" not in st.session_state:
    st.session_state.effective_hours = 5.9


# ============================================================
# LOGIN CHECK
# ============================================================

if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()


# ============================================================
# BACKEND CONNECTION
# ============================================================

backend_status = check_backend()

if backend_status:
    st.sidebar.success("🟢 Backend connected")
else:
    st.sidebar.error("🔴 Backend offline")


# ============================================================
# LOAD REAL TASKS FROM BACKEND
# ============================================================

task_response = api_get(
    "/projects/1/tasks"
)

if isinstance(task_response, list):
    tasks = task_response
else:
    tasks = []


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #94A3B8;
        font-size: 15px;
    }

    .metric-card {
        background: #1E293B;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #334155;
        min-height: 150px;
    }

    .metric-label {
        color: #94A3B8;
        font-size: 14px;
    }

    .metric-value {
        font-size: 34px;
        font-weight: 700;
        margin-top: 8px;
    }

    .metric-description {
        color: #CBD5E1;
        font-size: 13px;
        margin-top: 5px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .task-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
    }

    .task-name {
        font-size: 16px;
        font-weight: 600;
    }

    .muted {
        color: #94A3B8;
        font-size: 13px;
    }

    .activity-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .banner {
        background: #172554;
        border: 1px solid #2563EB;
        border-radius: 12px;
        padding: 18px;
        margin: 20px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

today = datetime.now()

st.markdown(
    f"""
    <div class="main-title">
        Good Morning, {st.session_state.user_name} 👋
    </div>

    <div class="subtitle">
        {today.strftime("%A, %d %B %Y")}
        • Here's your productivity overview
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MORNING CHECK-IN
# ============================================================

if not st.session_state.checkin_done:

    st.markdown(
        """
        <div class="banner">
            <strong>
                ☀️ You have not completed your morning check-in yet.
            </strong>
            <br>
            <span style="color:#BFDBFE;">
                Complete your check-in so WorkFlow AI can plan your day.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Plan My Day →",
        type="primary"
    ):
        st.switch_page(
            "pages/2_Morning_Checkin.py"
        )


# ============================================================
# CALCULATE TASK METRICS
# ============================================================

total_tasks = len(tasks)

completed_tasks = len(
    [
        task
        for task in tasks
        if task.get("status") == "Completed"
    ]
)

if total_tasks > 0:

    completion_rate = round(
        completed_tasks / total_tasks * 100
    )

else:

    completion_rate = 0


# ============================================================
# METRIC CARDS
# ============================================================

st.markdown(
    '<div class="section-title">Today at a glance</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Today's Capacity Score
            </div>

            <div class="metric-value">
                {st.session_state.capacity_score:.2f}
            </div>

            <div class="metric-description">
                Based on your current capacity
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Effective Work Hours
            </div>

            <div class="metric-value">
                {st.session_state.effective_hours} hrs
            </div>

            <div class="metric-description">
                Available working capacity
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Task Completion Rate
            </div>

            <div class="metric-value">
                {completion_rate}%
            </div>

            <div class="metric-description">
                Based on saved tasks
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TASK LIST
# ============================================================

st.markdown(
    '<div class="section-title">🎯 Today\'s Task List</div>',
    unsafe_allow_html=True
)


if not tasks:

    st.info(
        "No tasks found. Add tasks from Projects & Tasks."
    )

else:

    for i, task in enumerate(tasks):

        col_check, col_task, col_priority, col_time, col_status = st.columns(
            [0.5, 4, 1.4, 1.4, 1.5]
        )


        with col_check:

            completed = st.checkbox(
                "",
                key=f"dashboard_task_{task['id']}"
            )


        with col_task:

            st.markdown(
                f"""
                <div class="task-name">
                    {task["name"]}
                </div>

                <div class="muted">
                    {task.get("task_type", "Task")}
                    • Task ID: {task["id"]}
                </div>
                """,
                unsafe_allow_html=True
            )


        with col_priority:

            priority = task.get(
                "priority",
                "Medium"
            )

            if priority == "Critical":

                st.error(priority)

            elif priority == "High":

                st.warning(priority)

            elif priority == "Medium":

                st.info(priority)

            else:

                st.success(priority)


        with col_time:

            st.write(
                f"⏱️ {task.get('estimated_hours', 0)} hrs"
            )


        with col_status:

            st.write(
                task.get(
                    "status",
                    "Pending"
                )
            )


# ============================================================
# RE-OPTIMIZE
# ============================================================

st.write("")

if st.button(
    "🔄 Re-optimize My Day",
    type="primary"
):

    st.info(
        "Optimization Engine will be connected "
        "to the trained ML models once they are ready."
    )


# ============================================================
# BOTTOM SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📊 Activity & Dependencies</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)


# ============================================================
# GITHUB ACTIVITY
# ============================================================

with left:

    st.subheader("GitHub Activity")

    st.info(
        "GitHub activity will appear here once a "
        "GitHub repository is connected."
    )


# ============================================================
# DEPENDENCY TREE
# ============================================================

with right:

    st.subheader("Task Dependencies")

    st.info(
        "Dependency visualization will be connected "
        "to the task engine next."
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

    st.markdown("### Quick Actions")


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


    if st.button(
        "⚙️ Settings",
        use_container_width=True
    ):

        st.switch_page(
            "pages/6_Settings.py"
        )


    st.divider()


    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.rerun()