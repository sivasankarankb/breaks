import tkinter as tk
from tkinter import ttk

import config
import toolbar
import work_timer
import doing_now
import todo_list
import app_monitor
import about_box

class MainWindow:
    def __setup_window(self):
        self.__tk.minsize(width = 600, height = 450)
        self.__tk.rowconfigure(0, weight = 1)
        self.__tk.columnconfigure(0, weight = 1)

    def __setup_style(self):
        style = ttk.Style()

        style.configure("TButton", relief='solid')
        style.configure("TLabel", background='#eeeeee')
        style.configure("TFrame", background='#eeeeee')

        self.__tk['background'] = '#eeeeee'

    def __init__(self):
        self.__tk = tk.Tk()
        self.__tk.title(config.app_name)
        self.__tk.protocol("WM_DELETE_WINDOW", self.__exit)

        self.__tk.iconphoto(True, tk.PhotoImage(file='icons/icon.png'))

        self.__outer_frame = ttk.Frame(self.__tk)
        self.__outer_frame.grid(sticky=tk.NSEW, padx=16, pady=(16,0))

        self.__setup_window()
        self.__setup_style()

        master = self.__outer_frame
        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)

        toolbar_container = ttk.Frame(master)

        toolbar_container.grid(
            sticky=tk.NSEW, pady=(0,16), padx=(0,16), row=0, column=0
        )
        
        toolbar_obj = toolbar.Toolbar(
            master=toolbar_container,
            button_labels=['Home', 'To do', 'App Monitor', 'About'],
            button_icons=['home', 'notes', 'screen', 'info'],
        )

        home_container = ttk.Frame(master)
        home_container.grid(sticky=tk.NSEW, row=0, column=1)
        home_container.rowconfigure(0, weight=1)
        home_container.columnconfigure(0, weight=1)
        
        doing_now_container = ttk.Frame(home_container)
        doing_now_container.grid(sticky=tk.NSEW, pady=(0,16), row=0, column=0)
        doing_now_obj = doing_now.DoingNow(master=doing_now_container)

        work_timer_container = ttk.Frame(home_container)
        work_timer_container.grid(sticky=tk.NSEW, pady=(0,16), row=1, column=0)
        work_timer_ui = work_timer.WorkTimerUI(master=work_timer_container)
        
        todo_container = ttk.Frame(master)
        todo_container.grid(sticky=tk.NSEW, pady=(0,16), row=0, column=1)
        to_do_list = todo_list.ToDoList(master=todo_container)

        app_monitor_container = ttk.Frame(master)
        app_monitor_container.grid(sticky=tk.NSEW, pady=(0,16), row=0, column=1)
        app_monitor_ui = app_monitor.AppMonitorUI(master=app_monitor_container)

        about_box_container = ttk.Frame(master)
        about_box_container.grid(sticky=tk.NSEW, pady=(0,16), row=0, column=1)
        about_box_obj = about_box.AboutBox(master=about_box_container)

        self.__home_container = home_container
        self.__todo_container = todo_container
        self.__app_monitor_container = app_monitor_container
        self.__about_box_container = about_box_container
        self.__work_timer_ui = work_timer_ui
        self.__app_monitor_ui = app_monitor_ui
        self.__toolbar = toolbar_obj # Obj not saved -> Toolbar icons GC'd 

        self.__toolbar.set_listener('Home', self.__ui_state_home)
        self.__toolbar.set_listener('To do', self.__ui_state_todo)
        self.__toolbar.set_listener('App Monitor', self.__ui_state_monitor)
        self.__toolbar.set_listener('About', self.__ui_state_about)

        self.__ui_state_home()

    def __ui_state_home(self):
        self.__home_container.grid()
        self.__todo_container.grid_remove()
        self.__app_monitor_container.grid_remove()
        self.__about_box_container.grid_remove()

    def __ui_state_todo(self):
        self.__home_container.grid_remove()
        self.__todo_container.grid()
        self.__app_monitor_container.grid_remove()
        self.__about_box_container.grid_remove()

    def __ui_state_monitor(self):
        self.__home_container.grid_remove()
        self.__todo_container.grid_remove()
        self.__app_monitor_container.grid()
        self.__about_box_container.grid_remove()

    def __ui_state_about(self):
        self.__home_container.grid_remove()
        self.__todo_container.grid_remove()
        self.__app_monitor_container.grid_remove()
        self.__about_box_container.grid()

    def start(self): self.__tk.mainloop()

    def __exit(self): self.__tk.destroy()

    def get_work_timer_ui(self): return self.__work_timer_ui

    def get_app_monitor_ui(self): return self.__app_monitor_ui
