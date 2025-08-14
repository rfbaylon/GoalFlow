import streamlit as st
import requests

from modules.nav import SideBarLinks
SideBarLinks(show_home=True)

c1, c2 = st.columns([4, 1])
with c1: 
    st.title("Add New Project")
with c2:
    if st.button("Homepage", help="Return Home", type="primary", use_container_width=True):
        st.switch_page('Home.py')


# Form inputs
userID = st.text_input(f"User ID :red[*]")
title = st.text_input("Title :red[*]")
schedule = st.text_input("Deadline (YYYY-MM-DD) :red[*]")
tagID = st.text_input("Tag ID")
notes = st.text_area("Notes")
status = st.selectbox("Status", ['ON ICE', 'PLANNED', 'ACTIVE', 'ARCHIVED'])
priority = st.slider("Priority", 1, 4, 4)


if st.button("Submit"):
    project_data = {
        "userID": userID,
        "tagID": tagID,
        "title": title,
        "notes": notes,
        "status": status,
        "priority": priority,
        "schedule": schedule
    }

    try:
        # Replace this URL with your actual backend API URL
        response = requests.post("http://web-api:4000/goals/create", json=project_data)

        if response.status_code == 200:
            st.success("Project added successfully!")
        else:
            st.error(f"Failed to add project: {response.text}")
    except Exception as e:
        st.error(f"Error: {e}")
