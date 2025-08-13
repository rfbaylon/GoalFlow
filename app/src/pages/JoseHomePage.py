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
st.title("🛠️ GOOD MORNING, JOSE!")
st.write("*System Administrator Dashboard*")

# Create main layout: left column (system issues) and right column (quick actions + charts)
col1, col2 = st.columns([2, 1])



with col1:
    st.write("### 🚨 SYSTEM PRIORITIES")

    bugs = requests.get('http://web-api:4000/support/bugs').json()
    bugs = [list(item.values()) for item in bugs]
    st.write("---")
    #0 - completed
    #1 - title
    #2 = id
    #3 - priority
    #4 - desc

    for bug in bugs:
        with st.container():
            
            bug_col1, bug_col2, bug_col3 = st.columns([2, 1, 1])
            with bug_col1:
                st.write(f":red[**{bug[1]}**]") #title
                st.write(bug[4]) #desc
            with bug_col2:
                priority = st.write(bug[3])
            with bug_col3:
                if bug[0] == 0:
                    st.write("Unfinished")
                if bug[0] == 1:
                    st.write("Completed")
                
        st.write("---")
    
    #USELESS RN -- MAYBE EDIT
    # Save changes button
    if st.button("💾 Save All Changes", type="secondary", use_container_width=True):
        st.success("✅ System priorities updated successfully!")
        # Here you could add API calls to save to database

with col2:
    # st.write("### ⚡ ADMIN ACTIONS")
    
    # # Action buttons in a 2x2 grid like the wireframe
    # action_col1, action_col2 = st.columns(2)
    
    # with action_col1:
    #     if st.button("🐛 Bug Reports", use_container_width=True):
    #         st.switch_page('pages/01_Bug_Reports.py')
    
    
    # st.write("---")
    
    # System Charts Section
    st.write("### 📊 App Statistics")
    userstats = requests.get('http://web-api:4000/users/appstats').json()
    userstats = [list(item.values()) for item in userstats]

    def make_userstats(data):
        df = pd.DataFrame(data, columns=['registration_date', 'user_id'])
        
        # Convert string dates to datetime
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        df['date'] = df['registration_date'].dt.date

        # User count
        df = df.sort_values('date').reset_index(drop=True)
        df['user_count'] = range(1, len(df) + 1)
    
        return df
    df = make_userstats(userstats)

    fig_users = px.line(df, x='date', y='user_count', title="User Growth Trends")
    fig_users.update_layout(height=200, showlegend=True, title_font_size=12, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_users, use_container_width=True)
    
    # # Bug status pie chart
    # bug_data = pd.DataFrame({
    #     'Status': ['Fixed', 'In Progress', 'Open', 'Testing'],
    #     'Count': [15, 8, 5, 3]
    # })
    
    # fig_bugs = px.pie(bug_data, values='Count', names='Status', 
    #                  title="Bug Report Status",
    #                  color_discrete_map={'Fixed': '#2ca02c', 
    #                                    'In Progress': '#ff7f0e', 
    #                                    'Open': '#d62728',
    #                                    'Testing': '#9467bd'})
    # fig_bugs.update_layout(height=200, title_font_size=12, 
    #                       margin=dict(l=0, r=0, t=30, b=0))
    # st.plotly_chart(fig_bugs, use_container_width=True)

# Bottom metrics section
# st.write("---")
# st.write("### 📈 SYSTEM METRICS")

# metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

# with metric_col1:
#     st.metric(
#         label="Total Users", 
#         value="2,100",
#         delta="180 new this month"
#     )

# with metric_col2:
#     st.metric(
#         label="Active Bug Reports", 
#         value="13",
#         delta="-5 resolved today"
#     )

# with metric_col3:
#     st.metric(
#         label="System Uptime", 
#         value="99.8%",
#         delta="0.2% improvement"
#     )

# with metric_col4:
#     st.metric(
#         label="User Satisfaction", 
#         value="4.6/5",
#         delta="0.3 increase"
#     )

# Action buttons at bottom
st.write("---")
bottom_col1, bottom_col2, bottom_col3 = st.columns(3)

with bottom_col1:
    if st.button("🚨 Reply To Bug Report", type="primary", use_container_width=True):
        st.switch_page('pages/Add_New_Post.py')

with bottom_col2:
    if st.button("🗑 Delete Post Reply", type="primary", use_container_width=True):
        st.switch_page('pages/Delete_Post.py')

with bottom_col3:
    if st.button("🏠 Return To Dashboard", type="primary", use_container_width=True):
        st.switch_page('HomePage.py')