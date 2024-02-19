import bcrypt

# A mock, in-memory "database" of users. Each "row" includes the
# user's hashed password, the salt used to generate the password hash,
# and an "auth token". On successful login, the token is stored in
# browser local storage and is used to automatically authenticate the
# user on subsequent visits. Separating the token from the password in
# principle allows "expiring" tokens without affecting the login info,
# and allows auto-logging-in users without storing the password hash
# or salt in the browser. Token expiration is not demonstrated in this
# demo app.
users = [
    dict(
        name="Bob",
        username="bob",
        password="$2b$12$wDkN1RDLRC0XGIWR9mmTteqLtN.IGbTdPR4hFU2ENKUGLaWlnJ.am",
        salt="$2b$12$wDkN1RDLRC0XGIWR9mmTte",
        token="86229503f083477c9a4fef21f9de5ff1",
    ),
    dict(
        name="Lydia",
        username="lydia",
        password="$2b$12$xSuQSAPftsDxcSUcHBab5.QYb1W1Zn83Wyr5dcr9o23m2xxj0DJ9m",
        salt="$2b$12$xSuQSAPftsDxcSUcHBab5.",
        token="1e24b86f845849e6ac32aa1778aba958",
    ),
]


def get_user_by_token(token):
    return next((user for user in users if user["token"] == token), None)


def get_user_by_username(username):
    return next(
        (user for user in users if user["username"] == username),
        None,
    )


def gen_salted_password(passwd):
    """
    This function is unused in the app but was used to generate the
    hashed password and salt stored for each user in the
    'database'. Here for reference.
    """

    # Encode password to bytes
    passwd_bytes = passwd.encode("utf-8")

    # Generate salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_passwd = bcrypt.hashpw(passwd_bytes, salt)

    # Return the hashed password and salt both as decoded strings
    return hashed_passwd.decode("utf-8"), salt.decode("utf-8")


def check_password(passwd, hashed_passwd, stored_salt):
    """
    Takes the user-input password, and the hashed password and salt
    stored in the DB and checks if the password in the DB matches the
    user-input password.
    """

    # Encode the password, hashed password, and the salt to bytes
    passwd_bytes = passwd.encode("utf-8")
    hashed_passwd_bytes = hashed_passwd.encode("utf-8")
    salt_bytes = stored_salt.encode("utf-8")

    # Compute a hashed version of the provided password using the stored salt
    computed_hash = bcrypt.hashpw(passwd_bytes, salt_bytes)

    # Check if the computed hash matches the stored hash
    return computed_hash == hashed_passwd_bytes


def check_login(username, password):
    user = get_user_by_username(username)
    if not user:
        return None
    if check_password(password, user["password"], user["salt"]):
        return user
