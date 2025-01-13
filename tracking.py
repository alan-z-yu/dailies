import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt


def setup_database():
    conn = sqlite3.connect("progress.db")  # Create or connect to the database
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Timer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ms_passed INTEGER NOT NULL
        )
    """)
    # Check if there's a saved progress
    cursor.execute("SELECT ms_passed FROM Timer ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result[0] if result else 0  # Return the last saved progress or 0

def save_progress(ms):
    conn = sqlite3.connect("progress.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Timer (ms_passed) VALUES (?)", (ms,))
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

def update_timer():
    global ms_passed, timer_running
    if timer_running:
        ms_passed += 1
        progress["value"] = ms_passed
        timer.config(text=f"Counted time: {ms_passed}")
        save_progress(ms_passed)
        root.after(1, update_timer)

update_timer()
# Run the application
root.mainloop()