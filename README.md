# 🌐 Language Translation Tool

A simple Python Flask web application that translates text using the **Google Cloud Translation API**.

## Features

- Enter text in a web interface
- Select source language or use Auto Detect
- Select target language
- Translate using Google Cloud Translation API
- Display translated text clearly
- Copy translated text
- Text-to-speech
- Swap source and target languages
- Responsive interface

## Project Structure

```text
language_translation_tool/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

## 1. Install Python

Install Python 3.10+ from python.org.

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Google Cloud Translation API

Create a Google Cloud project, enable the **Cloud Translation API**, create an API key, and set it as an environment variable.

Windows PowerShell:

```powershell
$env:GOOGLE_TRANSLATE_API_KEY="YOUR_API_KEY"
```

Windows CMD:

```cmd
set GOOGLE_TRANSLATE_API_KEY=YOUR_API_KEY
```

macOS/Linux:

```bash
export GOOGLE_TRANSLATE_API_KEY="YOUR_API_KEY"
```

Do not put your API key directly into `app.py` or upload it to GitHub.

## 5. Run the project

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## How it works

1. User enters text.
2. User selects source and target languages.
3. Browser sends the text to Flask.
4. Flask sends the text to Google Cloud Translation API.
5. Google returns the translated text.
6. Flask sends the result back to the browser.
7. The translated text is displayed.

## Assignment Requirements Covered

| Requirement | Implementation |
|---|---|
| User interface | Flask + HTML/CSS |
| Select source/target language | Dropdown menus |
| Translation API | Google Cloud Translation API |
| Send text to API | Python `requests` |
| Display translated response | Output textarea |
| Copy button | JavaScript Clipboard API |
| Text-to-speech | Browser Speech Synthesis API |

## GitHub Upload

```bash
git init
git add .
git commit -m "Create language translation tool"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Make sure `.env`, API keys, and other secrets are never committed.
