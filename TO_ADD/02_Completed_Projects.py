import streamlit as st
import requests

st.title("Completed Projects")

try:
    response = requests.get("http://localhost:4000/projects/completedprojects")

    if response.status_code == 200:
        projects = response.json()

        if projects:
            for project in projects:
                st.subheader(project.get('title', 'Untitled Project'))
                st.write(f"Notes: {project.get('notes', 'No notes')}")
                st.write(f"Priority: {project.get('priority', 'N/A')}")
                st.write(f"Completed At: {project.get('completedAt', 'N/A')}")
                st.write("---")
        else:
            st.info("No completed projects found.")

    elif response.status_code == 404:
        st.info("No completed projects found.")

    else:
        st.error(f"Error fetching completed projects: {response.status_code}")

except Exception as e:
    st.error(f"Failed to fetch projects: {e}")
