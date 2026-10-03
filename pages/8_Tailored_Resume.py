import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from database.database import get_connection
from services.ai_service import generate_tailored_resume
from services.resume_service import extract_docx_text
from services.docx_service import create_resume_docx


st.title("✍️ AI Tailored Resume")
st.write("Generate a job-specific resume using your existing resume and job requirements.")

st.divider()


# -----------------------------
# Load Jobs
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
    st.warning("No resumes found. Upload a resume in Resume Manager first.")
    st.stop()


# -----------------------------
# Select Job and Resume
# -----------------------------

job_options = {
    f"{job['company']} — {job['role']}": job["id"]
    for job in jobs
}

resume_options = {
    f"{resume['resume_name']} — {resume['target_role'] or 'General'}": resume["id"]
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


job = next(j for j in jobs if j["id"] == job_id)
resume = next(r for r in resumes if r["id"] == resume_id)


st.divider()


# -----------------------------
# Generate Resume
# -----------------------------

if st.button("✨ Generate Tailored Resume", type="primary"):

    with st.spinner("AI is tailoring your resume..."):

        try:

            resume_text = extract_docx_text(
                resume["file_path"]
            )

            tailored_resume = generate_tailored_resume(
                resume_text,
                job["job_description"]
            )

            st.session_state["tailored_resume"] = tailored_resume

        except Exception as e:

            st.error(f"Error generating tailored resume: {e}")


# -----------------------------
# Display Result
# -----------------------------

if "tailored_resume" in st.session_state:

    st.divider()

    st.subheader("📄 Tailored Resume")

    st.text_area(
        "Generated Resume",
        st.session_state["tailored_resume"],
        height=700
    )

    st.divider()

    output_path = Path("data/tailored_resume.docx")

    create_resume_docx(
        st.session_state["tailored_resume"],
        output_path
    )

    with open(output_path, "rb") as file:

        st.download_button(
            label="📥 Download Tailored Resume (.docx)",
            data=file,
            file_name="Tailored_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )