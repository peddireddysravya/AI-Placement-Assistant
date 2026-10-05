import streamlit as st
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.6-flash:generateContent"
)


# Student data model
class Student(BaseModel):
    name: str
    branch: str
    skill: str
    level: str


# -----------------------------
# Gemini Function
# -----------------------------
def ask_gemini(prompt):

    if not API_KEY:
        return "❌ Gemini API key not found. Please check your .env file."

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:

        response = requests.post(
            API_URL,
            headers=headers,
            json=data
        )

        result = response.json()

        if response.status_code != 200:
            return "❌ API Error: " + str(result)

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return "❌ Error: " + str(e)


# -----------------------------
# Streamlit Page
# -----------------------------

st.set_page_config(
    page_title="AI Placement Preparation Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Placement Preparation Assistant")

st.write(
    "Your personal AI assistant for placement preparation 🚀"
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("📚 Menu")

option = st.sidebar.selectbox(
    "Choose an option",
    [
        "🏠 Home",
        "🎤 AI Interview",
        "💻 Coding Practice",
        "📄 Resume Assistant",
        "📅 Study Plan",
        "🤖 Ask AI"
    ]
)


# -----------------------------
# HOME
# -----------------------------

if option == "🏠 Home":

    st.header("Welcome! 👋")

    st.write("""
    This AI Placement Preparation Assistant helps students
    prepare for technical interviews and placements.
    """)

    st.write("### Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🎤 AI Interview")

    with col2:
        st.info("💻 Coding Practice")

    with col3:
        st.info("📄 Resume Assistant")

    st.success("Start your placement preparation today! 🚀")


# -----------------------------
# AI INTERVIEW
# -----------------------------

elif option == "🎤 AI Interview":

    st.header("🎤 AI Interview Preparation")

    subject = st.selectbox(
        "Select your subject",
        [
            "C Programming",
            "Python",
            "Java",
            "DBMS",
            "SQL",
            "Data Structures",
            "Computer Networks"
        ]
    )

    level = st.selectbox(
        "Select difficulty",
        ["Beginner", "Intermediate", "Advanced"]
    )

    number = st.slider(
        "Number of questions",
        1,
        10,
        5
    )

    if st.button("Generate Interview Questions"):

        prompt = f"""
        You are an AI placement interviewer.

        Generate {number} {level}-level interview questions
        for {subject}.

        For every question provide:
        1. Question
        2. Short answer
        3. Explanation

        Keep the language simple for a college student.
        """

        with st.spinner("Gemini is generating questions..."):

            answer = ask_gemini(prompt)

        st.markdown(answer)


# -----------------------------
# CODING PRACTICE
# -----------------------------

elif option == "💻 Coding Practice":

    st.header("💻 AI Coding Practice")

    language = st.selectbox(
        "Programming Language",
        ["C", "Python", "Java"]
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("Generate Coding Question"):

        prompt = f"""
        Act as a coding interviewer.

        Generate one {difficulty} coding problem
        in {language}.

        Give:
        - Problem statement
        - Input format
        - Output format
        - Example input
        - Example output
        - Hint

        Do NOT give the complete solution.
        """

        with st.spinner("Generating coding problem..."):

            answer = ask_gemini(prompt)

        st.markdown(answer)


# -----------------------------
# RESUME ASSISTANT
# -----------------------------

elif option == "📄 Resume Assistant":

    st.header("📄 AI Resume Assistant")

    resume_text = st.text_area(
        "Paste your resume here",
        height=300
    )

    if st.button("Analyze Resume"):

        if resume_text.strip() == "":
            st.warning("Please paste your resume first.")

        else:

            prompt = f"""
            You are an expert placement resume reviewer.

            Analyze this student's resume:

            {resume_text}

            Give:
            1. Resume strengths
            2. Weaknesses
            3. Missing skills
            4. Grammar improvements
            5. ATS suggestions
            6. Overall improvement suggestions

            Use simple language.
            """

            with st.spinner("Analyzing resume..."):

                answer = ask_gemini(prompt)

            st.markdown(answer)


# -----------------------------
# STUDY PLAN
# -----------------------------

elif option == "📅 Study Plan":

    st.header("📅 Personalized Placement Study Plan")

    name = st.text_input("Student Name")

    branch = st.text_input("Branch")

    skill = st.text_input("Strongest Skill")

    level = st.selectbox(
        "Current Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    if st.button("Generate Study Plan"):

        if name and branch and skill:

            student = Student(
                name=name,
                branch=branch,
                skill=skill,
                level=level
            )

            prompt = f"""
            Create a personalized placement preparation plan.

            Student name: {student.name}
            Branch: {student.branch}
            Strongest skill: {student.skill}
            Current level: {student.level}

            Create a 30-day plan covering:

            - Programming
            - Data Structures
            - DBMS
            - SQL
            - Aptitude
            - Communication
            - Technical interviews
            - HR interview

            Keep it simple and practical.
            """

            with st.spinner("Creating your study plan..."):

                answer = ask_gemini(prompt)

            st.markdown(answer)

        else:

            st.warning("Please fill all the details.")


# -----------------------------
# ASK AI
# -----------------------------

elif option == "🤖 Ask AI":

    st.header("🤖 Ask Your Placement AI")

    question = st.text_area(
        "Ask anything about placements:"
    )

    if st.button("Ask Gemini"):

        if question.strip() == "":
            st.warning("Please enter your question.")

        else:

            prompt = f"""
            You are an AI Placement Preparation Assistant.

            Help a college student prepare for placements.

            Student question:
            {question}

            Give a clear and beginner-friendly answer.
            """

            with st.spinner("Gemini is thinking..."):

                answer = ask_gemini(prompt)

            st.markdown(answer)