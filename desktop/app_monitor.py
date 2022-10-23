import time
import threading
import psutil

import tkinter as tk
from tkinter import ttk

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

class AppMonitorUI:
    def __init__(self, master):
        self.__container = ttk.Frame(master)
        self.__container.grid(column=0, columnspan=2, pady=(0,16))        
        
        self.__add_button = ttk.Button(self.__container, text='Add')
        self.__add_button.grid(row=0, column=0, padx=(0,8))

        self.__edit_button = ttk.Button(
            self.__container, text='Edit', command=self.__edit_click
        )
        
        self.__edit_button.grid(row=0, column=1, padx=(0,8))
        self.__edit_button_listener = None

        self.__remove_button = ttk.Button(
            self.__container, text='Remove', command=self.__remove_click
        )
        
        self.__remove_button.grid(row=0, column=2)
        self.__remove_button_listener = None

        self.__app_list = ttk.Treeview(master, height=8)
        self.__app_list.grid(row=1, padx=(0,8), sticky=tk.NSEW)

        self.__list_scroller = ttk.Scrollbar(
            master, command=self.__app_list.yview, orient='vertical'
        )

        self.__list_scroller.grid(row=1, column=1, sticky=tk.NS)

        self.__app_list.configure(yscrollcommand=self.__list_scroller.set)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.grid_configure(pady=(0,16))

        self.__app_list_iids = []

        self.__app_list_dlg = None
        self.__app_list_ok_listener = None

        self.__edit_app_dlg = None
        self.__edit_app_ok_listener = None

    def set_add_listener(self, listener=None):
        self.__add_button.configure(command=listener)

    def set_edit_listener(self, listener=None):
        self.__edit_button_listener = listener

    def set_remove_listener(self, listener=None):
        self.__remove_button_listener = listener

    def set_list_headings(self, headings):
        self.__app_list.configure(columns=headings[1:])
        self.__app_list.heading('#0', text=headings[0])
        for heading in headings[1:]:
            self.__app_list.heading(heading, text=heading)

    def set_list_content(self, content=[], idix=0, clear=True):
        if len(self.__app_list_iids) > 0 :
            old_iids = self.__app_list_iids[:]

        else: old_iids = []
            
        self.__app_list_iids = []

        for item in content:
            if item[idix] not in old_iids:
                self.__app_list.insert(
                    '', 'end', iid=item[idix], text=item[0], values=item[1:]
                )

            else:
                self.__app_list.item(item[idix], text=item[0], values=item[1:])
                old_iids.remove(item[idix])

            self.__app_list_iids.append(item[idix])

        if len(old_iids) > 0 and clear:
            for old_app in old_iids: self.__app_list.delete(old_app)

    def set_list_col_width(self, col, width):
        try: col = '#' + str(int(col))
        except: pass
        self.__app_list.column(col, width=width)

    def __selection_listener(self, listener):
        selection = self.__app_list.selection()
        
        if len(selection) == 1 and listener != None: listener(selection[0])

    def __edit_click(self):
        self.__selection_listener(self.__edit_button_listener)
    
    def __remove_click(self):
        self.__selection_listener(self.__remove_button_listener)

    def show_app_list(self):
        self.__app_list_dlg = AppListUI(self.__container)

    def set_app_list_ok_listener(self, listener):
        if self.__app_list_dlg != None:
            self.__app_list_dlg.set_ok_listener(self.__handle_app_list_ok)
            self.__app_list_ok_listener = listener

    def __handle_app_list_ok(self, *args, **kwargs):
        if self.__app_list_ok_listener != None:
            self.__app_list_ok_listener(*args, **kwargs)

        self.__app_list_dlg = None
        self.__app_list_ok_listener = None

    def show_edit_app(self, *defaults):
        self.__edit_app_dlg = AppEditUI(self.__container)
        self.__edit_app_dlg.set_default_values(*defaults)

    def set_edit_app_ok_listener(self, listener):
        if self.__edit_app_dlg != None:
            self.__edit_app_dlg.set_ok_listener(self.__handle_edit_app_ok)
            self.__edit_app_ok_listener = listener

    def __handle_edit_app_ok(self, *args, **kwargs):
        if self.__edit_app_ok_listener != None:
            self.__edit_app_ok_listener(*args, **kwargs)

        self.__edit_app_dlg = None
        self.__edit_app_ok_listener = None

class AppListUI:
    def __refresh_list(self):
        apps = {}

        for pid in psutil.pids():
            try: info = psutil.Process(pid).as_dict(['create_time', 'name', 'exe'])
            except: continue
            
            if info['exe'] == None or len(info['exe']) == 0: continue
                
            apps[info['exe']] = [info['create_time'], info['name'], info['exe']]


        try:
            if len(self.__app_ids) > 0:
                for app in self.__app_ids: self.__process_list.delete(app)

        except: pass

        self.__app_ids = list(apps.keys())
        list_entries = list(apps.values())
        list_entries.sort(key=lambda elt: elt[0], reverse=True)

        for entry in list_entries:
            self.__process_list.insert(
                '', 'end', iid=entry[2], text=entry[1], values=[entry[2]]
            )
        
    def __init__(self, master=None):
        self.__window = tk.Toplevel(master=master)
        self.__window.rowconfigure(0, weight=1)
        self.__window.columnconfigure(0, weight=1)

        self.__window.title('Select App')
        self.__window.minsize(width=480, height=450)
        
        self.__container = ttk.Frame(self.__window)
        self.__container.grid(
            row=0, column=0, sticky=tk.NSEW, padx=16, pady=16
        )
        
        self.__message = ttk.Label(
            self.__container, text='Select an app to add.'
        )
        
        self.__message.grid(pady=(0,8), sticky=tk.W)

        self.__process_list = ttk.Treeview(
            self.__container, height=16, columns=['path']
        )

        self.__process_list.heading('#0', text='Application')
        self.__process_list.heading('#1', text='Path')

        self.__process_list.column('#0', width=120, stretch=False)
        self.__process_list.column('#1', anchor=tk.W)
        
        self.__process_list.grid(
            row=1, column=0, pady=(0,8), sticky=tk.NSEW
        )

        self.__list_scroll_right = ttk.Scrollbar(
            self.__container, orient='vertical'
        )

        self.__list_scroll_right.grid(
            row=1, column=1, pady=(0,8), sticky=tk.NS
        )

        self.__process_list.configure(yscrollcommand=self.__list_scroll_right.set)
        self.__list_scroll_right.configure(command=self.__process_list.yview)
        

        self.__ok_button = ttk.Button(
            self.__container, text='Ok', command=self.__ok_click
        )

        self.__ok_button.grid(row=3, column=0, columnspan=2, sticky=tk.E)

        self.__ok_button_listener = None

        self.__container.rowconfigure(1, weight=1)
        self.__container.columnconfigure(0, weight=1)

        self.__refresh_list()

    def __ok_click(self):
        selection = self.__process_list.selection()
        if len(selection) != 1: return

        if self.__ok_button_listener != None:
            exe = selection[0]
            name = self.__process_list.item(exe, 'text')
            self.__ok_button_listener(name, exe)

        self.__window.destroy()

    def set_ok_listener(self, listener=None):
        self.__ok_button_listener = listener

class AppEditUI:
    def __init__(self, master=None):
        self.__window = tk.Toplevel(master=master)
        self.__window.rowconfigure(0, weight=1)
        self.__window.columnconfigure(0, weight=1)

        self.__window.title('Edit App Entry')
        self.__window.minsize(width=400, height=220)
        
        self.__container = ttk.Frame(self.__window)
        self.__container.grid(
            row=0, column=0, padx=16, pady=16
        )

        self.__name_label = ttk.Label(
            self.__container, text='App friendly name'
        )

        self.__name_label.grid(
            row=0, column=0, padx=(0,16), pady=(0,32), sticky=tk.E
        )

        self.__name_text = ttk.Entry(self.__container, width=30)
        self.__name_text.grid(row=0, column=1, sticky=tk.EW, pady=(0,32))

        # ---

        self.__time_limit_label = ttk.Label(
            self.__container, text='App usage limit'
        )

        self.__time_limit_label.grid(
            row=1, column=0, padx=(0,16), pady=(0,16), sticky=tk.E
        )

        self.__time_limit_frame = ttk.Frame(self.__container)
        self.__time_limit_frame.grid(row=1, column=1, pady=(0,16), sticky=tk.EW)


        self.__time_hrs = ttk.Entry(self.__time_limit_frame, width=4)
        self.__time_hrs.grid(row=0, column=0, padx=(0,8))

        self.__time_hrs_label = ttk.Label(
            self.__time_limit_frame, text='hours'
        )
        
        self.__time_hrs_label.grid(row=0, column=1, padx=(0,8), sticky=tk.W)

        self.__time_min = ttk.Entry(self.__time_limit_frame, width=4)
        self.__time_min.grid(row=0, column=2, padx=(0,8))

        self.__time_min_label = ttk.Label(
            self.__time_limit_frame, text='minutes'
        )
        self.__time_min_label.grid(row=0, column=3)

        self.__container.columnconfigure(1, weight=1)
        self.__time_limit_frame.columnconfigure(1, weight=1)
        
        # ---

        self.__limit_toggle_frame = ttk.Frame(self.__container)
        self.__limit_toggle_frame.grid(
            row=2, column=1, pady=(0,8), sticky=tk.EW
        )

        limit_toggle = tk.StringVar(value='off')
        self.__limit_toggle_var = limit_toggle

        self.__limit_radio_on = ttk.Radiobutton(
            self.__limit_toggle_frame, variable=limit_toggle,
            value='on', text='Enabled', command=self.__limit_toggled
        )

        self.__limit_radio_on.grid(row=0, column=0, padx=(0,8), sticky=tk.W)

        self.__limit_radio_off = ttk.Radiobutton(
            self.__limit_toggle_frame, variable=limit_toggle,
            value='off', text='Disabled', command=self.__limit_toggled
        )

        self.__limit_radio_off.grid(row=0, column=1)
        self.__limit_toggled()

        # ---

        self.__ok_button = ttk.Button(
            self.__container, text='Ok', command=self.__ok_click
        )

        self.__ok_button.grid(row=3, column=1, sticky=tk.E, pady=(24,0))
        self.__ok_button_listener = None
        self.__app_identity = None
        
    def __limit_toggled(self):
        if self.__limit_toggle_var.get() == 'on':
            self.__time_min.state(('!disabled',))
            self.__time_hrs.state(('!disabled',))
        else:
            self.__time_min.state(('disabled',))
            self.__time_hrs.state(('disabled',))

    def __ok_click(self):
        if self.__ok_button_listener != None:
            name = self.__name_text.get().strip()
            limit = None
            
            if self.__limit_toggle_var.get() == 'on':
                try: hrs = int(self.__time_hrs.get().strip())
                except: hrs = 0
                
                try: mins = int(self.__time_min.get().strip())
                except: mins = 0

                if hrs > -1 and mins > -1 and (hrs != 0 or mins != 0):
                    limit = (hrs * 60 + mins) * 60

            self.__ok_button_listener(name, limit, self.__app_identity)

        self.__window.destroy()

    def set_default_values(self, name, limit=None, identity=None):
        self.__app_identity = identity
        last = len(self.__name_text.get())

        if last > 0: self.__name_text.delete(0, last)

        self.__name_text.insert(0, name.strip())
        last = len(self.__time_hrs.get())
            
        if last > 0: self.__time_hrs.delete(0, last)
            
        last = len(self.__time_min.get())
            
        if last > 0: self.__time_min.delete(0, last)

        if limit == None:
            self.__limit_toggle_var.set('off')
            self.__limit_toggled()
            self.__time_hrs.insert(0, '0')
            self.__time_min.insert(0, '0')

        else:
            mins = int(limit) // 60
            hrs = int(mins // 60)
            mins =int(mins % 60)
            self.__limit_toggle_var.set('on')
            self.__limit_toggled()
            self.__time_hrs.insert(0, str(hrs))
            self.__time_min.insert(0, str(mins))

    def set_ok_listener(self, listener): self.__ok_button_listener = listener
