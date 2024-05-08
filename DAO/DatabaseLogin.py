from DAO import DatabaseInit as DAOInit

def get_user_data(username):
    """
    Retrieves user data from the 'USER' table based on the given username.

    Args:
        username (str): The username to search for in the database.

    Returns:
        tuple or None: A tuple containing user data if found, otherwise None.
    """
    connection = DAOInit.connect_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM USER WHERE UserName = %s", (username,))
    user_data = cursor.fetchone()
    connection.close()
    return user_data

def add_user(username, password):
    """
    Adds a new user to the 'USER' table.

    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.

    Returns:
        bool: True if the user was added successfully, False otherwise.
    """
    connection = DAOInit.connect_mysql()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO USER (UserName, Password) VALUES (%s, %s)", (username, password))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print("Error:", e)
        connection.rollback()
        connection.close()
        return False
