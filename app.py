import sqlite3
import os.path  # to use absolute path when connecting the database

from flask import Flask, redirect, render_template, request, session 
from flask_session import Session  # for cookies
from werkzeug.security import check_password_hash, generate_password_hash  # To encrypt the passwords

from helpers import apology, login_required, get_date, get_time, validate_email, verified_user_required, user_email_required


# Configure application
app = Flask(__name__)

# Code snippet taken from problem set 9 - finance - (CS50X 2024)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connecting the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# creating absolute path
db_path = os.path.join(BASE_DIR, "database/beemail.db")
db = sqlite3.connect(db_path, check_same_thread=False)
cur = db.cursor()  # cursor

VERIFICATION_QUESTIONS = {  
    "pet": "What is your first pet's name?",
    "school": "What is your first school's name?",
    "friend": "What is your best friend's name?",
    # make sure the keys are lowercase
}


def search_database(target_row, table, search_column, column_unique_val):
    """
    Search for a specific item in the database.

    Executes a query to retrieve the value of a target row
    from a specified table where the search column matches
    the given unique value. Returns the value if found; otherwise, None.
    """

    cur.execute(f"SELECT {target_row} FROM {table} WHERE {search_column}=?", (column_unique_val,))
    data = cur.fetchone()

    if data:
        return data[0]
    return data


# Code snippet taken from problem set 9 - finance - (CS50X 2024)
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required  
def index():
    """
    Render the homepage with user details and message counts.

    Checks the number of unread 'primary' and 'reply' messages for the logged-in user.
    Displays the user's name, email, and counts of new primary mails and responses.
    """
    name = session["user_name"]
    email = session["user_email"]

    # Define the query template
    new_mail_query = """
        SELECT COUNT(id) 
        FROM message_details 
        JOIN user_messages ON id = message_id 
        WHERE type = 'primary' 
        AND status = 0 
        AND recipient_email = ?
    """

    new_response_query = """
        SELECT COUNT(id) 
        FROM message_details 
        JOIN user_messages ON id = message_id 
        WHERE type = 'reply' 
        AND status = 0 
        AND recipient_email = ?
    """

    # Execute the queries and fetch the results
    cur.execute(new_mail_query, (email,))
    new_mails_num = cur.fetchone()[0]  # Get the count value

    cur.execute(new_response_query, (email,))
    new_responses_num = cur.fetchone()[0]  # Get the count value

    return render_template("index.html", name=name, new_mails_num=new_mails_num, new_responses_num=new_responses_num)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any info about the user
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login with validation.

    On GET, clears the session and renders the login page. On POST, validates the email, 
    password, and verifies the credentials. If successful, stores user data in the 
    session and redirects to the homepage.
    """

    if request.method == "GET":
        session.clear()
        return render_template("login.html")
    else:  # POST
        entered_email = request.form.get("email")
        entered_password = request.form.get("password")

        # Testing input values
        if not entered_email:
            return apology("Oops! You forgot to enter your email.")
        elif not entered_password:
            apology("Oops! You forgot to enter your password.")
        elif not validate_email(entered_email):
            return apology("Oops! Invalid email. Ensure it includes a username, the domain '@beemail.hive', " + 
                           "starts with a letter, and only uses periods, underscores, or hyphens as special characters.")
        elif not 8 <= len(entered_password.strip()) <= 16:
            return apology("Oops! The password you entered is invalid, " +
                            "Please ensure that it is between 8 and 16 characters in length.")
        else:
            entered_password = entered_password.strip()
            entered_email = entered_email.lower().strip()
            
        # check if the email in the database
        password_hash = search_database("hash", "users", "email", entered_email)

        # If the email is not in the database or if the password is incorrect
        if (not password_hash) or (not check_password_hash(password_hash, entered_password)): # type: ignore
            return apology("The email or password you entered is incorrect.")

        user_name = search_database("name", "users", "email", entered_email)

        # adding user info incase needed inside the beemail (easier access)
        session["login_success"] = "True"  # login indicator
        session["user_email"] = entered_email
        session["user_name"] = user_name
        session["user_hash"] = password_hash

        return redirect("/")
      

@app.route("/verify", methods=["GET", "POST"])
def verify_identity():
    """
    Handles email verification before accessing the reset password page.

    On GET, renders the verification page. On POST, validates the email, 
    retrieves the security question, and stores it in the session if valid.
    Returns an error if the email is invalid or not found.
    """

    if request.method == "GET":
        return render_template("verify.html")
    else:  # POST
        email = request.form.get("email")
        if not validate_email(email): # type: ignore
            return apology("Oops! Invalid email. Ensure it includes a username, the domain '@beemail.hive', " + 
                           "starts with a letter, and only uses periods, underscores, or hyphens as special characters.")
        
        question_type = search_database("question", "users", "email", email)
        if not question_type:  # question_type == None
            return apology("No email matching this entry was found!")
        else:
            session["question_type"] = question_type
            session["user_email"] = email
            return redirect("/verifqs")


@app.route("/verifqs", methods=["GET", "POST"])
@user_email_required
def verif_qs():
    """
    Handles user verification for password reset access.

    On GET, displays the security question. On POST, checks if the 
    provided answer matches the stored one. If correct, grants access 
    to the reset page. Returns an error if the answer is missing or 
    incorrect.
    """

    if request.method == "GET":
        question_type = session["question_type"]
        question = VERIFICATION_QUESTIONS[question_type]
        return render_template("verifqs.html", question=question)
    else:  # POST
        user_answer = request.form.get("answer")
        if not user_answer:
            return apology("You did not provide an answer to the question.")
        else:
            user_answer = user_answer.lower().strip()

        user_email = session["user_email"].lower().strip()
        correct_answer = search_database("answer", "users", "email", user_email)

        if user_answer != correct_answer:
            return apology("The answer you provided is incorrect.")
        
        session["user_verified"] = "True"
        return redirect("/pre_reset")
    

@app.route("/pre_reset", methods=["GET", "POST"])
@verified_user_required
def pre_login_reset():
    """
    Handles password reset for verified users.

    On GET, renders the reset page. On POST, validates and confirms 
    the new password. If valid, hashes and updates it in the database, 
    clears the session, and redirects to the login page.
    """

    if request.method == "GET":
        return render_template("pre_reset.html")
    else:
        new_pass = request.form.get("new_pass")
        conf = request.form.get("confirmation")

        if not new_pass:
            return apology("Oops! You forgot to enter your password.")
        elif not conf:
            return apology("Oops! You forgot to enter the password confirmation.")
        elif new_pass.strip() != conf.strip() or not 8 <= len(new_pass.strip()) <= 16:
            return apology("Oops! The password you entered is invalid, " + 
                           "Please ensure that your password matches the confirmation field and is between 8 and 16 characters in length.")
        else:
            hash = generate_password_hash(new_pass.strip())
            user_email = session["user_email"].strip().lower()
            cur.execute("UPDATE users SET hash = ? WHERE email = ?", (hash, user_email))
            db.commit()
            session.clear()
            return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle the user registration process with validation and database insertion.

    On GET request, renders the registration page with available verification questions.
    On POST request, validates the user's input, including name, email, password, and verification question.
    Ensures all fields are filled, the email is valid, and the password meets length requirements.
    If the inputs are valid, processes the data and inserts it into the database after hashing the password.
    Handles errors for duplicate emails or unexpected issues during insertion.
    Redirects to the login page upon successful registration.
    """

    if request.method == "GET":
        return render_template("register.html", questions=VERIFICATION_QUESTIONS)
    else:  # POST
        # all case insensitive data will be set to lower case to avoid any problems in the database
        full_name = request.form.get("name")
        email = request.form.get("email")  
        password = request.form.get("password") 
        confirmation = request.form.get("confirmation")
        question = request.form.get("question")
        answer = request.form.get("answer")

        if not full_name:
            return apology("Oops! You forgot to enter your name.")
        elif not email:
            return apology("Oops! You forgot to enter your email.")
        elif not password:
            return apology("Oops! You forgot to enter your password.")
        elif not confirmation:
            return apology("Oops! You forgot to enter the password confirmation.")
        elif not question:
            return apology("Oops! You forgot to select a question.")
        elif not answer:
            return apology("Oops! You forgot to enter your answer to the verification question.")
        elif not validate_email(email.lower()):
            return apology("Oops! Invalid email. Ensure it includes a username, the domain '@beemail.hive', " + 
                           "starts with a letter, and only uses periods, underscores, or hyphens as special characters.")
        elif password.strip() != confirmation.strip() or not 8 <= len(password.strip()) <= 16:
            return apology("Oops! The password you entered is invalid, " + 
                           "Please ensure that your password matches the confirmation field and is between 8 and 16 characters in length.")
        
        else: # all the input are  valid

            # Preparing data to before being entered in the database
            modified_full_name = full_name.title()
            modified_email = email.lower()
            password = password.strip()
            question = question.lower()  # The question key not the question it self
            answer = answer.lower()

            hash = generate_password_hash(password)

            
            try:  # Inserting the data into the database
                cur.execute("INSERT INTO users(name, email, hash, question, answer) VALUES(?, ?, ?, ?, ?)", 
                            (modified_full_name, modified_email, hash, question, answer))    
            except sqlite3.IntegrityError:
                return apology("The email you entered is already in use!")
            except:
                return apology("An unexpected issue has occurred. Please try again later.")
            else:
                db.commit()  # save changes
                return redirect("/login")


@app.route("/inbox")
@login_required
def inbox():
    """
    Display the user's inbox messages.

    This route is accessible only to logged-in users.
    It fetches the current user's email from the session, ensuring it's in the correct format.
    Then, it queries the database to get the user's received messages from the `message_details` and `user_messages` tables.
    The query orders the messages by the most recent (`id DESC`).
    The fetched messages are passed to the `inbox.html` template for display.
    """

    # Get the current user's email from the session, and ensure it's properly formatted
    curr_user = session["user_email"].lower().strip()

    # Define the SQL query for retrieving the messages
    query = """
        SELECT id, recipient_email, subject, date, time, status, type, sender_email
        FROM message_details
        JOIN user_messages ON user_messages.message_id = message_details.id
        WHERE user_messages.recipient_email = ?
        ORDER BY id DESC
    """

    # Execute the query and fetch all results
    cur.execute(query, (curr_user,))
    messages_list = cur.fetchall()

    # Now, `messages_list` contains all the retrieved messages
    return render_template("inbox.html", mails=messages_list)


@app.route("/sent")
@login_required
def sent():
    """
    Display the user's sent messages.

    This route is accessible only to logged-in users.
    It fetches the current user's email from the session, ensuring it's in the correct format.
    Then, it queries the database to get the user's sent messages from the `message_details` and `user_messages` tables.
    The query orders the messages by the most recent (`id DESC`).
    The fetched messages are passed to the `sent.html` template for display.
    """

    # Get the current user's email from the session, and ensure it's properly formatted
    curr_user = session["user_email"].lower().strip()

    # Define the SQL query for retrieving the messages
    query = """
        SELECT id, recipient_email, subject, date, time, status, type, sender_email
        FROM message_details
        JOIN user_messages ON user_messages.message_id = message_details.id
        WHERE user_messages.sender_email = ?
        ORDER BY id DESC
    """

    # Execute the query and fetch all results
    cur.execute(query, (curr_user,))
    messages_list = cur.fetchall()

    # Now, `messages_list` contains all the retrieved messages
    return render_template("sent.html", mails=messages_list)


@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    """
    Handles composing and sending emails.

    On GET, renders the compose email page. On POST, validates the input fields 
    like recipient, subject, and content. Checks if the recipient email exists in 
    the system. Inserts the message into the database 
    and associates it with the sender and recipient. Returns an error if any 
    validation fails or database issues occur.
    """

    if request.method == "GET":
        return render_template("compose.html")
    else:
        recipient_email = request.form.get("recipient")
        subject = request.form.get("subject")
        content = request.form.get("content")

        if not recipient_email or not subject or not content:
            return apology("Please ensure that all required fields for the email are filled in. Do not leave any areas empty.")
        elif not validate_email(recipient_email):
            return apology("Oops! Invalid recipient email. Ensure it includes a username, the domain '@beemail.hive', " + 
                           "starts with a letter, and only uses periods, underscores, or hyphens as special characters.")
        
        # Check if the recipient email is in the database:
        recipient_search = search_database("email", "users", "email", recipient_email.lower())
        if not recipient_search:
            return apology("The recipient email entered is invalid; no such email exists in our system.")
        
        sender_email = session["user_email"]
        if (recipient_email.lower().strip() == sender_email.strip().lower()):
            return apology("You can't send email to your self!")
        
        # just to make things looks better and avid any errors
        if len(subject) > 20 or len(content) > 250:
            return apology("The content or subject exceeds the maximum allowed length. Please shorten it and try again.")

        curr_date = get_date()
        curr_time = get_time()

        # Define the queries
        insert_query = """
            INSERT INTO message_details(subject, content, date, time, type)
            VALUES(?, ?, ?, ?, ?)
        """

        delete_query = """
            DELETE FROM message_details
            WHERE subject = ? AND content = ? AND date = ? AND time = ?
        """

        select_query = """
            SELECT id 
            FROM message_details 
            WHERE subject = ? AND content = ? AND date = ? AND time = ?
        """

        # Adding the message to the database
        try:
            # Insert the new message
            cur.execute(insert_query, (subject, content, curr_date, curr_time, "primary"))
            db.commit()
        except Exception as e:
            # In case of an error, delete the message and return an apology
            cur.execute(delete_query, (subject, content, curr_date, curr_time))
            db.commit()
            return apology("An error occurred while attempting to send your message. Please try again later.")

        # Retrieve the message ID if insertion was successful
        cur.execute(select_query, (subject, content, curr_date, curr_time))
        message_id = cur.fetchone()[0]

        # Now, `message_id` contains the ID of the inserted message

        # Inserting the message into the user messages database
        cur.execute("INSERT INTO user_messages(sender_email, recipient_email, message_id) VALUES(?, ?, ?)",
                    (sender_email, recipient_email, message_id))
        db.commit()
        return redirect("/sent")


@app.route("/view/<message_id>")
@login_required
def view_message(message_id):
    """
    View the details of a specific message.

    This route is accessible only to logged-in users.
    It retrieves the details of a message based on the provided `message_id` parameter from the URL.
    The function queries the database to fetch the message's content, recipient, sender, subject, and other relevant details.
    It also checks if the message is a response and retrieves the parent message's subject if applicable.

    If the current user is the recipient, the message status is updated to 'read' (status = 1).
    The message details, along with any parent message subject, are passed to the `view.html` template for display.
    """

    # Define the SQL query to retrieve the message details
    query = """
        SELECT id, recipient_email, subject, date, time, status, type, sender_email, content
        FROM message_details
        JOIN user_messages ON user_messages.message_id = message_details.id
        WHERE message_details.id = ?
    """

    # Execute the query and fetch the result
    cur.execute(query, (message_id,))

    # Get the first result (or None if no match is found)
    mail = cur.fetchone()
    
    recipient = mail[1].lower().strip()
    curr_user = session["user_email"].lower().strip()

    parent_id = search_database("parent_id", "responses", "response_id", mail[0])
    parent_subject = None

    if parent_id:
        parent_subject = search_database("subject", "message_details", "id", parent_id)

    if recipient == curr_user:
        # Changing the mail status
        cur.execute("UPDATE message_details SET status = 1 WHERE id = ?", (message_id,))
        db.commit()

    return render_template("view.html", mail=mail, parent_id=parent_id, parent_subject=parent_subject)


@app.route("/reply/<parent_id>", methods=["GET", "POST"])
@login_required
def reply(parent_id):
    """
    Handles replying to a message.

    If the request is GET, it renders a reply form. If POST, it:
    - Retrieves the recipient's email.
    - Validates the subject and content.
    - Adds the reply to the database and links it to the original message.
    - Redirects the user to the "sent" page after successful submission.
    """

    if request.method == "GET":
        return render_template("reply.html", parent_id=parent_id)
    else:
        recipient_email = search_database("sender_email", "user_messages", "message_id", parent_id).strip().lower()
        sender_email = session["user_email"].lower().strip()
        subject = request.form.get("subject")
        content = request.form.get("content")

        if not subject or not content:
            return apology("Please ensure that all required fields for the email are filled in. Do not leave any areas empty.")
        
        # just to make things looks better and aovid any errors
        if len(subject) > 20 or len(content) > 250:
            return apology("The content or subject exceeds the maximum allowed length. Please shorten it and try again.")

        curr_date = get_date()
        curr_time = get_time()

        # Adding the message to the database
        cur.execute("INSERT INTO message_details(subject, content, date, time, type) VALUES(?, ?, ?, ?, ?)",
                    (subject, content, curr_date, curr_time, "reply"))
        db.commit()
        
        message_id = search_database("id", "message_details", "time", curr_time)

        cur.execute("INSERT INTO user_messages(sender_email, recipient_email, message_id) VALUES(?, ?, ?)",
                    (sender_email, recipient_email, message_id))
        db.commit()
        
        # Now insert the emails inside the responses database:
        cur.execute("INSERT INTO responses(parent_id, response_id) VALUES(?, ?)",
                    (parent_id, message_id))
        db.commit()

        return redirect("/sent")
    

@app.route("/responses/<parent_id>")
@login_required
def responses(parent_id):
    """
    Handles displaying the responses to a parent message.

    It retrieves all reply messages for the current user related to the specified parent message.
    The results are rendered in the "responses.html" template.
    """

    # Get the current user's email from the session, and ensure it's properly formatted
    curr_user = session["user_email"].lower().strip()

    # Define the SQL query to retrieve the response messages
    query = """
        SELECT id, recipient_email, subject, date, time, status, type, sender_email
        FROM message_details
        JOIN user_messages ON user_messages.message_id = message_details.id
        WHERE user_messages.recipient_email = ?
        AND type = 'reply'
        AND id IN (SELECT response_id FROM responses WHERE parent_id = ?)
        ORDER BY id DESC
    """

    # Execute the query and fetch all the results
    cur.execute(query, (curr_user, parent_id))

    # Fetch all the rows (messages) into `messages_list`
    messages_list = cur.fetchall()

    # Render the template with the fetched messages
    return render_template("responses.html", mails=messages_list)


@app.route("/new_responses")
@login_required
def new_responses():
    """
    Displays new response messages for the current user.

    It retrieves all unread reply messages for the user and renders them in the "new_responses.html" template.
    """

    # Get the current user's email from the session and ensure it's formatted
    curr_user = session["user_email"].lower().strip()

    # Define the SQL query to retrieve new response messages
    query = """
        SELECT id, recipient_email, subject, date, time, status, type, sender_email
        FROM message_details
        JOIN user_messages ON user_messages.message_id = message_details.id
        WHERE user_messages.recipient_email = ?
        AND type = 'reply'
        AND status = 0
        ORDER BY id DESC
    """

    # Execute the query and fetch all the results
    cur.execute(query, (curr_user,))

    # Fetch all rows into `messages_list`
    messages_list = cur.fetchall()

    # Render the template with the fetched messages
    return render_template("new_responses.html", mails=messages_list)


@app.route("/new_primary")
@login_required
def new_primary():  # access only from index page (modify the code)
    """
    Displays new primary messages for the current user.

    It retrieves all unread primary messages for the user and renders them in the "new_primary.html" template.
    """

    curr_user = session["user_email"].lower().strip()

    query = (
        "SELECT id, recipient_email, subject, date, time, status, type, sender_email "
        "FROM message_details "
        "JOIN user_messages ON user_messages.message_id = message_details.id "
        "WHERE user_messages.recipient_email = ? AND type = 'primary' AND status = 0 "
        "ORDER BY id DESC"
    )

    data = cur.execute(query, (curr_user,))
    messages_list = data.fetchall()

    return render_template("new_primary.html", mails=messages_list)


@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():   
    """
    Handles the password reset functionality for the current user.

    It allows the user to change their password by providing the current password, a new password, 
    and confirmation of the new password. The function verifies the inputs, checks if the current 
    password matches the stored password, and updates the password in the database if valid.
    """

    if request.method == "GET":
        return render_template("reset.html")
    else:
        old_pass = request.form.get("old_pass")
        new_pass = request.form.get("new_pass")
        conf = request.form.get("confirmation")

        if not old_pass:
            return apology("Oops! You forgot to enter your current password.")
        elif not new_pass:
            return apology("Oops! You forgot to enter your new password.")
        elif not conf:
            return apology("Oops! You forgot to enter the new password confirmation.")
        elif new_pass.strip() != conf.strip() or not 8 <= len(new_pass.strip()) <= 16:
            return apology("Oops! The password you entered is invalid, " + 
                           "Please ensure that your password matches the confirmation field and is between 8 and 16 characters in length.")

        old_pass_hash = session["user_hash"]
        if not check_password_hash(old_pass_hash, old_pass.strip()):
            return apology("Oops! The password you entered is incorrect.")

        hash = generate_password_hash(new_pass.strip())
        user_email = session["user_email"].strip().lower()
        cur.execute("UPDATE users SET hash = ? WHERE email = ?", (hash, user_email))
        db.commit()

        return redirect("/")


@app.route("/profile")
@login_required
def profile():
    """
    Displays the profile page for the current user.

    It retrieves the user's name, email, and verification question/answer from the 
    database and renders the information on the profile page.
    """

    name = session["user_name"]
    email = session["user_email"]

    verif_key = search_database("question", "users", "email", email.strip().lower())
    verif_qs = VERIFICATION_QUESTIONS[verif_key]
    verif_ansr = search_database("answer", "users", "email", email.strip().lower())  

    return render_template("profile.html", name=name, email=email, verif_ansr=verif_ansr, verif_qs=verif_qs)


@app.route("/new_verif", methods=["GET", "POST"])
@login_required
def new_verif():    
    """
    Handles the creation or update of the user's verification question and answer.

    If the request method is GET, it renders the "new_verif.html" template with available 
    verification questions. If the method is POST, it updates the user's selected verification 
    question and answer in the database.
    """

    if request.method == "GET":
        return render_template("new_verif.html", questions=VERIFICATION_QUESTIONS)
    else:
        question = request.form.get("question")
        answer = request.form.get("answer")
    
        if not question:
            return apology("Oops! You forgot to select a question.")
        elif not answer:
            return apology("Oops! You forgot to enter your answer to the verification question.")
    
        question = question.lower()  # The question key not the question it self
        answer = answer.lower()   
            

        user_email = session["user_email"].strip().lower()
        cur.execute("UPDATE users SET question = ? WHERE email = ?", (question, user_email))
        db.commit()

        cur.execute("UPDATE users SET answer = ? WHERE email = ?", (answer, user_email))
        db.commit()

        return redirect("/profile")


@app.route("/new_name", methods=["GET", "POST"])
@login_required
def new_name():    
    """
    Handles the update of the user's name.

    If the request method is GET, it renders the "new_name.html" template. 
    If the method is POST, it updates the user's name in the database and updates the session to 
    reflect the new name, then redirects to the profile page.
    """

    if request.method == "GET":
        return render_template("new_name.html")
    else:
        name = request.form.get("name")
    
        if not name:
            return apology("Oops! You forgot to enter your name.")
    
        name = name.title() 
            

        user_email = session["user_email"].strip().lower()
        cur.execute("UPDATE users SET name = ? WHERE email = ?", (name, user_email))
        db.commit()

        session["user_name"] = name  # to update in the profile too

        return redirect("/profile")


if __name__== "__main__":
    app.run()


db.commit()  # to apply changes
db.close()


