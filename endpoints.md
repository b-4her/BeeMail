| Route                  | Method      | Description                                                   | Requires Auth          |
|------------------------|-------------|---------------------------------------------------------------|-----------------------|
| `/`                    | GET         | Render homepage showing user details and counts of unread primary and reply messages | Yes                   |
| `/login`               | GET, POST   | User login with validation and session management             | No                    |
| `/logout`              | GET         | Logs out the current user by clearing the session             | No                    |
| `/verify`              | GET, POST   | Email verification before allowing password reset, sends user to security question page | No             |
| `/verifqs`             | GET, POST   | Verify answer to security question before allowing password reset | Yes (email verified)  |
| `/pre_reset`           | GET, POST   | Password reset for verified users before login                | Yes (verified)        |
| `/register`            | GET, POST   | User registration with validation and database insertion      | No                    |
| `/inbox`               | GET         | Display logged-in user’s inbox messages                        | Yes                   |
| `/sent`                | GET         | Display logged-in user’s sent messages                         | Yes                   |
| `/compose`             | GET, POST   | Compose and send emails with validation                        | Yes                   |
| `/view/<message_id>`   | GET         | View details of a specific message                             | Yes                   |
| `/reply/<parent_id>`   | GET, POST   | Reply to a message                                            | Yes                   |
| `/responses/<parent_id>` | GET       | Display responses to a parent message                          | Yes                   |
| `/new_responses`       | GET         | Display new unread reply messages                              | Yes                   |
| `/new_primary`         | GET         | Display new unread primary messages                            | Yes                   |
| `/reset`               | GET, POST   | Password reset for logged-in users                             | Yes                   |
| `/profile`             | GET         | Display user profile with name, email, verification question and answer | Yes            |
| `/new_verif`           | GET, POST   | Create or update user verification question and answer        | Yes                   |
| `/new_name`            | GET, POST   | Update user name                                               | Yes                   |
