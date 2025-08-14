import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
from modules.nav import SideBarLinks
import streamlit as st
import requests

st.set_page_config(layout='wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

# Header with better styling
st.markdown("# 🎯 Welcome to GoalFlow!")
st.markdown("### *What are we going to get done today?*")
st.write("")

# Main layout
left, right = st.columns([2, 1])

with left:
    st.markdown("## 📋 Your Goal Dashboard")
    st.write("")
    
    # Sample goals display - simple and clean
    with st.container():
        st.markdown("**🎯 Active Goals**")
        
        # Goal 1
        goal1_col1, goal1_col2 = st.columns([3, 1])
        with goal1_col1:
            st.write("📊 **Increase Revenue by 5%**")
            st.write("*Due: March 15, 2025*")
            st.progress(0.7)
        with goal1_col2:
            st.write("70% Complete")
        
        st.write("---")
        
        # Goal 2
        goal2_col1, goal2_col2 = st.columns([3, 1])
        with goal2_col1:
            st.write("🎓 **Complete Research Paper**")
            st.write("*Due: April 20, 2025*")
            st.progress(0.4)
        with goal2_col2:
            st.write("40% Complete")
        
        st.write("---")
        
        # Goal 3
        goal3_col1, goal3_col2 = st.columns([3, 1])
        with goal3_col1:
            st.write("💻 **App Feature Development**")
            st.write("*Due: May 10, 2025*")
            st.progress(0.8)
        with goal3_col2:
            st.write("80% Complete")
    
    st.write("")
    
    # Today's tasks
    st.markdown("**✅ Today's Tasks**")
    col_task1, col_task2 = st.columns([1, 4])
    
    with col_task1:
        task1 = st.checkbox("", key="task1")
        task2 = st.checkbox("", key="task2")
        task3 = st.checkbox("", key="task3")
    
    with col_task2:
        st.write("Review quarterly financial reports")
        st.write("Meet with research advisor")
        st.write("Fix critical bug in authentication")

with right:
    st.markdown("## 👥 User Profiles")
    st.write("*Choose your role to get started*")
    st.write("")
    
    # Profile buttons with emojis and descriptions
    if st.button('🎨 Avery - Freelance Designer', 
                 type='primary', 
                 use_container_width=True,
                 help="Manage creative projects and client work"):
        st.switch_page('pages/AveryHomePage.py')
    
    st.write("")
    
    if st.button('📚 Dr. Alan - Math Professor', 
                 type='primary', 
                 use_container_width=True,
                 help="Research projects and academic tasks"):
        st.switch_page('pages/Dr.AlanHomePage.py')
    
    st.write("")
    
    if st.button('🛠️ Jose - System Admin', 
                 type='primary', 
                 use_container_width=True,
                 help="Manage app development and user support"):
        st.switch_page('pages/JoseHomePage.py')
    
    st.write("")
    
    if st.button('💼 Jack - Financial Analyst', 
                 type='primary', 
                 use_container_width=True,
                 help="Company goals and financial metrics"):
        st.switch_page('pages/JackHomePage.py')
    
    st.write("---")
    
    # Quick actions
    st.markdown("**⚡ Quick Actions**")
    
    if st.button('➕ Add New Goal', 
                 type='secondary', 
                 use_container_width=True):
        st.switch_page('pages/Add_New_Project.py')
    
    if st.button('📊 View Analytics', 
                 type='secondary', 
                 use_container_width=True):
        st.info("Analytics page coming soon!")
    
    # Stats summary
    st.write("---")
    st.markdown("**📈 Quick Stats**")
    
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric("Active Goals", "3", "1 new")
    with metric_col2:
        st.metric("Completed", "12", "2 this week")

# Bottom section
st.write("")
st.write("---")
st.markdown("### 💡 **Getting Started**")
st.write("Choose your profile above to access personalized goals and tasks, or add a new goal to get started!")

# Optional: Recent activity
with st.expander("📝 Recent Activity"):
    st.write("• Goal 'Increase Revenue by 5%' updated to 70% complete")
    st.write("• New task 'Review financial reports' added")
    st.write("• Research paper milestone reached")
    st.write("• Bug fix deployed successfully")
        
