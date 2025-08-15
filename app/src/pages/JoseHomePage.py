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
st.title("🛠️ Whats up, Jose?")

# Create main layout: left column (system issues) and right column (quick actions + charts)
col1, col2 = st.columns([2, 1])



with col1:
    st.write("### Uncompleted Bugs")

    bugs = requests.get('http://web-api:4000/support/bugs').json()
    bugs = [list(item.values()) for item in bugs]
    #0 - completed
    #1 - title
    #2 = id
    #3 - priority
    #4 - desc

    st.write("---")
    bug_col1, bug_col2, bug_col3 = st.columns([2, 1, 1])
    with bug_col1: st.write("**Bug**")
    with bug_col2: st.write("**Priority**")
    with bug_col3: st.write("**Completion**")
    st.write("---")

    for bug in bugs:
        with st.container():
            
            bug_col1, bug_col2, bug_col3 = st.columns([2, 1, 1])
            with bug_col1:
                st.write(f":red[**{bug[1]}**]") #title
                st.write(bug[4]) #desc
            with bug_col2:
                p = bug[3]
                if p == "critical":
                    st.markdown(f":red[**🔴 Critical!**]")
                elif p == "high":
                    st.markdown(f":orange[**🟠 High**]")
                elif p == "medium":
                    st.markdown("<span style='color:#DAA520'><strong>🟡 Medium</strong></span>", unsafe_allow_html=True)
                elif p == "low":
                    st.markdown(f":green[**🟢 Low**]")
                else:
                    st.write(p)
            with bug_col3:
                if bug[0] == 0:
                    if st.button("Mark Complete", key=f"complete_{bug[2]}"):
                        try:
                            response = requests.put(f'http://web-api:4000/support/bugs/{bug[2]}/complete')
                            if response.status_code == 200:
                                st.success("Bug marked as completed!")
                                st.rerun()  # Refresh the page to show updated status
                            else:
                                st.error(f"Error: {response.status_code}")
                        except Exception as e:
                            st.error(f"Error updating bug: {str(e)}")
            st.write("---")

        

with col2:
    
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
