#!/usr/bin/env python3

# app.py - What ties it all together.

import ui
import logic
import persistance

if __name__ == '__main__':
    app_ui = ui.App()
    master = app_ui.get_nesting_window()

    doing_now = ui.DoingNow(master=master, expand='both')

    work_timer_ui = ui.WorkTimer(master=master, expand='horizontal')
    work_timer_logic = logic.WorkTimer(work_timer_ui)

    #work_time_viewer = ui.WorkTimeViewer(master=master, expand=True)

    app_ui.start()
    work_timer_logic.cleanup()
