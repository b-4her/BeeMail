# BeeMail 

## Demo Link
#### Quick Demo:  <URL [HERE](https://youtu.be/HhA8Dpr6IvQ)>
#### In-Depth Demo:  <URL [HERE](https://youtu.be/k5HBm5l-yJ8?si=QjAO20z61ZZukZP7)>

---

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Database Design](#database-design)
4. [Challenges and Solutions](#challenges-and-solutions)
5. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Installation-Tutorial-Video](#inistallation-tutorial-video)
6. [Usage](#usage)
7. [Built With](#built-with)
8. [Contact Information](#contact-information)
9. [Acknowledgments](#acknowledgments)

---

## Overview
This project was developed as the final project for the CS50x course. It is a web-based application that allows users to send and receive emails. Built with Flask, HTML, CSS, Jinja templates, and a SQL database, the application integrates both front-end and back-end technologies to provide a seamless user experience.

### Goal
The primary goal of this project was to apply the web development concepts and database skills I learned in CS50x by creating an integrated web application.

---

## Key Features
- **User Registration**: Validates email structure and checks for duplicates before hashing passwords for secure storage.
- **Login System**: Ensures authentication by validating credentials against hashed passwords.
- **Password Reset**: Allows users to reset their password securely using a verification question.
- **Main Page**: Provides users with quick access to new emails and responses, streamlining communication.
- **Inbox**: Displays received emails, marking them as read or unread based on user actions.
- **Sent Items**: Allows users to review sent emails and their responses.
- **Compose Email**: Enables users to send emails with subject, content, and recipient validation.
- **Email Replies**: Supports replies linked to parent emails using a dedicated "responses" table.
- **Profile Management**: Lets users view and update their profile information.
- **Error Handling**: Catches database conflicts during simultaneous email submissions and prompts users to retry.

---

## Database Design
![Database Chart Image](Database/db_diagram.png) <!-- Add a link or embed the image here -->

### Schema Reference
![Database Schema](Database/database_scheme.sql)

### Explanation
- **Users Table**: Stores user details like name, email, hashed password, and verification question/answer.
- **Message Details Table**: Tracks email content, date, time,  reply/primary type, and read/unread status.
- **User Messages Table**: Links users to their sent and received emails.
- **Responses Table**: Maps replies to their parent emails.

---

## Challenges and Solutions
- **Simultaneous Email Submissions**: Solved using a unique database index combining content, subject, date, and time, along with `try-except` error handling.
- **Password Security**: Implemented hashing to ensure passwords are never stored in plaintext.
- **Data Integrity**: Used relational tables to maintain consistency between emails and responses.

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Flask
- SQLite3

### Installation Tutorial Video
1. Clone the repository:
   ```bash
   git clone https://github.com/username/project.git
2. Navigate to the project directory:
    ```bash  
   cd project
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Run the application:
   ```bash
   python3 app.py

## Tutorial
- link here 

### Usage

1. Open the application in your browser by navigating to the link provided in your terminal after running Flask.
2. Navigate through the following sections:
   - Registration: Create a new account.
   - Login: Log in with your credentials.
   - Inbox: View your received emails.
   - Compose: Send a new email.
   - Profile: Update your personal details.
3. Refer to the Screenshots Folder for visual guidance.
   ![Project Photos]()
   
For more information on how to use the website, please refer to [In-Depth Demo](https://youtu.be/k5HBm5l-yJ8?si=QjAO20z61ZZukZP7) video.

---

### Built With
- Python: Backend logic.
- Flask: Web framework.
- SQLite3: Database management.
- HTML/CSS: Frontend design.
- Jinja2: Template rendering.
- Werkzeug: Security utilities for password hashing.

### Contact Information
For any questions or feedback, reach out via:
- Email: your.email@example.com
- GitHub: username

### Acknowledgments
Special thanks to the CS50 team for inspiration.
Flask Documentation: For excellent resources.
Stack Overflow: For troubleshooting help.
