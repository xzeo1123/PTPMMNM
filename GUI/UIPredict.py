import tkinter as tk
from tkinter import ttk
from BUS import BusPredict as BUSPredict
from PIL import Image, ImageTk

# Tab predict
def create_prediction_tab(tab, user_id):
    tab_canvas = tk.Canvas(tab, width=600, height=600)
    tab_canvas.pack()
    
    set_background_image_for_tab(tab_canvas)
    
    main_font = ("Times New Roman", 12)
    small_font = ("Times New Roman", 10)
    
    # Text place
    tab_canvas.create_text(300, 70, text="MAKE A PREDICTION", font=("Times New Roman", 20, "bold"), fill="white")
    tab_canvas.create_text(180, 140, text="Select an image", font=main_font, anchor="w", fill="white")
    tab_canvas.create_text(345, 140, text="or", font=main_font, anchor="w", fill="white")
    predict_label_result = tab_canvas.create_text(225, 370, text="", font=main_font, fill="white", anchor="w")
    tab_canvas.create_text(305, 450, text="Is this prediction correct?", font=main_font, fill="white")
    
    # Input image place
    predict_canvas_image = tk.Canvas(tab_canvas, width=150, height=150)
    predict_canvas_image.place(x=225, y=170)
    set_user_image(predict_canvas_image)
        
    # Combobox feedback place
    emotion_combobox = ttk.Combobox(tab_canvas, values=['surprise', 'fear', 'disgust', 'happy', 'sad', 'angry', 'neutral'], font=small_font)
    emotion_combobox.place(x=230, y=480)
    emotion_combobox.current(0)  
    
    gender_combobox = ttk.Combobox(tab_canvas, values=['woman', 'man'], font=small_font)
    gender_combobox.place(x=230, y=510)
    gender_combobox.current(0)
    
    # Button place
    predict_button_browse = tk.Button(tab_canvas, text="Browse", font=small_font, 
        command=lambda: browse_and_update_result(predict_canvas_image, predict_label_result, user_id))
    tab_canvas.create_window(310, 140, anchor="center", window=predict_button_browse)

    predict_button_camera = tk.Button(tab_canvas, text="Take a picture", font=small_font, 
        command=lambda: browse_image_from_camera(predict_canvas_image, predict_label_result, user_id))
    tab_canvas.create_window(410, 140, anchor="center", window=predict_button_camera)
    
    predict_feedback_button = tk.Button(tab_canvas, text="Feedback", font=small_font, 
        command=lambda: BUSPredict.save_feedback(user_id, gender_combobox.get(), emotion_combobox.get()))
    tab_canvas.create_window(300, 550, anchor="center", window=predict_feedback_button)

    # Button functions
    def browse_and_update_result(predict_canvas_image, predict_label_result, user_id):
        result_image, result_predict = BUSPredict.browse_image(user_id)
        predict_canvas_image.create_image(0, 0, anchor="nw", image=result_image) 
        predict_canvas_image.image = result_image
        tab_canvas.itemconfig(predict_label_result, text=result_predict)
        
        predicted_emotion, predicted_gender = result_predict.split('\n\n')[0].split(': ')[1], result_predict.split('\n\n')[1].split(': ')[1]

        emotion_index = emotion_combobox['values'].index(predicted_emotion)
        gender_index = gender_combobox['values'].index(predicted_gender)

        emotion_combobox.current(emotion_index)
        gender_combobox.current(gender_index)
        
    def browse_image_from_camera(predict_canvas_image, predict_label_result, user_id):
        result_image, result_predict = BUSPredict.browse_image_from_camera(user_id)
        predict_canvas_image.create_image(0, 0, anchor="nw", image=result_image) 
        predict_canvas_image.image = result_image
        tab_canvas.itemconfig(predict_label_result, text=result_predict)
        
        predicted_emotion, predicted_gender = result_predict.split('\n\n')[0].split(': ')[1], result_predict.split('\n\n')[1].split(': ')[1]

        emotion_index = emotion_combobox['values'].index(predicted_emotion)
        gender_index = gender_combobox['values'].index(predicted_gender)

        emotion_combobox.current(emotion_index)
        gender_combobox.current(gender_index)


# Tab history
def create_history_tab(tab, user_id):
    tab_canvas = tk.Canvas(tab, width=600, height=600)
    tab_canvas.pack()
    
    set_background_image_for_tab(tab_canvas)
    
    main_font = ("Times New Roman", 12)
    small_font = ("Times New Roman", 10)
    
    # Text place
    tab_canvas.create_text(300, 70, text="YOUR PREDICT HISTORY", font=("Times New Roman", 20, "bold"), fill="white")
    tab_canvas.create_text(220, 160, text="Select an image: ", font=main_font, fill="white")
    tab_canvas.create_text(225, 470, text="Your feedback prediction", font=main_font, fill="white", anchor="w")
    history_label_AI_result = tab_canvas.create_text(225, 390, text="", font=main_font, fill="white", anchor="w")
    history_label_feedback_result = tab_canvas.create_text(225, 520, text="", font=main_font, fill="white", anchor="w")
    
    # Combobox place to get predicted values
    history_combo_image = ttk.Combobox(tab_canvas, state="readonly")
    history_combo_image.pack()
    BUSPredict.update_combobox(user_id, history_combo_image)
    history_combo_image.bind(
        "<<ComboboxSelected>>", lambda event: load(
            history_combo_image, history_canvas_image, history_label_AI_result, history_label_feedback_result
        )
    )
    tab_canvas.create_window(350, 160, width=150, height=20, anchor="center", window=history_combo_image)
    
    # Image place to show image selected by combobox
    history_canvas_image = tk.Canvas(tab_canvas, width=150, height=150)
    history_canvas_image.place(x=225, y=200)
    set_user_image(history_canvas_image)
    
    # Button place
    # Button refresh to refresh new value for combobox
    history_refresh_button = tk.Button(tab_canvas, text="Refresh combobox", font=small_font, 
        command=lambda: BUSPredict.update_combobox(user_id, history_combo_image))
    tab_canvas.create_window(300, 130, anchor="center", window=history_refresh_button)
    
    # Combobox support function
    def load(history_como_image, history_canvas_image, history_label_AI_result, history_label_feedback_result):
        result_image, result_predict, feedback_gender, feedback_emotion = BUSPredict.load_image_and_prediction(history_como_image)
        history_canvas_image.create_image(0, 0, anchor="nw", image=result_image) 
        history_canvas_image.image = result_image
        tab_canvas.itemconfig(history_label_AI_result, text=result_predict)
        tab_canvas.itemconfig(history_label_feedback_result, text="Emotion: "+feedback_emotion+"\nGender: "+feedback_gender)

def set_background_image_for_tab(tab_canvas):
    image = Image.open("imgs/predict.jpg")
    image = image.resize((600, 600), Image.FIXED)
    photo = ImageTk.PhotoImage(image)
    tab_canvas.create_image(0, 0, anchor="nw", image=photo)
    tab_canvas.image = photo

def set_user_image(tab_canvas):
    image = Image.open("imgs/user.png")
    image = image.resize((150, 150), Image.FIXED)
    photo = ImageTk.PhotoImage(image)
    tab_canvas.create_image(0, 0, anchor="nw", image=photo)
    tab_canvas.image = photo

def main(user_id):
    root = tk.Toplevel()
    root.title("Emotion and Gender Recognition")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = (screen_width - 600) // 2
    y_position = (screen_height - 600) // 2

    root.geometry("600x600+{}+{}".format(x_position, y_position))
    
    canvas = tk.Canvas(root, width=600, height=600)
    canvas.pack()
    
    tab_control = ttk.Notebook(canvas, width=600, height=600)
    tab_prediction = ttk.Frame(tab_control)
    tab_history = ttk.Frame(tab_control)

    tab_control.add(tab_prediction, text="Prediction")
    tab_control.add(tab_history, text="History")

    create_prediction_tab(tab_prediction, user_id)
    create_history_tab(tab_history, user_id)

    tab_control.pack(expand=1, fill="both")

    root.mainloop()
