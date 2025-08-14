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
    st.write("### Company Goals")

    goals = requests.get('http://web-api:4000/goals/active').json()
    with col1:
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

        st.write("---")
        goal_col1, goal_col2 = st.columns([3, 1])
        with goal_col1: st.write("**Goal**")
        with goal_col2: st.write("**Completion**")
        st.write("---")

        for goal in goals:
            goal_id, title, notes, schedule = goal

            with st.container():
                goal_col1, goal_col2 = st.columns([3, 1])

                with goal_col1:
                    st.write(f":red[**{title}**]")   # Title on top
                    if notes:
                        st.write(notes)              # Notes/desc underneath

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




# Fetch all goals
all_goals = requests.get('http://web-api:4000/goals/all').json()

# Filter ON ICE goals
on_ice_goals = [goal for goal in all_goals if goal.get('status') == 'ON ICE']

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
    # st.write("### ❄️ On Ice Goals")

    # for goal in on_ice_goals:
    #     goal_id = goal['id']
    #     title = goal['title']
    #     notes = goal.get('notes', '')

    #     with st.container():
    #         # Optional: smaller layout
    #         col_checkbox, col_text = st.columns([1, 4])

    #         with col_checkbox:
    #             # Checkbox to optionally mark as complete
    #             checked = st.checkbox("", key=f"onice_{goal_id}")
    #             if checked:
    #                 try:
    #                     response = requests.put(f"http://web-api:4000/goals/goals/{goal_id}/complete")
    #                     if response.status_code == 200:
    #                         st.success("Goal moved to archived!")
    #                         st.experimental_rerun()  # refresh so it disappears
    #                     else:
    #                         st.error(f"Error: {response.status_code}")
    #                 except Exception as e:
    #                     st.error(f"Error: {str(e)}")

    #         with col_text:
    #             st.write(f"**{title}**")
    #             if notes:
    #                 st.write(notes)

    #         st.write("---")
