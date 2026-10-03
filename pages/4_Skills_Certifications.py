import streamlit as st
import sys
from pathlib import Path
from datetime import date

sys.path.append(str(Path(__file__).parent.parent))

from database.database import get_connection


st.title("🧠 Skills & Certifications")

st.write(
    "Manage your technical skills and professional certifications."
)

st.divider()


# =============================
# SKILLS
# =============================

st.subheader("🛠️ Add Skill")

with st.form("skill_form"):

    skill_name = st.text_input(
        "Skill Name",
        placeholder="Python"
    )

    category = st.selectbox(
        "Category",
        [
            "Programming",
            "Data Analysis",
            "Database",
            "Machine Learning",
            "Visualization",
            "Cloud",
            "Tools",
            "Other"
        ]
    )

    proficiency = st.selectbox(
        "Proficiency",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    skill_submitted = st.form_submit_button(
        "➕ Add Skill"
    )


if skill_submitted:

    if not skill_name:

        st.error("Skill Name is required.")

    else:

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO skills (
                skill_name,
                category,
                proficiency
            )
            VALUES (?, ?, ?)
            """,
            (
                skill_name,
                category,
                proficiency
            )
        )

        connection.commit()
        connection.close()

        st.success(
            f"✅ {skill_name} added successfully!"
        )


st.divider()


# =============================
# CERTIFICATIONS
# =============================

st.subheader("🏆 Add Certification")

with st.form("certificate_form"):

    certificate_name = st.text_input(
        "Certificate Name",
        placeholder="Python for Data Science"
    )

    issuer = st.text_input(
        "Issuing Organization",
        placeholder="Example Organization"
    )

    issue_date = st.date_input(
        "Issue Date",
        value=date.today()
    )

    credential_url = st.text_input(
        "Credential URL"
    )

    certificate_file = st.file_uploader(
        "Upload Certificate",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    certificate_submitted = st.form_submit_button(
        "💾 Save Certification"
    )


if certificate_submitted:

    if not certificate_name:

        st.error("Certificate Name is required.")

    else:

        file_path = ""

        if certificate_file:

            certificate_folder = (
                Path(__file__).parent.parent / "certificates"
            )

            certificate_folder.mkdir(exist_ok=True)

            file_path = certificate_folder / certificate_file.name

            with open(file_path, "wb") as file:

                file.write(
                    certificate_file.getbuffer()
                )

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO certifications (
                certificate_name,
                issuer,
                issue_date,
                credential_url,
                file_path
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                certificate_name,
                issuer,
                str(issue_date),
                credential_url,
                str(file_path)
            )
        )

        connection.commit()
        connection.close()

        st.success(
            f"✅ {certificate_name} saved successfully!"
        )
st.divider()

st.subheader("📚 My Skills")

connection = get_connection()

skills = connection.execute(
    """
    SELECT id, skill_name, category, proficiency
    FROM skills
    ORDER BY id DESC
    """
).fetchall()

connection.close()


if skills:

    for skill in skills:

        col1, col2, col3 = st.columns([3, 2, 2])

        with col1:
            st.write(f"**{skill['skill_name']}**")

        with col2:
            st.write(skill["category"])

        with col3:
            st.write(skill["proficiency"])

else:

    st.info("No skills added yet.")
st.divider()

st.subheader("🏆 My Certifications")

connection = get_connection()

certifications = connection.execute(
    """
    SELECT
        id,
        certificate_name,
        issuer,
        issue_date,
        credential_url,
        file_path
    FROM certifications
    ORDER BY id DESC
    """
).fetchall()

connection.close()


if certifications:

    for certificate in certifications:

        with st.container(border=True):

            st.write(
                f"### 🏆 {certificate['certificate_name']}"
            )

            st.write(
                f"**Issuer:** {certificate['issuer']}"
            )

            st.write(
                f"**Issue Date:** {certificate['issue_date']}"
            )

            if certificate["credential_url"]:

                st.write(
                    f"🔗 Credential: "
                    f"{certificate['credential_url']}"
                )

            if certificate["file_path"]:

                file_path = Path(
                    certificate["file_path"]
                )

                if file_path.exists():

                    with open(file_path, "rb") as file:

                        st.download_button(
                            "⬇️ Download Certificate",
                            data=file,
                            file_name=file_path.name,
                            key=f"certificate_{certificate['id']}"
                        )

else:

    st.info("No certifications added yet.")