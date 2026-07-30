import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3
import matplotlib.pyplot as plt

# -----------------------------
# DATABASE
# -----------------------------
conn = sqlite3.connect("bmi_records.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT
)
""")

conn.commit()

# -----------------------------
# WINDOW
# -----------------------------
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("450x600")
root.configure(bg="#f0f8ff")


# -----------------------------
# BMI FUNCTION
# -----------------------------
def calculate_bmi():

    try:
        name = name_entry.get().strip()

        if name == "":
            messagebox.showerror("Error", "Please enter your name.")
            return

        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Weight and Height must be greater than zero."
            )
            return

        # cm to meter
        height_meter = height / 100

        bmi = weight / (height_meter ** 2)

        if bmi < 18.5:
            category = "Underweight"
            color = "blue"

        elif bmi < 25:
            category = "Normal"
            color = "green"

        elif bmi < 30:
            category = "Overweight"
            color = "orange"

        else:
            category = "Obese"
            color = "red"

        result_label.config(
            text=f"BMI : {bmi:.2f}\nCategory : {category}",
            fg=color
        )

        cursor.execute("""
        INSERT INTO bmi_records(name,weight,height,bmi,category)
        VALUES(?,?,?,?,?)
        """, (name, weight, height, bmi, category))

        conn.commit()

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numbers."
        )


# -----------------------------
# HISTORY
# -----------------------------
def view_history():

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("600x500")

    heading = tk.Label(
        history_window,
        text="BMI History",
        font=("Arial", 16, "bold")
    )
    heading.pack(pady=10)

    history_text = scrolledtext.ScrolledText(
        history_window,
        width=70,
        height=20,
        font=("Arial", 10)
    )
    history_text.pack(padx=10, pady=10, fill="both", expand=True)

    cursor.execute("SELECT * FROM bmi_records")
    records = cursor.fetchall()

    if not records:
        history_text.insert(tk.END, "No records found.")
    else:
        for row in records:
            history_text.insert(
                tk.END,
                f"""
ID        : {row[0]}
Name      : {row[1]}
Weight    : {row[2]} kg
Height    : {row[3]} cm
BMI       : {row[4]:.2f}
Category  : {row[5]}
----------------------------------------
"""
            )

    history_text.config(state="disabled")


# -----------------------------
# GRAPH
# -----------------------------
def show_graph():

    cursor.execute("SELECT bmi FROM bmi_records")

    data = cursor.fetchall()

    bmi_values = []

    for item in data:
        bmi_values.append(item[0])

    if len(bmi_values) == 0:
        messagebox.showinfo(
            "No Data",
            "No BMI Records Found."
        )
        return

    plt.figure(figsize=(8,5))

    plt.plot(
        range(1, len(bmi_values)+1),
        bmi_values,
        marker="o",
        linewidth=2
    )

    plt.title("BMI Progress")

    plt.xlabel("Record Number")

    plt.ylabel("BMI")

    plt.grid(True)

    plt.show()


# -----------------------------
# HEADING
# -----------------------------
heading = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial",22,"bold"),
    bg="#f0f8ff"
)

heading.pack(pady=20)

# -----------------------------
# NAME
# -----------------------------
name_label = tk.Label(
    root,
    text="Name",
    font=("Arial",12),
    bg="#f0f8ff"
)

name_label.pack()

name_entry = tk.Entry(
    root,
    width=30
)

name_entry.pack(pady=5)

# -----------------------------
# WEIGHT
# -----------------------------
weight_label = tk.Label(
    root,
    text="Weight (kg)",
    font=("Arial",12),
    bg="#f0f8ff"
)

weight_label.pack()

weight_entry = tk.Entry(
    root,
    width=30
)

weight_entry.pack(pady=5)

# -----------------------------
# HEIGHT
# -----------------------------
height_label = tk.Label(
    root,
    text="Height (cm)",
    font=("Arial",12),
    bg="#f0f8ff"
)

height_label.pack()

height_entry = tk.Entry(
    root,
    width=30
)

height_entry.pack(pady=5)

# -----------------------------
# CALCULATE BUTTON
# -----------------------------
calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    bg="#4CAF50",
    fg="white",
    width=20,
    font=("Arial",11,"bold")
)

calculate_button.pack(pady=15)

# -----------------------------
# HISTORY BUTTON
# -----------------------------
history_button = tk.Button(
    root,
    text="View History",
    command=view_history,
    bg="#2196F3",
    fg="white",
    width=20,
    font=("Arial",11,"bold")
)

history_button.pack(pady=10)

# -----------------------------
# GRAPH BUTTON
# -----------------------------
graph_button = tk.Button(
    root,
    text="Show BMI Graph",
    command=show_graph,
    bg="#9C27B0",
    fg="white",
    width=20,
    font=("Arial",11,"bold")
)

graph_button.pack(pady=10)

# -----------------------------
# RESULT
# -----------------------------
result_label = tk.Label(
    root,
    text="",
    font=("Arial",14,"bold"),
    bg="#f0f8ff"
)

result_label.pack(pady=20)

# -----------------------------
# MAIN LOOP
# -----------------------------
root.mainloop()

conn.close()