"""import google.generativeai as palm
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
palm.configure(api_key=API_KEY)
total_points = 0

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Milestonify")

        self.amount_of_tasks_label = ttk.Label(master, text="How many tasks do you have?")
        self.amount_of_tasks_label.pack()

        self.amount_of_tasks_entry = ttk.Entry(master)
        self.amount_of_tasks_entry.pack()

        self.task_label = ttk.Label(master, text="Task:")
        self.task_label.pack()

        self.task_entry = ttk.Entry(master)
        self.task_entry.pack()

        self.submit_button = ttk.Button(master, text="Submit", command=self.submit_task)
        self.submit_button.pack()

        self.total_points_label = ttk.Label(master, text="Total Points: 0")
        self.total_points_label.pack()

        self.starter_prompt = "I'm gonna give you a task, based on how difficult and rewarding it is, give me a number between 50 - 1000. If you can't answer it, say 0. Reply with only a number."
        self.total_points = 0

    def submit_task(self):
        amount_of_tasks = int(self.amount_of_tasks_entry.get())
        task = self.task_entry.get()

        while amount_of_tasks > 0:
            prompt = self.starter_prompt + task

            # Replace the next line with your API call
            output = palm.generate_text(prompt=prompt).result
            print(output)

            

            try:
                points = int(output)
                self.total_points += points
                amount_of_tasks -= 1
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a number.")

        self.total_points_label.config(text=f"Total Points: {self.total_points}")


def main():
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import google.generativeai as palm
import os
from dotenv import load_dotenv
from tkinter import font

load_dotenv()
API_KEY = os.getenv("API_KEY")
palm.configure(api_key=API_KEY)
total_points = 0

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Milestonify")

        # Set default font size
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)

        self.amount_of_tasks_label = ttk.Label(master, text="How many tasks do you have?")
        self.amount_of_tasks_label.grid(row=0, column=0, padx=5, pady=5)

        self.amount_of_tasks_entry = ttk.Entry(master)
        self.amount_of_tasks_entry.grid(row=0, column=1, padx=5, pady=5)

        self.task_label = ttk.Label(master, text="Task:")
        self.task_label.grid(row=1, column=0, padx=5, pady=5)

        self.task_entry = ttk.Entry(master)
        self.task_entry.grid(row=1, column=1, padx=5, pady=5)

        self.submit_button = ttk.Button(master, text="Submit", command=self.submit_task)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.total_points_label = ttk.Label(master, text="Total Points: 0")
        self.total_points_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.starter_prompt = "I'm gonna give you a task, based on how difficult and rewarding it is, give me a number between 50 - 1000. If you can't answer it, say 0. Reply with only a number."
        self.total_points = 0

    def submit_task(self):
        amount_of_tasks = int(self.amount_of_tasks_entry.get())
        task = self.task_entry.get()

        while amount_of_tasks > 0:
            prompt = self.starter_prompt + task

            # Replace the next line with your API call
            output = palm.generate_text(prompt=prompt).result
            print(output)
            output = int(''.join(filter(str.isdigit, output)))
            try:
                points = int(output)
                self.total_points += points
                amount_of_tasks -= 1
            except ValueError:
                messagebox.showinfo("AI Error", "AI made an invalid input. Program will now close.")
                exit()

        self.total_points_label.config(text=f"Total Points: {self.total_points}")
    


def main():
    root = tk.Tk()
    app = TaskApp(root)
    
    # Configure rows and columns to expand with the window
    for i in range(4):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)
    
    root.mainloop()

if __name__ == "__main__":
    main()
