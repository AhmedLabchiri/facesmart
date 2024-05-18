import os
import pickle

import tkinter as tk
from tkinter import messagebox
import face_recognition
from tkinter import ttk


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=1,
                        width=15,
                        font=('Poppins Regular', 20)
                    )

    return button


def get_button_CRUD(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=1,
                        width=10,
                        font=('Helvetica bold', 20)
                    )

    return button


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("Helvetica bold", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=15, font=("Helvetica bold", 32))
    return inputtxt
def get_entry_textT(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=13, font=("Helvetica bold", 32))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'

def create_form_label(window,text):
    label = tk.Label(window, text=text)
    label.config(font=("Helvetica bold", 15), justify="left")
    return label
def get_entry_create(window):
    inputtxt = tk.Text(window,
                       height=1.2,
                       width=25, font=("Helvetica bold", 15))
    return inputtxt
def get_entry_del(window):
    inputtxt = tk.Text(window,
                       height=1.2,
                       width=25, font=("Helvetica bold", 15))
    return inputtxt
def dropdown(window):
    def on_select(event):
        selected_item = optionchoosen.get()
        print("Selected Item:", selected_item)  # Add a print statement to check if the function is being called
        label.config(text="Selected Item: " + selected_item)
        if selected_item == ' Software Engineer':
            print("1")
        elif selected_item == ' MBA':
            print("2")
        elif selected_item == ' Computer Science':
            print("3")
        elif selected_item == ' Applied Mathematics':
            print("4")
        if selected_item != "None":
            return selected_item

    label = ttk.Label(window, text="Filter by major:",font=("Helvetica bold", 15))
    label.place(x="220",y="20")
    n = tk.StringVar()
    optionchoosen = ttk.Combobox(window, width=27,
                                textvariable=n)
    optionchoosen['values'] = (' Software Engineer',
                              ' MBA',
                              ' Computer Science',
                              ' Applied Mathematics'
                              )

    optionchoosen.grid(column=1, row=15)
    optionchoosen.place(x="380", y="25")
    optionchoosen.bind("<<ComboboxSelected>>", on_select)
    print(on_select)
    return on_select
def tree_read(window, a, b, data):
    tree = ttk.Treeview(window)
    # Define columns
    tree["columns"] = ("UserId", "Name", "Major", "Year", "Task")

    # Format column headings
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("UserId", anchor=tk.W, width=100)
    tree.column("Name", anchor=tk.W, width=150)
    tree.column("Major", anchor=tk.CENTER, width=100)
    tree.column("Year", anchor=tk.CENTER, width=150)
    tree.column("Task", anchor=tk.CENTER, width=150)

    # Create headings
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("UserId", text="UserId", anchor=tk.W)
    tree.heading("Name", text="Name", anchor=tk.W)
    tree.heading("Major", text="Major", anchor=tk.CENTER)
    tree.heading("Year", text="Year of Registration", anchor=tk.CENTER)
    tree.heading("Task", text="Task", anchor=tk.CENTER)

    for item in data:
        tree.insert("", tk.END, text="1", values=item)

    # Pack the Treeview widget
    tree.place(x=a, y=b)

def treed_read(window,data):
    tree = ttk.Treeview(window)
    # Define columns
    tree["columns"] = ("UserId", "Name", "Major", "Year", "Task")

    # Format column headings
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("UserId", anchor=tk.W, width=100)
    tree.column("Name", anchor=tk.W, width=150)
    tree.column("Major", anchor=tk.CENTER, width=100)
    tree.column("Year", anchor=tk.CENTER, width=150)
    tree.column("Task", anchor=tk.CENTER, width=150)

    # Create headings
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("UserId", text="UserId", anchor=tk.W)
    tree.heading("Name", text="Name", anchor=tk.W)
    tree.heading("Major", text="Major", anchor=tk.CENTER)
    tree.heading("Year", text="Year of Registration", anchor=tk.CENTER)
    tree.heading("Task", text="Task", anchor=tk.CENTER)

    for item in data:
        tree.insert("", tk.END, text="1", values=item)


    # Pack the Treeview widget
    tree.place(x=220,y=100)


