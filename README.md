# 💼 JobHuntAI

### AI-Powered Job Search & Application Assistant

JobHuntAI is a personal AI-powered job management platform built with **Python, Streamlit, SQLite, and Google Gemini API**.

It helps job seekers manage their job search from tracking opportunities to analyzing job descriptions, matching resumes, generating tailored resumes, and preparing for interviews.

---

## 🚀 Features

### 📋 Job & Application Tracker

* Add and manage job opportunities
* Track company, role, location, and job URL
* Track application status
* Set job priority
* Store application deadlines
* Record application dates
* Track the resume used for each application
* Schedule follow-up dates
* Add application notes
* Edit application details

### 👤 Master Profile

Maintain a centralized professional profile containing:

* Name
* Email
* Phone
* Location
* LinkedIn
* GitHub
* Portfolio
* Professional summary
* Skills

### 📄 Resume Manager

* Upload multiple resumes
* Store resumes for different target roles
* Support DOCX resumes
* Download stored resumes
* Reuse resumes for job matching and interview preparation

### 🧠 Skills & Certifications

* Manage technical skills
* Categorize skills
* Track proficiency
* Store certifications
* Store certification issuer and issue date
* Store credential URLs
* Upload certificate files

### 🤖 AI Job Description Analyzer

Uses Google Gemini to analyze job descriptions and identify:

* Required skills
* Preferred skills
* Experience requirements
* Education requirements
* Responsibilities
* Important keywords

### 🎯 AI Resume Matcher

Compare a resume against a selected job description and generate:

* Resume match score
* Matched skills
* Missing skills
* Matched keywords
* Missing keywords
* Experience match
* Education match
* Responsibility match
* Improvement recommendations

### 📊 Match History

Stores previous resume-to-job matching results so previous analyses can be reviewed later.

### ✍️ AI Tailored Resume Generator

Generates a job-specific resume based on:

* Existing resume
* Selected job description
* Job requirements

The generated resume can also be exported as a DOCX file.

### 🎤 AI Interview Preparation

Generates personalized interview preparation based on:

* Candidate resume
* Selected job description

The system generates:

* Resume-based interview questions
* Technical questions
* Job-specific questions
* Interview preparation guidance

### 🏠 Dashboard

The dashboard provides an overview of:

* Total jobs
* Applications
* Interviews
* Offers
* Application status
* Upcoming follow-ups
* Recent applications
* Recent jobs
* Resume activity
* AI analysis activity
* Resume matching activity
* Interview preparation activity

---

# 🛠️ Tech Stack

| Technology        | Purpose                               |
| ----------------- | ------------------------------------- |
| Python            | Application development               |
| Streamlit         | Web application interface             |
| SQLite            | Local database                        |
| Google Gemini API | AI-powered analysis and generation    |
| Google GenAI SDK  | Gemini API integration                |
| python-docx       | DOCX resume processing and generation |
| python-dotenv     | Environment variable management       |

---

# 🏗️ Project Architecture

```text
JobHuntAI/
│
├── app/
│   └── app.py
│
├── database/
│   └── database.py
│
├── pages/
│   ├── 0_Home.py
│   ├── 1_Job_Tracker.py
│   ├── 2_Master_Profile.py
│   ├── 3_Resume_Manager.py
│   ├── 4_Skills_Certifications.py
│   ├── 5_JD_Analyzer.py
│   ├── 6_Resume_Matcher.py
│   ├── 7_Match_History.py
│   ├── 8_Tailored_Resume.py
│   └── 9_Interview_Preparation.py
│
├── services/
│   ├── ai_service.py
│   ├── docx_service.py
│   └── resume_service.py
│
├── assets/
│   └── screenshots/
│       ├── dashboard.png
│       ├── job_tracker.png
│       └── jd_analyzer.png
│
├── certificates/
├── data/
├── portfolio/
├── resumes/
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🔄 Application Workflow

```text
                    ┌─────────────────┐
                    │    Add Job      │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Analyze Job         │
                  │ Description         │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Select Resume       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ AI Resume Matching  │
                  └──────────┬──────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │ Identify Skills & Gaps       │
              └──────────────┬───────────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
       ┌──────────────────┐    ┌────────────────────┐
       │ Tailored Resume  │    │ Interview          │
       │ Generation       │    │ Preparation        │
       └──────────────────┘    └────────────────────┘
                 │                       │
                 └───────────┬───────────┘
                             ▼
                  ┌─────────────────────┐
                  │ Track Application   │
                  └─────────────────────┘
```

---

# 🧠 AI Capabilities

JobHuntAI uses Google Gemini for several AI-powered workflows.

### Job Description Analysis

```text
Job Description
       ↓
Gemini API
       ↓
Structured Requirements
       ↓
Skills / Experience / Education /
Responsibilities / Keywords
```

### Resume Matching

```text
Resume + Job Description
          ↓
      Gemini API
          ↓
    Match Analysis
          ↓
Score + Skills + Gaps +
Recommendations
```

### Tailored Resume

```text
Resume + Job Description
          ↓
      Gemini API
          ↓
Job-Specific Resume
          ↓
       DOCX
```

### Interview Preparation

```text
Resume + Job Description
          ↓
      Gemini API
          ↓
Personalized Interview Preparation
```

---

# 🗄️ Database

JobHuntAI uses SQLite for local data storage.

The database contains tables for:

* Jobs
* Applications
* Master Profile
* Resumes
* Skills
* Certifications
* Job Analyses
* Resume Matches
* Interview Preparations

The database is intentionally excluded from GitHub because it can contain personal application data.

---

# 📸 Screenshots

### 🏠 Dashboard

<img src="https://raw.githubusercontent.com/vikasidea/JobHuntAI/main/assets/screenshots/dashboard.png" alt="JobHuntAI Dashboard" width="900"/>

---

### 📋 Job Tracker

<img src="https://raw.githubusercontent.com/vikasidea/JobHuntAI/main/assets/screenshots/job_tracker.png" alt="Job Tracker" width="900"/>

---

### 🤖 AI Job Description Analyzer

<img src="https://raw.githubusercontent.com/vikasidea/JobHuntAI/main/assets/screenshots/jd_analyzer.png" alt="JD Analyzer" width="900"/>

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/vikasidea/JobHuntAI.git
cd JobHuntAI
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Configure Gemini API

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit your `.env` file to GitHub.

---

# ▶️ Run the Application

From the project root:

```bash
python -m streamlit run app/app.py
```

The Streamlit application will open in your browser.

---

# 🔒 Security

The project uses `.gitignore` to prevent sensitive and user-specific files from being committed.

Excluded files include:

```text
.env
*.db
*.sqlite
*.sqlite3
resumes/*
certificates/*
```

This prevents API keys, local databases, and personal documents from being uploaded to the public repository.

---

# 🎯 Project Goals

JobHuntAI was designed to bring multiple parts of the job-search process into one application.

Instead of separately managing:

* Job listings
* Applications
* Resumes
* Skills
* Certifications
* Job descriptions
* Resume matching
* Interview preparation

JobHuntAI provides a centralized workflow with AI-assisted tools.

---

# 🔮 Future Improvements

Possible future versions may include:

* PostgreSQL / Supabase integration
* User authentication
* Job-board integrations
* Automated job discovery
* Email notifications
* Advanced analytics
* Resume version comparison
* Improved AI validation
* Cloud deployment

These features are outside the current **v1.0** scope.

---

# 📌 Version

**Current Version: v1.0**

JobHuntAI v1.0 focuses on the core job tracking, resume management, and AI-assisted job preparation workflow.

---

# 👨‍💻 Author

**Vikas Yadav**

Computer Science Engineering — Data Science & Data Analysis

GitHub: https://github.com/vikasidea

---

## ⭐ Project

If you find this project useful or interesting, consider giving the repository a star.
