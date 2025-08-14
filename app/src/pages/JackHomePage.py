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

def normalize_tag_row(row):
    """Make backend row (dict or tuple/list) into {'id','name','color'}."""
    if isinstance(row, dict):
        return {"id": row.get("id") or row.get("tag_id"),
                "name": row.get("name"),
                "color": row.get("color")}
    if isinstance(row, (list, tuple)):
        id_, name, color = (list(row) + [None, None, None])[:3]
        return {"id": id_, "name": name, "color": color}
    return {"id": None, "name": "Unnamed", "color": "#999999"}

# ---------------------- Page Init ----------------------
st.set_page_config(layout='wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

if "my_tags" not in st.session_state:
    st.session_state["my_tags"] = []  # each: {"id": int|None, "name": str, "color": "#hex"}

# Header
st.title("💼 Whats up, Jack?")

# ---------------------- Main Layout ----------------------
col1, col2 = st.columns([3, 1])

with col1:
    # GOALS
    goals = requests.get('http://web-api:4000/goals/active').json()
    goals = [
        [item.get("id"), item.get("title"), item.get("notes"), item.get("schedule")]
        for item in goals
    ]

    # SUBGOALS
    subgoals = requests.get('http://web-api:4000/goals/subgoals').json()
    subgoals = [
        [item.get("goalsId"), item.get("title")]
        for item in subgoals
    ]

    # HEADER
    goal_col1, goal_col2, goal_col3 = st.columns([3, 1, 1.5])
    with goal_col1:
        st.subheader("**Goal**", divider=True)

    with goal_col2:
        st.subheader("**Tags**", divider=True)

    for goal_id, title, notes, schedule in goals:
        # Fetch tags for a goal (GOAL route)
        try:
            resp = requests.get(f"http://web-api:4000/tags/goals/{goal_id}/tags", timeout=5)
            tags_raw = resp.json() if resp.headers.get("content-type","").startswith("application/json") else []
        except Exception as e:
            tags_raw = []
            st.warning(f"Failed to load tags for goal {goal_id}: {e}")

        # Normalize for display
        tags_for_display = []
        for t in tags_raw:
            nt = normalize_tag_row(t)
            tags_for_display.append({
                "name": nt.get("name") or "Unnamed",
                "color": safe_hex_color(nt.get("color"), "#999999")
            })

        with st.container():
            g1, g2, g3 = st.columns([3, 1.5, 1])

            with g1:
                st.write(f":red[**{title}**]")
                if notes:
                    st.write(notes)
                for sub in subgoals:
                    if sub[0] == goal_id:
                        st.write(f"- {sub[1]}")

            with g2:
                if tags_for_display:
                    tag_htmls = [
                        f"<span style='background:{t['color']}; padding:2px 6px; border-radius:4px; margin-right:4px; color:white;'>{t['name']}</span>"
                        for t in tags_for_display
                    ]
                    st.markdown("".join(tag_htmls), unsafe_allow_html=True)
                else:
                    st.write("—")  # placeholder if no tags

            with g3:
                if st.button("Mark Complete", key=f"complete_{goal_id}"):
                    try:
                        response = requests.put(f'http://web-api:4000/goals/{goal_id}/complete', timeout=5)
                        if response.status_code == 200:
                            st.success("Goal marked as completed!")
                            st.rerun()
                        else:
                            st.error(f"Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error updating goal: {str(e)}")

            st.write("---")

with col2:
    st.header("📊 Goal Status Overview")

    # Fetch goals for charts
    goals_all = requests.get('http://web-api:4000/goals/all').json()
    df = pd.DataFrame(goals_all)

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
    df_scatter['priority'] = df_scatter.get('priority', 'high')
    df_scatter['status'] = df_scatter.get('status', 'PLANNED')
    df_scatter['title'] = df_scatter.get('title', 'Untitled')

    fig2 = px.scatter(
        df_scatter,
        x='schedule',
        y='priority',
        hover_data=['title', 'notes', 'priority'],
        labels={'priority': 'Priority', 'schedule': 'Deadline'},
        title='High Priority Goals',
        height=500
    )

    fig2.update_yaxes(showgrid=True, gridcolor='lightgray')
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------- Tags API (TAG routes only) ----------------------
def create_tag_api(name: str, color: str):
    payload = {"name": (name or "").strip(), "color": (color or "").strip()}
    return requests.post("http://web-api:4000/tags/create_tag", json=payload, timeout=5)

def delete_tag_api(tag_id: int):
    return requests.delete(f"http://web-api:4000/tags/delete_tag/{int(tag_id)}", timeout=5)


# ---------------------- Tags UI (Create + Delete by ID) ----------------------
st.write("### 🏷️ Tags")

with st.expander("Create a tag", expanded=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        new_tag_name = st.text_input("Name (optional)", key="tag_new_name")
    with c2:
        new_tag_color = st.color_picker("Color (required)", value="#ff9900", key="tag_new_color")
    with c3:
        if st.button("Create", key="btn_create_tag", use_container_width=True, type="primary"):
            if not new_tag_color or not HEX_PATTERN.match(new_tag_color.strip()):
                st.error("Valid hex color is required.")
            else:
                try:
                    r = create_tag_api(new_tag_name or "", new_tag_color)
                    if 200 <= r.status_code < 300:
                        tag_id = None
                        try:
                            if r.headers.get("content-type","").startswith("application/json"):
                                data = r.json()
                                tag_id = data.get("id") or data.get("tag_id")
                        except Exception:
                            pass

                        # Add to session so it shows immediately below
                        st.session_state["my_tags"].append({
                            "id": int(tag_id) if tag_id is not None else None,
                            "name": new_tag_name or "",
                            "color": new_tag_color
                        })

                        st.success("Tag created.")
                        st.rerun()
                    else:
                        st.error(f"Create failed: {r.status_code} {r.text[:200]}")
                except Exception as e:
                    st.error(f"Create failed: {e}")

with st.expander("Delete a tag by ID", expanded=False):
    d1, d2 = st.columns([2, 1])
    with d1:
        del_id = st.text_input("Tag ID", key="quick_del_id", placeholder="e.g., 42")
    with d2:
        if st.button("Delete", key="quick_del_btn", use_container_width=True):
            if not del_id.strip().isdigit():
                st.error("Tag ID must be a number.")
            else:
                try:
                    r = delete_tag_api(int(del_id.strip()))
                    if r.status_code in (200, 202, 204):
                        # Remove from session list if present
                        tag_id_int = int(del_id.strip())
                        st.session_state["my_tags"] = [
                            x for x in st.session_state["my_tags"]
                            if x.get("id") != tag_id_int
                        ]
                        st.success("Tag deleted.")
                        st.rerun()
                    else:
                        st.error(f"Delete failed: {r.status_code} {r.text[:200]}")
                except Exception as e:
                    st.error(f"Delete failed: {e}")

# ---------------------- Session-created tags preview ----------------------
if st.session_state["my_tags"]:
    st.caption(f"Session tags: {len(st.session_state['my_tags'])}")
    for idx, t in enumerate(st.session_state["my_tags"]):
        raw_tid = t.get("id")
        uniq = f"{raw_tid}_{idx}"
        tname = t.get("name") or ""
        tcolor = safe_hex_color(t.get("color"), "#999999")
        with st.container():
            r1, r2 = st.columns([5, 1])
            with r1:
                st.write(f"**{tname}**  ·  `{raw_tid}`")
                st.markdown(
                    f"<div style='width:18px;height:18px;border-radius:4px;background:{tcolor};border:1px solid #ccc;display:inline-block;margin-top:4px;'></div>",
                    unsafe_allow_html=True
                )
            with r2:
                if st.button("Delete", key=f"btn_delete_tag_{uniq}", use_container_width=True):
                    try:
                        if raw_tid is None:
                            st.error("Cannot delete: missing server id.")
                        else:
                            r = delete_tag_api(int(raw_tid))
                            if r.status_code in (200, 202, 204):
                                st.session_state["my_tags"] = [
                                    x for x in st.session_state["my_tags"]
                                    if x.get("id") != raw_tid
                                ]
                                st.success("Tag deleted.")
                                st.rerun()
                            else:
                                st.error(f"Delete failed: {r.status_code} {r.text[:200]}")
                    except Exception as e:
                        st.error(f"Delete failed: {e}")
            st.write("---")
