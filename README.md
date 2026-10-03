# 🤖 AI Resume Analyzer

An AI-based web application that analyzes resumes and extracts important information using **Natural Language Processing (NLP)** and **Machine Learning** techniques.

🔗 **Live Website:**
 
 https://pushpa-c-30.github.io/AI-resume-analyzer/

🔗 **GitHub Repository:**

https://github.com/Pushpa-C-30/AI-Resume-Analyzer

---

## 📌 About the Project

**AI Resume Analyzer** is a resume analysis application developed to help users understand and evaluate their resumes.

The system processes the uploaded resume, extracts relevant information, analyzes skills and content, and provides a resume analysis report.

The project combines **Python, Flask, NLP, and Machine Learning** with a simple web-based frontend.

---

## ✨ Features

### 📄 Resume Upload

Upload your resume for automated analysis.

### 👤 Personal Information

Extracts important details such as:

* Name
* Email ID
* Phone Number
* Address

### 🎓 Education

Identifies and displays educational information from the resume.

### 💻 Technical Skills

Extracts technical skills mentioned in the resume.

### 🧠 Soft Skills

Identifies relevant soft skills from the resume.

### 🚀 Projects

Detects and displays projects included in the resume.

### 💼 Internship

Identifies internship information separately from other resume content.

### 🌐 Languages

Extracts languages mentioned in the resume.

### 📊 Resume Score

Generates a resume score based on the analyzed resume content.

### 🎯 Job Role Analysis

Analyzes the candidate's skills and identifies relevant job roles.

### 🔍 Job Matching

Compares resume content with job-related information using text similarity techniques.

### ⚠️ Skill Gap Analysis

Identifies skills that may be missing or need improvement for specific roles.

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask
* REST API

### NLP & Machine Learning

* Natural Language Processing
* TF-IDF
* Cosine Similarity
* Text Processing
* Skill Extraction

### Document Processing

* PDF
* DOCX
* TXT

---

## 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── backend/
│   ├── app.py
│   ├── resume_parser.py
│   ├── nlp_analyzer.py
│   ├── ml_model.py
│   └── skills_data.py
│
├── frontend/
│   └── index.html
│
├── requirements.txt
└── README.md
```


## 🔄 How the System Works

```text
        Resume Upload
              │
              ▼
      Resume Text Extraction
              │
              ▼
        NLP Processing
              │
              ▼
    ┌─────────┴─────────┐
    │                   │
    ▼                   ▼
Information          Skill
Extraction           Extraction
    │                   │
    └─────────┬─────────┘
              ▼
       Resume Analysis
              │
              ▼
        Resume Score
              │
              ▼
       Job Role Analysis
              │
              ▼
       Skill Gap Analysis
              │
              ▼
        Final Report
```

---

## 🧠 Machine Learning

The project uses **TF-IDF (Term Frequency–Inverse Document Frequency)** to convert text into numerical representations.

**Cosine Similarity** is then used to measure the similarity between resume content and job-related text.

This helps with:

* Resume and job-description matching
* Skill matching
* Similarity analysis
* Job-role analysis

---


## 🎯 Objectives

The main objectives of this project are:

* Automate resume analysis.
* Extract important information from resumes.
* Identify technical and soft skills.
* Analyze projects and internships.
* Generate a resume score.
* Match resume content with job-related information.
* Identify skill gaps.
* Help users understand and improve their resumes.

---

## 🔮 Future Enhancements

* AI-powered resume improvement suggestions
* Job description upload
* Advanced ATS analysis
* Resume comparison
* Resume history
* User authentication
* Database integration
* Interview question generation

---

## 📜 License

This project is open-source and available under the MIT License.

© 2026 AI Resume Analyzer | Developed & Designed by Pushpa C

---


