import re  # to use regexes in confirming input (emails)
from flask import redirect, render_template, session
from functools import wraps
from datetime import datetime

# Code snippet taken from problem set 9 - finance - (CS50X 2024)
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("login_success") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def verified_user_required(f):
    """
    Decorator to enforce that a user is verified.

    This ensures that the session variable 'user_verified' is set
    to a value other than 'None'. If the user is not verified,
    they are redirected to the '/verify' route.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_verified") is None:
            return redirect("/verify")
        return f(*args, **kwargs)

    return decorated_function


def user_email_required(f):
    """
    Decorator to require a user's email.

    This checks if the 'user_email' session variable is set.
    If not, the user is redirected to the '/verify' route.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_email") is None:
            return redirect("/verify")
        return f(*args, **kwargs)

    return decorated_function


# Code snippet taken from problem set 9 - finance - (CS50X 2024)
def apology(message, code=400):
    """Render message as an apology to user"""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def get_date() -> str:
    """Returns the current date in the form of: year-month-day"""
    time = datetime.now()
    current_date = f"{time.year}-{time.month}-{time.day}"
    return current_date


def get_time() -> str:
    """Returns the current time in the form of: hour:minutes:seconds"""
    time = datetime.now()
    current_time = f"{time.hour}:{time.minute}:{time.second}"
    return current_time


def validate_email(email: str) -> bool:
    """
    Validate an email address.

    Checks if the given email matches the required pattern:
    - Starts with letters.
    - May include dots, underscores, or hyphens.
    - Ends with '@beemail.hive'.
    Returns True if the email is valid, otherwise False.
    """
    pattern = r"^[a-zA-Z]+[-_.a-zA-Z0-9]*@beemail.hive$"
    match = re.search(pattern, email)
    if match:
        return True
    else:
        return False