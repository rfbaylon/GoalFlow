import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from modules.nav import SideBarLinks

st.set_page_config(layout='wide', page_title="🎨 Avery — Home")

# Header
st.title("🎨 GOOD MORNING, AVERY!")
st.write("*Freelance Designer Dashboard*")

# Sample Data
today = date.today()

projects_df = pd.DataFrame([
    {"title": "Portfolio Revamp", "priority": "High", "category": "Portfolio", "deadline": date(2025, 9, 5), "phase": 2, "phases_total": 4, "progress": 0.45},
    {"title": "Client Brand Kit", "priority": "High", "category": "Client Work", "deadline": date(2025, 8, 28), "phase": 1, "phases_total": 3, "progress": 0.30},
    {"title": "Illustration Series", "priority": "Medium", "category": "Hobbies", "deadline": date(2025, 10, 10), "phase": 3, "phases_total": 5, "progress": 0.60},
    {"title": "UX Case Study", "priority": "Low", "category": "Portfolio", "deadline": date(2025, 9, 25), "phase": 1, "phases_total": 2, "progress": 0.20},
])

def d_day(d):
    return (d - today).days

projects_df["d_day"] = projects_df["deadline"].apply(d_day)

daily_logs = {
    "Hobbies": [
        {"task": "Sketch 10 min", "done": True},
        {"task": "Read 20 min", "done": False},
    ],
    "Personal": [
        {"task": "Stretching 5 min", "done": True},
    ],
    "Work": [
        {"task": "Send invoice to ACME", "done": False},
        {"task": "Review wireframes", "done": True},
    ],
    "Daily": [
        {"task": "Inbox zero", "done": False},
    ],
}

completion_by_cat = pd.DataFrame([
    {"Category": "Client Work", "Completed": 6},
    {"Category": "Portfolio",   "Completed": 3},
    {"Category": "Hobbies",     "Completed": 4},
])

habit_trend = pd.DataFrame({
    "Date": pd.date_range(end=pd.Timestamp.today().normalize(), periods=14),
    "Done": [1,0,1,1,1,0,1,1,1,0,1,1,1,1],
})

# Create main layout: left column (goals) and right column (daily actions + charts)
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 🗂️ MAIN PROJECTS")
    for _, row in projects_df.sort_values(by=["priority", "d_day"]).iterrows():
        with st.container():
            left, right = st.columns([3, 1])
            with left:
                st.write(f"**{row['title']}**  — *{row['priority']}*")
                st.write(f"Category: {row['category']}  |  Phase: {row['phase']} / {row['phases_total']}")
                st.write(f"D-{row['d_day']}  (Due: {row['deadline'].strftime('%b %d, %Y')})")
                st.progress(row["progress"])
            with right:
                st.write("✏️ Edit")
                st.write("🗂️ Details")
        st.write("---")

with col2:
    st.write("### ⚡ QUICK ACTIONS")
    a1, a2 = st.columns(2)
    with a1:
        if st.button("📁 Projects", use_container_width=True):
            st.switch_page("pages/01_Projects.py")
    with a2:
        if st.button("✅ Habits / Logs", use_container_width=True):
            st.switch_page("pages/02_Habits.py")
    a3, a4 = st.columns(2)
    with a3:
        if st.button("📊 Analytics", use_container_width=True):
            st.switch_page("pages/03_Analytics.py")
    with a4:
        if st.button("🗄️ Archive", use_container_width=True):
            st.switch_page("pages/04_Archive.py")

    st.write("---")
    st.write("### ✍️ DAILY LOGS")

    for cat, items in daily_logs.items():
        with st.expander(f"{cat}"):
            for i, item in enumerate(items, start=1):
                st.checkbox(f"{item['task']}", value=item["done"], key=f"{cat}_{i}")

    st.write("---")
    st.write("### 📈 PROGRESS REPORT")

    fig_cat = px.pie(
        completion_by_cat, values="Completed", names="Category",
        title="Completed by Category"
    )
    fig_cat.update_layout(height=220, title_font_size=12, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_cat, use_container_width=True)

    fig_trend = px.line(habit_trend, x="Date", y="Done", markers=True, title="Habit Consistency (Last 14 days)")
    fig_trend.update_yaxes(tickmode="array", tickvals=[0,1], ticktext=["Miss","Done"])
    fig_trend.update_layout(height=220, title_font_size=12, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_trend, use_container_width=True)

# =========================
st.write("---")
st.write("### 🎯 KEY METRICS")
m1, m2, m3, m4 = st.columns(4)

streak_days = int(habit_trend["Done"].tail(7).sum())
tasks_today = sum(item["done"] for cat in daily_logs.values() for item in cat)
active_projects = (projects_df["progress"] < 1.0).sum()
next_deadline = projects_df.sort_values("d_day").iloc[0]["deadline"].strftime("%b %d")

with m1:
    st.metric("Habit Streak (7d)", f"{streak_days} days", delta="Keep it up")
with m2:
    st.metric("Tasks Checked Today", f"{tasks_today}", delta="vs. yesterday +1")
with m3:
    st.metric("Active Projects", f"{active_projects}")
with m4:
    st.metric("Next Deadline", next_deadline, delta=f"D-{projects_df['d_day'].min()}")

# Action buttons at bottom
st.write("---")
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("➕ Add New Project", type="primary", use_container_width=True):
        st.switch_page("pages/05_Add_Project.py")
with b2:
    if st.button("📝 Add Daily Log", type="primary", use_container_width=True):
        st.switch_page("pages/06_Add_Log.py")
with b3:
    if st.button("📤 Export Weekly Report", type="primary", use_container_width=True):
        st.switch_page("pages/07_Export_Report.py")