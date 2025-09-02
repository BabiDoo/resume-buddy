# Resume Buddy

## Project Description

Resume Buddy is a tool that leverages artificial intelligence to generate summaries from text files or notes. The application converts PDFs to `.txt`, processes the content using the Gemini model, and organizes the results into a `.md` file, making it easier to review and manage information.

---

## Quick Installation

Clone the repository and navigate into the project folder:

```bash
git clone github.com/BabiDoo/resume-buddy
cd resume-buddy
```

---

## Starting Virtual Environment

Create and activate the virtual environment:

```bash
# Create venv
python -m venv venv

# Activate venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 API Setup

* Create an API key to use **Gemini**: [Get key](https://aistudio.google.com/app/apikey)
* Add the key to the `.env` file with the name:

```env
LANGEXTRACT_API_KEY=your_api_key_here
```

---

## 📂 File Preparation

* **If you have a PDF file:**

  1. Convert it to `.txt` firt, running:

     ```bash
     py to_txt.py
     py -X utf8 run_resume_extract.py
     ```

* **If the file is already `.txt`:**
  Just run:

  ```bash
  py -X utf8 run_resume_extract.py
  ```

---

## Execution

* Wait for the results in the terminal (it may take up to **10 minutes**, depending on the file).
* The generated data will be saved in a `.md` file containing the **summary of the `.txt` file**.

---

## 💡 Project Idea

The goal is for the agent to assist in creating summaries of notes and files by extracting information of the content for you and making it easier to organize and review content.
