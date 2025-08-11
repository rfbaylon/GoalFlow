import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


from modules.nav import SideBarLinks
import streamlit as st
import mysql.connector

st.session_state['authenticated'] = False
SideBarLinks(show_home=True)
st.set_page_config(layout = 'wide')

@st.cache_resource
def init_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="1203",
        database="global-GoalFlow"
    )

# Function to run queries
def run_query(query, params=None):
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    return result

st.write("# Welcome to GoalFlow!")
st.write("What are we going to get done today?")

left, right = st.columns(2)

active = run_query("SELECT id, title, notes, schedule FROM goals g WHERE g.status = 'ACTIVE' LIMIT 3;")
subgoals = run_query("SELECT g.id, sg.title FROM subgoals sg JOIN goals g ON g.id = sg.goalsid;")

# completed=run_query("SELECT g.id, COUNT(sg.status) FROM subgoals sg JOIN goals g ON g.id = sg.goalsid WHERE sg.status = 'ARCHIVED' GROUP BY g.id;")
# uncompleted=run_query("SELECT g.id, COUNT(sg.status) FROM subgoals sg JOIN goals g ON g.id = sg.goalsid WHERE sg.status = 'ACTIVE' OR 'ON ICE' GROUP BY g.id;")




with left:
    a, b, c = st.columns(3)
    with a:
        st.header("Goal A", divider=True)
        st.subheader(active[0][1]) # Goal name
        st.write(f"Due :blue[{active[0][3]}]") # Due date
        st.write(active[0][2]) # Description
        st.write("### Subgoals") # Subgoals
        for subgoal in subgoals:
            if subgoal[0] == active[0][0]:
                st.write(f"- {subgoal[1]}") 

    with b:
        st.header("Goal B", divider=True)
        st.subheader(active[1][1])
        st.write(f"Due :blue[{active[1][3]}]")
        st.write(active[1][2])
        st.write("### Subgoals")
        for subgoal in subgoals:
            if subgoal[0] == active[1][0]:
                st.write(f"- {subgoal[1]}")        
    with c:
        st.header("Goal C", divider=True)
        st.subheader(active[2][1])
        st.write(f"Due :blue[{active[2][3]}]")
        st.write(active[2][2])
        st.write("### Subgoals")
        for subgoal in subgoals:
            if subgoal[0] == active[2][0]:
                st.write(f"- {subgoal[1]}")  

with right:
    st.header("Right Half")
    st.write("Content for the right side")
    if st.button('Add New Project', 
            type = 'primary', 
            use_container_width=False):
        st.switch_page('pages/NewProject.py')

