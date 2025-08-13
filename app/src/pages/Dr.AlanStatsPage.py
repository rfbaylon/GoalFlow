import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
#SideBarLinks()

# Header with back button
col_back, col_title = st.columns([1, 4])
with col_back:
    if st.button("← Back to Dashboard"):
        st.switch_page('pages/00_Dr_Alan_Home_Page.py')

with col_title:
    st.title("📊 Statistics Research Hub")
    st.write("*All your statistics projects and analysis tools*")

# Main layout: Statistics projects on left, tools and data on right
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 🔬 ACTIVE STATISTICS PROJECTS")
    
    # Statistics project cards with interactive controls
    with st.container():
        st.write("**📈 REGRESSION ANALYSIS STUDY**")
        stat1_col1, stat1_col2, stat1_col3 = st.columns([2, 1, 1])
        with stat1_col1:
            st.progress(0.8)
            st.write("📋 Data Collection: 80% Complete")
            st.write("📅 Due: March 15, 2025")
            st.write("🎯 Goal: Publish in Journal of Statistics")
        with stat1_col2:
            priority1 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=0, key="stat1_priority")
        with stat1_col3:
            status1 = st.selectbox("Status:", 
                                 ["Planning", "Data Collection", "Analysis", "Writing", "Review"],
                                 index=2, key="stat1_status")
    
    st.write("---")
    
    with st.container():
        st.write("**📊 PROBABILITY THEORY RESEARCH**")
        stat2_col1, stat2_col2, stat2_col3 = st.columns([2, 1, 1])
        with stat2_col1:
            st.progress(0.4)
            st.write("📋 Literature Review: 40% Complete")
            st.write("📅 Due: May 20, 2025")
            st.write("🎯 Goal: Conference Presentation")
        with stat2_col2:
            priority2 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=1, key="stat2_priority")
        with stat2_col3:
            status2 = st.selectbox("Status:", 
                                 ["Planning", "Data Collection", "Analysis", "Writing", "Review"],
                                 index=0, key="stat2_status")
    
    st.write("---")
    
    with st.container():
        st.write("**📉 TIME SERIES ANALYSIS PROJECT**")
        stat3_col1, stat3_col2, stat3_col3 = st.columns([2, 1, 1])
        with stat3_col1:
            st.progress(0.6)
            st.write("📋 Model Development: 60% Complete")
            st.write("📅 Due: April 10, 2025")
            st.write("🎯 Goal: Department Presentation")
        with stat3_col2:
            priority3 = st.selectbox("Priority:", 
                                   ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
                                   index=2, key="stat3_priority")
        with stat3_col3:
            status3 = st.selectbox("Status:", 
                                 ["Planning", "Data Collection", "Analysis", "Writing", "Review"],
                                 index=2, key="stat3_status")
    
    # Daily Statistics Tasks
    st.write("### ✅ TODAY'S STATISTICS TASKS")
    
    task_col1, task_col2 = st.columns([3, 1])
    
    with task_col1:
        task1_done = st.checkbox("📊 Review regression model assumptions", key="task1")
        task2_done = st.checkbox("📈 Analyze dataset for outliers", key="task2")
        task3_done = st.checkbox("📝 Write methodology section", key="task3")
        task4_done = st.checkbox("📚 Read 3 research papers on time series", key="task4")
        task5_done = st.checkbox("💻 Run statistical tests on new data", key="task5")
    
    with task_col2:
        st.write("**Deadlines:**")
        st.write("Today")
        st.write("Tomorrow")
        st.write("This Week")
        st.write("Next Week")
        st.write("Today")

with col2:
    st.write("### 🛠️ STATISTICS TOOLS")
    
    # Quick access tools
    if st.button("📊 Data Analysis Workspace", use_container_width=True):
        st.switch_page('pages/data_analysis.py')
    
    if st.button("📈 Statistical Visualizations", use_container_width=True):
        st.switch_page('pages/visualizations.py')
    
    if st.button("🧮 Calculator & Formulas", use_container_width=True):
        st.switch_page('pages/stat_calculator.py')
    
    if st.button("📚 Research References", use_container_width=True):
        st.switch_page('pages/references.py')
    
    st.write("---")
    
    # Quick stats visualization
    st.write("### 📊 QUICK DATA VIEW")
    
    # Sample dataset preview
    sample_data = pd.DataFrame({
        'Variable': ['X1', 'X2', 'X3', 'X4', 'X5'],
        'Mean': [12.5, 8.3, 15.7, 22.1, 9.8],
        'Std Dev': [2.1, 1.4, 3.2, 4.5, 1.8],
        'Sample Size': [100, 100, 100, 100, 100]
    })
    
    st.dataframe(sample_data, use_container_width=True)
    
    # Quick correlation plot
    correlation_data = pd.DataFrame({
        'X': [1, 2, 3, 4, 5, 6, 7, 8],
        'Y': [2.1, 3.8, 5.2, 7.1, 8.9, 10.2, 12.1, 13.8]
    })
    
    fig_corr = px.scatter(correlation_data, x='X', y='Y', 
                         title="Current Dataset Correlation",
                         trendline="ols")
    fig_corr.update_layout(height=200, title_font_size=12, 
                          margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Statistical summary
    st.write("**Quick Stats:**")
    st.write("• Correlation: r = 0.98")
    st.write("• P-value: < 0.001")
    st.write("• R²: 0.96")
    st.write("• Sample size: n = 8")

# Bottom section - Research notes and recent activity
st.write("---")

bottom_col1, bottom_col2 = st.columns(2)

with bottom_col1:
    st.write("### 📝 RESEARCH NOTES")
    
    notes = st.text_area("Quick notes and ideas:", 
                        value="• Need to check normality assumptions\n• Consider non-parametric alternatives\n• Review literature on robust statistics\n• Schedule meeting with co-author",
                        height=100)
    
    if st.button("💾 Save Notes"):
        st.success("Notes saved!")

with bottom_col2:
    st.write("### 📋 RECENT ACTIVITY")
    
    st.write("**This Week:**")
    st.write("• ✅ Completed ANOVA analysis")
    st.write("• ✅ Updated regression model")
    st.write("• 📝 Started probability paper draft")
    st.write("• 📊 Analyzed new dataset")
    st.write("• 📚 Read 5 research papers")

# Action buttons
st.write("---")
action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("➕ Add New Statistics Project", type="primary", use_container_width=True):
        st.switch_page('pages/add_statistics_project.py')

with action_col2:
    if st.button("📊 Generate Statistics Report", type="primary", use_container_width=True):
        st.switch_page('pages/statistics_report.py')

with action_col3:
    if st.button("📈 View All Statistics Data", type="primary", use_container_width=True):
        st.switch_page('pages/all_statistics_data.py')