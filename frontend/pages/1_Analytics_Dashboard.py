import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from openai import OpenAI
import os
from dotenv import load_dotenv
from config import API_URL

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =========================
# CUSTOM STYLING
# =========================

st.markdown("""
<style>

.main {
    padding-top: 2rem;
}

.stMetric {
    background-color: #FFFFFF;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("📊 Behavioral Analytics Dashboard")

st.markdown("""
Explore emotional patterns, behavioral trends and burnout signals over time.
""")

st.divider()

# =========================
# FETCH DATA
# =========================

#response = requests.get("http://127.0.0.1:8000/entries")
#response = requests.get("https://human-signals.onrender.com")

response=requests.get(f"{API_URL}/entries")

entries = response.json()

df = pd.DataFrame(entries)

if df.empty:
    st.warning("No entries available yet.")
    st.stop()

# =========================
# DATA PREP
# =========================

df["created_at"] = pd.to_datetime(df["created_at"])

# =========================
# TOP METRICS
# =========================

avg_mood = round(df["mood"].mean(), 1)
avg_stress = round(df["stress"].mean(), 1)
avg_energy = round(df["energy"].mean(), 1)

c1, c2, c3 = st.columns(3)

c1.metric("Average Mood", avg_mood)
c2.metric("Average Stress", avg_stress)
c3.metric("Average Energy", avg_energy)

st.divider()

# =========================
# AI SUMMARY DATA
# =========================

summary_data = f"""
Average mood: {avg_mood}
Average stress: {avg_stress}
Average energy: {avg_energy}

Exercise frequency: {round(df['exercised'].mean(), 2)}
Social interaction frequency: {round(df['met_friends'].mean(), 2)}
Worked late frequency: {round(df['worked_late'].mean(), 2)}

Average sleep: {round(df['sleep_hours'].mean(), 1)}

Recent journal entries:
{df['text'].tail(5).to_list()}
"""

# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Trends",
    "🧠 Insights",
    "🔥 Burnout Signals",
    "🤖 AI Reflection"
])

# =========================
# TRENDS TAB
# =========================

with tab1:

    st.subheader("Mood & Stress Trends")

    fig = px.line(
        df,
        x="created_at",
        y=["mood", "stress", "energy"],
        markers=True,
        title="Emotional Trends Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Sleep vs Mood Correlation")

    fig2 = px.scatter(
        df,
        x="sleep_hours",
        y="mood",
        size="stress",
        color="energy",
        hover_data=["text"],
        title="Sleep Impact on Mood"
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================
# INSIGHTS TAB
# =========================

with tab2:

    st.subheader("Behavioral Insights")

    # Exercise impact
    exercise_mood = df[df["exercised"] == True]["mood"].mean()
    no_exercise_mood = df[df["exercised"] == False]["mood"].mean()

    if pd.notna(exercise_mood) and pd.notna(no_exercise_mood):

        diff = round(exercise_mood - no_exercise_mood, 1)

        st.info(
            f"🏃 Mood increases by {diff} points on exercise days."
        )

    # Social interaction impact
    social_stress = df[df["met_friends"] == True]["stress"].mean()
    alone_stress = df[df["met_friends"] == False]["stress"].mean()

    if pd.notna(social_stress) and pd.notna(alone_stress):

        social_diff = round(alone_stress - social_stress, 1)

        st.info(
            f"🫂 Social interaction is associated with {social_diff} lower stress points."
        )

    # Music impact
    music_mood = df[df["listened_music"] == True]["mood"].mean()
    no_music_mood = df[df["listened_music"] == False]["mood"].mean()

    if pd.notna(music_mood) and pd.notna(no_music_mood):

        music_diff = round(music_mood - no_music_mood, 1)

        st.info(
            f"🎵 Listening to music correlates with a {music_diff} point increase in mood."
        )

    # Worked late impact
    worked_late_stress = df[df["worked_late"] == True]["stress"].mean()
    normal_stress = df[df["worked_late"] == False]["stress"].mean()

    if pd.notna(worked_late_stress) and pd.notna(normal_stress):

        work_diff = round(worked_late_stress - normal_stress, 1)

        st.warning(
            f"💻 Working late is associated with {work_diff} higher stress points."
        )

# =========================
# BURNOUT TAB
# =========================

with tab3:

    st.subheader("Burnout Risk Analysis")

    burnout_score = (
        df["stress"].mean()
        - df["sleep_hours"].mean() / 2
        - df["energy"].mean() / 2
    )

    burnout_score = round(burnout_score, 1)

    st.metric(
        "Burnout Risk Score",
        burnout_score
    )

    st.divider()

    if burnout_score > 5:
        st.error("⚠️ High burnout risk detected.")
    elif burnout_score > 3:
        st.warning("⚠️ Moderate burnout signals detected.")
    else:
        st.success("✅ Burnout risk currently low.")

    st.divider()

    st.subheader("Potential Risk Factors")

    avg_sleep = round(df["sleep_hours"].mean(), 1)

    if avg_sleep < 6:
        st.warning("😴 Low sleep consistency detected.")

    avg_stress_level = round(df["stress"].mean(), 1)

    if avg_stress_level > 7:
        st.warning("📈 Elevated stress levels observed.")

    worked_late_ratio = df["worked_late"].mean()

    if worked_late_ratio > 0.5:
        st.warning("💻 Frequent late work sessions detected.")

# =========================
# AI REFLECTION TAB
# =========================

with tab4:

    st.subheader("AI Behavioral Reflection")

    try:

        ai_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a behavioral analytics assistant.

                    Analyze emotional and behavioral patterns.
                    Be insightful, concise and supportive.
                    """
                },
                {
                    "role": "user",
                    "content": summary_data
                }
            ]
        )

        insight = ai_response.choices[0].message.content

        st.info(insight)

    except Exception:

        st.warning("AI service unavailable — using local behavioral analysis.")

        insights = []

        if avg_stress > 7:
            insights.append(
                "📈 Elevated stress levels detected across recent entries."
            )

        if df["sleep_hours"].mean() < 6:
            insights.append(
                "😴 Reduced sleep consistency may be impacting emotional stability."
            )

        if df["exercised"].mean() > 0.5:
            insights.append(
                "🏃 Exercise appears positively associated with mood regulation."
            )

        if df["worked_late"].mean() > 0.5:
            insights.append(
                "💻 Frequent late work sessions correlate with increased stress."
            )

        if len(insights) == 0:
            insights.append(
                "✅ Emotional and behavioral patterns currently appear relatively stable."
            )

        for insight in insights:
            st.info(insight)

st.divider()

st.caption("HumanSignals • AI-Powered Behavioral Analytics")