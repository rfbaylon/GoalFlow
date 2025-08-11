import streamlit as st
import mysql.connector
import pandas as pd

st.title("Backlog")

@st.cache_resource
def init_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="1203",
        database="global-GoalFlow"
    )

def run_query(query, params=None):
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    return result

on_ice = run_query("SELECT title, notes FROM goals WHERE status = 'ON ICE'")
print(on_ice)

for goal in on_ice:
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.write(f"**{goal[1]}**")
    
    with col2:
        if st.button("Activate", key=f"activate_{goal[0]}"):
            # activate_goal(goal[0])
            st.rerun()