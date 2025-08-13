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

active = requests.get('http://web-api:4000/goals/active').json()
active = [list(item.values()) for item in active]

subgoals = requests.get('http://web-api:4000/goals/subgoals').json()
subgoals = [list(item.values()) for item in subgoals]

#0 - id
#1 - title
#2 - due
#3 -desc

with left:
    a, b, c = st.columns(3)
    with a:
        st.header("Goal A", divider=True)
        st.subheader(active[0][1]) # Goal name
        st.write(f"Due :red[{active[0][2]}]") # Due date
        st.write(active[0][3]) # Description
        st.write("### Subgoals") # Subgoals
        for subgoal in subgoals:
            if subgoal[0] == active[0][0]:
                st.write(f"- {subgoal[1]}") 

    with b:
        st.header("Goal B", divider=True)
        st.subheader(active[1][1])
        st.write(f"Due :red[{active[1][2]}]")
        st.write(active[1][3])
        st.write("### Subgoals")
        for subgoal in subgoals:
            if subgoal[0] == active[1][0]:
                st.write(f"- {subgoal[1]}")        

    with c:
        st.header("Goal C", divider=True)
        st.subheader(active[2][1])
        st.write(f"Due :red[{active[2][2]}]")
        st.write(active[2][3])
        st.write("### Subgoals")
        for subgoal in subgoals:
            if subgoal[0] == active[2][0]:
                st.write(f"- {subgoal[1]}")  

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
        
