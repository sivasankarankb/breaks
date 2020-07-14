
# logic.py - Core logic

import plyer
import psutil
import time
import threading

import timers
import config
import settings
import persistance

class Notifier:
    def notify(message):
        plyer.notification.notify(title=config.app_name, message=message)

class WorkTimer:
    def __init__(self, ui):
        self.__ui = ui
        self.__ui.set_time_text('Ready?')
        self.__ui.set_timer_set_button_text('Set')

        self.__ui.set_timer_set_button_listener(
          self.__timer_set_button_listener
        )

        self.__ui.set_timer_button_text('Let\'s begin!')
        self.__ui.set_timer_button_listener(self.__timer_button_listener)

        self.__timer_button_state = 'init'
        #self.__work_data = persistance.WorkData()

    def __timer_button_listener(self):
        if self.__timer_button_state == 'init':
            #self.__work_data.begin()
            self.__ui.set_timer_button_text('Take a break.')

            self.__countdown_timer = timers.Countdown(
                settings.work_period, self.__timer_done
            )

            self.__countdown_timer.set_progress_callback(self.__timer_update)
            self.__countdown_timer.start()
            self.__timer_button_state = 'break'

        elif self.__timer_button_state == 'begin':
            #self.__work_data.record_event('start-work')
            self.__ui.set_timer_button_text('Take a break.')

            self.__countdown_timer = timers.Countdown(
                settings.work_period, self.__timer_done
            )

            self.__countdown_timer.set_progress_callback(self.__timer_update)
            self.__countdown_timer.start()
            self.__timer_button_state = 'break'

        elif self.__timer_button_state == 'break':
            #self.__work_data.record_event('take-break')
            self.__ui.set_timer_button_text('Let\'s work!')

            if not self.__countdown_timer.completed():
                self.__countdown_timer.cancel()
                self.__ui.set_time_text('Done')

            self.__countdown_timer = None
            self.__timer_button_state = 'begin'

    def __timer_set_button_listener(self):
        dur = self.__ui.get_integer("Duration:")

        if dur != None and dur > 0: settings.work_period = dur * 60

    def __timer_done(self):
        #self.__work_data.record_event('time-up')
        self.__ui.set_time_text('Done')
        Notifier.notify('Take a break.')

    def __timer_update(self, seconds):
        minutes = seconds // 60
        self.__ui.set_time_text( str(minutes) + ' minute(s) left')

    def cleanup(self): pass #self.__work_data.end()

class AppMonitor:
    def __init__(self, ui):
        ui.set_list_headings(['App', 'Open for'])
        ui.set_list_col_width(1, 60)

        ui.set_add_listener(self.__add_app)
        ui.set_edit_listener(self.__edit_app)
        ui.set_remove_listener(self.__remove_app)
        
        self.__ui = ui
        self.__list_class = None
        self.__list_class_params = ()

        self.__monlist = {}
        self.__monlist_lock = threading.Lock()
        
        self.__app_edit_class = None
        self.__app_edit_class_params = ()

    def set_app_list_class(self, list_class, params=()):
        self.__list_class = list_class
        self.__list_class_params = params

    def set_app_edit_class(self, edit_class, params=()):
        self.__app_edit_class = edit_class
        self.__app_edit_class_params = params

    def __update_info(self, info):
        key = info['exe']

        start = info['create_time']
        now = time.time()
        
        if 'last-seen' not in self.__monlist[key]: # Initial entry
            self.__monlist[key]['or-first-seen'] = start
            self.__monlist[key]['first-seen'] = start
            self.__monlist[key]['last-seen'] = now
            self.__monlist[key]['duration'] = now - start

        else:
            
            last = self.__monlist[key]['last-seen']
            delay = now - last

            if delay > 60: # Stale
                if start > self.__monlist[key]['first-seen']:
                    self.__monlist[key]['first-seen'] = start
                    last = start

                self.__monlist[key]['duration'] += now - last
                self.__monlist[key]['last-seen'] = now
        

    def __render_list(self):
        content = []

        for exe in self.__monlist:
            task = self.__monlist[exe]

            min = int(task['duration'] // 60)
            hrs = int(min // 60)
            min = min % 60

            duration = str(hrs) + 'hr ' + str(min) + 'min'
            
            entry = [task['name']]
            entry.append(duration)
            entry.append(exe)
            
            content.append(entry)

        self.__ui.set_list_content(content, idix=2)

    def __refresh_tasks(self):
        self.__monlist_lock.acquire(blocking=False)

        if not self.__monlist_lock.locked(): return
        
        for pid in psutil.pids():
            try: info = psutil.Process(pid).as_dict(
                  ['create_time', 'exe', 'pid']
                )

            except: continue

            if info['exe'] in self.__monlist: self.__update_info(info)

        self.__render_list()
        self.__monlist_lock.release()
        
    def __add_app(self):
        if self.__list_class == None: return
        dialog = self.__list_class(*self.__list_class_params)
        dialog.set_ok_listener(self.__add_ok)

    def __add_ok(self, app_name, app_path):
        if app_path not in self.__monlist:
            with self.__monlist_lock:
                self.__monlist[app_path] = {'name': app_name, 'limit': None}
            self.__refresh_tasks()

    def __edit_app(self, selection):
        if self.__edit_class == None: return

    def __remove_app(self, selection):
        with self.__monlist_lock:
            self.__monlist.pop(selection, None)
        self.__refresh_tasks()
