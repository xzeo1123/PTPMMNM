import os
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog
from tensorflow.keras.preprocessing import image # type: ignore
from tensorflow.keras.models import load_model # type: ignore
from DAO import DatabasePredict as DAOPredict
import io
import subprocess
import psutil
import time


emotion_model_path = os.path.join(os.path.dirname(__file__), '..', 'TrainedModel', 'trained_emotion.h5')
emotion_model = load_model(emotion_model_path)

gender_model_path = os.path.join(os.path.dirname(__file__), '..', 'TrainedModel', 'trained_gender.h5')
gender_model = load_model(gender_model_path)

img_size = 100

emotion_mapping = {
    0: 'surprise',
    1: 'fear',
    2: 'disgust',
    3: 'happy',
    4: 'sad',
    5: 'angry',
    6: 'neutral'
}

gender_mapping = {
    0: 'woman',
    1: 'man'
}

def predict_emotion(image_path):
    """
    Predicts the emotion from the given image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The predicted emotion.
    """
    img = image.load_img(image_path, target_size=(img_size, img_size))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    pred_label = emotion_model.predict(img_array)
    pred_label = np.argmax(pred_label)
    return emotion_mapping[pred_label]

def predict_gender(image_path):
    """
    Predicts the gender from the given image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The predicted gender.
    """
    img = image.load_img(image_path, target_size=(img_size, img_size))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    pred_label = gender_model.predict(img_array)
    pred_label = np.argmax(pred_label)
    return gender_mapping[pred_label]

def predict_emotion_and_gender(image_path):
    """
    Predicts both emotion and gender from the given image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        tuple: A tuple containing the predicted emotion and gender.
    """
    predicted_emotion = predict_emotion(image_path)
    predicted_gender = predict_gender(image_path)
    return predicted_emotion, predicted_gender

def browse_image(user_id):
    """
    Opens a file dialog to browse and select an image file, then predicts emotion and gender from it.

    Args:
        user_id (int): The ID of the user.

    Returns:
        tuple: A tuple containing the image data and a string with predicted emotion and gender.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        get_image = get_image_by_file_path(file_path)
        predicted_emotion, predicted_gender = predict_emotion_and_gender(file_path) 
        return_string = "AI predicted emotion: " + predicted_emotion + "\n\nAI predicted gender: " + predicted_gender
        DAOPredict.save_prediction_to_db(file_path, predicted_emotion, predicted_gender, user_id)
        return get_image, return_string 
        
def get_image_by_file_path(file_path):
    """
    Opens and resizes an image file.

    Args:
        file_path (str): The path to the image file.

    Returns:
        ImageTk.PhotoImage: An image object ready to be displayed in Tkinter.
    """
    img = Image.open(file_path)
    img = img.resize((160, 160), Image.FIXED)
    photo_img = ImageTk.PhotoImage(img)
    return photo_img
    
def load_image_and_prediction(combo_image):
    """
    Loads image data and prediction from the database based on the selected image.

    Args:
        combo_image (tkinter.ttk.Combobox): The combo box containing image names.

    Returns:
        tuple: A tuple containing the image data, a string with predicted emotion and gender, and feedback data.
    """
    selected_image = combo_image.get()
    image_info = DAOPredict.load_image_from_db(selected_image)
    if image_info:
        blob_data, predicted_gender, predicted_emotion, feedback_gender, feedback_emotion = image_info
        get_image = get_image_by_blob(blob_data)
        return_string = "AI predicted emotion: " + predicted_emotion + "\n\nAI Predicted gender: " + predicted_gender
        return get_image, return_string, feedback_gender, feedback_emotion

def get_image_by_blob(blob_data):
    """
    Converts blob data into an image object.

    Args:
        blob_data (bytes): The blob data representing the image.

    Returns:
        ImageTk.PhotoImage or None: An image object ready to be displayed in Tkinter, or None if an error occurs.
    """
    try:
        img = Image.open(io.BytesIO(blob_data))
        img = img.resize((160, 160), Image.FIXED)
        photo_img = ImageTk.PhotoImage(img)
        return photo_img
    except Exception as e:
        print("Error:", e)
        return None
        
def update_combobox(user_id, combo_image):
    """
    Updates the combo box with image names associated with the user.

    Args:
        user_id (int): The ID of the user.
        combo_image (tkinter.ttk.Combobox): The combo box to update.
    """
    image_names = DAOPredict.fetch_image_names(user_id)
    combo_image['values'] = image_names

def save_feedback(user_id, gender_feedback, emotion_feedback):
    """
    Saves feedback data to the database.

    Args:
        user_id (int): The ID of the user.
        gender_feedback (str): The feedback on gender prediction.
        emotion_feedback (str): The feedback on emotion prediction.
    """
    DAOPredict.save_feedback(user_id, gender_feedback, emotion_feedback)

# Define function to use camera for take a picture and return guesses
def is_camera_running():
    # Lặp lại qua tất cả các quy trình đang chạy
    for proc in psutil.process_iter(['pid', 'name']):
        # Kiểm tra xem có quy trình nào có tên là "WindowsCamera.exe" hay không
        if proc.info['name'] == 'WindowsCamera.exe':
            return True
    return False

def capture_image():    
    subprocess.run(["start", "microsoft.windows.camera:"], shell=True)
    
    while is_camera_running():
        time.sleep(1)
    
    latest_image = max([os.path.join("C:/Users/Admin/Pictures/Camera Roll", f) for f in os.listdir("C:/Users/Admin/Pictures/Camera Roll")], key=os.path.getctime)
    
    return latest_image

def predict_from_captured_image(user_id):
    image_path = capture_image()
    img = Image.open(image_path)
    img = img.resize((160, 160), Image.FIXED)
    photo_img = ImageTk.PhotoImage(img)
    
    if image_path:
        predicted_emotion, predicted_gender = predict_emotion_and_gender(image_path) 
        
        DAOPredict.save_prediction_to_db(image_path, predicted_emotion, predicted_gender, user_id)
        
        return photo_img, predicted_emotion, predicted_gender
    else:
        return None, None

def browse_image_from_camera(user_id):
    photo_img, predicted_emotion, predicted_gender = predict_from_captured_image(user_id)
    if predicted_emotion and predicted_gender:
        return_string = "AI predicted emotion: " + predicted_emotion + "\n\nAI predicted gender: " + predicted_gender
        return photo_img, return_string
    else:
        return None, "Failed to capture image from camera"
