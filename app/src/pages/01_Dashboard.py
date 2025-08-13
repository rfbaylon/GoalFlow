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

API_URL = "http://web-api:4000/goals"

def fetch_goals():
    """Fetch goals from the API with error handling"""
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API returned status code: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API server. Please ensure it's running on http://web-api:4000")
        return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. The API server may be slow to respond.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        return None

# Fetch and display goals
goals_data = fetch_goals()

if goals_data:
    st.success("Successfully connected to API!")
    
    if goals_data:
        st.write("## Your Active Goals")
        
        for goal in goals_data:
            with st.expander(f"📋 {goal.get('title', 'Untitled Goal')}"):
                st.write(f"**Schedule:** {goal.get('schedule', 'No schedule set')}")
                st.write(f"**Notes:** {goal.get('notes', 'No notes available')}")
                
                # Add action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Mark Complete", key=f"complete_{goal.get('id')}"):
                        st.success(f"Goal '{goal.get('title')}' marked as complete!")
                with col2:
                    if st.button(f"Edit", key=f"edit_{goal.get('id')}"):
                        st.info("Edit functionality would open a form here")
    else:
        st.info("No active goals found. Time to create some!")


# try:
#     response = requests.get(API_URL)
#     if response.status_code == 200:
#         st.write("Success!!!!")
        

# except requests.exceptions.RequestException as e:
#     st.error(f"Error connecting to the API: {str(e)}")
#     st.info("Please ensure the API server is running on http://web-api:4000")

# @st.cache_resource
# def init_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         port=3306,
#         user="root",
#         password="1203",
#         database="global-GoalFlow"
#     )

# # Function to run queries
# def run_query(query, params=None):
#     conn = init_connection()
#     cursor = conn.cursor()
#     cursor.execute(query, params or ())
#     result = cursor.fetchall()
#     cursor.close()
#     return result



# left, right = st.columns(2)

# active = run_query("SELECT id, title, notes, schedule FROM goals g WHERE g.status = 'ACTIVE' LIMIT 3;")
# subgoals = run_query("SELECT g.id, sg.title FROM subgoals sg JOIN goals g ON g.id = sg.goalsid;")

# # completed=run_query("SELECT g.id, COUNT(sg.status) FROM subgoals sg JOIN goals g ON g.id = sg.goalsid WHERE sg.status = 'ARCHIVED' GROUP BY g.id;")
# # uncompleted=run_query("SELECT g.id, COUNT(sg.status) FROM subgoals sg JOIN goals g ON g.id = sg.goalsid WHERE sg.status = 'ACTIVE' OR 'ON ICE' GROUP BY g.id;")




# with left:
#     a, b, c = st.columns(3)
#     with a:
#         st.header("Goal A", divider=True)
#         st.subheader(active[0][1]) # Goal name
#         st.write(f"Due :blue[{active[0][3]}]") # Due date
#         st.write(active[0][2]) # Description
#         st.write("### Subgoals") # Subgoals
#         for subgoal in subgoals:
#             if subgoal[0] == active[0][0]:
#                 st.write(f"- {subgoal[1]}") 

#     with b:
#         st.header("Goal B", divider=True)
#         st.subheader(active[1][1])
#         st.write(f"Due :blue[{active[1][3]}]")
#         st.write(active[1][2])
#         st.write("### Subgoals")
#         for subgoal in subgoals:
#             if subgoal[0] == active[1][0]:
#                 st.write(f"- {subgoal[1]}")        
#     with c:
#         st.header("Goal C", divider=True)
#         st.subheader(active[2][1])
#         st.write(f"Due :blue[{active[2][3]}]")
#         st.write(active[2][2])
#         st.write("### Subgoals")
#         for subgoal in subgoals:
#             if subgoal[0] == active[2][0]:
#                 st.write(f"- {subgoal[1]}")  

# with right:
#     st.header("Right Half")
#     st.write("Content for the right side")
#     if st.button('Add New Project', 
#             type = 'primary', 
#             use_container_width=False):
#         st.switch_page('pages/NewProject.py')

