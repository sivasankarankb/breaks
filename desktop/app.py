#!/usr/bin/env python3

# app.py - What ties it all together.

import ui
import logic

if __name__ == '__main__':
    app_ui = ui.App()
    master = app_ui.get_nesting_window()

    toolbar = ui.Toolbar(
        button_labels=['Home', 'To do', 'App Monitor', 'About'],
        button_icons=['home', 'notes', 'screen', 'info'],
        master=master, row=0, column=0, expand='vertical'
    )
    
    doing_now = ui.DoingNow(master=master, row=0, column=1, expand='both')

    work_timer_ui = ui.WorkTimer(master=master, column=1, expand='horizontal')
    work_timer_logic = logic.WorkTimer(work_timer_ui)
    
    to_do_list = ui.ToDoList(master=master, row=0, column=1, expand='both')

    app_monitor_ui = ui.AppMonitor(
        master=master, row=0, column=1, expand='both'
    )

    app_monitor = logic.AppMonitor(app_monitor_ui)
    app_monitor.set_app_list_class(ui.AppList, (master,))
    app_monitor.set_app_edit_class(ui.AppEdit, (master,))
    
    #work_time_viewer = ui.WorkTimeViewer(master=master, expand=True)

    about_box = ui.AboutBox(
        master=master, row=0, column=1, expand='both'
    )

    def ui_state_home():
        global doing_now, work_timer_ui, to_do_list, app_monitor_ui, about_box
        
        doing_now.show()
        work_timer_ui.show()
        to_do_list.hide()
        app_monitor_ui.hide()
        about_box.hide()

    def ui_state_todo():
        global doing_now, work_timer_ui, to_do_list, app_monitor_ui, about_box
        
        doing_now.hide()
        work_timer_ui.hide()
        to_do_list.show()
        app_monitor_ui.hide()
        about_box.hide()

    def ui_state_monitor():
        global doing_now, work_timer_ui, to_do_list, app_monitor_ui, about_box
        
        doing_now.hide()
        work_timer_ui.hide()
        to_do_list.hide()
        app_monitor_ui.show()
        about_box.hide()

    def ui_state_about():
        global doing_now, work_timer_ui, to_do_list, app_monitor_ui, about_box
        
        doing_now.hide()
        work_timer_ui.hide()
        to_do_list.hide()
        app_monitor_ui.hide()
        about_box.show()

    ui_state_home()

    toolbar.set_listener('Home', ui_state_home)
    toolbar.set_listener('To do', ui_state_todo)
    toolbar.set_listener('App Monitor', ui_state_monitor)
    toolbar.set_listener('About', ui_state_about)

    app_ui.start()
    work_timer_logic.cleanup()
    app_monitor.cleanup()
