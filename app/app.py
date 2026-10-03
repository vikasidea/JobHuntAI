import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from database.database import initialize_database


st.set_page_config(
    page_title="Job Hunt AI",
    page_icon="💼",
    layout="wide"
)

initialize_database()


home_page = st.Page(
    "../pages/0_Home.py",
    title="Home",
    icon="🏠"
)

job_tracker_page = st.Page(
    "../pages/1_Job_Tracker.py",
    title="Job Tracker",
    icon="📋"
)
master_profile_page = st.Page(
    "../pages/2_Master_Profile.py",
    title="Master Profile",
    icon="👤"
)
resume_manager_page = st.Page(
    "../pages/3_Resume_Manager.py",
    title="Resume Manager",
    icon="📄"
)
skills_certifications_page = st.Page(
    "../pages/4_Skills_Certifications.py",
    title="Skills & Certifications",
    icon="🧠"
)
jd_analyzer_page = st.Page(
    "../pages/5_JD_Analyzer.py",
    title="JD Analyzer",
    icon="🤖"
)
resume_matcher_page = st.Page(
    "../pages/6_Resume_Matcher.py",
    title="Resume Matcher",
    icon="🎯"
)
match_history_page = st.Page(
    "../pages/7_Match_History.py",
    title="Match History",
    icon="📊"
)
tailored_resume_page = st.Page(
    "../pages/8_Tailored_Resume.py",
    title="Tailored Resume",
    icon="✍️"
)
interview_prep_page = st.Page(
    "../pages/9_Interview_Preparation.py",
    title="Interview Preparation",
    icon="🎤"
)

pg = st.navigation(
    [
        home_page,
        job_tracker_page,
        master_profile_page,
        resume_manager_page,
        skills_certifications_page,
        jd_analyzer_page,
        resume_matcher_page,
        match_history_page,
        tailored_resume_page,
        interview_prep_page
    ]
)
pg.run()