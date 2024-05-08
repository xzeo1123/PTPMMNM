import mysql.connector

def connect_mysql():
    """
    Connects to MySQL database.

    Returns:
        connection (mysql.connector.connection.MySQLConnection): Connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect (
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'mnm_project'
        )
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)
        return None

def create_database_if_not_exists():
    """
    Creates the 'mnm_project' database if it does not already exist.
    """
    try:
        connection = connect_mysql()
        if connection is None:
            return
        
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'mnm_project'")
        result = cursor.fetchone()
        if not result: 
            cursor.execute("CREATE DATABASE mnm_project")
        connection.close()
        print("Database created successfully.")
    except mysql.connector.Error as e:
        print("Error:", e)


def create_tables_if_not_exists():
    """
    Creates 'USER' and 'PREDICT' tables if they do not already exist in the database.
    """
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS USER (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            UserName VARCHAR(255),
            Password VARCHAR(255)
        )
    """)
    connection.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PREDICT (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Image BLOB,
            Name VARCHAR(255),
            PredictGender VARCHAR(50),
            PredictEmotion VARCHAR(50),
            FeedbackGender VARCHAR(50),
            FeedbackEmotion VARCHAR(50),
            UserID INT,
            FOREIGN KEY (UserID) REFERENCES USER(ID)
        )
    """)
    connection.commit()
    
    connection.close()
