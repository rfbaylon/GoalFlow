import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
from modules.nav import SideBarLinks
import streamlit as st
import requests

st.set_page_config(layout = 'wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

st.write("# Welcome to GoalFlow!")
st.write("What are we going to get done today?")


left, right = st.columns(2)

#0 - id
#1 - title
#2 - due
#3 -desc



with right:
    st.header("Right Half")
    st.write("Content for the right side")

    if st.button('Avery View', 
            type = 'primary', 
            use_container_width=False):
        st.switch_page('pages/AveryHomePage.py')

    if st.button('Alan Home', 
            type = 'primary', 
            use_container_width=False):
        st.switch_page('pages/Dr.AlanHomePage.py')

    if st.button('Developer View', 
            type = 'primary', 
            use_container_width=False):
        st.switch_page('pages/JoseHomePage.py')

    if st.button('Add New Project', 
            type = 'primary', 
            use_container_width=False):
        st.switch_page('pages/Add_New_Project.py')
        
