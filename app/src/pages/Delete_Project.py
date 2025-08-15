import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

col_back, col_title = st.columns([1, 4])
with col_back:
    if st.button("Back to Dashboard"):
        st.switch_page('Home.py')
        
with col_title:
    st.title("Delete Project")
    st.write("*Permanently remove a project from goals*")

st.write("")
st.warning("**Warning:** This action cannot be undone. All data related to this project will be permanently deleted.")

st.write("")

with st.form("delete_project_form"):
    st.write("###Select Project to Delete")

    project_options = [
        
    ]