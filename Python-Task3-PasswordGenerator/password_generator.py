import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import secrets
import string
import sqlite3
import pyperclip


# ================= DATABASE ================= #

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS password_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT,
    strength TEXT
)
""")

conn.commit()


# ================= FUNCTIONS ================= #

def password_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in string.punctuation for c in password):
        score += 1


    if score <= 2:
        return "Weak"

    elif score <= 4:
        return "Medium"

    else:
        return "Strong"



def generate_password():

    try:

        length = int(length_entry.get())

        if length <= 0:
            messagebox.showerror(
                "Error",
                "Length must be greater than zero"
            )
            return


        characters = ""


        if lowercase_var.get():
            characters += string.ascii_lowercase

        if uppercase_var.get():
            characters += string.ascii_uppercase

        if numbers_var.get():
            characters += string.digits

        if symbols_var.get():
            characters += string.punctuation


        if characters == "":
            messagebox.showerror(
                "Error",
                "Select at least one option"
            )
            return


        password = ""

        for i in range(length):
            password += secrets.choice(characters)


        password_entry.config(state="normal")
        password_entry.delete(0, END)
        password_entry.insert(0, password)
        password_entry.config(state="readonly")


        strength = password_strength(password)

        strength_label.config(
            text=f"💪 Strength : {strength}"
        )


        if strength == "Weak":
            strength_bar["value"] = 30

        elif strength == "Medium":
            strength_bar["value"] = 65

        else:
            strength_bar["value"] = 100



        cursor.execute(
            """
            INSERT INTO password_history(password,strength)
            VALUES (?,?)
            """,
            (password,strength)
        )

        conn.commit()



    except ValueError:

        messagebox.showerror(
            "Error",
            "Enter valid number"
        )




def copy_password():

    password = password_entry.get()

    if password:

        pyperclip.copy(password)

        messagebox.showinfo(
            "Copied",
            "Password copied!"
        )

    else:

        messagebox.showwarning(
            "Warning",
            "Generate password first"
        )




def show_history():

    window = ttk.Toplevel(root)

    window.title(
        "Password History"
    )

    window.geometry(
        "500x350"
    )


    frame = ttk.Frame(window)

    frame.pack(
        fill=BOTH,
        expand=True,
        padx=10,
        pady=10
    )


    scrollbar = ttk.Scrollbar(frame)

    scrollbar.pack(
        side=RIGHT,
        fill=Y
    )


    history_box = ttk.Treeview(
        frame,
        columns=("Password","Strength"),
        show="headings",
        yscrollcommand=scrollbar.set
    )


    history_box.heading(
        "Password",
        text="Password"
    )

    history_box.heading(
        "Strength",
        text="Strength"
    )


    history_box.pack(
        fill=BOTH,
        expand=True
    )


    scrollbar.config(
        command=history_box.yview
    )


    cursor.execute(
        "SELECT password,strength FROM password_history"
    )

    data = cursor.fetchall()


    for row in data:

        history_box.insert(
            "",
            END,
            values=row
        )





def clear_history():

    answer = messagebox.askyesno(
        "Confirm",
        "Delete all history?"
    )


    if answer:

        cursor.execute(
            "DELETE FROM password_history"
        )

        conn.commit()


        messagebox.showinfo(
            "Success",
            "History cleared"
        )




def close_app():

    conn.close()

    root.destroy()



# ================= GUI ================= #

root = ttk.Window(
    title="Advanced Password Generator",
    themename="darkly"
)


root.geometry(
    "600x650"
)

root.resizable(
    False,
    False
)



title = ttk.Label(
    root,
    text=" Advanced Password Generator",
    font=("Segoe UI",24,"bold"),
    bootstyle="primary"
)

title.pack(
    pady=20
)



ttk.Label(
    root,
    text="📏 Password Length",
    font=("Segoe UI",13)
).pack()



length_entry = ttk.Entry(
    root,
    width=20,
    justify=CENTER
)

length_entry.insert(
    0,
    "12"
)

length_entry.pack(
    pady=10
)



# Options

lowercase_var = ttk.BooleanVar(value=True)
uppercase_var = ttk.BooleanVar(value=True)
numbers_var = ttk.BooleanVar(value=True)
symbols_var = ttk.BooleanVar(value=True)



ttk.Checkbutton(
    root,
    text="Lowercase (a-z)",
    variable=lowercase_var
).pack(pady=5)



ttk.Checkbutton(
    root,
    text="Uppercase (A-Z)",
    variable=uppercase_var
).pack(pady=5)



ttk.Checkbutton(
    root,
    text="Numbers (0-9)",
    variable=numbers_var
).pack(pady=5)



ttk.Checkbutton(
    root,
    text="Symbols (!@#$)",
    variable=symbols_var
).pack(pady=5)




ttk.Button(
    root,
    text="🔐 Generate Password",
    bootstyle="primary",
    command=generate_password,
    width=25
).pack(pady=15)



ttk.Label(
    root,
    text="Generated Password"
).pack()



password_entry = ttk.Entry(
    root,
    width=40,
    justify=CENTER,
    state="readonly"
)

password_entry.pack(
    pady=10
)



strength_label = ttk.Label(
    root,
    text="💪 Strength : -",
    font=("Segoe UI",12,"bold")
)

strength_label.pack(
    pady=10
)



strength_bar = ttk.Progressbar(
    root,
    length=350,
    maximum=100,
    bootstyle="success"
)

strength_bar.pack(
    pady=10
)



ttk.Button(
    root,
    text="📋 Copy Password",
    bootstyle="success",
    command=copy_password,
    width=25
).pack(pady=5)



ttk.Button(
    root,
    text="📜 View History",
    bootstyle="info",
    command=show_history,
    width=25
).pack(pady=5)



ttk.Button(
    root,
    text="🗑 Clear History",
    bootstyle="danger",
    command=clear_history,
    width=25
).pack(pady=5)



ttk.Label(
    root,
    text="Developed by Rutuja Sabale",
    font=("Segoe UI",10)
).pack(
    side=BOTTOM,
    pady=15
)



root.protocol(
    "WM_DELETE_WINDOW",
    close_app
)


root.mainloop()