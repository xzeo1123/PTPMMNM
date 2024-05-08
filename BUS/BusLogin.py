from DAO import DatabaseLogin as DAOLogin

def sign_in(username, password):
    """
    Validates user credentials for sign-in.

    Args:
        username (str): The username provided by the user.
        password (str): The password provided by the user.

    Returns:
        tuple: A tuple containing a message indicating the result of the sign-in attempt and the user ID if successful.
    """
    user_data = DAOLogin.get_user_data(username)
    if user_data:
        if password == user_data[2]:
            return "Login successfully", user_data[0]
        else:
            return "Wrong username or password", None
    else:
        return "Invalid username", None

def sign_up(username, password):
    """
    Registers a new user.

    Args:
        username (str): The username provided by the user.
        password (str): The password provided by the user.

    Returns:
        bool: True if the user is successfully registered, False otherwise.
    """
    return DAOLogin.add_user(username, password)
