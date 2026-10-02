# PasswordGuard

## Password Strength Analyzer & Security Suggestion Tool

PasswordGuard is a defensive cybersecurity application that analyzes password characteristics and provides security recommendations.

The project is designed for cybersecurity awareness and education. It does not store passwords.

---

## Features

- Password strength scoring
- Password length analysis
- Uppercase/lowercase detection
- Number detection
- Special-character detection
- Common-password detection
- Sequential-pattern detection
- Repeated-character detection
- Entropy estimation
- Security warnings
- Personalized security suggestions
- Password security awareness section
- Responsive dashboard
- Automated unit tests

---

## Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Flask
- Flask-CORS

### Testing

- Python unittest

### Deployment

- Render

---

## Architecture

```text
User
 |
 v
PasswordGuard Web Interface
 |
 v
JavaScript Fetch API
 |
 v
Flask REST API
 |
 v
Password Analyzer
 |
 +--> Strength Score
 +--> Security Checks
 +--> Entropy Estimate
 +--> Warnings
 +--> Suggestions