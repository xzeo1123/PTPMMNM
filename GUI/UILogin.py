import sys
sys.path.append(r"D:\My Folder\Studying\N4HK2\MNM\ProjectMNM")

import tkinter as tk
from DAO import DatabaseInit
from BUS import BusLogin
from GUI import UIPredict
from PIL import Image, ImageTk
    
def set_background_image(canvas):
    image_path = "imgs/login.jpg"
    image = Image.open(image_path)
    image = image.resize((400, 400), Image.FIXED)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo

def sign_in():
    username = entry_username.get()
    password = entry_password.get()
    result, user_id = BusLogin.sign_in(username, password)
    if result == "Login successfully":
        canvas.itemconfig(label_message, text="")
        root.withdraw()
        open_new_UI(user_id)
    else:
        canvas.itemconfig(label_message, text=result)
        entry_username.focus_set()

def sign_up():
    username = entry_username.get()
    password = entry_password.get()
    result = BusLogin.sign_up(username, password)
    canvas.itemconfig(label_message, text=result)

def open_new_UI(user_id):
    UIPredict.main(user_id)

DatabaseInit.create_database_if_not_exists()
DatabaseInit.create_tables_if_not_exists()

root = tk.Tk()
root.title("AI PREDICTION APP")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - 400) // 2
y_position = (screen_height - 400) // 2

root.geometry("400x400+{}+{}".format(x_position, y_position))

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

set_background_image(canvas)

canvas.create_text(200, 70, text="LOGIN", font=("Times New Roman", 25, "bold"), fill="white")

small_font = ("Times New Roman", 12)

canvas.create_text(50, 150, text="Username:", anchor="w", font=small_font, fill="white")
entry_username = tk.Entry(root, width=25, font=small_font)
entry_username_window = canvas.create_window(210, 150, window=entry_username, anchor="e")

canvas.create_text(50, 190, text="Password:", anchor="w", font=small_font, fill="white")
entry_password = tk.Entry(root, show="*", width=25, font=small_font) 
entry_password_window = canvas.create_window(210, 190, window=entry_password, anchor="e")

frame_main_button = tk.Frame(canvas, width=300, bg="", highlightthickness=0, bd=0)
frame_main_button.place(relx=0.5, rely=0.7, anchor="center")

button_sign_in = tk.Button(frame_main_button, text="Sign In", command=sign_in, width=10, font=small_font)
button_sign_in.pack(side="left", padx=(0, 30))

button_sign_up = tk.Button(frame_main_button, text="Sign Up", command=sign_up, width=10, font=small_font)
button_sign_up.pack(side="left")

label_message = canvas.create_text(150, 250, text="", font=small_font, fill="red")

canvas.move(entry_username_window, 125, 0)
canvas.move(entry_password_window, 125, 0)

root.mainloop()
