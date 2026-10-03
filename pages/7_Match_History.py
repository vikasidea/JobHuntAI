import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from database.database import get_connection


st.title("📊 Match History")
st.write("View previous resume-to-job matching results.")

st.divider()


connection = get_connection()

matches = connection.execute(
    """
    SELECT
        resume_matches.id,
        jobs.company,
        jobs.role,
        jobs.location,
        resumes.resume_name,
        resume_matches.match_score,
        resume_matches.matched_skills,
        resume_matches.missing_skills,
        resume_matches.experience_match,
        resume_matches.education_match,
        resume_matches.responsibility_match,
        resume_matches.recommendations,
        resume_matches.match_date
    FROM resume_matches
    JOIN jobs
        ON resume_matches.job_id = jobs.id
    JOIN resumes
        ON resume_matches.resume_id = resumes.id
    ORDER BY resume_matches.id DESC
    """
).fetchall()

connection.close()


if not matches:
    st.info("No resume matches found yet.")

else:

    st.subheader(f"Total Matches: {len(matches)}")

    for match in matches:

        with st.expander(
            f"🎯 {match['company']} — {match['role']} | Match: {match['match_score']}"
        ):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**Company**")
                st.write(match["company"])

            with col2:
                st.write("**Role**")
                st.write(match["role"])

            with col3:
                st.write("**Resume**")
                st.write(match["resume_name"])

            st.write("**Location:**", match["location"] or "Not specified")
            st.write("**Match Date:**", match["match_date"])

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matched Skills")
                st.write(match["matched_skills"] or "None")

            with col2:
                st.subheader("❌ Missing Skills")
                st.write(match["missing_skills"] or "None")

            st.divider()

            st.subheader("💼 Experience Match")
            st.write(match["experience_match"] or "Not available")

            st.subheader("🎓 Education Match")
            st.write(match["education_match"] or "Not available")

            st.subheader("📋 Responsibility Match")
            st.write(match["responsibility_match"] or "Not available")

            st.subheader("💡 Recommendations")
            st.write(match["recommendations"] or "No recommendations")