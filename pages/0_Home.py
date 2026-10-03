import streamlit as st
import sys
from pathlib import Path
from datetime import date, timedelta

sys.path.append(str(Path(__file__).parent.parent))

from database.database import get_connection


# =========================
# Page Header
# =========================

st.title("💼 Job Hunt AI")
st.subheader("Personal AI Job Hunt Assistant")

st.write(
    "Track jobs, applications, resumes, skills, "
    "certifications and interview preparation."
)

st.divider()


# =========================
# Database Connection
# =========================

connection = get_connection()


# =========================
# Job Statistics
# =========================

total_jobs = connection.execute(
    "SELECT COUNT(*) FROM jobs"
).fetchone()[0]

applied_jobs = connection.execute(
    "SELECT COUNT(*) FROM jobs WHERE status = 'Applied'"
).fetchone()[0]

interview_jobs = connection.execute(
    "SELECT COUNT(*) FROM jobs WHERE status = 'Interview'"
).fetchone()[0]

offer_jobs = connection.execute(
    "SELECT COUNT(*) FROM jobs WHERE status = 'Offer'"
).fetchone()[0]

pending_jobs = connection.execute(
    """
    SELECT COUNT(*)
    FROM jobs
    WHERE status IN ('Saved', 'Applied', 'Assessment')
    """
).fetchone()[0]


# =========================
# Application Statistics
# =========================

total_applications = connection.execute(
    """
    SELECT COUNT(*)
    FROM applications
    """
).fetchone()[0]


today = date.today()
week_start = today - timedelta(days=today.weekday())

applications_this_week = connection.execute(
    """
    SELECT COUNT(*)
    FROM applications
    WHERE application_date >= ?
    """,
    (str(week_start),)
).fetchone()[0]


# =========================
# Upcoming Follow-ups
# =========================

upcoming_followups = connection.execute(
    """
    SELECT COUNT(*)
    FROM applications
    WHERE follow_up_date IS NOT NULL
    AND follow_up_date >= ?
    AND follow_up_date <= ?
    """,
    (
        str(today),
        str(today + timedelta(days=7))
    )
).fetchone()[0]


# =========================
# Main Metrics
# =========================

st.subheader("📊 Job Hunt Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Jobs",
        total_jobs
    )

with col2:
    st.metric(
        "Applications",
        total_applications
    )

with col3:
    st.metric(
        "Interviews",
        interview_jobs
    )

with col4:
    st.metric(
        "Offers",
        offer_jobs
    )


# =========================
# Application Metrics
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📝 Applied Jobs",
        applied_jobs
    )

with col2:
    st.metric(
        "📅 Applications This Week",
        applications_this_week
    )

with col3:
    st.metric(
        "🔔 Follow-ups Next 7 Days",
        upcoming_followups
    )

with col4:
    st.metric(
        "⏳ Jobs Needing Attention",
        pending_jobs
    )


st.divider()


# =========================
# Application Status
# =========================

statuses = [
    "Saved",
    "Applied",
    "Assessment",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn",
    "No Response"
]

status_counts = {}

for status in statuses:

    count = connection.execute(
        """
        SELECT COUNT(*)
        FROM jobs
        WHERE status = ?
        """,
        (status,)
    ).fetchone()[0]

    status_counts[status] = count


st.subheader("📈 Application Status")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💾 Saved",
        status_counts["Saved"]
    )

    st.metric(
        "📝 Applied",
        status_counts["Applied"]
    )

with col2:

    st.metric(
        "🧪 Assessment",
        status_counts["Assessment"]
    )

    st.metric(
        "🎤 Interview",
        status_counts["Interview"]
    )

with col3:

    st.metric(
        "🎉 Offer",
        status_counts["Offer"]
    )

    st.metric(
        "❌ Rejected",
        status_counts["Rejected"]
    )

with col4:

    st.metric(
        "↩️ Withdrawn",
        status_counts["Withdrawn"]
    )

    st.metric(
        "📭 No Response",
        status_counts["No Response"]
    )


st.divider()


# =========================
# Upcoming Follow-ups
# =========================

st.subheader("🔔 Upcoming Follow-ups")

followups = connection.execute(
    """
    SELECT
        applications.id,
        applications.application_date,
        applications.follow_up_date,
        applications.resume_used,
        applications.status,
        jobs.company,
        jobs.role
    FROM applications
    JOIN jobs
        ON applications.job_id = jobs.id
    WHERE applications.follow_up_date IS NOT NULL
    AND applications.follow_up_date >= ?
    AND applications.follow_up_date <= ?
    ORDER BY applications.follow_up_date ASC
    """,
    (
        str(today),
        str(today + timedelta(days=7))
    )
).fetchall()


if followups:

    for followup in followups:

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.write("**Company**")
                st.write(followup["company"])

            with col2:
                st.write("**Role**")
                st.write(followup["role"])

            with col3:
                st.write("**Follow-up Date**")
                st.write(followup["follow_up_date"])

            with col4:
                st.write("**Status**")
                st.write(followup["status"])

else:

    st.info(
        "No follow-ups scheduled for the next 7 days."
    )


st.divider()


# =========================
# Recent Applications
# =========================

st.subheader("📝 Recent Applications")

recent_applications = connection.execute(
    """
    SELECT
        applications.id,
        applications.application_date,
        applications.resume_used,
        applications.status,
        applications.follow_up_date,
        jobs.company,
        jobs.role,
        jobs.location
    FROM applications
    JOIN jobs
        ON applications.job_id = jobs.id
    ORDER BY applications.id DESC
    LIMIT 5
    """
).fetchall()


if recent_applications:

    for application in recent_applications:

        with st.container(border=True):

            col1, col2, col3, col4, col5 = st.columns(
                [1.5, 2, 1.5, 1.5, 1.5]
            )

            with col1:
                st.write("**Company**")
                st.write(application["company"])

            with col2:
                st.write("**Role**")
                st.write(application["role"])

            with col3:
                st.write("**Applied On**")
                st.write(
                    application["application_date"]
                    or "N/A"
                )

            with col4:
                st.write("**Status**")
                st.write(
                    application["status"]
                    or "N/A"
                )

            with col5:
                st.write("**Resume Used**")
                st.write(
                    application["resume_used"]
                    or "N/A"
                )

else:

    st.info(
        "No applications recorded yet."
    )


st.divider()


# =========================
# Recent Jobs
# =========================

st.subheader("🕐 Recent Jobs")

recent_jobs = connection.execute(
    """
    SELECT
        company,
        role,
        location,
        status,
        priority,
        date_found
    FROM jobs
    ORDER BY id DESC
    LIMIT 5
    """
).fetchall()


if recent_jobs:

    for job in recent_jobs:

        with st.container(border=True):

            col1, col2, col3, col4, col5, col6 = st.columns(
                [1.5, 2, 1.5, 1.2, 1.2, 1.2]
            )

            with col1:
                st.write("**Company**")
                st.write(job["company"])

            with col2:
                st.write("**Role**")
                st.write(job["role"])

            with col3:
                st.write("**Location**")
                st.write(
                    job["location"]
                    or "Not specified"
                )

            with col4:
                st.write("**Status**")
                st.write(job["status"])

            with col5:
                st.write("**Priority**")
                st.write(job["priority"])

            with col6:
                st.write("**Date Found**")
                st.write(
                    job["date_found"]
                    or "N/A"
                )

else:

    st.info(
        "No jobs added yet."
    )


st.divider()


# =========================
# Resume & AI Activity
# =========================

resume_count = connection.execute(
    """
    SELECT COUNT(*)
    FROM resumes
    """
).fetchone()[0]

analysis_count = connection.execute(
    """
    SELECT COUNT(*)
    FROM job_analyses
    """
).fetchone()[0]

match_count = connection.execute(
    """
    SELECT COUNT(*)
    FROM resume_matches
    """
).fetchone()[0]

interview_count = connection.execute(
    """
    SELECT COUNT(*)
    FROM interview_preparations
    """
).fetchone()[0]


connection.close()


st.subheader("🤖 Resume & AI Activity")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📄 Resumes",
        resume_count
    )

with col2:

    st.metric(
        "🔍 JD Analyses",
        analysis_count
    )

with col3:

    st.metric(
        "🎯 Resume Matches",
        match_count
    )

with col4:

    st.metric(
        "🎤 Interview Preps",
        interview_count
    )


st.divider()


# =========================
# Quick Overview
# =========================

st.subheader("🚀 Quick Overview")

col1, col2, col3 = st.columns(3)

with col1:

    st.write("📋 **Job Tracker**")

    st.write(
        "Track jobs, applications, deadlines, "
        "statuses and follow-ups."
    )


with col2:

    st.write("🤖 **AI Job Analysis**")

    st.write(
        "Analyze job descriptions and identify "
        "important skills and requirements."
    )


with col3:

    st.write("🎯 **Resume Matching**")

    st.write(
        "Compare your resume with job requirements "
        "using AI."
    )


st.divider()

st.success(
    "✅ Database connected successfully!"
)