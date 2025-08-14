# app/pages/AveryHomePage.py

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
        return "No deadline"
    days = (d - date.today()).days
    prefix = "D-" if days >= 0 else "D+"
    return f"{prefix}{abs(days)} · {d.strftime('%b %d, %Y')}"

def fetch_active_goals():
    try:
        r = requests.get(f"{API_URL}/goals/active", timeout=5)
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

# --------------------------
# UI
# --------------------------
st.set_page_config(layout="wide", page_title="Avery — Home")

st.title("🎨 Avery — Projects")

col1, col2 = st.columns([2, 1])

# ========== LEFT: Active Projects + Archive ==========
with col1:
    st.write("### Active Projects")

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
                                st.rerun()
                            else: st.write(response.status_code)

                    if st.button("Delete", key=f"delete_{gid}", use_container_width=True):
                        if gid is None:
                            st.error("Archive failed: missing goal id")
                        else:
                            response = requests.put(f'http://web-api:4000/goals/{gid}/delete')
                            if response.status_code == 200:
                                st.success("Deleted.") 
                                st.rerun()
                            else: st.write(response.status_code)

                

                        # if st.button("Mark Complete", key=f"complete_{bug[2]}"):
                        #     try:
                        #     response = requests.put(f'http://web-api:4000/support/bugs/{bug[2]}/complete')
                        #     if response.status_code == 200:
                        #         st.success("Bug marked as completed!")
                        #         st.rerun()  # Refresh the page to show updated status
                        #     else:
                        #         st.error(f"Error: {response.status_code}")
                                # else:
                                #     url2 = f"{API_URL}/support/goals/{gid}/complete"
                                #     code2, body2 = try_put(url2)
                                #     if code2 == 200:
                                #         st.success("Archived (temporary mapping via support/bugs).")
                                #         st.rerun()
                                #     else:
                                #         fallback_id = get_first_bug_id()
                                #         if fallback_id is not None:
                                #             url3 = f"{API_URL}/support/bugs/{fallback_id}/complete"
                                #             code3, body3 = try_put(url3)
                                #             if code3 == 200:
                                #                 st.warning(
                                #                     "Goals completed, but archived via fallback bug id."
                                #                 )
                                #                 st.rerun()
                                #             else:
                                #                 st.error("Archive failed on all routes.")
                                #                 with st.expander("Details"):
                                #                     st.write(f"1) {url1} → {code}"); st.code((body or "")[:500])
                                #                     st.write(f"2) {url2} → {code2}"); st.code((body2 or "")[:500])
                                #                     st.write(f"3) {url3} → {code3}"); st.code((body3 or "")[:500])
                                #         else:
                                #             st.error("Archive failed. No fallback bug id.")
                                #             with st.expander("Details"):
                                #                 st.write(f"1) {url1} → {code}"); st.code((body or "")[:500])
                                #                 st.write(f"2) {url2} → {code2}"); st.code((body2 or "")[:500])

            st.write("---")

# ========== RIGHT: Daily Log ==========
with col2:
    st.write("### Daily Log")

    if "habit_logs" not in st.session_state:
        st.session_state["habit_logs"] = []

    with st.form("habit_form", clear_on_submit=True):
        log_date = st.date_input("Date", value=date.today())
        log_time = st.time_input("Time", value=time(9, 0))
        habit = st.text_input("What did you do?", placeholder="Sketching / Reading / Branding / Prototype ...")
        duration = st.number_input("Minutes", min_value=5, max_value=480, value=30, step=5)
        notes = st.text_area("Notes (optional)", placeholder="Breakthroughs, blockers, references, etc.")
        submitted = st.form_submit_button("Log")

        if submitted:
            payload = {
                "date": log_date.isoformat(),
                "time": log_time.strftime("%H:%M"),
                "habit": (habit or "General").strip(),
                "duration_min": int(duration),
                "notes": notes.strip() or None,
            }
            try:
                resp = requests.post(f"{API_URL}/habits/log", json=payload, timeout=5)
                if 200 <= resp.status_code < 300:
                    st.success("Logged.")
                else:
                    st.session_state["habit_logs"].append(payload)
                    st.warning("Logged locally (server endpoint not ready).")
            except Exception:
                st.session_state["habit_logs"].append(payload)
                st.warning("Logged locally (server unreachable).")

    if st.session_state["habit_logs"]:
        st.write("Recent Logs")
        for h in st.session_state["habit_logs"][-5:][::-1]:
            line = f"- {h['date']} {h['time']} · {h['habit']} · {h['duration_min']}m"
            if h.get("notes"):
                line += f"\n  \n  :grey[{h['notes']}]"
            st.markdown(line)