import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
#SideBarLinks()

#st.title(f"Welcome Professor, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Add new project', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Add_New_Project.py')

if st.button('View completed projects', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Completed_Projects.py')

if st.button('View project by tags', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_Project_Tags.py')

if st.button('Manage planner and tasks', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/04_Planner_And_Tasks.py')