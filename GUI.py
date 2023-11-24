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

        # Set the icon
        #icon = wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Left panel with scrolling capability
        self.left_panel = wx.ScrolledWindow(self.panel, style=wx.VSCROLL)
        self.left_panel.SetScrollRate(0, 20)

        # Task list
        self.task_list = wx.ListCtrl(self.left_panel, style=wx.LC_REPORT)
        self.task_list.InsertColumn(0, "Task", width=150)
        self.task_list.InsertColumn(1, "Points", width=80)

        # Right panel with input fields and buttons
        self.right_panel = wx.Panel(self.panel)

        self.amount_of_tasks_label = wx.StaticText(self.right_panel, label="How many tasks do you have?")
        self.amount_of_tasks_entry = wx.TextCtrl(self.right_panel, style=wx.TE_PROCESS_ENTER)

        self.submit_button = wx.Button(self.right_panel, label="Submit")
        self.submit_button.Bind(wx.EVT_BUTTON, self.submit_task)

        self.total_points_label = wx.StaticText(self.right_panel, label="Total Points: 0")

        # Set up sizers for the right panel
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(self.amount_of_tasks_label, 0, wx.ALL, 5)
        right_sizer.Add(self.amount_of_tasks_entry, 0, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(self.submit_button, 0, wx.ALL, 5)
        right_sizer.Add(self.total_points_label, 0, wx.ALL, 5)

        self.right_panel.SetSizer(right_sizer)

        # Set up sizer for the main panel
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.left_panel, 1, wx.EXPAND)
        main_sizer.Add(self.right_panel, 1, wx.EXPAND)

        self.panel.SetSizer(main_sizer)
        self.Show()

    def submit_task(self, event):
        amount_of_tasks = int(self.amount_of_tasks_entry.GetValue())

        while amount_of_tasks > 0:
            dialog = wx.TextEntryDialog(self, "Enter task", "Task", style=wx.OK | wx.CANCEL)


            if dialog.ShowModal() == wx.ID_OK:
                task = dialog.GetValue()
                

                dialog.Destroy()
            prompt = self.starter_prompt + task

            # Replace the next line with your API call
            output = palm.generate_text(prompt=prompt).result
            print(output)
            output = int(''.join(filter(str.isdigit, output)))

            try:
                points = int(output)
                self.total_points += points
                amount_of_tasks -= 1

                # Add task to the list
                index = self.task_list.InsertItem(self.task_list.GetItemCount(), task)
                self.task_list.SetItem(index, 1, str(points))
            except ValueError:
                wx.MessageBox("AI Error", "AI made an invalid input.", wx.OK | wx.ICON_ERROR)
                break

        self.total_points_label.SetLabel(f"Total Points: {self.total_points}")


def main():
    app = wx.App(False)
    frame = TaskApp(None, title="Milestonify", size=(800, 400))
    app.MainLoop()


if __name__ == "__main__":
    main()
