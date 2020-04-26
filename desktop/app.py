#!/usr/bin/env python3

# app.py - What ties it all together.

import ui
import logic

app_ui = ui.App()
work_timer_ui = ui.WorkTimer(master=app_ui.get_top_level_window())
work_timer_logic = logic.WorkTimer(work_timer_ui)

app_ui.start()
work_timer_logic.cleanup()
