import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from database.database import get_connection
from services.ai_service import generate_interview_preparation
from services.resume_service import extract_docx_text


st.title("🎤 Interview Preparation")
st.write(
    "Generate personalized interview questions and sample answers "
    "based on your resume and the selected job."
)

st.divider()


# -----------------------------
# Load Jobs and Resumes
# -----------------------------

connection = get_connection()

jobs = connection.execute(
    """
    SELECT id, company, role, job_description
    FROM jobs
    WHERE job_description IS NOT NULL
    AND job_description != ''
    ORDER BY id DESC
    """
).fetchall()

resumes = connection.execute(
    """
    SELECT id, resume_name, file_path, target_role
    FROM resumes
    ORDER BY id DESC
    """
).fetchall()

connection.close()


if not jobs:
    st.warning("No jobs with job descriptions found.")
    st.stop()

if not resumes:
    st.warning("No resumes found. Upload a resume first.")
    st.stop()


# -----------------------------
# Selection
# -----------------------------

job_options = {
    f"{job['company']} — {job['role']}": job["id"]
    for job in jobs
}

resume_options = {
    f"{resume['resume_name']} — {resume['target_role'] or 'General'}":
    resume["id"]
    for resume in resumes
}


selected_job = st.selectbox(
    "Select Job",
    list(job_options.keys())
)

selected_resume = st.selectbox(
    "Select Resume",
    list(resume_options.keys())
)


job_id = job_options[selected_job]
resume_id = resume_options[selected_resume]


job = next(
    j for j in jobs
    if j["id"] == job_id
)

resume = next(
    r for r in resumes
    if r["id"] == resume_id
)


st.divider()


# -----------------------------
# Generate Interview Preparation
# -----------------------------

if st.button(
    "🎤 Generate Interview Preparation",
    type="primary"
):

    with st.spinner(
        "AI is preparing your interview questions..."
    ):

        try:

            resume_text = extract_docx_text(
                resume["file_path"]
            )

            interview_result = generate_interview_preparation(
                resume_text,
                job["job_description"]
            )

            # Store result in Streamlit session
            st.session_state[
                "interview_preparation"
            ] = interview_result

            # Save result to database
            connection = get_connection()

            connection.execute(
                """
                INSERT INTO interview_preparations (
                    job_id,
                    resume_id,
                    preparation,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    job_id,
                    resume_id,
                    interview_result,
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            )

            connection.commit()
            connection.close()

            st.success(
                "✅ Interview preparation generated and saved!"
            )

        except Exception as e:

            st.error(
                f"Error generating interview preparation: {e}"
            )


# -----------------------------
# Display Result
# -----------------------------

if "interview_preparation" in st.session_state:

    st.divider()

    st.subheader("🎯 Your Interview Preparation")

    st.text_area(
        "AI Generated Preparation",
        st.session_state["interview_preparation"],
        height=900
    )