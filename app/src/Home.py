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

    # <<< Added: mock user ID mapping >>>
    MOCK_USER_IDS = {
        "avery": 1,
        "dr_alan": 2,
        "jose": 3,
        "jack": 4
}
    
    # Profile buttons with emojis and descriptions
    if st.button('🎨 Avery - Freelance Designer', 
                 type='primary', 
                 use_container_width=True,
                 help="Manage creative projects and client work"):
        
        # Set mock user ID for Avery
        st.session_state['authenticated'] = True
        st.session_state['user_id'] = MOCK_USER_IDS["avery"]

        st.switch_page('pages/AveryHomePage.py')
    
    st.write("")
    


    if st.button('📚 Dr. Alan - Math Professor', 
                 type='primary', 
                 use_container_width=True,
                 help="Research projects and academic tasks"):
        
        # Set mock user ID for Dr. Alan
        st.session_state['authenticated'] = True
        st.session_state['user_id'] = MOCK_USER_IDS["dr_alan"]

        st.switch_page('pages/Dr.AlanHomePage.py')
    
    st.write("")
    


    if st.button('🛠️ Jose - System Admin', 
                 type='primary', 
                 use_container_width=True,
                 help="Manage app development and user support"):
        
        # Set mock user ID for Jose
        st.session_state['authenticated'] = True
        st.session_state['user_id'] = MOCK_USER_IDS["jose"]

        st.switch_page('pages/JoseHomePage.py')
    
    st.write("")
    


    if st.button('💼 Jack - Financial Analyst', 
                 type='primary', 
                 use_container_width=True,
                 help="Company goals and financial metrics"):
        
        # Set mock user ID for Jack
        st.session_state['authenticated'] = True
        st.session_state['user_id'] = MOCK_USER_IDS["jack"]

        st.switch_page('pages/JackHomePage.py')
    
    st.write("---")
    
  