import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

def setup_database():
    conn = sqlite3.connect("progress.db")  # Create or connect to the database
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Timer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ms_passed INTEGER NOT NULL,
            date DATE NOT NULL
        )
    """)
    # Check if there's a saved progress
    cursor.execute("SELECT ms_passed FROM Timer ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result[0] if result else 0  # Return the last saved progress or 0

def add_column_if_not_exists(column_name):
    conn = sqlite3.connect("progress.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(Timer);")
    columns = [row[1] for row in cursor.fetchall()]  # Column names are in the second position

    # Add the column if it doesn't exist
    if column_name not in columns:
        cursor.execute(f"ALTER TABLE Timer ADD COLUMN {column_name} {column_name.upper()};")
        print(f"Column '{column_name}' added successfully.")
    else:
        print(f"Column '{column_name}' already exists.")

    conn.commit()
    conn.close()

def save_progress(ms):
    conn = sqlite3.connect("progress.db")
    cursor = conn.cursor()
    today = datetime.now().date()
    cursor.execute("INSERT INTO Timer (ms_passed, date) VALUES (?, ?)", (ms, today))
    conn.commit()
    conn.close()

def on_button_click():
    global timer_running
    if timer_running:
        button.config(text="Start Timer")
    else:
        button.config(text="Stop Timer")
    timer_running = not timer_running
    update_timer()

def show_history_chart():
    data = get_data_by_day()
    if data:
        dates = [str(row[0]) for row in data]
        ms_values = [row[1] for row in data]
        
        plt.figure(figsize=(8, 5))
        plt.bar(dates, ms_values, color="skyblue")
        plt.xlabel("Date")
        plt.ylabel("Milliseconds Passed")
        plt.title("Time Progress by Day")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("No data available!")

def get_data_by_day():
    conn = sqlite3.connect("progress.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, SUM(ms_passed) FROM Timer GROUP BY date ORDER BY date")
    results = cursor.fetchall()
    conn.close()
    return results

def update_timer():
    global ms_passed, timer_running
    if timer_running:
        ms_passed += 1
        progress["value"] = ms_passed
        timer.config(text=f"Counted time: {ms_passed}")
        save_progress(ms_passed)
        root.after(1, update_timer)

ms_passed = setup_database()
timer_running = False
max_time_ms = 100000

# Create the main window
root = tk.Tk()
root.title("Timer test")
root.geometry("300x200")  # Set the window size

# Create a label

timer = tk.Label(root, text=f"Counted time: {ms_passed}")
timer.pack(pady=10)

progress = ttk.Progressbar(root, value=ms_passed, orient="horizontal", length = 300, mode="determinate", maximum=max_time_ms)
progress.pack(pady = 10)

# Create a button
button = tk.Button(root, text="Start Timer", command=on_button_click)
button.pack(pady=10)

history_button = tk.Button(root, text="View History Chart", command=show_history_chart)
history_button.pack(pady=10)



update_timer()
add_column_if_not_exists("ms_passed")
add_column_if_not_exists("date")
# Run the application
root.mainloop()
