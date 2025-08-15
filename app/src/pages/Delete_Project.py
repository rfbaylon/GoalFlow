import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# SIDEBAR
SideBarLinks()

# BACK BUTTON & TITLE
col_back, col_title = st.columns([1, 4])
with col_back:
    if st.button("← Back to Dr. Alan Home"):
        st.switch_page('pages/Dr.AlanHomePage.py')

with col_title:
    st.title("🗑️ Delete Project")
    st.write("*Permanently remove a project from your goals*")

st.write("")
st.warning("⚠️ **Warning**: This action cannot be undone. The project will be permanently deleted from the database.")
st.write("")

# --- Fetch projects from API ---
try:
    response = requests.get("http://web-api:4000/goals/user/2/active_and_priority")  # <-- fixed underscore
    response.raise_for_status()
    project_data = response.json()
except Exception as e:
    st.error(f"Failed to fetch projects: {e}")
    project_data = []

# Map project title → ID
project_map = {proj["title"]: proj["id"] for proj in project_data}

# Dropdown options
project_options = ["Select a project..."] + list(project_map.keys())

# --- Main form ---
with st.form("delete_project_form"):
    st.write("### Select Project to Delete")
    selected_project = st.selectbox(
        "Choose the project you want to delete:",
        project_options,
        help="Select from your active projects"
    )
    
    st.write("")
    
    confirm_delete = False
    deletion_reason = ""
    
    if selected_project != "Select a project...":
        # Find the full project info
        proj = next((p for p in project_data if p["title"] == selected_project), None)
        
        if proj:
            st.write("### Project Details")
            with st.container():
                detail_col1, detail_col2 = st.columns(2)
                
            with detail_col1:
                    st.write("**Project Name:**", proj["title"])
                    st.write("**Current Status:**", "In Progress" if not proj.get("completed") else "Completed")
                
            with detail_col2:
                    created_at = proj.get("createdAt", "Unknown date")
                    st.write("**Created Date:**", created_at)
                    st.write("**Progress:**")
                    st.progress(0.6)  # Placeholder — replace with real progress if available
                    st.write("60% Complete")
            
            confirm_delete = st.checkbox(
                f"I understand that '{selected_project}' will be permanently deleted",
                help="Check this box to confirm you want to delete this project",
                key='confirm_delete' 
            )
            
            deletion_reason = st.text_area(
                "Reason for deletion (optional):",
                placeholder="Project cancelled, Duplicate entry, No longer relevant...",
                help="This helps us improve the app",
                key='deletion_reason'
            )

    st.write("")
    col1, _, col3 = st.columns([1, 1, 1])
    
    cancel_button = col1.form_submit_button("Cancel", use_container_width=True)
    delete_button = col3.form_submit_button(
        "🗑️ Delete Project", 
        type="primary",
        use_container_width=True,
        disabled=not confirm_delete or selected_project == "Select a project..."
    )

# --- Handle actions ---
if cancel_button:
    st.info("Operation cancelled. Returning to dashboard...")
    st.switch_page('pages/Dr.AlanHomePage.py')

if delete_button and confirm_delete and selected_project != "Select a project...":
    project_id = project_map[selected_project]
    try:
        delete_resp = requests.delete(f"http://web-api:4000/goals/{project_id}/delete")
        if delete_resp.status_code == 200:
            st.success(f"✅ Project '{selected_project}' has been successfully deleted!")
            st.balloons()
            if deletion_reason:
                logger.info(f"Project deleted: {selected_project}. Reason: {deletion_reason}")
            st.info("Redirecting to dashboard in 3 seconds...")
        else:
            st.error(f"Failed to delete project: {delete_resp.text}")
    except Exception as e:
        st.error(f"Error deleting project: {e}")

# --- Extra info ---
st.write("")
st.write("---")

with st.expander("ℹ️ What happens when I delete a project?"):
    st.write("""
    **When you delete a project:**
    - The project is permanently removed from your active goals
    - All associated tasks and subtasks are also deleted
    - Progress data and history are permanently lost
    - The project cannot be recovered after deletion
    
    **Alternatives to deletion:**
    - Mark the project as 'Completed' instead
    - Archive the project for future reference
    - Put the project 'On Hold' temporarily
    """)
