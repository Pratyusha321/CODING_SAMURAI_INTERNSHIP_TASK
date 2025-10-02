import tkinter as tk
from tkinter import messagebox

# Save tasks to file
def save_tasks():
    with open("tasks.txt", "w") as f:
        for i in task_listbox.get(0, tk.END):
            f.write(i + "\n")

# Load tasks from file
def load_tasks():
    try:
        with open("tasks.txt", "r") as f:
            for line in f:
                task_listbox.insert(tk.END, line.strip())
    except FileNotFoundError:
        pass

# Add task
def add_task():
    task = task_entry.get()
    if task != "":
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Enter a task!")

# Delete task
def delete_task():
    try:
        selected = task_listbox.curselection()[0]
        task_listbox.delete(selected)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to delete!")

# Mark completed
def mark_completed():
    try:
        index = task_listbox.curselection()[0]
        task = task_listbox.get(index)
        if "(Completed)" not in task:
            task_listbox.delete(index)
            task_listbox.insert(index, task + " (Completed)")
            save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to mark completed!")

# GUI setup
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x400")

# Input field
task_entry = tk.Entry(root, width=25, font=("Arial", 14))
task_entry.pack(pady=10)

# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task, width=15)
add_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task, width=15)
delete_button.pack(pady=5)

complete_button = tk.Button(root, text="Mark Completed", command=mark_completed, width=15)
complete_button.pack(pady=5)

# Task listbox
task_listbox = tk.Listbox(root, width=40, height=10, selectmode=tk.SINGLE, font=("Arial", 12))
task_listbox.pack(pady=10)

# Load tasks from file
load_tasks()

# Run GUI
root.mainloop()
