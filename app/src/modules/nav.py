# modules/nav.py
# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator
# This file has function to add certain functionality to the left side bar of the app

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

def AboutPageNav():
    st.sidebar.page_link("pages/About.py", label="About", icon="🧠")

#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link("pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤")

def WorldBankVizNav():
    st.sidebar.page_link("pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦")

def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")

## ------------------------ Examples for Role of usaid_worker ------------------------
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")

def PredictionNav():
    st.sidebar.page_link("pages/11_Prediction.py", label="Regression Prediction", icon="📈")

def ClassificationNav():
    st.sidebar.page_link("pages/13_Classification.py", label="Classification Demo", icon="🌺")

def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")

def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")

#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link("pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢")

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home: bool = False):
    """
    Adds links to the sidebar based on the logged-in user's role.
    Uses safe defaults so missing session keys never crash the app.
    """

    # ---- Safe defaults (중요) ----
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("role", "guest")
    st.session_state.setdefault("user_id", None)

    role = st.session_state.get("role", "guest")
    is_auth = bool(st.session_state.get("authenticated", False))

    #st.sidebar.image("assets/logo.png", width=150)

    if show_home:
        HomeNav()

    # Role-based links 
    if is_auth:
        if role == "pol_strat_advisor":
            PolStratAdvHomeNav()
            WorldBankVizNav()
            MapDemoNav()

        if role == "usaid_worker":
            PredictionNav()
            ApiTestNav()
            ClassificationNav()
            NgoDirectoryNav()
            AddNgoNav()

        if role == "administrator":
            AdminPageNav()

    # Always show About
    AboutPageNav()

    # Logout 
    if is_auth:
        if st.sidebar.button("Logout"):
            for k in ("role", "authenticated", "user_id"):
                if k in st.session_state:
                    del st.session_state[k]
            st.switch_page("Home.py")
