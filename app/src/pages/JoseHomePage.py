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
st.title("🛠️ GOOD MORNING, JOSE!")
st.write("*System Administrator Dashboard*")

# Create main layout: left column (system issues) and right column (quick actions + charts)
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 🚨 SYSTEM PRIORITIES")
    
    # Bug/Issue cards with interactive dropdowns
    with st.container():
        st.write("**BUG #1** - Login Authentication Failure")
        bug1_col1, bug1_col2, bug1_col3 = st.columns([2, 1, 1])
        with bug1_col1:
            st.progress(0.3)
            st.write("Under Investigation")
        with bug1_col2:
            priority1 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=0, key="bug1_priority")
        with bug1_col3:
            status1 = st.selectbox("Status:", 
                                 ["Open", "In Progress", "Testing", "Fixed"],
                                 index=1, key="bug1_status")
    
    st.write("---")
    
    with st.container():
        st.write("**BUG #2** - Database Performance Issues")
        bug2_col1, bug2_col2, bug2_col3 = st.columns([2, 1, 1])
        with bug2_col1:
            st.progress(0.8)
            st.write("Patch Ready")
        with bug2_col2:
            priority2 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=1, key="bug2_priority")
        with bug2_col3:
            status2 = st.selectbox("Status:", 
                                 ["Open", "In Progress", "Testing", "Fixed"],
                                 index=2, key="bug2_status")
    
    st.write("---")
    
    with st.container():
        st.write("**FEATURE #3** - Community Forum Enhancement")
        bug3_col1, bug3_col2, bug3_col3 = st.columns([2, 1, 1])
        with bug3_col1:
            st.progress(0.6)
            st.write("Development Phase")
        with bug3_col2:
            priority3 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=2, key="bug3_priority")
        with bug3_col3:
            status3 = st.selectbox("Status:", 
                                 ["Open", "In Progress", "Testing", "Fixed"],
                                 index=1, key="bug3_status")
    
    st.write("---")
    
    with st.container():
        st.write("**TASK #4** - User Documentation Update")
        bug4_col1, bug4_col2, bug4_col3 = st.columns([2, 1, 1])
        with bug4_col1:
            st.progress(0.4)
            st.write("Content Review")
        with bug4_col2:
            priority4 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=3, key="bug4_priority")
        with bug4_col3:
            status4 = st.selectbox("Status:", 
                                 ["Open", "In Progress", "Testing", "Fixed"],
                                 index=1, key="bug4_status")
    
    # Save changes button
    if st.button("💾 Save All Changes", type="secondary", use_container_width=True):
        st.success("✅ System priorities updated successfully!")
        # Here you could add API calls to save to database

with col2:
    st.write("### ⚡ ADMIN ACTIONS")
    
    # Action buttons in a 2x2 grid like the wireframe
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("🐛 Bug Reports", use_container_width=True):
            st.switch_page('pages/01_Bug_Reports.py')
    
    with action_col2:
        if st.button("👥 User Support", use_container_width=True):
            st.switch_page('pages/02_User_Support.py')
    
    with action_col1:
        if st.button("📊 App Analytics", use_container_width=True):
            st.switch_page('pages/03_App_Analytics.py')
    
    with action_col2:
        if st.button("💬 Community", use_container_width=True):
            st.switch_page('pages/04_Community_Forum.py')
    
    st.write("---")
    
    # System Charts Section
    st.write("### 📊 SYSTEM OVERVIEW")
    
    # Sample data for system charts
    user_growth_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Active Users': [1200, 1350, 1580, 1750, 1920, 2100],
        'New Signups': [150, 200, 230, 170, 170, 180]
    })
    
    # User growth chart
    fig_users = px.line(user_growth_data, x='Month', y=['Active Users', 'New Signups'], 
                       title="User Growth Trends",
                       color_discrete_map={'Active Users': '#1f77b4', 'New Signups': '#ff7f0e'})
    fig_users.update_layout(height=200, showlegend=True, 
                           title_font_size=12, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_users, use_container_width=True)
    
    # Bug status pie chart
    bug_data = pd.DataFrame({
        'Status': ['Fixed', 'In Progress', 'Open', 'Testing'],
        'Count': [15, 8, 5, 3]
    })
    
    fig_bugs = px.pie(bug_data, values='Count', names='Status', 
                     title="Bug Report Status",
                     color_discrete_map={'Fixed': '#2ca02c', 
                                       'In Progress': '#ff7f0e', 
                                       'Open': '#d62728',
                                       'Testing': '#9467bd'})
    fig_bugs.update_layout(height=200, title_font_size=12, 
                          margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_bugs, use_container_width=True)

# Bottom metrics section
st.write("---")
st.write("### 📈 SYSTEM METRICS")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric(
        label="Total Users", 
        value="2,100",
        delta="180 new this month"
    )

with metric_col2:
    st.metric(
        label="Active Bug Reports", 
        value="13",
        delta="-5 resolved today"
    )

with metric_col3:
    st.metric(
        label="System Uptime", 
        value="99.8%",
        delta="0.2% improvement"
    )

with metric_col4:
    st.metric(
        label="User Satisfaction", 
        value="4.6/5",
        delta="0.3 increase"
    )

# Action buttons at bottom
st.write("---")
bottom_col1, bottom_col2, bottom_col3 = st.columns(3)

with bottom_col1:
    if st.button("🚨 Create Bug Report", type="primary", use_container_width=True):
        st.switch_page('pages/05_Create_Bug_Report.py')

with bottom_col2:
    if st.button("📧 Send User Notifications", type="primary", use_container_width=True):
        st.switch_page('pages/06_User_Notifications.py')

with bottom_col3:
    if st.button("📊 Generate System Report", type="primary", use_container_width=True):
        st.switch_page('pages/07_System_Report.py')