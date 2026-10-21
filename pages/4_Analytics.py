import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Analytics | WorkFlow AI",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = "Arjun"

if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

# ============================================================
# HEADER
# ============================================================

st.title("📊 Productivity Analytics")
st.caption(
    "Understand your capacity, task completion and productivity patterns."
)

st.divider()

# ============================================================
# DATE RANGE
# ============================================================

period = st.selectbox(
    "Analysis period",
    [
        "Last 7 days",
        "Last 30 days",
        "Custom"
    ]
)

if period == "Last 7 days":
    days = 7

elif period == "Last 30 days":
    days = 30

else:
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start date",
            value=date.today() - timedelta(days=7)
        )

    with col2:
        end_date = st.date_input(
            "End date",
            value=date.today()
        )

    days = max(
        (end_date - start_date).days + 1,
        1
    )

# ============================================================
# DUMMY DATA
# ============================================================

today = date.today()

dates = [
    today - timedelta(days=i)
    for i in range(days - 1, -1, -1)
]

capacity_values = [
    0.62,
    0.71,
    0.68,
    0.82,
    0.74,
    0.79,
    0.76
]

completion_values = [
    52,
    61,
    58,
    74,
    68,
    81,
    76
]

# Repeat values if Last 30 Days is selected
if days > 7:

    capacity_values = [
        capacity_values[i % 7]
        for i in range(days)
    ]

    completion_values = [
        completion_values[i % 7]
        for i in range(days)
    ]

else:

    capacity_values = capacity_values[-days:]
    completion_values = completion_values[-days:]


analytics_df = pd.DataFrame(
    {
        "Date": dates,
        "Capacity": capacity_values,
        "Completion": completion_values
    }
)

# ============================================================
# TOP SUMMARY
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Average Capacity",
        "0.74",
        "+6%"
    )

with c2:
    st.metric(
        "Avg. Completion",
        "68%",
        "+12%"
    )

with c3:
    st.metric(
        "Tasks Completed",
        "24",
        "+5"
    )

with c4:
    st.metric(
        "Effective Hours",
        "5.9 hrs",
        "+0.7"
    )

st.divider()

# ============================================================
# ROW 1 — CAPACITY + COMPLETION
# ============================================================

left, right = st.columns(2)

with left:

    st.subheader("Capacity Score Trend")

    fig_capacity = px.line(
        analytics_df,
        x="Date",
        y="Capacity",
        markers=True,
        range_y=[0, 1]
    )

    fig_capacity.update_layout(
        xaxis_title="Date",
        yaxis_title="Capacity Score",
        height=350,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        fig_capacity,
        use_container_width=True
    )

with right:

    st.subheader("Daily Task Completion")

    fig_completion = px.bar(
        analytics_df,
        x="Date",
        y="Completion"
    )

    fig_completion.update_layout(
        xaxis_title="Date",
        yaxis_title="Completion (%)",
        yaxis=dict(range=[0, 100]),
        height=350,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        fig_completion,
        use_container_width=True
    )

# ============================================================
# ROW 2 — PRODUCTIVITY HEATMAP
# ============================================================

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("🗓️ Productivity Calendar")

    heatmap_data = []

    for i in range(28):

        current_day = today - timedelta(days=27 - i)

        productivity = [
            35,
            52,
            67,
            82,
            74,
            91,
            63
        ][i % 7]

        heatmap_data.append(
            {
                "Date": current_day,
                "Week": current_day.strftime("%A"),
                "Productivity": productivity
            }
        )

    heatmap_df = pd.DataFrame(
        heatmap_data
    )

    heatmap_df["Week Number"] = (
        heatmap_df["Date"]
        .apply(lambda x: x.isocalendar().week)
    )

    fig_heatmap = px.density_heatmap(
        heatmap_df,
        x="Week Number",
        y="Week",
        z="Productivity",
        histfunc="avg",
        color_continuous_scale="Blues"
    )

    fig_heatmap.update_layout(
        height=350,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )

with right:

    st.subheader("📌 Task Completion Breakdown")

    task_types = pd.DataFrame(
        {
            "Type": [
                "Bug Fix",
                "Feature",
                "Research",
                "Documentation"
            ],
            "Percentage": [
                35,
                28,
                20,
                17
            ]
        }
    )

    fig_donut = px.pie(
        task_types,
        names="Type",
        values="Percentage",
        hole=0.55
    )

    fig_donut.update_layout(
        height=350,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        fig_donut,
        use_container_width=True
    )

# ============================================================
# INSIGHTS
# ============================================================

st.divider()

st.subheader("🧠 What the system has learned about you")

st.caption(
    "These are currently illustrative insights. "
    "The ML learning engine will generate them from your actual history later."
)

insight1, insight2 = st.columns(2)

with insight1:

    st.info(
        """
        ### 📅 Peak productivity

        **Wednesday**

        Your historical productivity pattern currently
        shows your strongest performance around the middle
        of the week.
        """
    )

    st.warning(
        """
        ### ⏱️ Task estimation

        **You underestimate task time by 34% on average.**

        Future task planning can account for this estimation gap.
        """
    )

with insight2:

    st.warning(
        """
        ### 😴 Sleep impact

        **Capacity drops 28% after less than 6 hours of sleep.**

        The behavioral model can use sleep as one of its inputs.
        """
    )

    st.success(
        """
        ### 🐛 Task performance

        **Bug-fix tasks have your highest completion rate at 88%.**

        The optimizer can consider historical task performance.
        """
    )

# ============================================================
# EXPORT
# ============================================================

st.divider()

st.subheader("📥 Export Analytics")

csv_data = analytics_df.to_csv(index=False)

st.download_button(
    label="Download Analytics CSV",
    data=csv_data,
    file_name="workflow_ai_analytics.csv",
    mime="text/csv"
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