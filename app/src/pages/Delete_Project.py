import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# SIDEBAR
SideBarLinks()

# BACK 
col_back, col_title = st.columns([1, 4])
with col_back:
    if st.button("← Back to Dashboard"):
        st.switch_page('pages/Home.py')

with col_title:
    st.title("🗑️ Delete Project")
    st.write("*Permanently remove a project from your goals*")

st.write("")

# Warning message
st.warning("⚠️ **Warning**: This action cannot be undone. The project will be permanently deleted from the database.")

st.write("")

# Main form
with st.form("delete_project_form"):
    st.write("### Select Project to Delete")
    
    # SAMPLE PROJ DROPDOWN (FROM DB)
    project_options = [
        "Select a project...",
        "Increase Revenue by 5%", 
        "Complete Research Paper",
        "App Feature Development",
        "Statistical Analysis Study",
        "Community Forum Enhancement",
        "User Documentation Update"
    ]
    
    selected_project = st.selectbox(
        "Choose the project you want to delete:",
        project_options,
        help="Select from your active projects"
    )
    
    st.write("")
    
    # PROJ DETAILS (woulda be populated)
    if selected_project != "Select a project...":
        st.write("### Project Details")
        
        # Show project info in a nice container
        with st.container():
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                st.write("**Project Name:**")
                st.write(selected_project)
                st.write("")
                st.write("**Current Status:**")
                st.write("In Progress")
                
            with detail_col2:
                st.write("**Created Date:**")
                st.write("January 15, 2025")
                st.write("")
                st.write("**Progress:**")
                st.progress(0.6)
                st.write("60% Complete")
        
        st.write("")
        
        # CHECKBOX THING
        confirm_delete = st.checkbox(
            f"I understand that '{selected_project}' will be permanently deleted",
            help="Check this box to confirm you want to delete this project"
        )
        
        st.write("")
        
        # DELETION REASON
        deletion_reason = st.text_area(
            "Reason for deletion (optional):",
            placeholder=" Project cancelled, Duplicate entry, No longer relevant...",
            help="This helps us improve the app"
        )
    
    else:
        confirm_delete = False
        deletion_reason = ""
    
    st.write("")
    
    # FORM SUBMISSION DETAILS
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        cancel_button = st.form_submit_button(
            "Cancel", 
            use_container_width=True
        )
    
    with col2:
        # SPACING - MT
        pass
    
    with col3:
        delete_button = st.form_submit_button(
            "🗑️ Delete Project", 
            type="primary",
            use_container_width=True,
            disabled=not confirm_delete or selected_project == "Select a project..."
        )

# FOR HANDLING THE FORM SUBMISSION THING
if cancel_button:
    st.info("Operation cancelled. Returning to dashboard...")
    st.switch_page('pages/Home.py')

if delete_button and confirm_delete and selected_project != "Select a project...":
    # In a real app, you'd make an API call here to delete from database
    # Example API call:
    # try:
    #     response = requests.delete(f"http://api:4000/goals/{project_id}")
    #     if response.status_code == 200:
    #         st.success("Project deleted successfully!")
    #     else:
    #         st.error("Failed to delete project. Please try again.")
    # except Exception as e:
    #     st.error(f"Error: {str(e)}")
    
    # For now, just show success message
    st.success(f"✅ Project '{selected_project}' has been successfully deleted!")
    st.balloons()
    
    # Log the deletion reason if provided
    if deletion_reason:
        logger.info(f"Project deleted: {selected_project}. Reason: {deletion_reason}")
    
    st.write("")
    st.info("Redirecting to dashboard in 3 seconds...")
    
    # Auto-redirect after success 
    # st.rerun()

# EXTRA INFO SEC
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

st.write("")
st.write("Need help? Contact support or return to your dashboard.")