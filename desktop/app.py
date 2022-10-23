#!/usr/bin/env python3

# app.py - What ties it all together.

import tkinter as tk
from tkinter import ttk

import main_window
import toolbar
import work_timer
import doing_now
import todo_list
import app_monitor
import about_box

if __name__ == '__main__':
    main_window = main_window.MainWindow()
    master = main_window.get_nesting_window()
    master.rowconfigure(0, weight=1)
    master.columnconfigure(1, weight=1)

    toolbar_container = ttk.Frame(master)

    toolbar_container.grid(
        sticky=tk.NSEW, pady=(0,16), padx=(0,16), row=0, column=0
    )
    
    toolbar = toolbar.Toolbar(
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
    doing_now = doing_now.DoingNow(master=doing_now_container)

    work_timer_container = ttk.Frame(home_container)
    work_timer_container.grid(sticky=tk.NSEW, pady=(0,16), row=1, column=0)
    work_timer_ui = work_timer.WorkTimerUI(master=work_timer_container)
    work_timer_logic = work_timer.WorkTimer(work_timer_ui)
    
    todo_container = ttk.Frame(master)
    todo_container.grid(sticky=tk.NSEW, pady=(0,16), row=0, column=1)
    to_do_list = todo_list.ToDoList(master=todo_container)

    app_monitor_container = ttk.Frame(master)
    app_monitor_container.grid(sticky=tk.NSEW, pady=(0,16), row=0, column=1)
    app_monitor_ui = app_monitor.AppMonitorUI(master=app_monitor_container)
    app_monitor_inst = app_monitor.AppMonitor(app_monitor_ui)

    about_box_container = ttk.Frame(master)
    about_box_container.grid(sticky=tk.NSEW, pady=(0,16), row=0, column=1)
    about_box = about_box.AboutBox(master=about_box_container)

    def ui_state_home():
        global home_container
        global todo_container, app_monitor_container, about_box_container
        
        home_container.grid()
        todo_container.grid_remove()
        app_monitor_container.grid_remove()
        about_box_container.grid_remove()

    def ui_state_todo():
        global home_container
        global todo_container, app_monitor_container, about_box_container
        
        home_container.grid_remove()
        todo_container.grid()
        app_monitor_container.grid_remove()
        about_box_container.grid_remove()

    def ui_state_monitor():
        global home_container
        global todo_container, app_monitor_container, about_box_container
        
        home_container.grid_remove()
        todo_container.grid_remove()
        app_monitor_container.grid()
        about_box_container.grid_remove()

    def ui_state_about():
        global home_container
        global todo_container, app_monitor_container, about_box_container
        
        home_container.grid_remove()
        todo_container.grid_remove()
        app_monitor_container.grid_remove()
        about_box_container.grid()

    ui_state_home()

    toolbar.set_listener('Home', ui_state_home)
    toolbar.set_listener('To do', ui_state_todo)
    toolbar.set_listener('App Monitor', ui_state_monitor)
    toolbar.set_listener('About', ui_state_about)

    main_window.start()
    work_timer_logic.cleanup()
    app_monitor_inst.cleanup()
