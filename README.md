<a id="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/b-4her/BeeMail">
    <img src="./assets/project_logo.png" alt="Logo" width="160" height="160">
  </a>
  <h3 align="center"><b>BeeMail</b></h3>
  <p align="center"">
    <i>Speeding up your communication and uniting your team, BeeMail</i>
    <br/>
    <a href="https://youtu.be/HhA8Dpr6IvQ"><strong>Quick Demo</strong></a>
    ·
    <a href="https://youtu.be/k5HBm5l-yJ8?si=QjAO20z61ZZukZP7"><strong>In-Depth Demo</strong></a>
  </p>
</div>

---

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#key-features">Key Features</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#database-design">Database Design</a></li>
    <li><a href="#api-endpoints">API Endpoints</a></li>
    <li><a href="#challenges-and-solutions">Challenges and Solutions</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#installation-tutorial-video">Installation Tutorial Video</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact-information">Contact Information</a></li>
    <li><a href="#acknowledgments">Resources Used</a></li>
  </ol>
</details>

---

## Overview
This project was developed as the final project for the CS50x course. It is a web-based application that allows users to send and receive emails. Built with Flask, HTML, CSS, Jinja templates, and a SQL database, the application integrates both front-end and back-end technologies to provide a seamless user experience.

### Goal
The primary goal of this project was to apply the web development concepts and database skills I learned in CS50x by creating an integrated web application.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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
- **Unread Message Notifications**: Highlights new/unread primary and reply messages for better visibility.
- **Verification Question Management**: Allows users to set or update their security question and answer for password recovery.
- **Responsive Design**: Uses Bootstrap and custom CSS to ensure the application works well on different devices.
- **Detailed Email View**: Lets users view full details of each message, including threaded replies.
- **Robust Access Control**: Restricts access to sensitive routes and data based on authentication status.
- **Comprehensive Feedback**: Provides clear error and success messages for all major actions.
- **Error Handling**: Catches database conflicts during simultaneous email submissions and prompts users to retry.

  <p align="right">(<a href="#readme-top">back to top</a>)</p>

---

### Built With

* [![Python][Python.com]][Python-url]
* [![Flask][Flask.com]][Flask-url]
* [![Jinja][Jinja.com]][Jinja-url]
* [![SQLite][SQLite.com]][SQLite-url]
* [![HTML][HTML.com]][HTML-url]
* [![CSS][CSS.com]][CSS-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![Werkzeug][Werkzeug.com]][Werkzeug-url]

  <p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Database Design
![Database Chart Image](Database/db_diagram.png) <!-- Add a link or embed the image here -->

### Schema Reference
> <a href="./Database/db_schema.sql">Database Schema</a>

### Explanation
- **Users Table**: Stores user details like name, email, hashed password, and verification question/answer.
- **Message Details Table**: Tracks email content, date, time,  reply/primary type, and read/unread status.
- **User Messages Table**: Links users to their sent and received emails.
- **Responses Table**: Maps replies to their parent emails.

  <p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## API Endpoints

Below is a summary of the main routes and their functionality in BeeMail:

| Route                      | Method(s)   | Description                                                                 | Requires Auth         |
|----------------------------|-------------|-----------------------------------------------------------------------------|-----------------------|
| `/`                        | GET         | Render homepage showing user details and counts of unread primary and reply messages | Yes           |
| `/login`                   | GET, POST   | User login with validation and session management                            | No                    |
| `/logout`                  | GET         | Logs out the current user by clearing the session                            | No                    |
| `/verify`                  | GET, POST   | Email verification before allowing password reset, sends user to security question page | No           |
| `/verifqs`                 | GET, POST   | Verify answer to security question before allowing password reset            | Yes (email verified)  |
| `/pre_reset`               | GET, POST   | Password reset for verified users before login                               | Yes (verified)        |
| `/register`                | GET, POST   | User registration with validation and database insertion                     | No                    |
| `/inbox`                   | GET         | Display logged-in user’s inbox messages                                      | Yes                   |
| `/sent`                    | GET         | Display logged-in user’s sent messages                                       | Yes                   |
| `/compose`                 | GET, POST   | Compose and send emails with validation                                      | Yes                   |
| `/view/<message_id>`       | GET         | View details of a specific message                                           | Yes                   |
| `/reply/<parent_id>`       | GET, POST   | Reply to a message                                                           | Yes                   |
| `/responses/<parent_id>`   | GET         | Display responses to a parent message                                        | Yes                   |
| `/new_responses`           | GET         | Display new unread reply messages                                            | Yes                   |
| `/new_primary`             | GET         | Display new unread primary messages                                          | Yes                   |
| `/reset`                   | GET, POST   | Password reset for logged-in users                                           | Yes                   |
| `/profile`                 | GET         | Display user profile with name, email, verification question and answer      | Yes                   |
| `/new_verif`               | GET, POST   | Create or update user verification question and answer                       | Yes                   |
| `/new_name`                | GET, POST   | Update user name                                                            | Yes                   |

> **Note:** All routes requiring authentication will redirect to the login page if the user is not logged in.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Challenges and Solutions

- **User Authentication & Security**:  
  Implemented secure password hashing and session management to protect user data. Verification questions add an extra layer of security for password resets.

- **Data Integrity & Consistency**:  
  Utilized relational database design with foreign keys to ensure messages, users, and responses remain consistent and linked correctly.

- **Simultaneous Email Submissions**:  
  Addressed potential database conflicts by using a unique index on email content, subject, date, and time, combined with `try-except` error handling to prevent duplicate entries.

- **Email Threading & Replies**:  
  Designed a dedicated "responses" table to efficiently map replies to parent emails, enabling clear conversation threads.

- **User Experience & Error Handling**:  
  Provided clear feedback for invalid actions (e.g., duplicate registration, invalid login, or failed email delivery) and ensured users are prompted to retry when necessary.

- **Frontend & Backend Integration**:  
  Integrated Flask with Jinja templates, Bootstrap, and custom CSS to deliver a responsive and intuitive user interface.

- **Deployment & Environment Setup**:  
  Simplified installation and setup with clear prerequisites, requirements file, and tutorial resources to help users get started quickly.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

### Prerequisites
- Python 3.10 or higher

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/b-4her/BeeMail.git
2. Navigate to the project directory:
    ```bash  
   cd BeeMail
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Run the application:
   ```bash
   python app.py

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation Tutorial Video
https://github.com/user-attachments/assets/c1b57928-aa4c-4e0c-8d67-67175f7eb412

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

### Usage

1. Start the application by running `python app.py` and open the provided local URL in your browser.

2. Explore the main features:
   - **Registration:** Create a new account with your email and password.
   - **Login:** Access your account using your credentials.
   - **Inbox:** View all received emails, with unread messages highlighted.
   - **Sent:** Review emails you have sent.
   - **Compose:** Send new emails to other users.
   - **Reply:** Respond to received emails and view threaded conversations.
   - **Profile:** View and update your personal information, including your verification question.

3. For a visual walkthrough, see the Project Photos:
   > <a href="./assets/project photos/pages.pdf">Project Photos</a>

4. For a detailed demonstration, watch the [In-Depth Demo](https://youtu.be/k5HBm5l-yJ8?si=QjAO20z61ZZukZP7) video.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

### Contact Information
For any questions or feedback, reach out via:
- LinkedIn: [b-4her](https://www.linkedin.com/in/b-4her)
- GitHub: [b-4her](https://github.com/b-4her)
- YouTube: [b-4her](https://www.youtube.com/@b-4her)
- Email: baher.alabbar@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

### Resources Used

This project was developed using the CS50x course materials as a foundation. Frontend implementation was supported by documentation from W3Schools for HTML and CSS. Badge visuals were generated using Shields.io.

- [CS50x](https://cs50.harvard.edu/x)  
- [W3Schools](https://www.w3schools.com/)  
- [Shields.io](https://shields.io)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[Python.com]: https://img.shields.io/badge/python-b?style=for-the-badge&logo=python&logoColor=yellow&color=blue
[python-url]: https://www.python.org

[flask.com]: https://img.shields.io/badge/flask-b?style=for-the-badge&logo=flask&logoColor=white&color=black
[flask-url]: https://flask.palletsprojects.com/en/stable/

[Jinja.com]: https://img.shields.io/badge/Jinja-b?logo=jinja&color=red
[Jinja-url]: https://jinja.palletsprojects.com/en/stable/

[SQLite.com]: https://img.shields.io/badge/SQLite-b?style=for-the-badge&logo=SQLite&logoColor=white&color=blue
[SQlite-url]: https://www.sqlite.org

[HTML.com]: https://img.shields.io/badge/Html-b?style=for-the-badge&logo=Html&logoColor=white&color=red
[HTML-url]:https://developer.mozilla.org/en-US/docs/Web/HTML

[CSS.com]: https://img.shields.io/badge/css-b?style=for-the-badge&logo=css&logoColor=white&color=blue
[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS

[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com

[Werkzeug.com]: https://img.shields.io/badge/Werkzeug-b?style=for-the-badge&logo=Werkzeug&logoColor=white&color=orange
[Werkzeug-url]: https://werkzeug.palletsprojects.com/en/stable/


