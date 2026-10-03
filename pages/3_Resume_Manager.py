import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from database.database import get_connection


st.title("📄 Resume Manager")

st.write(
    "Manage different versions of your resume for different job roles."
)

st.divider()

st.subheader("➕ Add Resume")


with st.form("resume_form"):

    resume_name = st.text_input(
        "Resume Name",
        placeholder="Data Analyst Resume"
    )

    target_role = st.selectbox(
        "Target Role",
        [
            "Data Analyst",
            "Data Scientist",
            "Python Developer",
            "Software Developer",
            "Machine Learning Engineer",
            "Other"
        ]
    )

    description = st.text_area(
        "Description",
        placeholder="ATS resume focused on Python, SQL, Excel and Power BI."
    )

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    submitted = st.form_submit_button(
        "💾 Save Resume"
    )


if submitted:

    if not resume_name:
        st.error("Resume Name is required.")

    elif not uploaded_file:
        st.error("Please upload a PDF or DOCX resume.")

    else:

        resume_folder = (
            Path(__file__).parent.parent / "resumes"
        )

        resume_folder.mkdir(exist_ok=True)

        file_path = resume_folder / uploaded_file.name

        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO resumes (
                resume_name,
                target_role,
                file_path,
                description,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                resume_name,
                target_role,
                str(file_path),
                description,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        connection.commit()
        connection.close()

        st.success(
            f"✅ {resume_name} saved successfully!"
        )

st.divider()

st.subheader("📚 Resume Library")

connection = get_connection()

resumes = connection.execute(
    """
    SELECT
        id,
        resume_name,
        target_role,
        file_path,
        description,
        created_at
    FROM resumes
    ORDER BY id DESC
    """
).fetchall()

connection.close()


if resumes:

    for resume in resumes:

        with st.container(border=True):

            col1, col2 = st.columns([3, 2])

            with col1:

                st.write(f"### 📄 {resume['resume_name']}")

                st.write(
                    f"**Target Role:** {resume['target_role']}"
                )

                if resume["description"]:
                    st.write(resume["description"])

            with col2:

                st.write(
                    f"**Added:** {resume['created_at']}"
                )

                file_path = Path(resume["file_path"])

                if file_path.exists():

                    with open(file_path, "rb") as file:

                        st.download_button(
                            "⬇️ Download Resume",
                            data=file,
                            file_name=file_path.name,
                            key=f"download_{resume['id']}"
                        )

else:

    st.info("No resumes uploaded yet.")