import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    This is a demo app to demonstrate the data and software of GoalFlow in the 2025 SU2 Intro to Databases Project.  

    The goal of this demo is to show the capabilities of the tech stack 
    being used as well as demo some of the features of the platforms. 

    Stay tuned for more information and features!
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
