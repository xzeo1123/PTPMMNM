from DAO import DatabaseInit as DAOInit
import os

def save_prediction_to_db(file_path, predicted_emotion, predicted_gender, user_id):
    """
    Saves prediction data to the 'PREDICT' table in the database.

    Args:
        file_path (str): The path to the image file.
        predicted_emotion (str): The predicted emotion.
        predicted_gender (str): The predicted gender.
        user_id (int): The ID of the user associated with the prediction.
    """
    image_name = os.path.basename(file_path)
    with open(file_path, 'rb') as file:
        blob_data = file.read()
    connection = DAOInit.connect_mysql()
    cursor = connection.cursor()
    sql_insert_query = """INSERT INTO PREDICT 
    (Image, Name, PredictGender, PredictEmotion, FeedbackGender, FeedbackEmotion, UserID) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    insert_tuple = (blob_data, image_name, predicted_gender, predicted_emotion, predicted_gender, predicted_emotion, user_id)
    cursor.execute(sql_insert_query, insert_tuple)
    connection.commit()
    cursor.close()
    connection.close()

def save_feedback(user_id, gender_feedback, emotion_feedback):
    """
    Saves feedback data to the latest prediction made by the user in the 'PREDICT' table.

    Args:
        user_id (int): The ID of the user associated with the feedback.
        gender_feedback (str): The feedback on gender prediction.
        emotion_feedback (str): The feedback on emotion prediction.
    """
    connection = DAOInit.connect_mysql()
    cursor = connection.cursor()

    sql_select_max_id = """SELECT MAX(ID) FROM PREDICT WHERE UserID = %s"""
    cursor.execute(sql_select_max_id, (user_id,))
    max_id = cursor.fetchone()[0]

    sql_update_query = """UPDATE PREDICT 
    SET FeedbackGender = %s, FeedbackEmotion = %s 
    WHERE ID = %s AND UserID = %s"""
    update_tuple = (gender_feedback, emotion_feedback, max_id, user_id)

    cursor.execute(sql_update_query, update_tuple)
    connection.commit()

    cursor.close()
    connection.close()

def fetch_image_names(user_id):
    """
    Fetches the names of images associated with a specific user from the 'PREDICT' table.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of image names associated with the user.
    """
    connection = DAOInit.connect_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT Name FROM PREDICT WHERE UserID = %s", (user_id,))
    image_names = [row[0] for row in cursor.fetchall()]
    connection.close()
    return image_names

def load_image_from_db(image_name):
    """
    Loads image data and prediction feedback from the 'PREDICT' table based on the image name.

    Args:
        image_name (str): The name of the image.

    Returns:
        tuple: A tuple containing image data, predicted gender, predicted emotion, feedback gender, and feedback emotion.
    """
    connection = DAOInit.connect_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT Image, PredictGender, PredictEmotion, FeedbackGender, FeedbackEmotion FROM PREDICT WHERE Name = %s", (image_name,))
    result = cursor.fetchone()
    connection.close()
    return result
