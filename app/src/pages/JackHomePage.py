import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)

from modules.nav import SideBarLinks
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import re

# ---------------------- Utils ----------------------
HEX_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")

def safe_hex_color(c: str, default="#999999") -> str:
    if isinstance(c, str) and HEX_PATTERN.match(c.strip()):
        return c.strip()
    return default

# ---------------------- Page Init ----------------------
st.set_page_config(layout='wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

# Header
st.title("🛠️ Whats up, Jack?")

# ---------------------- Main Layout ----------------------
col1, col2 = st.columns([2, 1])

with col1:
    # GOALS
    goals = requests.get('http://web-api:4000/goals/active').json()
    goals = [
        [
            item.get("id"),       # 0 - goal_id
            item.get("title"),    # 1 - title
            item.get("notes"),    # 2 - notes/description
            item.get("schedule"), # 3 - schedule
        ]
        for item in goals
    ]

    # SUBGOALS
    subgoals = requests.get('http://web-api:4000/goals/subgoals').json()
    subgoals = [
        [
            item.get("goalsId"),  # 0 - parent goal ID
            item.get("title"),    # 1 - subgoal title
        ]
        for item in subgoals
    ]

    # HEADER
    goal_col1, goal_col2 = st.columns([3, 1])
    with goal_col1:
        st.subheader("**Goal**")
    with goal_col2:
        st.subheader("**Completion**")
    st.write("---")

    for goal in goals:
        goal_id, title, notes, schedule = goal

        with st.container():
            g1, g2 = st.columns([3, 1])

            with g1:
                st.write(f":red[**{title}**]")
                if notes:
                    st.write(notes)
                for sub in subgoals:
                    if sub[0] == goal_id:
                        st.write(f"- {sub[1]}")

            with g2:
                if st.button("Mark Complete", key=f"complete_{goal_id}"):
                    try:
                        response = requests.put(f'http://web-api:4000/goals/goals/{goal_id}/complete')
                        if response.status_code == 200:
                            st.success("Goal marked as completed!")
                            st.rerun()
                        else:
                            st.error(f"Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error updating goal: {str(e)}")

            st.write("---")

with col2:
    st.title("📊 Goal Status Overview")

    # Fetch goals for charts
    goals_all = requests.get('http://web-api:4000/goals/all').json()
    df = pd.DataFrame(goals_all)

    # Ensure columns exist
    if 'status' not in df.columns:
        df['status'] = 'ACTIVE'

    # Bar chart: goals by status
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']

    color_map = {
        'ACTIVE': 'orange',
        'PLANNED': 'blue',
        'ON ICE': 'gray',
        'ARCHIVED': 'green'
    }

    st.subheader("Goals by Status")
    fig = px.bar(
        status_counts,
        x='Status',
        y='Count',
        color='Status',
        color_discrete_map=color_map
    )
    st.plotly_chart(fig, use_container_width=True)

    # Scatter: goals vs deadline
    st.subheader("Goals vs Deadline")

    df_scatter = pd.DataFrame(goals_all)
    df_scatter['schedule'] = pd.to_datetime(df_scatter.get('schedule', pd.NaT))
    df_scatter['priority'] = df_scatter.get('priority', 'low')
    df_scatter['status'] = df_scatter.get('status', 'PLANNED')
    df_scatter['title'] = df_scatter.get('title', 'Untitled')

    priority_map = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
    df_scatter['priority_num'] = df_scatter['priority'].map(priority_map)

    fig2 = px.scatter(
        df_scatter,
        x='schedule',
        y='priority_num',
        color='status',
        hover_data=['title', 'notes', 'priority'],
        labels={'priority_num': 'Priority', 'schedule': 'Deadline'},
        title='Goals vs Deadline by Priority and Status',
        height=500
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------- Tags API ----------------------
def fetch_tags(name: str | None = None, color: str | None = None):
    params = {}
    if name:
        params["name"] = name.strip()
    if color:
        params["color"] = color.strip()
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
    if new_name:
        body["name"] = new_name.strip()
    if new_color:
        body["color"] = new_color.strip()
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

# ---------------------- Tags UI ----------------------
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

for idx, t in enumerate(tags_data):
    raw_tid = t.get("id") or t.get("tag_id") or ""
    # Ensure uniqueness even if id is missing/duplicated
    safe_tid = str(raw_tid).strip() or f"idx{idx}"
    uniq = f"{safe_tid}_{idx}"

    tname = t.get("name") or ""
    tcolor = safe_hex_color(t.get("color"), "#999999")

    with st.container():
        r1, r2, r3, r4 = st.columns([2, 1, 2, 1])

        with r1:
            st.write(f"**{tname}**")
            st.markdown(
                f"<div style='width:18px;height:18px;border-radius:4px;background:{tcolor};border:1px solid #ccc;'></div>",
                unsafe_allow_html=True
            )

        with r2:
            new_name = st.text_input(
                "Rename",
                value=tname,
                key=f"rename_name_{uniq}",
                label_visibility="collapsed"
            )

        with r3:
            new_color = st.color_picker(
                "Color",
                value=tcolor,
                key=f"rename_color_{uniq}"
            )

        with r4:
            if st.button("Save", key=f"btn_save_tag_{uniq}", use_container_width=True):
                # Try to use numeric id if present; otherwise fall back to raw_tid
                target_id = t.get("id") or t.get("tag_id")
                ok, msg = rename_tag_api(target_id, new_name, new_color)
                if ok:
                    st.success("Tag updated.")
                    st.rerun()
                else:
                    st.error(f"Update failed: {msg}")

            if st.button("Delete", key=f"btn_delete_tag_{uniq}", use_container_width=True):
                target_id = t.get("id") or t.get("tag_id")
                ok, msg = delete_tag_api(target_id)
                if ok:
                    st.success("Tag deleted.")
                    st.rerun()
                else:
                    st.error(f"Delete failed: {msg}")

        st.write("---")
