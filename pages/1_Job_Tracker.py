import streamlit as st
import sys
from pathlib import Path
from datetime import date

sys.path.append(str(Path(__file__).parent.parent))

from database.database import get_connection


st.title("📋 Job Tracker")
st.write("Track jobs, applications, deadlines and their current status.")
st.divider()


# =========================
# Add New Job
# =========================

st.subheader("➕ Add New Job")

with st.form("add_job_form"):

    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input("Company *")
        role = st.text_input("Role *")
        location = st.text_input("Location")
        job_url = st.text_input("Job URL")

    with col2:
        date_found = st.date_input(
            "Date Found",
            value=date.today()
        )

        deadline = st.date_input(
            "Application Deadline",
            value=None
        )

        status = st.selectbox(
            "Status",
            [
                "Saved",
                "Applied",
                "Assessment",
                "Interview",
                "Offer",
                "Rejected",
                "Withdrawn",
                "No Response"
            ]
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"],
            index=1
        )

    job_description = st.text_area("Job Description")
    notes = st.text_area("Notes")

    submitted = st.form_submit_button(
        "💾 Save Job",
        type="primary"
    )

    if submitted:

        if not company or not role:
            st.error("Company and Role are required.")

        else:

            connection = get_connection()

            cursor = connection.execute(
                """
                INSERT INTO jobs (
                    company,
                    role,
                    location,
                    job_url,
                    job_description,
                    date_found,
                    deadline,
                    status,
                    priority,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    company,
                    role,
                    location,
                    job_url,
                    job_description,
                    str(date_found),
                    str(deadline) if deadline else None,
                    status,
                    priority,
                    notes
                )
            )

            job_id = cursor.lastrowid

            connection.commit()
            connection.close()

            st.success(
                f"✅ Job saved successfully! Job ID: {job_id}"
            )


st.divider()


# =========================
# Saved Jobs
# =========================

st.subheader("📌 Saved Jobs")

connection = get_connection()

jobs = connection.execute(
    """
    SELECT *
    FROM jobs
    ORDER BY id DESC
    """
).fetchall()

connection.close()


if not jobs:

    st.info("No jobs added yet.")

else:

    st.write(f"**Total Jobs: {len(jobs)}**")

    for job in jobs:

        with st.expander(
            f"🏢 {job['company']} — {job['role']} | "
            f"{job['status']} | {job['priority']}"
        ):

            # =========================
            # Job Information
            # =========================

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**Company**")
                st.write(job["company"])

            with col2:
                st.write("**Role**")
                st.write(job["role"])

            with col3:
                st.write("**Location**")
                st.write(
                    job["location"] or "Not specified"
                )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**Status**")
                st.write(job["status"])

            with col2:
                st.write("**Priority**")
                st.write(job["priority"])

            with col3:
                st.write("**Date Found**")
                st.write(
                    job["date_found"] or "Not specified"
                )

            if job["deadline"]:
                st.write(
                    "**Application Deadline:**",
                    job["deadline"]
                )

            if job["job_url"]:
                st.write(
                    "**Job URL:**",
                    job["job_url"]
                )

            if job["notes"]:
                st.write(
                    "**Notes:**",
                    job["notes"]
                )

            st.divider()


            # =========================
            # Update Job
            # =========================

            st.write("### 🔄 Update Job")

            status_options = [
                "Saved",
                "Applied",
                "Assessment",
                "Interview",
                "Offer",
                "Rejected",
                "Withdrawn",
                "No Response"
            ]

            priority_options = [
                "Low",
                "Medium",
                "High"
            ]

            with st.form(
                f"update_job_{job['id']}"
            ):

                new_status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(
                        job["status"]
                    )
                )

                new_priority = st.selectbox(
                    "Priority",
                    priority_options,
                    index=priority_options.index(
                        job["priority"]
                    )
                )

                update_button = st.form_submit_button(
                    "Update Job"
                )

                if update_button:

                    connection = get_connection()

                    connection.execute(
                        """
                        UPDATE jobs
                        SET status = ?,
                            priority = ?
                        WHERE id = ?
                        """,
                        (
                            new_status,
                            new_priority,
                            job["id"]
                        )
                    )

                    connection.commit()
                    connection.close()

                    st.success(
                        "✅ Job updated successfully!"
                    )

                    st.rerun()


            # =========================
            # Application Details
            # =========================

            if job["status"] in [
                "Applied",
                "Assessment",
                "Interview",
                "Offer",
                "Rejected",
                "Withdrawn",
                "No Response"
            ]:

                st.divider()
                st.write("### 📝 Application Details")

                connection = get_connection()

                application = connection.execute(
                    """
                    SELECT *
                    FROM applications
                    WHERE job_id = ?
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (job["id"],)
                ).fetchone()

                resumes = connection.execute(
                    """
                    SELECT id, resume_name
                    FROM resumes
                    ORDER BY id DESC
                    """
                ).fetchall()

                connection.close()


                # =========================
                # Existing Application
                # =========================

                if application:

                    st.success(
                        "✅ Application details recorded"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write("**Application Date**")
                        st.write(
                            application["application_date"]
                            or "Not specified"
                        )

                    with col2:

                        st.write("**Resume Used**")
                        st.write(
                            application["resume_used"]
                            or "Not specified"
                        )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write("**Application Status**")
                        st.write(
                            application["status"]
                            or "Not specified"
                        )

                    with col2:

                        st.write("**Follow-up Date**")
                        st.write(
                            application["follow_up_date"]
                            or "Not specified"
                        )

                    if application["notes"]:

                        st.write(
                            "**Application Notes:**"
                        )

                        st.write(
                            application["notes"]
                        )


                    # =========================
                    # Edit Application
                    # =========================

                    st.write("#### ✏️ Edit Application")

                    resume_names = [
                        resume["resume_name"]
                        for resume in resumes
                    ]

                    application_status_options = [
                        "Applied",
                        "Assessment",
                        "Interview",
                        "Offer",
                        "Rejected",
                        "Withdrawn",
                        "No Response"
                    ]


                    with st.form(
                        f"edit_application_{application['id']}"
                    ):

                        # Application date
                        try:
                            current_application_date = date.fromisoformat(
                                application["application_date"]
                            )
                        except:
                            current_application_date = date.today()


                        edited_application_date = st.date_input(
                            "Application Date",
                            value=current_application_date
                        )


                        # Resume
                        if resume_names:

                            current_resume = application["resume_used"]

                            if current_resume in resume_names:

                                resume_index = resume_names.index(
                                    current_resume
                                )

                            else:

                                resume_index = 0


                            edited_resume = st.selectbox(
                                "Resume Used",
                                resume_names,
                                index=resume_index
                            )

                        else:

                            edited_resume = None

                            st.warning(
                                "No resumes available."
                            )


                        # Status
                        current_application_status = (
                            application["status"]
                            if application["status"]
                            in application_status_options
                            else "Applied"
                        )

                        status_index = (
                            application_status_options.index(
                                current_application_status
                            )
                        )

                        edited_application_status = st.selectbox(
                            "Application Status",
                            application_status_options,
                            index=status_index
                        )


                        # Follow-up date
                        current_followup = (
                            application["follow_up_date"]
                        )

                        if current_followup:

                            try:

                                current_followup_date = (
                                    date.fromisoformat(
                                        current_followup
                                    )
                                )

                            except:

                                current_followup_date = None

                        else:

                            current_followup_date = None


                        edited_followup_date = st.date_input(
                            "Follow-up Date",
                            value=current_followup_date
                        )


                        # Notes
                        edited_notes = st.text_area(
                            "Application Notes",
                            value=application["notes"] or ""
                        )


                        update_application = st.form_submit_button(
                            "💾 Update Application",
                            type="primary"
                        )


                        if update_application:

                            connection = get_connection()

                            connection.execute(
                                """
                                UPDATE applications
                                SET
                                    application_date = ?,
                                    resume_used = ?,
                                    status = ?,
                                    follow_up_date = ?,
                                    notes = ?
                                WHERE id = ?
                                """,
                                (
                                    str(
                                        edited_application_date
                                    ),

                                    edited_resume,

                                    edited_application_status,

                                    str(
                                        edited_followup_date
                                    )
                                    if edited_followup_date
                                    else None,

                                    edited_notes,

                                    application["id"]
                                )
                            )

                            connection.commit()
                            connection.close()

                            st.success(
                                "✅ Application updated successfully!"
                            )

                            st.rerun()


                # =========================
                # New Application
                # =========================

                else:

                    st.info(
                        "No application details recorded yet."
                    )

                    st.write(
                        "#### ➕ Add Application Details"
                    )

                    resume_names = [
                        resume["resume_name"]
                        for resume in resumes
                    ]

                    with st.form(
                        f"application_form_{job['id']}"
                    ):

                        application_date = st.date_input(
                            "Application Date",
                            value=date.today()
                        )


                        if resume_names:

                            selected_resume = st.selectbox(
                                "Resume Used",
                                resume_names
                            )

                        else:

                            selected_resume = None

                            st.warning(
                                "No resume found. "
                                "Upload a resume in Resume Manager first."
                            )


                        application_status = st.selectbox(
                            "Application Status",
                            [
                                "Applied",
                                "Assessment",
                                "Interview",
                                "Offer",
                                "Rejected",
                                "Withdrawn",
                                "No Response"
                            ]
                        )


                        follow_up_date = st.date_input(
                            "Follow-up Date",
                            value=None
                        )


                        application_notes = st.text_area(
                            "Application Notes"
                        )


                        save_application = st.form_submit_button(
                            "💾 Save Application Details",
                            type="primary"
                        )


                        if save_application:

                            if not resumes:

                                st.error(
                                    "Please upload a resume before "
                                    "saving application details."
                                )

                            else:

                                connection = get_connection()

                                connection.execute(
                                    """
                                    INSERT INTO applications (
                                        job_id,
                                        application_date,
                                        resume_used,
                                        status,
                                        follow_up_date,
                                        notes
                                    )
                                    VALUES (?, ?, ?, ?, ?, ?)
                                    """,
                                    (
                                        job["id"],
                                        str(application_date),
                                        selected_resume,
                                        application_status,
                                        str(follow_up_date)
                                        if follow_up_date
                                        else None,
                                        application_notes
                                    )
                                )

                                connection.commit()
                                connection.close()

                                st.success(
                                    "✅ Application details saved!"
                                )

                                st.rerun()