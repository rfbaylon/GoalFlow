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

def is_json_2xx(resp):
    return (200 <= resp.status_code < 300) and resp.headers.get("content-type","").lower().startswith("application/json")

# ---------------------- Page Init ----------------------
st.set_page_config(layout='wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

# keep just IDs of tags created during this session, but persist them via URL
def _get_query_tag_ids():
    try:
        csv = st.query_params.get("tag_ids", "")
    except Exception:
        params = st.experimental_get_query_params()
        csv = params.get("tag_ids", [""])[0] if "tag_ids" in params else ""
    ids = []
    for tok in (csv.split(",") if csv else []):
        tok = tok.strip()
        if tok.isdigit():
            ids.append(int(tok))
    return ids

def _set_query_tag_ids(ids):
    csv = ",".join(str(i) for i in ids)
    try:
        st.query_params["tag_ids"] = csv
    except Exception:
        st.experimental_set_query_params(tag_ids=csv)

if "created_tag_ids" not in st.session_state:
    st.session_state["created_tag_ids"] = _get_query_tag_ids()

def _sync_from_query_if_needed():
    q_ids = _get_query_tag_ids()
    if q_ids != st.session_state.get("created_tag_ids", []):
        st.session_state["created_tag_ids"] = q_ids

def _sync_to_query():
    _set_query_tag_ids(st.session_state["created_tag_ids"])

# Header
st.title("💼 Whats up, Jack?")

# ---------------------- Main Layout ----------------------
col1, col2 = st.columns([3, 1])

with col1:
    # SETS THE USER_ID BASED UPON SESSION STATE.
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("No user ID found. Please log in or select a user profile.")
        st.stop()
    user_id = 4 # Incase you refresh the page and it "logs you out" or something.
    
    # GOALS
    try:
        goals = requests.get(f'http://web-api:4000/goals/user/{user_id}/active_and_priority').json()
    except Exception as e:
        st.error(f"Could not fetch goals: {e}")
        goals = []

    goals = [
        [item.get("id"), 
         item.get("title"), 
         item.get("notes"), 
         item.get("schedule")
         ]
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
        # Fetch tags for a goal (goal-specific route, unchanged)
        try:
            resp = requests.get(f"http://web-api:4000/tags/goals/{goal_id}/tags", timeout=5)
            tags_raw = resp.json() if resp.headers.get("content-type","").lower().startswith("application/json") else []
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
    goals = requests.get(f'http://web-api:4000/goals/user/{user_id}/active_and_priority').json()
    df = pd.DataFrame(goals)

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

    df_scatter = pd.DataFrame(goals)
    df_scatter['schedule'] = pd.to_datetime(df_scatter.get('schedule', pd.NaT))
    df_scatter['priority'] = df_scatter.get('priority', 'critical')
    df_scatter['status'] = df_scatter.get('status', 'PLANNED')
    df_scatter['title'] = df_scatter.get('title', 'Untitled')

    fig2 = px.scatter(
        df_scatter,
        x='schedule',
        y='priority',
        hover_data=['title', 'notes', 'priority'],
        labels={'priority': 'Priority', 'schedule': 'Deadline'},
        title='Goal Deadline By Priority',
        height=500
    )

    fig2.update_yaxes(showgrid=True, gridcolor='lightgray')
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------- Tags (server-backed; strict 2xx+JSON; refresh-persistent) ----------------------
API_BASE = "http://web-api:4000"

def _first_json_2xx(responses):
    """Return first response that is 2xx and application/json."""
    for r in responses:
        if r is not None and is_json_2xx(r):
            return r
    return None

def _try_paths_json_2xx(method, paths, **kwargs):
    """Try paths in order; return first 2xx+JSON response (or first 2xx for DELETE)."""
    last_exc = None
    results = []
    for p in paths:
        try:
            if method == "GET":
                r = requests.get(API_BASE + p, timeout=kwargs.get("timeout", 5))
            elif method == "POST":
                r = requests.post(API_BASE + p, json=kwargs.get("json", {}), timeout=kwargs.get("timeout", 5))
            elif method == "DELETE":
                r = requests.delete(API_BASE + p, timeout=kwargs.get("timeout", 5))
            else:
                raise ValueError("Unsupported method")
            results.append(r)
        except Exception as e:
            last_exc = e
            results.append(None)

    if method in ("GET", "POST"):
        ok = _first_json_2xx(results)
        if ok is not None:
            return ok
    else:  # DELETE: accept any 2xx (no need for JSON)
        for r in results:
            if r is not None and 200 <= r.status_code < 300:
                return r

    # If none matched, raise the last exception or an informative error
    if last_exc:
        raise last_exc
    raise RuntimeError(f"No {method} path returned 2xx JSON (paths tried: {paths})")

def api_delete_tag(tag_id: int):
    pid = int(tag_id)
    # Your blueprint has "/delete_tag/<id>". With url_prefix="/tags" it becomes "/tags/delete_tag/<id>".
    return _try_paths_json_2xx("DELETE", [f"/delete_tag/{pid}", f"/tags/delete_tag/{pid}"])

def api_get_tag_by_id(tag_id: int):
    pid = int(tag_id)
    # Your blueprint route is "/tags/<id>". If url_prefix="/tags", it becomes "/tags/tags/<id>".
    return _try_paths_json_2xx("GET", [f"/tags/{pid}", f"/tags/tags/{pid}"])

st.write("### 🏷️ Tags")


# Delete by ID (manual)
with st.expander("Delete a tag by ID", expanded=False):
    d1, d2 = st.columns([2, 1])
    with d1:
        del_id = st.text_input("Tag ID", key="quick_del_id", placeholder="e.g., 42")
    with d2:
        if st.button("Delete", key="quick_del_btn", use_container_width=True):
            did = (del_id or "").strip()
            if not did.isdigit():
                st.error("Tag ID must be a number.")
            else:
                try:
                    rid = int(did)
                    api_delete_tag(rid)  # raises if no 2xx
                    _sync_from_query_if_needed()
                    st.session_state["created_tag_ids"] = [x for x in st.session_state["created_tag_ids"] if x != rid]
                    _sync_to_query()
                    st.success("Tag deleted.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Delete failed: {e}")

