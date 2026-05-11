import streamlit as st
import requests

st.set_page_config(
    page_title="HumanSignals",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>

.main {
    padding-top: 2rem;
}

.stButton button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
}

textarea {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.header("🧠 HumanSignals")

    st.markdown("""
    AI-powered emotional pattern tracking and behavioral insights.
    """)

    st.divider()

    st.write("Version 0.1")

# HEADER
st.title("🧠 HumanSignals")

st.markdown("""
Track emotional patterns, stress levels and behavioral trends over time.
""")

st.divider()

# METRICS
m1, m2, m3 = st.columns(3)

m1.metric("Current Mood", "7/10")
m2.metric("Stress Level", "Medium")
m3.metric("Sleep Average", "6.8h")

st.divider()

# FORM SECTION
st.subheader("Daily Emotional Check-in")

col1, col2 = st.columns(2)

with col1:
    mood = st.slider("Mood", 1, 10, 5)
    stress = st.slider("Stress", 1, 10, 5)

with col2:
    energy = st.slider("Energy", 1, 10, 5)
    sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 7.0)

text = st.text_area(
    "Journal Entry",
    placeholder="How are you feeling today?"
)

st.divider()

st.subheader("Behavioral Signals")

c1, c2, c3 = st.columns(3)

with c1:
    exercised = st.checkbox("🏃 Exercised")
    met_friends = st.checkbox("🫂 Met Friends")

with c2:
    listened_music = st.checkbox("🎵 Listened to Music")
    worked_late = st.checkbox("💻 Worked Late")

with c3:
    meditated = st.checkbox("🧘 Meditated")
    spent_time_outside = st.checkbox("🌿 Spent Time Outside")
    
# SUBMIT BUTTON
if st.button("✨ Analyze Entry"):

    payload = {
        "text": text,
        "mood": mood,
        "stress": stress,
        "energy": energy,
        "sleep_hours": sleep_hours,
        "exercised": exercised,
        "met_friends": met_friends,
        "listened_music": listened_music,
        "worked_late": worked_late,
        "meditated": meditated,
        "spent_time_outside": spent_time_outside
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/entries",
            json=payload
        )

        if response.status_code == 200:
            st.success("Entry submitted successfully!")
        else:
            st.error("Something went wrong")

    except requests.exceptions.ConnectionError:
        st.error("Backend server is not running. Start FastAPI first.")

st.divider()

st.caption("Built with FastAPI, Streamlit and PostgreSQL")