import logging
import streamlit as st
import requests
from datetime import datetime, date, time

logging.basicConfig(
    format="%(filename)s:%(lineno)s:%(levelname)s -- %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

API_URL = "http://web-api:4000"

# --------------------------
# helpers
# --------------------------
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
        return "no time of completion"
    days = (d - date.today()).days
    prefix = "D-" if days >= 0 else "D+"
    return f"{prefix}{abs(days)} · {d.strftime('%b %d, %Y')}"

def fetch_active_goals():
    try:
        r = requests.get(f"{API_URL}/goals/archive", timeout=5)
        if r.status_code == 200:
            return r.json()
        st.error(f"Failed to load archived goals: {r.status_code}")
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

# --------------------------
# UI
# --------------------------
st.set_page_config(layout="wide", page_title="Avery — Home")



col1, col2 = st.columns([2, 1])

# ========== LEFT: Active Projects + Archive ==========
with col1:
    title_col1, title_col2 = st.columns([6,1])
    with title_col1: st.title("Archive")
    with title_col2:
        if st.button("Avery's Homepage", 
                        type='primary', 
                        help="Return to Avery's tasks"):
                st.switch_page('pages/AveryHomePage.py')
    st.write("---")

    goals = fetch_active_goals()

    if not goals:
        st.info("No archived projects.")
    else:
        def _sort_key(g):
            sched = _parse_schedule(g.get("completedAt"))
            return (sched is None, sched or date.max, (g.get("title") or "").lower())

        for g in sorted(goals, key=_sort_key):
            gid = g.get("id") or g.get("goal_id") or g.get("goalsid")
            title = g.get("title") or "Untitled"
            notes = (g.get("notes") or "").strip()
            sched = _parse_schedule(g.get("completedAt"))
            comp_date = _due_label(sched)
            

            col1, col2 = st.columns([3,1])
            with col1:
                st.write(f"**{title}**")
                if notes:
                    st.write(notes)
            with col2: 
                st.write(f"archived at:")
                st.write(comp_date)  
            st.write("---")
