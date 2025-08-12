import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
#SideBarLinks()

# Header
st.title("📈 GOOD MORNING, JACK!")
st.write("*Financial Analyst Dashboard*")

# Create main layout: left column (goals) and right column (daily actions + charts)
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 🏢 COMPANY GOALS")
    
    # Goal cards that look like the wireframe
    with st.container():
        goal1_col1, goal1_col2 = st.columns([3, 1])
        with goal1_col1:
            st.write("**GOAL #1** 🎯 *High Priority*")
            st.write("Increase Meta Revenue by 5%")
            st.write("Phase: Q4 Analysis")
            st.progress(0.7)
        with goal1_col2:
            st.write("📊")
            st.write("⚙️")
    
    st.write("---")
    
    with st.container():
        goal2_col1, goal2_col2 = st.columns([3, 1])
        with goal2_col1:
            st.write("**GOAL #2** 📊 *High Priority*")
            st.write("Optimize Team Productivity")
            st.write("Phase: Employee Analysis")
            st.progress(0.4)
        with goal2_col2:
            st.write("📊")
            st.write("⚙️")
    
    st.write("---")
    
    with st.container():
        goal3_col1, goal3_col2 = st.columns([3, 1])
        with goal3_col1:
            st.write("**GOAL #3** 💰 *Medium Priority*")
            st.write("Reduce Operational Costs")
            st.write("Phase: Budget Review")
            st.progress(0.6)
        with goal3_col2:
            st.write("📊")
            st.write("⚙️")
    
    st.write("---")
    
    with st.container():
        goal4_col1, goal4_col2 = st.columns([3, 1])
        with goal4_col1:
            st.write("**GOAL #4** 🎯 *Low Priority*")
            st.write("Implement New KPI Dashboard")
            st.write("Phase: Requirements Gathering")
            st.progress(0.2)
        with goal4_col2:
            st.write("📊")
            st.write("⚙️")

with col2:
    st.write("### ⚡ QUICK ACTIONS")
    
    # Action buttons in a 2x2 grid like the wireframe
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("📈 Financial", use_container_width=True):
            st.switch_page('pages/01_Financial_Goals.py')
    
    with action_col2:
        if st.button("👥 Team Goals", use_container_width=True):
            st.switch_page('pages/02_Team_Goals.py')
    
    with action_col1:
        if st.button("📊 Analytics", use_container_width=True):
            st.switch_page('pages/03_Analytics.py')
    
    with action_col2:
        if st.button("⏰ Deadlines", use_container_width=True):
            st.switch_page('pages/04_Deadlines.py')
    
    st.write("---")
    
    # Financial Charts Section
    st.write("### 📊 FINANCIAL OVERVIEW")
    
    # Sample data for financial charts
    revenue_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Revenue': [85, 88, 92, 89, 95, 98],
        'Target': [90, 90, 90, 90, 90, 90]
    })
    
    # Revenue trend chart
    fig_revenue = px.line(revenue_data, x='Month', y=['Revenue', 'Target'], 
                         title="Revenue vs Target (Millions $)",
                         color_discrete_map={'Revenue': '#1f77b4', 'Target': '#ff7f0e'})
    fig_revenue.update_layout(height=200, showlegend=True, 
                             title_font_size=12, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Goal completion pie chart
    completion_data = pd.DataFrame({
        'Status': ['Completed', 'In Progress', 'Not Started'],
        'Count': [8, 12, 3]
    })
    
    fig_pie = px.pie(completion_data, values='Count', names='Status', 
                     title="Goal Completion Status",
                     color_discrete_map={'Completed': '#2ca02c', 
                                       'In Progress': '#ff7f0e', 
                                       'Not Started': '#d62728'})
    fig_pie.update_layout(height=200, title_font_size=12, 
                         margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

# Bottom metrics section
st.write("---")
st.write("### 📈 KEY METRICS")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric(
        label="Revenue Growth", 
        value="5.2%",
        delta="0.8% vs target"
    )

with metric_col2:
    st.metric(
        label="Goals Completed", 
        value="8/23",
        delta="2 this week"
    )

with metric_col3:
    st.metric(
        label="Team Efficiency", 
        value="87%",
        delta="12% improvement"
    )

with metric_col4:
    st.metric(
        label="Budget Variance", 
        value="-$2.1M",
        delta="Under budget"
    )

# Action buttons at bottom
st.write("---")
bottom_col1, bottom_col2, bottom_col3 = st.columns(3)

with bottom_col1:
    if st.button("➕ Add New Company Goal", type="primary", use_container_width=True):
        st.switch_page('pages/05_Add_Goal.py')

with bottom_col2:
    if st.button("📋 Assign Tasks to Employees", type="primary", use_container_width=True):
        st.switch_page('pages/06_Assign_Tasks.py')

with bottom_col3:
    if st.button("📊 Generate Financial Report", type="primary", use_container_width=True):
        st.switch_page('pages/07_Financial_Report.py') 