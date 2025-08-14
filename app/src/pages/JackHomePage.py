import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
from modules.nav import SideBarLinks
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout = 'wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

# Header
st.title("🛠️ Whats up, Jack?")

# Create main layout: left column (system issues) and right column (quick actions + charts)
col1, col2 = st.columns([2, 1])
with col1:

    # GOALS
    goals = requests.get('http://web-api:4000/goals/active').json()

    # Use explicit mapping instead of list(item.values())
    goals = [
        [
            item.get("id"),      # 0 - goal_id
            item.get("title"),   # 1 - title
            item.get("notes"),   # 2 - notes/description
            item.get("schedule") # 3 - schedule
        ]
        for item in goals
    ]

    # SUBGOALS
    subgoals = requests.get('http://web-api:4000/goals/subgoals').json()
    subgoals = [
    [
        item.get("goalsId"),     # 2 - parent goal ID
        item.get("title"),      # 1 - subgoal title
        
    ]
    for item in subgoals
    ]

    # HEADER
    goal_col1, goal_col2 = st.columns([3, 1])
    with goal_col1: st.subheader("**Goal**")
    with goal_col2: st.subheader("**Completion**")
    st.write("---")

    for goal in goals:
        goal_id, title, notes, schedule = goal

        with st.container():
            goal_col1, goal_col2 = st.columns([3, 1])

            with goal_col1:
                st.write(f":red[**{title}**]")   # Title on top
                if notes:
                    st.write(notes)              # Notes/desc underneath
                for subgoal in subgoals:
                    if subgoal[0] == goal[0]:
                        st.write(f"- {subgoal[1]}")

            with goal_col2:
                # Use unique keys per goal
                if st.button("Mark Complete", key=f"complete_{goal_id}"):
                    try:
                        response = requests.put(f'http://web-api:4000/goals/goals/{goal_id}/complete')
                        if response.status_code == 200:
                            st.success("Goal marked as completed!")
                            st.rerun()  # Refresh page
                        else:
                            st.error(f"Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error updating goal: {str(e)}")

            st.write("---")

with col2:
    st.title("📊 Goal Status Overview")

    # Fetch goals from API
    goals = requests.get('http://web-api:4000/goals/all').json()  # or endpoint for all goals

    # Convert to DataFrame
    df = pd.DataFrame(goals)

    # Ensure 'status' column exists
    if 'status' not in df.columns:
        df['status'] = 'ACTIVE'  # default fallback

    # Count goals per status
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']

    # Optional: color mapping for clarity
    color_map = {
        'ACTIVE': 'orange',
        'PLANNED': 'blue',
        'ON ICE': 'gray',
        'ARCHIVED': 'green'
    }

    # Create bar chart
    st.subheader("Goals by Status")
    fig = px.bar(
        status_counts,
        x='Status',
        y='Count',
        color='Status',
        color_discrete_map=color_map
    )

    st.plotly_chart(fig, use_container_width=True)


    st.subheader("Goals vs Deadline")

    goals = requests.get('http://web-api:4000/goals/all').json()

    df = pd.DataFrame(goals)

    df['schedule'] = pd.to_datetime(df.get('schedule', pd.NaT))
    df['priority'] = df.get('priority', 'low')
    df['status'] = df.get('status', 'PLANNED')
    df['title'] = df.get('title', 'Untitled')

    priority_map = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
    df['priority_num'] = df['priority'].map(priority_map)

    # Scatter plot
    fig = px.scatter(
        df,
        x='schedule',
        y='priority_num',  # numeric representation for vertical positioning
        color='status',
        hover_data=['title', 'notes', 'priority'],
        labels={'priority_num': 'Priority', 'schedule': 'Deadline'},
        title='Goals vs Deadline by Priority and Status',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

# Fetch all goals
all_goals = requests.get('http://web-api:4000/goals/active').json()

# Filter ON ICE goals
on_ice_goals = [goal for goal in all_goals if goal.get('status') == 'ON ICE']


def fetch_tags(name: str | None = None, color: str | None = None):
   """GET /tags/get_tag?name=&color="""
   params = {}
   if name: params["name"] = name.strip()
   if color: params["color"] = color.strip()
   try:
       r = requests.get(f"{API_BASE}/tags/get_tag", params=params, timeout=5)
       if r.ok:
           return r.json()
       st.error(f"Failed to load tags: {r.status_code}")
   except Exception as e:
       st.error(f"Error contacting tags API: {e}")
   return []

# ---------------------- API Calls ----------------------

def fetch_tags(name: str | None = None, color: str | None = None):
    params = {}
    if name: params["name"] = name.strip()
    if color: params["color"] = color.strip()
    try:
        r = requests.get("http://web-api:4000/tags/get_tag", params=params, timeout=5)
        if r.ok:
            return r.json()
        st.error(f"Failed to load tags: {r.status_code}")
    except Exception as e:
        st.error(f"Error contacting tags API: {e}")
    return []

def create_tag_api(name: str, color: str):
    try:
        payload = {"name": (name or "").strip(), "color": (color or "").strip()}
        r = requests.post("http://web-api:4000/tags/create_tag", json=payload, timeout=5)
        if 200 <= r.status_code < 300:
            if r.headers.get("content-type", "").startswith("application/json"):
                return True, r.json()
            return True, r.text
        return False, f"{r.status_code} {r.text[:200]}"
    except Exception as e:
        return False, str(e)

def rename_tag_api(tag_id: int, new_name: str | None = None, new_color: str | None = None):
    body = {}
    if new_name: body["name"] = new_name.strip()
    if new_color: body["color"] = new_color.strip()
    if not body:
        return False, "No fields to update"
    try:
        r = requests.put(f"http://web-api:4000/tags/rename_tag/{tag_id}", json=body, timeout=5)
        if 200 <= r.status_code < 300:
            return True, r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text
        return False, f"{r.status_code} {r.text[:200]}"
    except Exception as e:
        return False, str(e)

def delete_tag_api(tag_id: int):
    try:
        r = requests.delete(f"http://web-api:4000/tags/delete_tag/{tag_id}", timeout=5)
        if r.status_code in (200, 202, 204):
            return True, r.text
        return False, f"{r.status_code} {r.text[:200]}"
    except Exception as e:
        return False, str(e)



#Tags code

st.write("### 🏷️ Tags")


with st.expander("Create a tag"):
   c1, c2, c3 = st.columns([2, 1, 1])
   with c1:
       new_tag_name = st.text_input("Name", key="tag_new_name")
   with c2:
       new_tag_color = st.color_picker("Color", value="#ff9900", key="tag_new_color")
   with c3:
       if st.button("Create", key="btn_create_tag", use_container_width=True, type="primary"):
           if not new_tag_color:
               st.error("Color is required.")
           else:
               ok, msg = create_tag_api(new_tag_name or "", new_tag_color)
               if ok:
                   st.success("Tag created.")
                   st.rerun()
               else:
                   st.error(f"Create failed: {msg}")


# Filters
f1, f2, f3 = st.columns([2, 2, 1])
with f1:
   filter_name = st.text_input("Filter by name", key="tag_filter_name")
with f2:
   filter_color = st.text_input("Filter by color (e.g. #ff0000)", key="tag_filter_color")
with f3:
   do_search = st.button("Search", key="btn_search_tags", use_container_width=True)


# Load & list
tags_data = fetch_tags(filter_name if do_search else None, filter_color if do_search else None)
st.caption(f"Results: {len(tags_data)} tag(s)")


for t in tags_data:
   tid = t.get("id") or t.get("tag_id")
   tname = t.get("name") or ""
   tcolor = t.get("color") or "#999999"


   with st.container():
       r1, r2, r3, r4 = st.columns([2, 1, 2, 1])


       with r1:
           st.write(f"**{tname}**")
           st.markdown(f"<div style='width:18px;height:18px;border-radius:4px;background:{tcolor};border:1px solid #ccc;'></div>",
                       unsafe_allow_html=True)


       with r2:
           new_name = st.text_input("Rename", value=tname, key=f"rename_name_{tid}", label_visibility="collapsed")


       with r3:
           new_color = st.color_picker("Color", value=tcolor, key=f"rename_color_{tid}")


       with r4:
           if st.button("Save", key=f"btn_save_tag_{tid}", use_container_width=True):
               ok, msg = rename_tag_api(tid, new_name, new_color)
               if ok:
                   st.success("Tag updated.")
                   st.rerun()
               else:
                   st.error(f"Update failed: {msg}")


           if st.button("Delete", key=f"btn_delete_tag_{tid}", use_container_width=True):
               ok, msg = delete_tag_api(tid)
               if ok:
                   st.success("Tag deleted.")
                   st.rerun()
               else:
                   st.error(f"Delete failed: {msg}")


       st.write("---")
