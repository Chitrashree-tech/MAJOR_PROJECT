import streamlit as st
from datetime import date

from utils.api_client import api_post, api_get


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Projects & Tasks | WorkFlow AI",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = 1

if "selected_project_id" not in st.session_state:
    st.session_state.selected_project_id = 1

if "show_add_task" not in st.session_state:
    st.session_state.show_add_task = False


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

    .project-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
    }

    .task-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .muted {
        color: #94A3B8;
        font-size: 13px;
    }

    .dependency-box {
        background: #0F172A;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="page-title">📋 Projects & Tasks</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Manage your projects, tasks and dependencies.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# BACKEND STATUS
# ============================================================

backend_health = api_get("/health")

if "error" in backend_health:
    st.error("🔴 Backend offline")
else:
    st.success("🟢 Backend connected")


# ============================================================
# MAIN LAYOUT
# ============================================================

left, right = st.columns([3, 7])


# ============================================================
# LEFT — PROJECT LIST
# ============================================================

with left:

    st.subheader("Projects")

    # For now we use the existing demo project.
    # Backend project endpoints will be added next.

    projects = {
        1: {
            "name": "WorkFlow AI Demo",
            "deadline": "2026-12-31",
            "progress": 0
        }
    }

    for project_id, project in projects.items():

        if st.button(
            project["name"],
            key=f"project_{project_id}",
            use_container_width=True
        ):

            st.session_state.selected_project_id = (
                project_id
            )

            st.rerun()

        st.markdown(
            f"""
            <div class="project-card">

                <strong>{project["name"]}</strong>

                <div class="muted">
                    Deadline: {project["deadline"]}
                </div>

                <div style="margin-top:8px;">
                    Progress: {project["progress"]}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            project["progress"] / 100
        )


# ============================================================
# SELECT PROJECT
# ============================================================

selected_project_id = (
    st.session_state.selected_project_id
)

selected_project = projects.get(
    selected_project_id,
    projects[1]
)


# ============================================================
# RIGHT — PROJECT DETAILS
# ============================================================

with right:

    st.subheader(
        selected_project["name"]
    )

    st.caption(
        f"Deadline: {selected_project['deadline']}"
    )


    # --------------------------------------------------------
    # LOAD TASKS FROM BACKEND
    # --------------------------------------------------------

    task_response = api_get(
        f"/projects/{selected_project_id}/tasks"
    )

    if isinstance(task_response, dict) and "error" in task_response:

        backend_tasks = []

        st.warning(
            "Could not load tasks from backend."
        )

    elif isinstance(task_response, list):

        backend_tasks = task_response

    else:

        backend_tasks = []


    # --------------------------------------------------------
    # PROJECT METRICS
    # --------------------------------------------------------

    total_tasks = len(backend_tasks)

    completed_tasks = len(
        [
            task
            for task in backend_tasks
            if task.get("status") == "Completed"
        ]
    )

    if total_tasks > 0:

        progress = round(
            completed_tasks / total_tasks * 100
        )

    else:

        progress = 0


    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric(
            "Total Tasks",
            total_tasks
        )

    with m2:

        st.metric(
            "Completed",
            completed_tasks
        )

    with m3:

        st.metric(
            "Progress",
            f"{progress}%"
        )

    st.progress(
        progress / 100
    )

    st.divider()


    # ========================================================
    # TASK HEADER
    # ========================================================

    task_header, task_button = st.columns(
        [7, 2]
    )

    with task_header:

        st.subheader("Tasks")

    with task_button:

        if st.button(
            "➕ Add Task",
            use_container_width=True
        ):

            st.session_state.show_add_task = True


    # ========================================================
    # ADD TASK FORM
    # ========================================================

    if st.session_state.show_add_task:

        with st.expander(
            "Create New Task",
            expanded=True
        ):

            with st.form("new_task_form"):

                task_name = st.text_input(
                    "Task name"
                )

                description = st.text_area(
                    "Description"
                )

                c1, c2 = st.columns(2)

                with c1:

                    priority = st.selectbox(
                        "Priority",
                        [
                            "Critical",
                            "High",
                            "Medium",
                            "Low"
                        ]
                    )

                    estimated_hours = st.number_input(
                        "Estimated hours",
                        min_value=0.5,
                        max_value=100.0,
                        value=1.0,
                        step=0.5
                    )

                with c2:

                    deadline = st.date_input(
                        "Deadline",
                        value=date.today()
                    )

                    task_type = st.selectbox(
                        "Task type",
                        [
                            "Bug Fix",
                            "Feature",
                            "Research",
                            "Documentation",
                            "Testing"
                        ]
                    )

                github_issue = st.text_input(
                    "GitHub issue number",
                    placeholder="Example: #123"
                )

                submitted = st.form_submit_button(
                    "Create Task",
                    type="primary"
                )


                # ------------------------------------------------
                # CREATE TASK THROUGH FASTAPI
                # ------------------------------------------------

                if submitted:

                    if not task_name.strip():

                        st.error(
                            "Task name is required."
                        )

                    else:

                        result = api_post(
                            "/tasks",
                            {
                                "name": task_name,
                                "description": description,
                                "priority": priority,
                                "task_type": task_type,
                                "estimated_hours": estimated_hours,
                                "deadline": deadline.strftime(
                                    "%Y-%m-%d"
                                ),
                                "github_issue": (
                                    github_issue
                                    if github_issue
                                    else None
                                ),
                                "project_id": selected_project_id
                            }
                        )


                        if (
                            isinstance(result, dict)
                            and "error" in result
                        ):

                            st.error(
                                result["error"]
                            )

                        else:

                            st.success(
                                "✅ Task saved to database!"
                            )

                            st.session_state.show_add_task = False

                            st.rerun()


    # ========================================================
    # TASK LIST
    # ========================================================

    if not backend_tasks:

        st.info(
            "No tasks yet. Add your first task."
        )

    else:

        for task in backend_tasks:

            with st.expander(
                f"{task['name']} • "
                f"{task['priority']}"
            ):

                c1, c2, c3, c4 = st.columns(4)

                with c1:

                    st.write("**Priority**")

                    st.write(
                        task["priority"]
                    )

                with c2:

                    st.write("**Estimated Time**")

                    st.write(
                        f"{task['estimated_hours']} hrs"
                    )

                with c3:

                    st.write("**Deadline**")

                    st.write(
                        task["deadline"]
                        or "No deadline"
                    )

                with c4:

                    st.write("**Status**")

                    st.write(
                        task["status"]
                    )

                st.divider()

                st.write(
                    f"**Task ID:** {task['id']}"
                )

                st.write(
                    f"**Task Type:** "
                    f"{task.get('task_type', 'Not specified')}"
                )


# ============================================================
# DEPENDENCY TREE
# ============================================================

st.divider()

st.subheader(
    "🔗 Dependency Tree"
)

st.info(
    "Task dependency visualization will be connected "
    "to the database in the next backend step."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## ⚡ WorkFlow AI"
    )

    st.caption(
        f"Logged in as "
        f"{st.session_state.get('user_name', 'User')}"
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