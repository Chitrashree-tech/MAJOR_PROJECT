import streamlit as st
from datetime import date

from utils.api_client import check_backend


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Morning Check-in | WorkFlow AI",
    page_icon="☀️",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "checkin_done" not in st.session_state:
    st.session_state.checkin_done = False

if "capacity_score" not in st.session_state:
    st.session_state.capacity_score = 0.74

if "effective_hours" not in st.session_state:
    st.session_state.effective_hours = 5.9

if "energy_level" not in st.session_state:
    st.session_state.energy_level = 7

if "stress_level" not in st.session_state:
    st.session_state.stress_level = 3

if "sleep_hours" not in st.session_state:
    st.session_state.sleep_hours = 7.0

if "mood" not in st.session_state:
    st.session_state.mood = "🙂"

if "blockers" not in st.session_state:
    st.session_state.blockers = ""

if "meeting_hours" not in st.session_state:
    st.session_state.meeting_hours = 0.0


# ============================================================
# LOGIN CHECK
# ============================================================

if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()


# ============================================================
# BACKEND STATUS
# ============================================================

if check_backend():
    st.sidebar.success("🟢 Backend connected")
else:
    st.sidebar.error("🔴 Backend offline")


# ============================================================
# HEADER
# ============================================================

st.title("☀️ Good Morning")
st.subheader("Let's plan your day")

st.caption(
    date.today().strftime("%A, %d %B %Y")
)

st.divider()


# ============================================================
# SECTION 1 — FEELING
# ============================================================

st.header("1. How are you feeling today?")

col1, col2 = st.columns(2)


with col1:

    energy = st.slider(
        "Energy level",
        min_value=1,
        max_value=10,
        value=st.session_state.energy_level
    )

    st.session_state.energy_level = energy

    if energy <= 3:
        st.info("😴 Exhausted")

    elif energy <= 6:
        st.info("😐 Okay")

    else:
        st.success("⚡ Energized")


with col2:

    stress = st.slider(
        "Stress level",
        min_value=1,
        max_value=10,
        value=st.session_state.stress_level
    )

    st.session_state.stress_level = stress

    if stress <= 3:
        st.success("🟢 Low stress")

    elif stress <= 6:
        st.info("🟡 Moderate stress")

    else:
        st.warning("🔴 High stress")


# ============================================================
# SLEEP
# ============================================================

st.subheader("Sleep last night")

sleep = st.number_input(
    "Sleep hours",
    min_value=0.0,
    max_value=12.0,
    value=st.session_state.sleep_hours,
    step=0.5
)

st.session_state.sleep_hours = sleep

sleep_cols = st.columns(4)

for col, hours in zip(
    sleep_cols,
    [5, 6, 7, 8]
):

    with col:

        if st.button(
            f"{hours} hours",
            use_container_width=True
        ):

            st.session_state.sleep_hours = float(
                hours
            )

            st.rerun()


# ============================================================
# SECTION 2 — AVAILABILITY
# ============================================================

st.divider()

st.header("2. Today's availability")

blockers = st.text_input(
    "Any blockers or distractions today?",
    value=st.session_state.blockers,
    placeholder="Example: Waiting for API credentials..."
)

st.session_state.blockers = blockers


meetings = st.toggle(
    "Do you have meetings today?"
)


meeting_hours = 0.0

if meetings:

    meeting_hours = st.number_input(
        "How many hours of meetings?",
        min_value=0.0,
        max_value=12.0,
        value=1.0,
        step=0.5
    )

st.session_state.meeting_hours = meeting_hours


# ============================================================
# SECTION 3 — MOOD
# ============================================================

st.divider()

st.header("3. Mood")

moods = [
    "😴",
    "😟",
    "😐",
    "🙂",
    "😊",
    "😄"
]

mood = st.radio(
    "How would you describe your mood?",
    moods,
    horizontal=True,
    index=moods.index(
        st.session_state.mood
    )
)

st.session_state.mood = mood


# ============================================================
# CAPACITY CALCULATION
# ============================================================

capacity = (
    (sleep / 10 * 0.35)
    + ((10 - stress) / 10 * 0.25)
    + (energy / 10 * 0.40)
)

capacity = min(
    max(capacity, 0),
    1
)


# Account for meetings.

available_hours = max(
    0,
    8 - meeting_hours
)

effective_hours = round(
    capacity * available_hours,
    1
)


# ============================================================
# LIVE PREVIEW
# ============================================================

st.divider()

st.header("🔮 Your predicted capacity")

metric1, metric2 = st.columns(2)


with metric1:

    st.metric(
        "Capacity Score",
        f"{capacity:.2f}"
    )


with metric2:

    st.metric(
        "Effective Work Hours",
        f"{effective_hours} hrs"
    )


st.progress(capacity)


if capacity < 0.4:

    st.warning(
        "Low capacity day — your plan will prioritize essential tasks."
    )

elif capacity < 0.7:

    st.info(
        "Moderate capacity — your plan will balance important and normal tasks."
    )

else:

    st.success(
        "Good capacity — you can handle a larger workload today."
    )


# ============================================================
# SUBMIT
# ============================================================

st.divider()

if st.button(
    "🚀 Generate My Day Plan",
    type="primary",
    use_container_width=True
):

    # Save today's check-in.
    # The trained Behavior Model will replace the
    # temporary capacity calculation once available.

    st.session_state.checkin_done = True

    st.session_state.capacity_score = capacity

    st.session_state.effective_hours = effective_hours

    st.session_state.energy_level = energy

    st.session_state.stress_level = stress

    st.session_state.sleep_hours = sleep

    st.session_state.mood = mood

    st.session_state.blockers = blockers

    st.session_state.meeting_hours = meeting_hours


    st.success(
        "✅ Check-in saved! Your current capacity has been calculated."
    )


    st.switch_page(
        "pages/1_Dashboard.py"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚡ WorkFlow AI")

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