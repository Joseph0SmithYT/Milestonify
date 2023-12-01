import wx
import google.generativeai as palm
import os
import os.path
from dotenv import load_dotenv
import dill as pickle

load_dotenv()
API_KEY = os.getenv("API_KEY")
palm.configure(api_key=API_KEY)
total_points = 0

class TaskApp(wx.Frame):
    def __init__(self, *args, **kw):
        
        super(TaskApp, self).__init__(*args, **kw)
        os.path.isfile('points.pkl')
        self.total_points = 0
        with open('points.pkl', 'rb') as f:
            self.total_points = pickle.load(f)
            print(self.total_points)
        
        self.starter_prompt = "Task: Provide a numerical response between 50 and 1000, reflecting the difficulty and reward level of the task. If unable to answer, respond with 0. Your reply should consist solely of the numerical value, without additional commentary or text."
        

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
        self.task_list.SetSize(round(self.GetSize().x / 2) - 10, self.GetSize().y)

        # Right panel with input fields and buttons
        self.right_panel = wx.Panel(self.panel)

        self.task_entry_label = wx.StaticText(self.right_panel, label="Task:")
        self.task_entry = wx.TextCtrl(self.right_panel, style=wx.TE_PROCESS_ENTER)
        self.task_entry.SetForegroundColour((255,255,255))
        self.task_entry.SetBackgroundColour((0, 0, 0))
        self.task_entry_label.SetForegroundColour((255,255,255))

        self.submit_button = wx.Button(self.right_panel, label="Submit")
        self.submit_button.Bind(wx.EVT_BUTTON, self.submit_task)

        self.total_points_label = wx.StaticText(self.right_panel, label=f"Total Points: {str(self.total_points)}")
        self.total_points_label.SetForegroundColour((255,255,255))

        self.reset_points_btn = wx.Button(self.right_panel, label="Reset Points")
        self.reset_points_btn.Bind(wx.EVT_BUTTON, self.reset_points)

        # Set up sizers for the right panel
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(self.task_entry_label, 0, wx.ALL, 5)
        right_sizer.Add(self.task_entry, 0, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(self.submit_button, 0, wx.ALL, 5)
        right_sizer.Add(self.total_points_label, 0, wx.ALL, 5)
        right_sizer.Add(self.reset_points_btn, 0, wx.ALL, 5)

        # Put reset_points_btn to the bottom right


        self.right_panel.SetSizer(right_sizer)

        # Set up sizers for the left panel
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(self.task_list, 1, wx.EXPAND)
        self.left_panel.SetSizer(left_sizer)

        # Set up sizer for the main panel
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.left_panel, 1, wx.EXPAND)
        main_sizer.Add(self.right_panel, 1, wx.EXPAND)
        
        self.right_panel.SetBackgroundColour((0,0,0))
        self.right_panel.SetForegroundColour((255,255,255))

        self.panel.SetSizer(main_sizer)
        self.Show()

    def reset_points(self, event):
        self.reset_points_prompt = wx.MessageBox("Are you sure you want to reset your points?", "Reset Points", wx.OK | wx.ICON_INFORMATION | wx.CANCEL)
        if self.reset_points_prompt == wx.OK:
            self.total_points = 0
            self.total_points_label.SetLabel(f"Total Points: {self.total_points}")
            self.task_list.DeleteAllItems()
            with open('points.pkl', 'wb') as f:
                pickle.dump(self.total_points, f)
    
    def submit_task(self, event):
        task = self.task_entry.GetValue()
        if task is None or task == "":
            wx.MessageBox("Hi! Our little robots have scanned your text for innapropriate information! But.. They came across something empty and sent it away! You can't do nothing, always have to do something!", "Please enter a task.", wx.OK | wx.WXK_CONTROL_A)
            return

        prompt = self.starter_prompt + task

        output = palm.generate_text(prompt=prompt).result
        try:
            output = int(''.join(filter(str.isdigit, output)))
        except TypeError:
            output = 0

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
        with open('points.pkl', 'wb') as f:

            pickle.dump(self.total_points, f)


def main():
    app = wx.App(False)
    frame = TaskApp(None, title="Milestonify", size=(800, 400))
    app.MainLoop()


if __name__ == "__main__":
    main()
