import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from database.database import get_connection
from services.ai_service import analyze_job_description, parse_analysis


st.title("🤖 Job Description Analyzer")

st.write(
    "Analyze a job description using Gemini AI and organize the important requirements."
)

st.divider()


# =============================
# SELECT JOB
# =============================

st.subheader("📄 Job Description")

connection = get_connection()

jobs = connection.execute(
    """
    SELECT id, company, role
    FROM jobs
    ORDER BY id DESC
    """
).fetchall()

connection.close()


job_options = {
    "New Job Description": None
}

for job in jobs:

    job_options[
        f"{job['company']} - {job['role']}"
    ] = job["id"]


selected_job = st.selectbox(
    "Select an existing job or analyze a new description",
    list(job_options.keys())
)

job_id = job_options[selected_job]


job_description = st.text_area(
    "Paste Job Description",
    height=300,
    placeholder="Paste the complete job description here..."
)


# =============================
# AI ANALYSIS
# =============================

st.divider()

if st.button("🤖 Analyze with AI"):

    if not job_description.strip():

        st.error("Please enter a job description first.")

    else:

        with st.spinner(
            "🤖 Gemini is analyzing the job description..."
        ):

            try:

                ai_result = analyze_job_description(
                    job_description
                )

                parsed_result = parse_analysis(
                    ai_result
                )

                st.session_state["ai_result"] = ai_result
                st.session_state["parsed_result"] = parsed_result

                st.success(
                    "✅ Job description analyzed successfully!"
                )

            except Exception as e:

                st.error(
                    f"AI analysis failed: {e}"
                )


# =============================
# DISPLAY AI RESULT
# =============================

if "parsed_result" in st.session_state:

    result = st.session_state["parsed_result"]

    st.divider()

    st.subheader("🤖 AI Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.text_area(
            "Required Skills",
            value=result["required_skills"],
            height=120,
            key="required_skills_result"
        )

        st.text_area(
            "Experience Requirement",
            value=result["experience"],
            height=100,
            key="experience_result"
        )

        st.text_area(
            "Education Requirement",
            value=result["education"],
            height=100,
            key="education_result"
        )

    with col2:

        st.text_area(
            "Preferred Skills",
            value=result["preferred_skills"],
            height=120,
            key="preferred_skills_result"
        )

        st.text_area(
            "Important Keywords",
            value=result["keywords"],
            height=120,
            key="keywords_result"
        )

    st.text_area(
        "Key Responsibilities",
        value=result["responsibilities"],
        height=150,
        key="responsibilities_result"
    )


# =============================
# SAVE ANALYSIS
# =============================

st.divider()

st.subheader("💾 Save Analysis")

if st.button("💾 Save AI Analysis"):

    if "parsed_result" not in st.session_state:

        st.error(
            "Please analyze the job description with AI first."
        )

    else:

        result = st.session_state["parsed_result"]

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO job_analyses (
                job_id,
                job_description,
                required_skills,
                preferred_skills,
                experience,
                education,
                responsibilities,
                keywords,
                analysis_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_id,
                job_description,
                result["required_skills"],
                result["preferred_skills"],
                result["experience"],
                result["education"],
                result["responsibilities"],
                result["keywords"],
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        connection.commit()
        connection.close()

        st.success(
            "✅ AI analysis saved successfully!"
        )