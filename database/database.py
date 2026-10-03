import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "jobhunt.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            job_url TEXT,
            job_description TEXT,
            date_found TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'Saved',
            priority TEXT DEFAULT 'Medium',
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            application_date TEXT,
            resume_used TEXT,
            status TEXT DEFAULT 'Applied',
            interview_date TEXT,
            follow_up_date TEXT,
            notes TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            location TEXT,
            linkedin TEXT,
            github TEXT,
            portfolio TEXT,
            summary TEXT,
            skills TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT NOT NULL,
            target_role TEXT,
            file_path TEXT,
            description TEXT,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            category TEXT,
            proficiency TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            certificate_name TEXT NOT NULL,
            issuer TEXT,
            issue_date TEXT,
            credential_url TEXT,
            file_path TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            job_description TEXT NOT NULL,
            required_skills TEXT,
            preferred_skills TEXT,
            experience TEXT,
            education TEXT,
            responsibilities TEXT,
            keywords TEXT,
            analysis_date TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            resume_id INTEGER NOT NULL,
            match_score TEXT,
            matched_skills TEXT,
            missing_skills TEXT,
            matched_keywords TEXT,
            missing_keywords TEXT,
            experience_match TEXT,
            education_match TEXT,
            responsibility_match TEXT,
            recommendations TEXT,
            match_date TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs(id),
            FOREIGN KEY (resume_id) REFERENCES resumes(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_preparations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            resume_id INTEGER NOT NULL,
            preparation TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs(id),
            FOREIGN KEY (resume_id) REFERENCES resumes(id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")