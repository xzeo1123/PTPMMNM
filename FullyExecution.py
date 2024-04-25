import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from tensorflow.keras.preprocessing import image # type: ignore
from tensorflow.keras.models import load_model # type: ignore
import mysql.connector

# Load emotion model
emotion_model_path = os.path.join(os.path.dirname(__file__), 'trained_emotion.h5')
emotion_model = load_model(emotion_model_path)

# Load gender model
gender_model_path = os.path.join(os.path.dirname(__file__), 'trained_gender.h5')
gender_model = load_model(gender_model_path)

# Model Params
img_size = 100

# Emotion mapping
emotion_mapping = {
    0: 'surprise',
    1: 'fear',
    2: 'disgust',
    3: 'happy',
    4: 'sad',
    5: 'angry',
    6: 'neutral'
}

# Gender mapping
gender_mapping = {
    0: 'man',
    1: 'woman'
}

def connect_mysql():
    connection = mysql.connector.connect (
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'mnm_project'  # Thay đổi tên cơ sở dữ liệu tại đây
    )
    return connection

def create_predict_table_if_not_exists():
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PREDICT (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Image VARCHAR(255),
            Name VARCHAR(255),
            PredictGender VARCHAR(50),
            PredictEmotion VARCHAR(50)
        )
    """)
    connection.commit()
    connection.close()

def fetch_image_names():
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT Name FROM PREDICT")
    image_names = [row[0] for row in cursor.fetchall()]
    connection.close()
    return image_names

def load_image_from_db(image_name):
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT Image, PredictGender, PredictEmotion FROM PREDICT WHERE Name = %s", (image_name,))
    result = cursor.fetchone()
    connection.close()
    return result

def update_combobox():
    image_names = fetch_image_names()
    combo_image['values'] = image_names

def predict_emotion(image_path):
    img = image.load_img(image_path, target_size=(img_size, img_size))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    pred_label = emotion_model.predict(img_array)
    pred_label = np.argmax(pred_label)
    return emotion_mapping[pred_label]

def predict_gender(image_path):
    img = image.load_img(image_path, target_size=(img_size, img_size))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    pred_label = gender_model.predict(img_array)
    pred_label = np.argmax(pred_label)
    return gender_mapping[pred_label]

def predict_emotion_and_gender(image_path):
    predicted_emotion = predict_emotion(image_path)
    predicted_gender = predict_gender(image_path)
    return predicted_emotion, predicted_gender

def browse_image():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filename:
        show_image(filename)
        predicted_emotion, predicted_gender = predict_emotion_and_gender(filename)
        label_result.config(text="Predicted emotion: " + predicted_emotion + "\nPredicted gender: " + predicted_gender)
        save_prediction_to_db(filename, predicted_emotion, predicted_gender)
        update_combobox()

def show_image(filename):
    img = Image.open(filename)
    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    label_image.config(image=img)
    label_image.image = img

def save_prediction_to_db(image_path, predicted_emotion, predicted_gender):
    image_name = os.path.basename(image_path)
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO PREDICT (Image, Name, PredictGender, PredictEmotion) VALUES (%s, %s, %s, %s)",
                   (image_path, image_name, predicted_gender, predicted_emotion))
    connection.commit()
    connection.close()

def load_image_and_prediction(event):
    selected_image = combo_image.get()
    image_info = load_image_from_db(selected_image)
    if image_info:
        image_path, predicted_gender, predicted_emotion = image_info
        show_image(image_path)
        label_result.config(text="Predicted emotion: " + predicted_emotion + "\nPredicted gender: " + predicted_gender)

create_predict_table_if_not_exists()

# Create GUI
root = tk.Tk()
root.title("Emotion and Gender Recognition")
root.geometry("400x400")

label_select = tk.Label(root, text="Select an image:")
label_select.pack()

combo_image = ttk.Combobox(root, state="readonly")
combo_image.pack()
update_combobox()
combo_image.bind("<<ComboboxSelected>>", load_image_and_prediction)

button_browse = tk.Button(root, text="Browse", command=browse_image)
button_browse.pack()

label_image = tk.Label(root)
label_image.pack()

label_result = tk.Label(root, text="", justify="left")
label_result.pack()

root.mainloop()