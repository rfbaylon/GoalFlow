#                   ===== INITIAL IMPORTS =====                   #
# app/pages/Dr.AlanHomePage.py
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', 
    level=logging.INFO)

from modules.nav import SideBarLinks
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import re





#                   ===== UI LAYOUT =====                   #
# Left Side Bar that links abck to Home Page / About Page.
st.set_page_config(layout='wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

# Header
st.title("📚 Good Morning, Dr. Alan!")
st.write("*Project Dashboard for Math Research*")





#                   ===== MAIN LAYOUT =====                   #
# Create main layout: left column (research projects) ((((and right column (quick actions + charts)))))
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 🔬 ACTIVE RESEARCH PROJECTS")

    # SETS THE USER_ID BASED UPON SESSION STATE.
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("No user ID found. Please log in or select a user profile.")
        st.stop()
    # user_id = 2 # Incase you refresh the page and it "logs you out" or something.

    # FETCH PROJECTS (AKA: GOALS)
    try:
        projects = requests.get(f'http://web-api:4000/goals/user/{user_id}/active_and_priority').json()
    except Exception as e:
        st.error(f"Could not fetch projects: {e}")
        projects = []

        # --- Explicit mapping and display of Goals (Projects)  ---
    # Map only the attributes I want to display from the API response.
    projects = [
        [
        item.get("id"),         # 0 - goal_id
        item.get("title"),      # 1 - title
        item.get("notes"),      # 2 - notes/description
        item.get("priority"),   # 3 - priority
        item.get("completed"),  # 4 - completed
        item.get("status"),     # 5 - status
        ]
        for item in projects
    ]

    # HEADER
    project_col1, project_col2, project_col3 = st.columns([2, 1, 1])
    with project_col1: 
        st.write("**Project**")
    with project_col2: 
        st.write("**Priority**")
    with project_col3: 
        # st.markdown("**Change Priority**")
        st.markdown("**Completion &**  \n**Change Priority**")
    st.write("---")

    for project in projects:
        project_id, title, notes, priority, completed, status = project

        with st.container():
            pc1, pc2, pc3 = st.columns([2, 1, 1])


            # A. Project title + notes
            with pc1:
                st.write(f":red[**{title}**]")
                st.write(notes)


            # B. Priority with color coding
            with pc2:
                p = priority
                if p == "critical":
                    st.markdown(f":red[**🔴 Critical!**]")
                elif p == "high":
                    st.markdown(f":orange[**🟠 High**]")
                elif p == "medium":
                    st.markdown("<span style='color:#DAA520'><strong>🟡 Medium</strong></span>", unsafe_allow_html=True)
                elif p == "low":
                    st.markdown(f":green[**🟢 Low**]")
                else:
                    st.write(p)


            # C. Interactive priority dropdown + mark complete button
            with pc3:
                # 1. Map labels <--> values
                label_to_val = {
                    "🔴 Critical": "critical",
                    "🟠 High":     "high",
                    "🟡 Medium":   "medium",
                    "🟢 Low":      "low",
                }
                val_to_label = {v: k for k, v in label_to_val.items()}

                # 2. Preselect current priority
                opts = list(label_to_val.keys())
                default = val_to_label.get(priority, opts[-1])
                idx = opts.index(default)

                # 3. Render the dropdown
                new_label = st.selectbox(
                    "Priority",
                    options=opts,
                    index=idx,
                    key=f"prio_select_{project_id}",
                    label_visibility="collapsed"
                )
                new_priority = label_to_val[new_label]

                # 4. Push change when clicked
                if new_priority != priority:
                    if st.button("Update Priority", key=f"prio_btn_{project_id}"):
                        try:
                            r = requests.put(f"http://web-api:4000/goals/{project_id}/priority", 
                                        json={"priority": new_priority},
                                        headers={"Content-Type": "application/json"}, timeout=5)
                            if r.status_code == 200:
                                st.success("Priority updated!")
                                st.rerun()
                            else:
                                st.error(f"Failed ({r.status_code})")
                        except Exception as e:
                            st.error(f"Error updating priority of project: {e}")

                # 5. And still allow marking complete
                st.write("")  # spacer

                if int(completed or 0) == 0:
                    if st.button("Mark Complete", key=f"complete_{project_id}"):
                        try:
                            response = requests.put(
                                f'http://web-api:4000/goals/{project_id}/complete',
                                timeout=5
                            )
                            if response.status_code == 200:
                                st.success("Project marked as completed!")
                                st.rerun()
                            else:
                                st.error(f"Error: {response.status_code}")
                        except Exception as e:
                            st.error(f"Error updating project: {str(e)}")
                else:
                    st.write("✅ Completed")


        st.write("---")

    
    
# Action buttons at bottom
st.write("---")
bottom_col1, bottom_col2, bottom_col3 = st.columns(3)

with bottom_col1:
    if st.button("🚨 Create New Project", type="primary", use_container_width=True):
        st.switch_page('pages/Add_New_Project.py')

with bottom_col2:
    if st.button("🗑 Delete Project", type="primary", use_container_width=True):
        st.switch_page('pages/Delete_Project.py')

with bottom_col3:
    if st.button("🏠 Return To Dashboard", type="primary", use_container_width=True):
        st.switch_page('Home.py')