
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from database.database import get_connection

from services.resume_service import extract_docx_text

from services.ai_service import (
    match_resume_to_job,
    parse_match_result
)


st.title("🎯 Resume ↔ Job Matcher")

st.write(
    "Compare your resume against an analyzed job description "
    "and identify your strengths, missing skills and improvement areas."
)

st.divider()


# =============================
# SELECT JOB
# =============================

st.subheader("💼 Select Job")

connection = get_connection()

jobs = connection.execute(
    """
    SELECT DISTINCT
        jobs.id,
        jobs.company,
        jobs.role
    FROM jobs
    INNER JOIN job_analyses
        ON jobs.id = job_analyses.job_id
    ORDER BY jobs.id DESC
    """
).fetchall()

connection.close()


if not jobs:

    st.warning(
        "No analyzed jobs found. Analyze a job description first."
    )

    st.stop()


job_options = {
    f"{job['company']} - {job['role']}": job["id"]
    for job in jobs
}

selected_job = st.selectbox(
    "Select an analyzed job",
    list(job_options.keys())
)

job_id = job_options[selected_job]


# =============================
# SELECT RESUME
# =============================

st.subheader("📄 Select Resume")

connection = get_connection()

resumes = connection.execute(
    """
    SELECT
        id,
        resume_name,
        target_role,
        file_path
    FROM resumes
    ORDER BY id DESC
    """
).fetchall()

connection.close()


if not resumes:

    st.warning(
        "No resumes found. Upload a resume in Resume Manager first."
    )

    st.stop()


resume_options = {
    f"{resume['resume_name']} ({resume['target_role']})":
        resume["id"]
    for resume in resumes
}

selected_resume = st.selectbox(
    "Select a resume",
    list(resume_options.keys())
)

resume_id = resume_options[selected_resume]


st.divider()


# =============================
# MATCH RESUME
# =============================

if st.button("🎯 Analyze Resume Match"):

    connection = get_connection()

    job_analysis = connection.execute(
        """
        SELECT *
        FROM job_analyses
        WHERE job_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (job_id,)
    ).fetchone()

    resume = connection.execute(
        """
        SELECT *
        FROM resumes
        WHERE id = ?
        """,
        (resume_id,)
    ).fetchone()

    connection.close()


    if not job_analysis:

        st.error(
            "No AI analysis found for this job."
        )

    elif not resume:

        st.error(
            "Resume could not be found."
        )

    else:

        resume_path = Path(resume["file_path"])

        if not resume_path.exists():

            st.error(
                "Resume file could not be found."
            )

        else:

            with st.spinner(
                "🤖 AI is comparing your resume with the job..."
            ):

                try:

                    resume_text = extract_docx_text(
                        resume_path
                    )

                    raw_result = match_resume_to_job(
                        resume_text,
                        dict(job_analysis)
                    )

                    parsed_result = parse_match_result(
                        raw_result
                    )

                    st.session_state[
                        "resume_match_result"
                    ] = raw_result

                    st.session_state[
                        "parsed_match_result"
                    ] = parsed_result


                    # =============================
                    # SAVE MATCH RESULT
                    # =============================

                    connection = get_connection()

                    connection.execute(
                        """
                        INSERT INTO resume_matches (
                            job_id,
                            resume_id,
                            match_score,
                            matched_skills,
                            missing_skills,
                            matched_keywords,
                            missing_keywords,
                            experience_match,
                            education_match,
                            responsibility_match,
                            recommendations,
                            match_date
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            job_id,
                            resume_id,
                            parsed_result["match_score"],
                            parsed_result["matched_skills"],
                            parsed_result["missing_skills"],
                            parsed_result["matched_keywords"],
                            parsed_result["missing_keywords"],
                            parsed_result["experience_match"],
                            parsed_result["education_match"],
                            parsed_result["responsibility_match"],
                            parsed_result["recommendations"],
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        )
                    )

                    connection.commit()
                    connection.close()

                    st.success(
                        "✅ Resume matching completed!"
                    )

                except Exception as e:

                    st.error(
                        f"Matching failed: {e}"
                    )


# =============================
# DISPLAY RESULT
# =============================

if "parsed_match_result" in st.session_state:

    result = st.session_state[
        "parsed_match_result"
    ]

    st.divider()

    st.subheader("🎯 Resume Match Results")


    # =============================
    # MATCH SCORE
    # =============================

    score_text = (
        result["match_score"]
        .replace("%", "")
        .strip()
    )

    try:

        score = int(score_text)

    except ValueError:

        score = 0


    st.metric(
        "🎯 Match Score",
        f"{score}%"
    )

    st.progress(
        score / 100
    )


    st.divider()


    # =============================
    # SKILLS
    # =============================

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("✅ Matched Skills")

        st.write(
            result["matched_skills"]
        )


    with col2:

        st.subheader("⚠️ Missing Skills")

        st.write(
            result["missing_skills"]
        )


    st.divider()


    # =============================
    # KEYWORDS
    # =============================

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("🔑 Matched Keywords")

        st.write(
            result["matched_keywords"]
        )


    with col2:

        st.subheader("❌ Missing Keywords")

        st.write(
            result["missing_keywords"]
        )


    st.divider()


    # =============================
    # EXPERIENCE & EDUCATION
    # =============================

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("💼 Experience Match")

        st.write(
            result["experience_match"]
        )


    with col2:

        st.subheader("🎓 Education Match")

        st.write(
            result["education_match"]
        )


    st.divider()


    # =============================
    # RESPONSIBILITY MATCH
    # =============================

    st.subheader(
        "📋 Responsibility Match"
    )

    st.write(
        result["responsibility_match"]
    )


    st.divider()


    # =============================
    # RECOMMENDATIONS
    # =============================

    st.subheader(
        "💡 Resume Improvement Recommendations"
    )

    st.write(
        result["recommendations"]
    )
