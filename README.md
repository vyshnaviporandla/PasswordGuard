# 🔐 PasswordGuard — Password Strength Analyzer

PasswordGuard is a defensive cybersecurity project that analyzes password strength and provides security recommendations without storing passwords.

The project demonstrates fundamental password-security concepts such as password complexity, estimated entropy, common-password detection, security checks, and defensive security awareness.

## 🚀 Live Demo

**Frontend:** https://passwordguard-v1a3.onrender.com/

**Backend API:** https://passwordguard-api.onrender.com

**GitHub:** https://github.com/vyshnaviporandla/PasswordGuard

---

## 📌 Project Overview

Weak and predictable passwords are a common security risk. PasswordGuard helps users understand the characteristics that make passwords stronger or weaker.

The application analyzes a password and provides:

* Password strength score
* Strength classification
* Estimated entropy
* Password length analysis
* Character-type checks
* Common-password warnings
* Pattern detection
* Security recommendations
* Password-security awareness guidance

> **Privacy:** PasswordGuard does not save passwords in a database or file. The deployed frontend sends the entered password to the backend API over HTTPS for analysis, and the application does not persist it.

---

## ✨ Features

### 🔍 Password Analysis

PasswordGuard evaluates:

* Password length
* Uppercase letters
* Lowercase letters
* Numbers
* Special characters
* Common password patterns
* Repeated characters
* Sequential numbers
* Keyboard/alphabet patterns

### 📊 Strength Score

The analyzer calculates a score based on password characteristics and classifies the result as:

|  Score | Classification |
| -----: | -------------- |
|   0–29 | Very Weak      |
|  30–49 | Weak           |
|  50–69 | Moderate       |
|  70–89 | Strong         |
| 90–100 | Very Strong    |

### 🧮 Estimated Entropy

The application provides an estimated entropy value based on:

* Password length
* Character sets detected in the password

Entropy is presented as an estimate for educational purposes and is not a prediction of exact password-cracking time.

### ⚠️ Security Warnings

The analyzer detects examples of:

* Common passwords
* Repeated characters
* Sequential numbers
* Common keyboard patterns
* Alphabetic patterns

### 💡 Security Suggestions

Users receive actionable recommendations such as:

* Increase password length
* Add uppercase letters
* Add lowercase letters
* Add numbers
* Add special characters
* Avoid predictable patterns
* Avoid password reuse

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    │   Enters Password    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Frontend           │
                    │ HTML + CSS + JS      │
                    └──────────┬───────────┘
                               │ HTTPS
                               ▼
                    ┌──────────────────────┐
                    │   Flask REST API     │
                    │      /api/analyze    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Password Analyzer     │
                    │                      │
                    │ • Complexity checks   │
                    │ • Pattern detection   │
                    │ • Entropy estimate    │
                    │ • Score calculation   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ JSON Analysis Result │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Dashboard Results    │
                    │ Score / Warnings /   │
                    │ Suggestions / Checks │
                    └──────────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Responsive UI

### Backend

* Python
* Flask
* Flask-CORS
* Gunicorn

### Testing

* Python `unittest`

### Deployment

* Render Static Site — Frontend
* Render Web Service — Backend

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```text
PasswordGuard/
│
├── backend/
│   ├── analyzer.py
│   ├── app.py
│   └── requirements.txt
│
├── data/
│
├── docs/
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── tests/
│   └── test_analyzer.py
│
├── .gitignore
└── README.md
```

---

## 🔌 API

### Analyze Password

**Endpoint**

```text
POST /api/analyze
```

### Request

```json
{
  "password": "ExamplePassword!47"
}
```

### Response

```json
{
  "score": 100,
  "strength": "Very Strong",
  "length": 18,
  "entropy": 113.44,
  "checks": [],
  "warnings": [],
  "suggestions": []
}
```

The exact response values depend on the password being analyzed.

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/vyshnaviporandla/PasswordGuard.git
cd PasswordGuard
```

### 2. Create a Python virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Start the Flask API

```bash
python app.py
```

The backend will run at:

```text
http://127.0.0.1:5000
```

### 5. Run the frontend

Open:

```text
frontend/index.html
```

in your browser.

For local development, make sure `frontend/script.js` points to:

```text
http://127.0.0.1:5000/api/analyze
```

For the deployed version, it should point to:

```text
https://passwordguard-api.onrender.com/api/analyze
```

---

## 🧪 Run Tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

The test suite covers:

* Empty passwords
* Weak passwords
* Common passwords
* Stronger passwords
* Uppercase-character detection
* Special-character detection

---

## 🔐 Security Design

PasswordGuard follows a simple defensive security design.

### No Database Storage

The application does not store analyzed passwords in a database.

### No Password Logging

The analyzer does not intentionally write passwords to application files or databases.

### HTTPS Deployment

The deployed frontend communicates with the Render backend using HTTPS.

### Input Validation

The backend verifies that:

* A request body exists
* The `password` field exists
* The password value is a string

### Defensive Purpose

The project is designed for:

* Cybersecurity education
* Password-security awareness
* Demonstrating basic security analysis
* Learning REST API development

---

## ⚠️ Limitations

PasswordGuard is an educational security analyzer and should not be considered an enterprise password-security or breach-detection system.

Current limitations include:

* The common-password list is intentionally small.
* Entropy is an estimate based on detected character sets.
* The application does not query real-world breach databases.
* It does not estimate exact password-cracking time.
* It does not use advanced password-strength models.
* Passwords are transmitted to the deployed backend for analysis but are not intentionally persisted by the application.

For sensitive environments, organizations should use established password-management and authentication solutions.

---

## 🔮 Future Improvements

Possible future enhancements include:

* Larger common-password datasets
* Integration with privacy-preserving breach checking
* Password-manager integration
* More advanced pattern detection
* Better passphrase analysis
* Rate limiting
* API authentication
* Automated security testing
* Detailed audit logging without recording passwords
* Docker deployment
* CI/CD with GitHub Actions

---

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

* Password-security fundamentals
* Python programming
* Flask REST APIs
* Frontend/backend integration
* JSON-based APIs
* Regular expressions
* Entropy estimation
* Input validation
* CORS
* Unit testing
* Git and GitHub
* Cloud deployment
* Defensive cybersecurity principles

---

## 👩‍💻 Project Information

**Project:** PasswordGuard — Password Strength Analyzer

**Domain:** Cybersecurity

**Type:** Educational / Defensive Security Project

**Developer:** Vyshnavi Porandla

**Repository:**
https://github.com/vyshnaviporandla/PasswordGuard

---

## 📜 License

This project is intended for educational and portfolio purposes.

---

## ⚖️ Security Notice

PasswordGuard should be used only for passwords created specifically for testing and education.

**Do not enter passwords that you currently use for real accounts into a publicly deployed demonstration application.**
