import streamlit as st
import requests

from modules.nav import SideBarLinks
SideBarLinks(show_home=True)

st.title("Add New Post Reply")

# Form inputs
userID = st.text_input("User ID")
postID = st.text_input("Post ID")
title = st.text_input("Title")
content = st.text_area("Content")

if st.button("Submit"):
    project_data = {
        "userID": userID,
        "postID": postID,
        "title": title,
        "content": content,
    }

    try:
        # Replace this URL with your actual backend API URL
        response = requests.post("http://localhost:4000/post_reply", json=project_data)

        if response.status_code == 200:
            st.success("Project added successfully!")
        else:
            st.error(f"Failed to add project: {response.text}")
    except Exception as e:
        st.error(f"Error: {e}")
