# app/pages/AveryHomePage.py

import streamlit as st
st.set_page_config(layout="wide", page_title="Avery — Home")

import logging
import requests
from datetime import datetime, date

logging.basicConfig(
    format="%(filename)s:%(lineno)s:%(levelname)s -- %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

API_URL = "http://web-api:4000"

# ---- Session defaults ----
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("role", "guest")
st.session_state.setdefault("user_id", 1)

# Sidebar: user switcher
st.sidebar.write("## User")
new_uid = st.sidebar.number_input("user_id", min_value=1, value=int(st.session_state["user_id"]), step=1)
if new_uid != st.session_state["user_id"]:
    st.session_state["user_id"] = int(new_uid)
    st.rerun()
user_id = int(st.session_state["user_id"])

# --------------------------
# Helpers
# --------------------------
def _parse_schedule(s: str | None):
    if not s:
        return None
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %Z",
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

def _coerce_goals_list(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("goals", "items", "results", "data"):
            if isinstance(data.get(key), list):
                return data[key]
    return []

def _get_json_list(url, tried):
    try:
        r = requests.get(url, timeout=5)
        tried.append((url, r.status_code, r.text[:300]))
        if r.status_code == 200:
            return _coerce_goals_list(r.json())
        return []
    except Exception as e:
        tried.append((url, "EXC", str(e)))
        return []

def fetch_active_goals(uid: int):
    tried = []
    base = f"{API_URL}/goals"
    goals = _get_json_list(f"{base}/user/{uid}/active_and_priority", tried)

    # Normalize date-ish field into "schedule"
    for g in goals:
        if g.get("schedule") is None:
            for k in ("due", "due_date", "deadline", "date", "scheduled_for"):
                if k in g and g[k]:
                    g["schedule"] = g[k]
                    break

    st.session_state["__goals_debug__"] = tried
    st.session_state["__goals_sample__"] = goals[:3] if isinstance(goals, list) else []
    return goals

def scan_users_for_goals(start_uid=1, end_uid=20):
    report = []
    for uid in range(start_uid, end_uid + 1):
        tried = []
        items = _get_json_list(f"{API_URL}/goals/user/{uid}/active_and_priority", tried)
        count = len(items) if isinstance(items, list) else 0
        report.append({"user_id": uid, "count": count})
    return report

# --------------------------
# UI
# --------------------------
st.title("🎨 Avery — Projects")

col1, col2 = st.columns([2, 1])

# LEFT: Active Projects + Archive
with col1:
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

    goals = fetch_active_goals(user_id)

    st.write("---")
    h1, h2, h3 = st.columns([2, 1, 1])
    h1.write("**Project**")
    h2.write("**Due**")
    h3.write("**Actions**")
    st.write("---")

    if not goals:
        st.info("No active projects for this user on /goals/user/{uid}/active_and_priority.")
        st.caption("Use the sidebar to try a different user_id, or create a goal that is active & priority for this user.")
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
                            resp = requests.put(f'{API_URL}/goals/{gid}/complete')
                            if resp.status_code == 200:
                                st.success("Archived.")
                                st.rerun()
                            else:
                                st.error(resp.status_code)

                    if st.button("Delete", key=f"delete_{gid}", use_container_width=True):
                        if gid is None:
                            st.error("Delete failed: missing goal id")
                        else:
                            resp = requests.delete(f'{API_URL}/goals/{gid}/delete')
                            if resp.status_code == 200:
                                st.success("Deleted.")
                                st.rerun()
                            else:
                                st.error(resp.status_code)

            st.write("---")

# RIGHT: Daily Log + Scanner
with col2:
    st.write("### Daily Log")

    if "habit_logs" not in st.session_state:
        st.session_state["habit_logs"] = []

    with st.form("habit_form", clear_on_submit=True):
        uid = st.text_input("User ID", value=str(user_id))
        title = st.text_input("Title")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Log")

        if submitted:
            payload = {
                "uid": uid.strip(),
                "title": title.strip(),
                "notes": notes.strip() or None,
            }
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
            st.write(payload)

    if st.session_state["habit_logs"]:
        st.write("Recent Logs")
        for h in st.session_state["habit_logs"][-5:][::-1]:
            st.markdown(f"- {h['title']}")

    st.write("---")
    st.write("### Goal Scanner")
    start_uid = st.number_input("Scan from user_id", min_value=1, value=1, step=1)
    end_uid = st.number_input("Scan to user_id", min_value=start_uid, value=max(start_uid, 10), step=1)
    if st.button("Scan"):
        rows = scan_users_for_goals(start_uid, end_uid)
        st.write(rows)

# Debug expander
with st.expander("🔎 Debug — Goals API"):
    tried = st.session_state.get("__goals_debug__", [])
    sample = st.session_state.get("__goals_sample__", [])
    st.write("Tried requests (url, status, preview):")
    for url, status, preview in tried:
        st.code(f"{url} -> {status}\n{preview}", language="text")
    st.write("Sample parsed items (first 3):")
    st.json(sample)
