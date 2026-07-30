# 🏥 BMI Calculator (Advanced)

## 📌 Project Overview

The **BMI Calculator** is a Python desktop application developed using **Tkinter**. It calculates a user's Body Mass Index (BMI), classifies the BMI into standard health categories, stores records in an SQLite database, displays previous BMI history, and visualizes BMI trends using a graph.

This project was developed as part of the **Oasis Infobyte Python Programming Internship (OIBSIP)**.

---

## 🎯 Features

- GUI developed using Tkinter
- Calculate BMI using weight and height
- Automatic BMI category classification
- Color-coded BMI result
- Input validation
- Store BMI records in SQLite database
- View BMI calculation history
- Display BMI progress graph using Matplotlib
- Multi-user support using Name field

---

## 🛠 Technologies Used

- Python 3
- Tkinter
- SQLite3
- Matplotlib

---

## 📂 Project Structure

```
Python-Task2-BMICalculator/
│
├── bmi.py
├── bmi_records.db
├── README.md
├── requirements.txt
└── screenshots/
```

---

## 📐 BMI Formula

```
BMI = Weight (kg) / Height² (m²)
```

---

## 📊 BMI Categories

| BMI Range | Category |
|-----------|----------|
| Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal Weight |
| 25 – 29.9 | Overweight |
| 30 and Above | Obese |

---

## 🚀 How to Run the Project

### Step 1

Clone the repository

```bash
git clone https://github.com/YourUsername/OIBSIP.git
```

### Step 2

Open the project folder

```bash
cd OIBSIP/Python-Task2-BMICalculator
```

### Step 3

Install required library

```bash
pip install matplotlib
```

### Step 4

Run the project

```bash
python bmi.py
```

---

## 💾 Database

The application stores BMI records in an **SQLite database** named:

```
bmi_records.db
```

Each record contains:

- Name
- Weight
- Height
- BMI
- Category

---

## 📈 Future Improvements

- Add Date & Time for each BMI record
- Export BMI history to PDF or CSV
- Delete or update records
- Improve UI with modern themes
- Add health recommendations based on BMI

---

## 👩‍💻 Developed By

**Rutuja Sabale**

Python Programming Intern

Oasis Infobyte (OIBSIP)

---

## 📄 License

This project is developed for educational purposes as part of the Oasis Infobyte Internship Program.