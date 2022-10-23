#!/usr/bin/env python3

# app.py - What ties it all together.

import tkinter as tk
from tkinter import ttk

import main_window
import work_timer
import app_monitor

if __name__ == '__main__':
    main_window_obj = main_window.MainWindow()
    
    work_timer_logic = work_timer.WorkTimer(
        main_window_obj.get_work_timer_ui()
    )
    
    app_monitor_logic = app_monitor.AppMonitor(
        main_window_obj.get_app_monitor_ui()
    )

    main_window_obj.start()
    work_timer_logic.cleanup()
    app_monitor_logic.cleanup()
