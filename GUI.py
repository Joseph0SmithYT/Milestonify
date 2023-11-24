import wx
import google.generativeai as palm
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
palm.configure(api_key=API_KEY)
total_points = 0

class TaskApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(TaskApp, self).__init__(*args, **kw)

        self.starter_prompt = "I'm gonna give you a task, based on how difficult and rewarding it is, give me a number between 50 - 1000. If you can't answer it, say 0. Reply with only a number."
        self.total_points = 0

        self.panel = wx.Panel(self)

        self.amount_of_tasks_label = wx.StaticText(self.panel, label="How many tasks do you have?")
        self.amount_of_tasks_entry = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)

        self.task_label = wx.StaticText(self.panel, label="Task:")
        self.task_entry = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)

        self.submit_button = wx.Button(self.panel, label="Submit")
        self.submit_button.Bind(wx.EVT_BUTTON, self.submit_task)

        self.total_points_label = wx.StaticText(self.panel, label="Total Points: 0")

        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.layout.Add(self.amount_of_tasks_label, 0, wx.ALL, 5)
        self.layout.Add(self.amount_of_tasks_entry, 0, wx.EXPAND | wx.ALL, 5)
        self.layout.Add(self.task_label, 0, wx.ALL, 5)
        self.layout.Add(self.task_entry, 0, wx.EXPAND | wx.ALL, 5)
        self.layout.Add(self.submit_button, 0, wx.ALL, 5)
        self.layout.Add(self.total_points_label, 0, wx.ALL, 5)

        icon = self.SetIcon(wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO))

        self.panel.SetSizer(self.layout)
        self.Show()

    def submit_task(self, event):
        amount_of_tasks = int(self.amount_of_tasks_entry.GetValue())
        task = self.task_entry.GetValue()

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
                wx.MessageBox("AI Error", "AI made an invalid input.", wx.OK | wx.ICON_ERROR)
                break

        self.total_points_label.SetLabel(f"Total Points: {self.total_points}")


def main():
    app = wx.App(False)
    frame = TaskApp(None, title="Milestonify", size=(400, 300))
    app.MainLoop()


if __name__ == "__main__":
    main()
