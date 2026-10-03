import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def analyze_job_description(job_description):

    prompt = f"""
You are an expert job description analyzer.

Analyze the following job description and extract:

1. Required technical skills
2. Preferred technical skills
3. Experience requirement
4. Education requirement
5. Key responsibilities
6. Important keywords

Return the answer in this exact format:

REQUIRED_SKILLS:
skill1, skill2, skill3

PREFERRED_SKILLS:
skill1, skill2, skill3

EXPERIENCE:
...

EDUCATION:
...

RESPONSIBILITIES:
- responsibility 1
- responsibility 2
- responsibility 3

KEYWORDS:
keyword1, keyword2, keyword3

Job Description:

{job_description}
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if "503" in str(e) and attempt < 2:

                time.sleep(3)

            else:

                raise
def parse_analysis(ai_result):

    sections = {
        "required_skills": "",
        "preferred_skills": "",
        "experience": "",
        "education": "",
        "responsibilities": "",
        "keywords": ""
    }

    section_names = [
        "REQUIRED_SKILLS:",
        "PREFERRED_SKILLS:",
        "EXPERIENCE:",
        "EDUCATION:",
        "RESPONSIBILITIES:",
        "KEYWORDS:"
    ]

    current_section = None

    # Put every section on a new line
    cleaned_text = ai_result

    for section in section_names:

        cleaned_text = cleaned_text.replace(
            section,
            "\n" + section
        )

    for line in cleaned_text.splitlines():

        line = line.strip()

        if not line:
            continue

        upper_line = line.upper()

        if upper_line.startswith("REQUIRED_SKILLS:"):

            current_section = "required_skills"

            sections[current_section] = (
                line.split(":", 1)[1].strip()
            )

        elif upper_line.startswith("PREFERRED_SKILLS:"):

            current_section = "preferred_skills"

            sections[current_section] = (
                line.split(":", 1)[1].strip()
            )

        elif upper_line.startswith("EXPERIENCE:"):

            current_section = "experience"

            sections[current_section] = (
                line.split(":", 1)[1].strip()
            )

        elif upper_line.startswith("EDUCATION:"):

            current_section = "education"

            sections[current_section] = (
                line.split(":", 1)[1].strip()
            )

        elif upper_line.startswith("RESPONSIBILITIES:"):

            current_section = "responsibilities"

            sections[current_section] = (
                line.split(":", 1)[1].strip()
            )

        elif upper_line.startswith("KEYWORDS:"):

            current_section = "keywords"

            sections[current_section] = (
                line.split(":", 1)[1].strip()
            )

        elif current_section:

            if current_section == "responsibilities":

                if sections[current_section]:

                    sections[current_section] += "\n"

                sections[current_section] += line

            else:

                if sections[current_section]:

                    sections[current_section] += " "

                sections[current_section] += line

    return sections

    sections = {
        "required_skills": "",
        "preferred_skills": "",
        "experience": "",
        "education": "",
        "responsibilities": "",
        "keywords": ""
    }

    current_section = None

    for line in ai_result.splitlines():

        line = line.strip()

        if not line:
            continue

        upper_line = line.upper()

        if upper_line.startswith("REQUIRED_SKILLS:"):
            current_section = "required_skills"
            sections[current_section] = line.split(":", 1)[1].strip()

        elif upper_line.startswith("PREFERRED_SKILLS:"):
            current_section = "preferred_skills"
            sections[current_section] = line.split(":", 1)[1].strip()

        elif upper_line.startswith("EXPERIENCE:"):
            current_section = "experience"
            sections[current_section] = line.split(":", 1)[1].strip()

        elif upper_line.startswith("EDUCATION:"):
            current_section = "education"
            sections[current_section] = line.split(":", 1)[1].strip()

        elif upper_line.startswith("RESPONSIBILITIES:"):
            current_section = "responsibilities"
            sections[current_section] = ""

        elif upper_line.startswith("KEYWORDS:"):
            current_section = "keywords"
            sections[current_section] = line.split(":", 1)[1].strip()

        elif current_section == "responsibilities":

            if sections[current_section]:
                sections[current_section] += "\n"

            sections[current_section] += line

    return sections

def match_resume_to_job(resume_text, job_analysis):

    prompt = f"""
You are an expert ATS resume and job-matching assistant.

Compare the candidate's resume with the job requirements.

JOB ANALYSIS:

Required Skills:
{job_analysis["required_skills"]}

Preferred Skills:
{job_analysis["preferred_skills"]}

Experience:
{job_analysis["experience"]}

Education:
{job_analysis["education"]}

Responsibilities:
{job_analysis["responsibilities"]}

Keywords:
{job_analysis["keywords"]}


CANDIDATE RESUME:

{resume_text}


Analyze the match and return the result in exactly this format:

MATCH_SCORE:
Give a percentage from 0 to 100 based on the overall match.

MATCHED_SKILLS:
List the required/preferred skills the candidate already has.

MISSING_SKILLS:
List important required or preferred skills missing from the resume.

MATCHED_KEYWORDS:
List important job keywords already present in the resume.

MISSING_KEYWORDS:
List important job keywords missing from the resume.

EXPERIENCE_MATCH:
Explain whether the candidate's experience matches the job requirement.

EDUCATION_MATCH:
Explain whether the candidate's education matches the job requirement.

RESPONSIBILITY_MATCH:
Explain how the candidate's projects/internship/experience relate to the job responsibilities.

RECOMMENDATIONS:
Give specific improvements the candidate could make to better align the resume with this job.
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if "503" in str(e) and attempt < 2:

                time.sleep(5)

            else:

                raise

    prompt = f"""
You are an expert ATS resume and job-matching assistant.

Compare the candidate's resume with the job requirements.

JOB ANALYSIS:

Required Skills:
{job_analysis["required_skills"]}

Preferred Skills:
{job_analysis["preferred_skills"]}

Experience:
{job_analysis["experience"]}

Education:
{job_analysis["education"]}

Responsibilities:
{job_analysis["responsibilities"]}

Keywords:
{job_analysis["keywords"]}


CANDIDATE RESUME:

{resume_text}


Analyze the match and return the result in exactly this format:

MATCH_SCORE:
Give a percentage from 0 to 100 based on the overall match.

MATCHED_SKILLS:
List the required/preferred skills the candidate already has.

MISSING_SKILLS:
List important required or preferred skills missing from the resume.

MATCHED_KEYWORDS:
List important job keywords already present in the resume.

MISSING_KEYWORDS:
List important job keywords missing from the resume.

EXPERIENCE_MATCH:
Explain whether the candidate's experience matches the job requirement.

EDUCATION_MATCH:
Explain whether the candidate's education matches the job requirement.

RESPONSIBILITY_MATCH:
Explain how the candidate's projects/internship/experience relate to the job responsibilities.

RECOMMENDATIONS:
Give specific improvements the candidate could make to better align the resume with this job.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text
def parse_match_result(ai_result):

    sections = {
        "match_score": "",
        "matched_skills": "",
        "missing_skills": "",
        "matched_keywords": "",
        "missing_keywords": "",
        "experience_match": "",
        "education_match": "",
        "responsibility_match": "",
        "recommendations": ""
    }

    section_map = {
        "MATCH_SCORE:": "match_score",
        "MATCHED_SKILLS:": "matched_skills",
        "MISSING_SKILLS:": "missing_skills",
        "MATCHED_KEYWORDS:": "matched_keywords",
        "MISSING_KEYWORDS:": "missing_keywords",
        "EXPERIENCE_MATCH:": "experience_match",
        "EDUCATION_MATCH:": "education_match",
        "RESPONSIBILITY_MATCH:": "responsibility_match",
        "RECOMMENDATIONS:": "recommendations"
    }

    # Make section headings start on new lines
    cleaned_text = ai_result

    for heading in section_map:
        cleaned_text = cleaned_text.replace(
            heading,
            "\n" + heading
        )

    current_section = None

    for line in cleaned_text.splitlines():

        line = line.strip()

        if not line:
            continue

        upper_line = line.upper()

        found_section = False

        for heading, section_name in section_map.items():

            if upper_line.startswith(heading):

                current_section = section_name

                sections[current_section] = (
                    line.split(":", 1)[1].strip()
                )

                found_section = True
                break

        if found_section:
            continue

        if current_section:

            if sections[current_section]:

                sections[current_section] += "\n"

            sections[current_section] += line

    return sections
def generate_tailored_resume(resume_text, job_description):

    prompt = f"""
You are an expert ATS resume writer.

Create a tailored resume using the candidate's existing resume
and the target job description.

IMPORTANT RULES:

1. Do NOT invent, assume, infer, or add any information.
2. Use ONLY facts explicitly present in the candidate resume.
3. NEVER change dates, years, company names, university names,
   job titles, project names, scores, percentages, or numbers.
4. NEVER add a skill unless that skill is explicitly listed in
   the candidate resume.
5. NEVER add experience with a technology, tool, methodology,
   framework, process, or domain unless it is explicitly present
   in the candidate resume.
6. NEVER add achievements, responsibilities, certifications,
   qualifications, or job duties that are not explicitly supported
   by the candidate resume.
7. You may ONLY:
   - reorder existing skills
   - prioritize relevant existing information
   - rewrite existing statements for clarity
   - improve grammar
   - use stronger wording without changing the factual meaning
8. If a job requirement is missing from the candidate resume,
   do NOT add it to the resume.
9. Preserve all factual dates and numerical values EXACTLY.
10. The tailored resume must remain truthful and ATS-friendly.
11. Do not claim that any model, project, or system is "error-free",
    "robust", "production-ready", "tested", or "validated" unless
    the candidate resume explicitly states that.
12. Do not add SDLC, QA/testing, troubleshooting, requirement
    analysis, or similar concepts unless explicitly present.

Return the resume in this structure:

NAME AND CONTACT INFORMATION

PROFESSIONAL SUMMARY

SKILLS

EDUCATION

INTERNSHIPS / EXPERIENCE

PROJECTS

CERTIFICATIONS

ACHIEVEMENTS / EXTRACURRICULAR ACTIVITIES


CANDIDATE RESUME:

{resume_text}


TARGET JOB DESCRIPTION:

{job_description}
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if "503" in str(e) and attempt < 2:
                time.sleep(5)

            else:
                raise
def generate_interview_preparation(resume_text, job_description):

    prompt = f"""
You are an expert technical interview preparation assistant.

Generate interview preparation material specifically for this
candidate and this job.

IMPORTANT RULES:

1. Use the candidate's resume only for claims about the candidate.
2. Do NOT invent, assume, or fabricate experience, skills,
   technologies, projects, responsibilities, achievements,
   certifications, or work activities.
3. Never write a sample answer that claims the candidate has
   performed an activity unless it is explicitly supported by
   the resume.
4. Questions may cover technologies or responsibilities mentioned
   in the job description even if the candidate does not have them.
5. If a question asks about something not present in the resume,
   the sample answer must honestly acknowledge the gap and explain
   how the candidate would approach learning or handling it.
6. Do not present hypothetical knowledge as real work experience.
7. Do not claim the candidate has designed test cases, performed
   software validation, analyzed production issues, maintained
   software, worked with customers, or used a technology unless
   the resume explicitly supports that claim.
8. Keep answers realistic for a fresher/student.
9. Use the candidate's actual projects, internship, education,
   certifications, and achievements when answering resume-based
   questions.
10. Do not change or invent dates, numbers, percentages, company
    names, project names, or other factual information.
11. For resume-based sample answers, use only activities explicitly
    documented in the resume.

12. Do not convert a listed skill into a claim of hands-on experience.
    For example, if Pandas is listed under skills but the resume does
    not describe a specific Pandas task, do not say "I used Pandas to..."
    as if that activity is documented.

13. Do not invent the candidate's specific contribution, workflow,
    methodology, tools used, or technical steps for a project unless
    the resume explicitly states them.

14. When explaining a technical concept that is not documented as
    hands-on experience, phrase the answer as knowledge or a proposed
    approach, for example:
    "My understanding is..."
    "I would approach it by..."
    "A typical approach would be..."

15. Never turn a generic technical best practice into a claim about
    what the candidate actually did.

16. For behavioral questions asking for a real past situation,
    only use situations explicitly supported by the resume.
    If the resume does not provide enough information, clearly say
    that the candidate would need to provide their own real example
    rather than inventing one.

Generate:

SECTION 1 — RESUME-BASED QUESTIONS
Generate 5 questions based specifically on the candidate's resume.

SECTION 2 — TECHNICAL QUESTIONS
Generate 10 technical questions relevant to the job.

SECTION 3 — PROJECT QUESTIONS
Generate 5 questions about the candidate's projects.

SECTION 4 — BEHAVIORAL QUESTIONS
Generate 5 common behavioral/HR questions.

SECTION 5 — JOB-SPECIFIC QUESTIONS
Generate 5 questions based specifically on the job description.

For every question provide:

QUESTION:
...

SAMPLE ANSWER:
...

CANDIDATE RESUME:

{resume_text}

TARGET JOB DESCRIPTION:

{job_description}
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if "503" in str(e) and attempt < 2:
                time.sleep(5)

            else:
                raise