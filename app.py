import os
import google.generativeai as palm 
from dotenv import load_dotenv
import dill as pickle

load_dotenv()
API_KEY = os.getenv("API_KEY")
palm.configure(api_key=API_KEY)
total_points = 0

starter_prompt = "I'm gonna give you a task, based on how difficult and rewarding it is, give me a number between 50 to 1000. If you can't answer it, say 0. Only reply with a number."
# -- START OF SCRIPT --
amountOfTasks = int(input("How many tasks do you have?: "))


while not amountOfTasks == 0:
    task = input("Task: ")
    prompt = starter_prompt + task

    output = palm.generate_text(prompt = prompt).result

    if output == None:
        print("Task not accepted. Pick another one.")
        break
        
    if output.isdigit() == True:
        points = int(output)
        print("You got {points} points" .format(points=points))
    else:
        print(output)
    try:
        total_points = total_points + points
        amountOfTasks = amountOfTasks - 1
    except TypeError:
        print("DOesn't work")
        
print("You now have {total_points} total points." .format(total_points=total_points))