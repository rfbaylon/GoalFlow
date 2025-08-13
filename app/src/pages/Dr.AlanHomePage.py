import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
#SideBarLinks()

# Header
st.title("📚 GOOD MORNING, DR. ALAN!")
st.write("*Math Professor Research Dashboard*")

# Create main layout: left column (research projects) and right column (quick actions + charts)
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 🔬 ACTIVE RESEARCH PROJECTS")
    
    # Research project cards with interactive dropdowns
    with st.container():
        st.write("**PROJECT #1** - AI Statistical Models Research")
        proj1_col1, proj1_col2, proj1_col3 = st.columns([2, 1, 1])
        with proj1_col1:
            st.progress(0.7)
            st.write("Data Collection Phase")
        with proj1_col2:
            priority1 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=0, key="proj1_priority")
        with proj1_col3:
            status1 = st.selectbox("Status:", 
                                 ["ON ICE", "PLANNED", "ACTIVE", "ARCHIVED"],
                                 index=1, key="proj1_status")
    
    st.write("---")
    
    with st.container():
        st.write("**PROJECT #2** - Statistical Analysis Course Development")
        proj2_col1, proj2_col2, proj2_col3 = st.columns([2, 1, 1])
        with proj2_col1:
            st.progress(0.4)
            st.write("Curriculum Design")
        with proj2_col2:
            priority2 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=1, key="proj2_priority")
        with proj2_col3:
            status2 = st.selectbox("Status:", 
                                 ["ON ICE", "PLANNED", "ACTIVE", "ARCHIVED"],
                                 index=0, key="proj2_status")
    
    st.write("---")
    
    with st.container():
        st.write("**PROJECT #3** - Machine Learning Paper Publication")
        proj3_col1, proj3_col2, proj3_col3 = st.columns([2, 1, 1])
        with proj3_col1:
            st.progress(0.9)
            st.write("Final Review")
        with proj3_col2:
            priority3 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=2, key="proj3_priority")
        with proj3_col3:
            status3 = st.selectbox("Status:", 
                                 ["ON ICE", "PLANNED", "ACTIVE", "ARCHIVED"],
                                 index=3, key="proj3_status")
    
    st.write("---")
    
    with st.container():
        st.write("**PROJECT #4** - Student Thesis Supervision")
        proj4_col1, proj4_col2, proj4_col3 = st.columns([2, 1, 1])
        with proj4_col1:
            st.progress(0.5)
            st.write("Methodology Review")
        with proj4_col2:
            priority4 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=3, key="proj4_priority")
        with proj4_col3:
            status4 = st.selectbox("Status:", 
                                 ["ON ICE", "PLANNED", "ACTVIE", "ARCHIVED"],
                                 index=1, key="proj4_status")
    
    # Save changes button
    if st.button("💾 Save All Changes", type="secondary", use_container_width=True):
        st.success("✅ Research projects updated successfully!")
        # Here you could add API calls to save to database
    
    st.write("---")
    
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