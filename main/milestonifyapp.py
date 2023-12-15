import google.generativeai as palm
import os
import os.path
from dotenv import load_dotenv

#Initialize
load_dotenv()
API_KEY = os.getenv('API_KEY')
palm.configure(api_key=API_KEY)
total_points = 0
starter_prompt = "Task: Provide a numerical response between 50 and 1000, reflecting the difficulty and reward level of the task. If unable to answer, respond with 0. Your reply should consist solely of the numerical value, without additional commentary or text."
lTaskList = {}
# -- START OF SCRIPT --
def main():
    print("Milestonify")
    task = input("Task: ")
    submit_task(task, total_points=total_points)

def submit_task(task, total_points):
    if task is None or task == "":
        print("Uhh.. Bro?")
        return
    prompt = starter_prompt + task
    output = palm.generate_text(prompt=prompt).result
    try: 
        output = int(''.join(filter(str.isdigit, output)))
    except TypeError:
        output = 0
    try:
        points = int(output)
        total_points += points
        
    except TypeError:
        return
    if __name__ == "__main__":
        print("Points: " + str(points))
        print(f"Total Points: {total_points}")
    else:
        return total_points

if __name__ == "__main__":
    main()