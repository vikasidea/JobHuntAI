import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from database.database import get_connection


st.title("👤 Master Profile")

st.write(
    "Store your professional information in one place. "
    "This profile will later be used for resume tailoring and job matching."
)

st.divider()

st.subheader("📝 Personal & Professional Information")

connection = get_connection()

profile = connection.execute(
    "SELECT * FROM profile WHERE id = 1"
).fetchone()

connection.close()


with st.form("master_profile_form"):

    name = st.text_input(
        "Full Name",
        value=profile["name"] if profile else ""
    )

    email = st.text_input(
        "Email",
        value=profile["email"] if profile else ""
    )

    phone = st.text_input(
        "Phone",
        value=profile["phone"] if profile else ""
    )

    location = st.text_input(
        "Location",
        value=profile["location"] if profile else ""
    )

    linkedin = st.text_input(
        "LinkedIn URL",
        value=profile["linkedin"] if profile else ""
    )

    github = st.text_input(
        "GitHub URL",
        value=profile["github"] if profile else ""
    )

    portfolio = st.text_input(
        "Portfolio URL",
        value=profile["portfolio"] if profile else ""
    )

    summary = st.text_area(
        "Professional Summary",
        value=profile["summary"] if profile else "",
        height=150
    )

    skills = st.text_area(
        "Skills",
        value=profile["skills"] if profile else "",
        placeholder="Python, SQL, Excel, Power BI, Machine Learning...",
        height=100
    )

    submitted = st.form_submit_button(
        "💾 Save Profile"
    )


if submitted:

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO profile (
            id,
            name,
            email,
            phone,
            location,
            linkedin,
            github,
            portfolio,
            summary,
            skills
        )
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            email = excluded.email,
            phone = excluded.phone,
            location = excluded.location,
            linkedin = excluded.linkedin,
            github = excluded.github,
            portfolio = excluded.portfolio,
            summary = excluded.summary,
            skills = excluded.skills
        """,
        (
            name,
            email,
            phone,
            location,
            linkedin,
            github,
            portfolio,
            summary,
            skills
        )
    )

    connection.commit()
    connection.close()

    st.success("✅ Master Profile saved successfully!")