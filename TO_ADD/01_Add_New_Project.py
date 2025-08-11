import streamlit as st
import requests

from modules.nav import SideBarLinks
SideBarLinks(show_home=True)

st.title("Add New Project")

# Form inputs
userID = st.text_input("User ID")
tagID = st.text_input("Tag ID")
title = st.text_input("Title")
notes = st.text_area("Notes")
status = st.selectbox("Status", ["onIce", "inProgress", "completed"])
priority = st.slider("Priority", 1, 4, 4)
schedule = st.text_input("Deadline")

if st.button("Submit"):
    project_data = {
        "userID": userID,
        "tagID": tagID,
        "title": title,
        "notes": notes,
        "status": status,
        "priority": priority,
        "completedAt": completedAt or None,
        "schedule": schedule
    }

    try:
        # Replace this URL with your actual backend API URL
        response = requests.post("http://localhost:4000/projects", json=project_data)

        if response.status_code == 200:
            st.success("Project added successfully!")
        else:
            st.error(f"Failed to add project: {response.text}")
    except Exception as e:
        st.error(f"Error: {e}")
