#!/usr/bin/env python3

# app.py - What ties it all together.

import pathlib
import config

import main_window
import work_timer
import app_monitor

if __name__ == '__main__':
    data_dir = pathlib.Path(config.data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

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
