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

# Center the user selection
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
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
        
