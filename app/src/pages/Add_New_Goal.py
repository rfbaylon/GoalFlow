import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks(show_home=True)
st.title("Add New Goal")

userId = st.text_input("User ID")
title = st.text_input("Title")
notes = st.text_area("Notes")
status = st.selectbox("Status", ["ON ICE", "PLANNED", "ACTIVE", "ARCHIVED"])
priority = st.selectbox("Priority", ["critical", "high", "medium", "low"])
schedule = st.date_input("Deadline")  # returns a datetime.date object

if st.button("Submit"):
    goal_data = {
        "userId": userId,
        "title": title,
        "notes": notes,
        "status": status,
        "priority": priority,
        "schedule": schedule.isoformat()  # convert date to string
    }

    try:
        response = requests.post("http://localhost:4000/goals/creategoals", json=goal_data)
        if response.status_code == 200:
            st.success("Goal added successfully!")
        else:
            st.error(f"Failed to add goal: {response.text}")
    except Exception as e:
        st.error(f"Error: {e}")
