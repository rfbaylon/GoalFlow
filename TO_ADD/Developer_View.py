import logging
logger = logging.getLogger(__name__)

import streamlit as st
import mysql.connector


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
    conn.close()
    return result


st.title(f"Welcome Jose!")

emails = run_query("SELECT COUNT(email) FROM users")

st.write("Total users on the app:")
st.write(emails[0][0])
        
