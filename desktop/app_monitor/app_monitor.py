import time
import threading
import psutil

import timers
import persistance

from notifier import Notifier

class AppMonitor:
    def __init__(self, ui):
        ui.set_list_headings(['App', 'Open for'])
        ui.set_list_col_width(1, 60)

        ui.set_add_listener(self.__add_app)
        ui.set_edit_listener(self.__edit_app)
        ui.set_remove_listener(self.__remove_app)
        
        self.__ui = ui

        self.__monlist = {}
        self.__monlist_lock = threading.Lock()

        self.__autorefresh_on = False
        self.__autorefresh_interval = 60 # seconds

        pers = persistance.AppMonitorData()
        data = pers.load() # Load monitoring list, if any.

        if data != None:
            self.__monlist = data
            if len(data) > 0: self.__begin_autorefresh()

    def __update_info(self, info):
        key = info['exe']

        start = info['create_time']
        now = time.time()
        
        if 'last-seen' not in self.__monlist[key]: # Initial entry
            self.__monlist[key]['or-first-seen'] = start
            self.__monlist[key]['first-seen'] = start
            self.__monlist[key]['last-seen'] = now
            self.__monlist[key]['duration'] = now - start

            return True

        else:
            
            last = self.__monlist[key]['last-seen']
            delay = now - last
            first = self.__monlist[key]['first-seen']

            if delay > self.__autorefresh_interval or start==first: # Stale
                
                if start > self.__monlist[key]['first-seen']:
                    self.__monlist[key]['first-seen'] = start
                    last = start

                self.__monlist[key]['duration'] += now - last
                self.__monlist[key]['last-seen'] = now

                return True

        return False

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

            if info['exe'] in self.__monlist:
                changed = self.__update_info(info)

                if changed:
                    name = self.__monlist[info['exe']]['name']
                    limit = self.__monlist[info['exe']]['limit']
                    duration = self.__monlist[info['exe']]['duration']

                    if limit != None and duration > limit:
                        Notifier.notify(name + ' has exceeded it\'s time limit!\nPlease consider closing it.')

        self.__render_list()
        self.__monlist_lock.release()
        
    def __add_app(self):
        self.__ui.show_app_list()
        self.__ui.set_app_list_ok_listener(self.__add_ok)

    def __autorefresh_task(self):
        if not self.__autorefresh_on: return
        
        self.__autorefresh_timer = timers.Countdown(
            self.__autorefresh_interval, self.__autorefresh_task
        )

        self.__autorefresh_timer.start()
        self.__refresh_tasks()

    def __begin_autorefresh(self):
        if not self.__autorefresh_on:
            self.__autorefresh_on = True
            self.__autorefresh_task()

    def __end_autorefresh(self):
        if self.__autorefresh_on:
            self.__autorefresh_on = False
            self.__autorefresh_timer.cancel()

    def __add_ok(self, app_name, app_path):
        if app_path not in self.__monlist:
            with self.__monlist_lock:
                self.__monlist[app_path] = {'name': app_name, 'limit': None, 'duration': 0}

            self.__refresh_tasks()
            self.__edit_app(app_path)

            self.__begin_autorefresh()

    def __edit_app(self, selection):
        self.__ui.show_edit_app(
            self.__monlist[selection]['name'],
            self.__monlist[selection]['limit'], selection
        )

        self.__ui.set_edit_app_ok_listener(self.__edit_ok)

    def __edit_ok(self, name, limit, selection):
        with self.__monlist_lock:
            self.__monlist[selection]['name'] = name
            self.__monlist[selection]['limit'] = limit

        self.__refresh_tasks()

    def __remove_app(self, selection):
        with self.__monlist_lock:
            self.__monlist.pop(selection, None)
            if len(self.__monlist) == 0: self.__end_autorefresh()
        self.__refresh_tasks()

    def cleanup(self):
        self.__end_autorefresh()
        
        pers = persistance.AppMonitorData()

        data = {}
        ml = self.__monlist

        for key in ml:
            data[key] = {
                'name': ml[key]['name'], 'limit': ml[key]['limit'],
                'duration': 0
            }
            
        pers.save(data)
