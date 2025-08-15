#                   ===== INITIAL IMPORTS =====                   #
# app/pages/AveryHomePage.py
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', 
    level=logging.INFO)

from modules.nav import SideBarLinks
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import re
from datetime import datetime, date, time

logging.basicConfig(
    format="%(filename)s:%(lineno)s:%(levelname)s -- %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

API_URL = "http://web-api:4000"





#                   ===== UI LAYOUT =====                   #
st.set_page_config(layout='wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("role", "guest")





#                   ===== HELPERS =====                   #
def _parse_schedule(s: str | None):
    if not s:
        return None
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %Z",  # "Fri, 15 Aug 2025 00:00:00 GMT"
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
    ):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    try:
        return datetime.strptime(s.split(" GMT")[0], "%a, %d %b %Y %H:%M:%S").date()
    except Exception:
        return None


def _due_label(d):
    if not d:
        return "No deadline"
    days = (d - date.today()).days
    prefix = "D-" if days >= 0 else "D+"
    return f"{prefix}{abs(days)} · {d.strftime('%b %d, %Y')}"

user_id = st.session_state.get("user_id")
if not user_id:
    st.error("No user ID found. Please log in or select a user profile.")
    st.stop()
user_id = 1 # Incase you refresh the page and it "logs you out" or something.

def fetch_active_goals():
    try:
        r = requests.get(f"{API_URL}/goals/user/{user_id}/active_and_priority", timeout=5)
        if r.status_code == 200:
            return r.json()
        st.error(f"Failed to load active goals: {r.status_code}")
    except Exception as e:
        st.error(f"Error contacting API: {e}")
    return []

def try_put(url: str):
    try:
        resp = requests.put(url, timeout=5, allow_redirects=False)
        return resp.status_code, (resp.text or "")
    except Exception as e:
        return None, str(e)

def get_first_bug_id():
    try:
        r = requests.get(f"{API_URL}/support/bugs", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                item = data[0]
                if isinstance(item, dict):
                    return item.get("id") or item.get("bug_id")
        return None
    except Exception:
        return None





#                   ===== PAGE CONTENT =====                   #
st.set_page_config(layout="wide", page_title="Avery — Home")
st.title("🎨 Avery — Projects")



col1, col2 = st.columns([2, 1])



# ========== LEFT: Active Projects + Archive ==========
with col1:

    # SETS THE USER_ID BASED UPON SESSION STATE.
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("No user ID found. Please log in or select a user profile.")
        st.stop()
    # user_id = 2 # Incase you refresh the page and it "logs you out" or something.


    title_col1, title_col2, title_col3, title_col4 = st.columns([4, 1, 1, 1])

    with title_col1: 
        st.write("### Active Projects")

    with title_col2:
        if st.button('Archive', type='primary', use_container_width=True, help="View archived tasks"):
            st.switch_page('pages/Archive.py')

    with title_col3:
        if st.button("Homepage", type='primary', use_container_width=True, help="Return Home"):
            st.switch_page('Home.py')

    with title_col4:
        if st.button("Add Goal", type='primary', use_container_width=True, help="Add Goal"):
            st.switch_page('pages/Add_New_Project.py')      


    goals = fetch_active_goals()



    st.write("---")
    h1, h2, h3 = st.columns([2, 1, 1])
    h1.write("**Project**")
    h2.write("**Due**")
    h3.write("**Actions**")
    st.write("---")



    if not goals:
        st.info("No active projects.")
    else:
        def _sort_key(g):
            sched = _parse_schedule(g.get("schedule"))
            return (sched is None, sched or date.max, (g.get("title") or "").lower())

        for g in sorted(goals, key=_sort_key):
            gid = g.get("id") or g.get("goal_id") or g.get("goalsid")
            title = g.get("title") or "Untitled"
            notes = (g.get("notes") or "").strip()
            sched = _parse_schedule(g.get("schedule"))
            due_str = _due_label(sched)
            
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.write(f"**{title}**")
                    if notes:
                        st.write(notes)
                with c2:
                    st.write(due_str)
                with c3:
                    if st.button("Archive", key=f"archive_{gid}", use_container_width=True):
                        if gid is None:
                            st.error("Archive failed: missing goal id")
                        else:
                            response = requests.put(f'http://web-api:4000/goals/{gid}/complete')
                            if response.status_code == 200:
                                st.success("Archived.") 
                                st.write("successfully archived :)")
                                st.rerun()
                            else: st.write(response.status_code)

                    if st.button("Delete", key=f"delete_{gid}", use_container_width=True):
                        if gid is None:
                            st.error("delete failed: missing goal id")
                        else:
                            response = requests.delete(f'http://web-api:4000/goals/{gid}/delete')
                            if response.status_code == 200:
                                st.success("Deleted.") 
                                st.write("successfully deleted :)")
                                st.rerun()
                            else: st.write(response.status_code)

            st.write("---")

            




# ========== RIGHT: Daily Log ==========
with col2:
    st.write("### Daily Log")

    # Initialize session state if not exists
    if "habit_logs" not in st.session_state:
        st.session_state["habit_logs"] = []

    # Fetch tasks from API
    def fetch_daily_tasks():
        try:
            r = requests.get(f"{API_URL}/get_daily_tasks", params={"userId": user_id}, timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            st.warning(f"Could not fetch daily tasks: {e}")
        return []

    daily_tasks = fetch_daily_tasks()

    # Display task form
    with st.form("habit_form", clear_on_submit=True):
        uid = st.text_input("User ID", value=user_id)
        title = st.text_input("Title")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Log")

        if submitted:
            payload = {"uid": uid.strip(), "title": title.strip(), "notes": notes.strip() or None}
            try:
                resp = requests.post(f"{API_URL}/habits/create", json=payload, timeout=5)
                if 200 <= resp.status_code < 300:
                    st.success("Logged.")
                else:
                    st.session_state["habit_logs"].append(payload)
                    st.warning("Logged locally (server endpoint not ready).")
            except Exception:
                st.session_state["habit_logs"].append(payload)
                st.warning("Logged locally (server unreachable).")
            # st.write(payload)  # displays the raw payload for debugging
    
    # Display existing daily tasks
    if daily_tasks or st.session_state["habit_logs"]:
        st.write("Recent Logs")

        # Combine session state logs with API logs
        all_logs = st.session_state["habit_logs"] + daily_tasks

        for task in all_logs[::-1]:  # show newest first
            task_id = task.get("id") or task.get("task_id")
            title = task.get("title") or "Untitled"
            notes = task.get("notes") or ""

            with st.container():
                col_title, col_notes, col_delete = st.columns([3, 3, 2])
                col_title.write(f"**{title}**")
                col_notes.write(notes)

                if col_delete.button("Delete", key=f"delete_{task_id}"):
                    if task_id:
                        try:
                            resp = requests.delete(f"{API_URL}/delete_daily_task/{task_id}", timeout=5)
                            if resp.status_code == 200:
                                st.success("Deleted task.")
                                st.rerun()  # refresh the page
                            else:
                                st.error(f"Failed to delete task: {resp.status_code}")
                        except Exception as e:
                            st.error(f"Error deleting task: {e}")
                    else:
                        st.warning("Task not synced to server yet. Removing locally.")
                        st.session_state["habit_logs"].remove(task)
                        st.rerun()