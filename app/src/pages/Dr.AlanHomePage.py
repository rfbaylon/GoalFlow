#                   ===== INITIAL IMPORTS =====                   #
# app/pages/Dr.AlanHomePage.py
import logging

logging.basicConfig(
    format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', 
    level=logging.INFO)
logger = logging.getLogger(__name__)

from modules.nav import SideBarLinks
import streamlit as st
import requests
import pandas as pd
import plotly.express as px





#                   ===== UI LAYOUT =====                   #
# Left Side Bar that links abck to Home Page / About Page.
st.set_page_config(layout = 'wide')
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

        # --- Explicit mapping and display of Goals (Projects)  ---
    # Map only the attributes I want to display from the API response.

    # SETS THE USER_ID BASED UPON SESSION STATE.
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("No user ID found. Please log in or select a user profile.")
        st.stop()
    user_id = 3 # Incase you refresh the page and it "logs you out" or something.

    # PROJECTS (AKA: GOALS)
    response = requests.get(f'http://web-api:4000/goals/user/{user_id}/active_and_priority', timeout=5)
    st.write("Status Code:", response.status_code)
    st.write("Raw JSON:", response.text)

    # Now try to parse, letting any JSON errors bubble up
    projects = response.json()


    # try:
    #     projects = requests.get(f'http://web-api:4000/goals/user/{user_id}/active_and_priority').json()
    # except Exception as e:
    #     st.error(f"Could not fetch projects: {e}")
    #     projects = []

    projects = [
        [
            item.get("id"),         # 0 - goal_id
            item.get("title"),      # 1 - title
            item.get("notes"),      # 2 - notes/description
            item.get("priority"),   # 3 - priority
            item.get("completed")   # 4 - completed
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
        project_id, title, notes, priority, completed = project

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
                            r = requests.put(f"http://web-api:4000/goals/{project_id}/priority", timeout=5)
                            if r.status_code == 200:
                                st.success("Priority updated!")
                                st.rerun()
                            else:
                                st.error(f"Failed ({r.status_code})")
                        except Exception as e:
                            st.error(f"Error updating priority of project: {e}")

                # 5. And still allow marking complete
                st.write("")  # spacer
                if completed == 0:
                    if st.button("Mark Complete", key=f"complete_{project_id}"):
                        try:
                            response = requests.put(f'http://web-api:4000/goals/{project_id}/complete', timeout=5)
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

    
    with col2:
    # Academic Charts Section
        st.write("### 📊 RESEARCH OVERVIEW")
    
    # Sample data for academic charts
        research_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Papers Published': [1, 0, 2, 1, 1, 3],
            'Research Hours': [45, 52, 38, 48, 55, 42]
        })
        
        # Research productivity chart
        fig_research = px.line(research_data, x='Month', y=['Papers Published', 'Research Hours'], 
                            title="Research Productivity",
                            color_discrete_map={'Papers Published': '#1f77b4', 'Research Hours': '#ff7f0e'})
        fig_research.update_layout(height=200, showlegend=True, 
                                title_font_size=12, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_research, use_container_width=True)
        
        # Project status pie chart
        project_data = pd.DataFrame({
            'Status': ['Research', 'Writing', 'Review', 'Published'],
            'Count': [5, 3, 2, 4]
        })
        
        fig_projects = px.pie(project_data, values='Count', names='Status', 
                            title="Project Status Distribution",
                            color_discrete_map={'Research': '#ff7f0e', 
                                            'Writing': '#1f77b4', 
                                            'Review': '#9467bd',
                                            'Published': '#2ca02c'})
        fig_projects.update_layout(height=200, title_font_size=12, 
                                margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_projects, use_container_width=True)

# Bottom metrics section
st.write("---")
st.write("### 📈 ACADEMIC METRICS")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric(
        label="Active Projects", 
        value="8",
        delta="2 new this semester"
    )

with metric_col2:
    st.metric(
        label="Papers Published", 
        value="3",
        delta="1 under review"
    )

with metric_col3:
    st.metric(
        label="Research Progress", 
        value="67%",
        delta="12% this month"
    )

with metric_col4:
    st.metric(
        label="Student Supervision", 
        value="5 students",
        delta="2 thesis defenses"
    )

# Next Goals Section - NEW ADDITION!
st.write("---")
st.write("### 🎯 NEXT GOALS TO PURSUE")

next_col1, next_col2, next_col3 = st.columns(3)

with next_col1:
    with st.container():
        st.write("**🔬 Deep Learning Research**")
        st.write("*Neural Networks in Statistics*")
        st.write("📅 Target: Fall 2025")
        if st.button("➕ Add to Active Projects", key="add_goal1", use_container_width=True):
            st.success("Added to active projects!")

with next_col2:
    with st.container():
        st.write("**📚 Advanced Statistics Textbook**")
        st.write("*Undergraduate Level*")
        st.write("📅 Target: Spring 2026")
        if st.button("➕ Add to Active Projects", key="add_goal2", use_container_width=True):
            st.success("Added to active projects!")

with next_col3:
    with st.container():
        st.write("**🌍 International Conference**")
        st.write("*Mathematics & AI Symposium*")
        st.write("📅 Target: Summer 2025")
        if st.button("➕ Add to Active Projects", key="add_goal3", use_container_width=True):
            st.success("Added to active projects!")

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
        st.switch_page('HomePage.py')