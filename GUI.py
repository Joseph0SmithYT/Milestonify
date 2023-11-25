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

        self.starter_prompt = "Task: Provide a numerical response between 50 and 1000, reflecting the difficulty and reward level of the task. If unable to answer, respond with 0. Your reply should consist solely of the numerical value, without additional commentary or text."
        self.total_points = 0

        self.panel = wx.Panel(self)

        # Set the icon
        #icon = wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO)
        #self.SetIcon(icon)

        # Left panel with scrolling capability
        self.left_panel = wx.ScrolledWindow(self.panel, style=wx.VSCROLL)
        self.left_panel.SetScrollRate(0, 20)
        self.left_panel.SetBackgroundColour((0, 0, 0))


        # Task list
        self.task_list = wx.ListCtrl(self.left_panel, style=wx.LC_REPORT)
        self.task_list.InsertColumn(0, "Task", width=150)
        self.task_list.InsertColumn(1, "Points", width=80)
        self.task_list.SetForegroundColour((255,255,255))
        self.task_list.SetBackgroundColour((0, 0, 0))
        self.task_list.SetTextColour((255,255,255))

        # Right panel with input fields and buttons
        self.right_panel = wx.Panel(self.panel)

        self.task_entry_label = wx.StaticText(self.right_panel, label="Task:")
        self.task_entry = wx.TextCtrl(self.right_panel, style=wx.TE_PROCESS_ENTER)
        self.task_entry.SetForegroundColour((255,255,255))
        self.task_entry.SetBackgroundColour((0, 0, 0))
        self.task_entry_label.SetForegroundColour((255,255,255))

        self.submit_button = wx.Button(self.right_panel, label="Submit")
        self.submit_button.Bind(wx.EVT_BUTTON, self.submit_task)

        self.total_points_label = wx.StaticText(self.right_panel, label="Total Points: 0")
        self.total_points_label.SetForegroundColour((255,255,255))

        # Set up sizers for the right panel
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(self.task_entry_label, 0, wx.ALL, 5)
        right_sizer.Add(self.task_entry, 0, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(self.submit_button, 0, wx.ALL, 5)
        right_sizer.Add(self.total_points_label, 0, wx.ALL, 5)

        self.right_panel.SetSizer(right_sizer)

        # Set up sizer for the main panel
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.left_panel, 1, wx.EXPAND)
        main_sizer.Add(self.right_panel, 1, wx.EXPAND)
        
        self.right_panel.SetBackgroundColour((0,0,0))
        self.right_panel.SetForegroundColour((255,255,255))

        self.panel.SetSizer(main_sizer)
        self.Show()

    def submit_task(self, event):
        task = self.task_entry.GetValue()

        
        prompt = self.starter_prompt + task

        output = palm.generate_text(prompt=prompt).result
        output = int(''.join(filter(str.isdigit, output)))

        try:
            points = int(output)
            self.total_points += points

            # Add task to the list
            index = self.task_list.InsertItem(self.task_list.GetItemCount(), task)
            self.task_list.SetItem(index, 1, str(points))
            self.task_entry.SetValue("")
        except ValueError:
            wx.MessageBox("AI Error", "AI made an invalid input.", wx.OK | wx.ICON_ERROR)
            

        self.total_points_label.SetLabel(f"Total Points: {self.total_points}")


def main():
    app = wx.App(False)
    frame = TaskApp(None, title="Milestonify", size=(800, 400))
    app.MainLoop()


if __name__ == "__main__":
    main()
