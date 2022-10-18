
# ui.py - (Graphical) User Interface stuff

import tkinter as tk
import tkinter.simpledialog as tkdlg
from tkinter import ttk

import config
import persistance

import psutil

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

    def start(self): self.__tk.mainloop()

    def get_nesting_window(self): return self.__outer_frame

    def minimise_main_window(self): self.__tk.iconify()

    def hide_main_window(self): self.__tk.withdraw()

    def show_main_window(self): self.__tk.deiconify()

    def __exit(self): self.__tk.destroy()

class GridPlaceable:
    def __init__(self, master = None, row=None, column=None, expand=None):
        params = {}
        if row != None: params['row'] = row
        if column != None: params['column'] = column

        frame = ttk.Frame(master)
        frame.grid(sticky=tk.NSEW, pady=(0,16), **params)

        if master != None and expand != None:
            info = frame.grid_info()
            row = int(info['row'])
            col = int(info['column'])

            if expand == 'horizontal' or expand == 'both':
                master.columnconfigure(col, weight=1)

            if expand == 'vertical' or expand == 'both':
                master.rowconfigure(row, weight=1)

        self.__frame = frame
        self.initialise(frame)

    def initialise(self, frame): pass

    def hide(self): self.__frame.grid_remove()

    def show(self): self.__frame.grid()

class WorkTimer(GridPlaceable):
    def initialise(self, frame): self.__create_widgets(frame)

    def __create_widgets(self, frame):
        iframe = ttk.Frame(frame, padding=8, borderwidth=1, relief='solid')
        iframe.grid(sticky=tk.NSEW)

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        frame = iframe

        self.__timer_time = ttk.Label(frame)
        self.__timer_time.grid(row=0, column=0)

        self.__timer_set_button = ttk.Button(
            frame, command=self.__click_timer_set_button
        )

        self.__timer_set_button.grid(row=0, column=1, padx=(0,8))
        self.__timer_set_button_listener = None

        self.__timer_button = ttk.Button(
            frame, command=self.__click_timer_button
        )
        self.__timer_button.grid(row=0, column=2)
        self.__timer_button_listener = None

        frame.columnconfigure(0, weight = 1)

    def __click_timer_button(self):
        if self.__timer_button_listener != None: self.__timer_button_listener()

    def __click_timer_set_button(self):
        if self.__timer_set_button_listener != None:
            self.__timer_set_button_listener()

    def set_time_text(self, txt): self.__timer_time.config(text = txt)

    def set_timer_button_text(self, txt): self.__timer_button.config(text = txt)

    def set_timer_button_listener(self, listener = None):
        self.__timer_button_listener = listener

    def set_timer_set_button_text(self, txt):
        self.__timer_set_button.config(text = txt)

    def set_timer_set_button_listener(self, listener = None):
        self.__timer_set_button_listener = listener

    def get_integer(self, message, default='0', title=''):
        value = tkdlg.askstring(title, message, initialvalue=default)

        try: return int(value)
        except: return None


class TimeGraph(GridPlaceable):
    def initialise(self, frame): self.__create_widgets(frame)

    def __create_widgets(self, frame):
        self.__canvas = tk.Canvas(frame, width=1, height=16)
        self.__canvas.grid(sticky=tk.NSEW)
        
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.__graph_data = []
        self.draw()

        frame.bind('<Configure>', self.__canvas_reconfigure, add=True)

    def __canvas_reconfigure(self, event):
        changes = str(event)[1:-1].split()[2:] #Angle Brackets sliced off
        params = {}

        for item in changes:
            key, value = item.split('=')
            if key == 'width' or key == 'height': params[key] = value

        if len(params) > 0: self.draw(**params)

    def set_data(self, data, normalise=True):
        total = 0
        for item in data: total += item[0]

        if normalise:
            normalised = []
            for item in data: normalised.append((item[0] / total, item[1]))

        else: normalised = data

        self.__graph_data = normalised

    def set_height(self, height=16): self.__canvas['height'] = height

    def draw(self, width=None, height=None):
        try:
            for item in self.__graph_ids: self.__canvas.delete(item)
        except: pass

        self.__graph_ids = []

        x1, y1 = 3, 3

        if height != None: height = int(height)
        else: height = int(self.__canvas['height'])

        y2 = height - 3

        if width != None: width = int(width) - 5
        else: width = int(self.__canvas['width']) - 5

        for point in self.__graph_data:
            x2 = x1 + (width * point[0])
            fill = point[1]

            item = self.__canvas.create_rectangle(
                x1, y1, x2, y2, fill=fill, outline=''
            )

            self.__graph_ids.append(item)
            x1 = x2

class WorkTimeViewer(GridPlaceable):
    def initialise(self, frame):
        self.__parse_data()
        self.__create_widgets(frame)
        self.__show_day(-1)

    def __parse_data(self):
        self.__data = persistance.WorkData().load()

    def __create_widgets(self, frame):
        self.__day_graph = TimeGraph(frame)

        self.__graph_date = ttk.Label(frame, text='Last day')
        self.__graph_date.grid()

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

    def __show_day(self, index):
        if self.__data == None: return

        timings = []

        try: events = self.__data[index][1]
        except: return

        colors = ['#339900', '#003399']
        icolor = 0

        for event in events:
            timings.append([event[2], colors[icolor]])
            icolor = (icolor + 1) % 2

        self.__day_graph.set_data(timings)
        self.__day_graph.draw()

class DoingNow(GridPlaceable):
    def initialise(self, frame): self.__create_widgets(frame)

    def __create_widgets(self, frame):
        self.__doing_now_label = ttk.Label(frame, text='Doing now:')

        self.__doing_now_label.grid(
            row=0, column=0, sticky=tk.W, pady=(0,8)
        )

        self.__clear_button = ttk.Button(
            frame, text='Clear', command=self.__clear_click
        )

        self.__clear_button.grid(row=0, column=1, sticky=tk.E, pady=(0,8))

        self.__current_task = tk.Text(
            frame, width=40, height=6, wrap='word', padx=4, pady=4
        )

        self.__current_task.grid(sticky=tk.NSEW, columnspan=2)

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

    def __clear_click(self): self.__current_task.delete('0.0', 'end')

class ToDoList(GridPlaceable):
    def initialise(self, frame):
        self.__tasks = {}
        self.__create_widgets(frame)

    def __create_widgets(self, frame):
        self.__todo_list_top_frame = ttk.Frame(frame)

        self.__todo_list_top_frame.grid(
            row=0, column=0, sticky=tk.NSEW, padx=(0,8), pady=(0,8)
        )

        self.__todo_list_label = ttk.Label(
            self.__todo_list_top_frame, text='To do:'
        )

        self.__todo_list_label.grid(row=0, column=0, sticky=tk.W, padx=(0,8))

        self.__todo_clear = ttk.Button(
            self.__todo_list_top_frame, text='Clear', command=self.__list_clear
        )

        self.__todo_clear.grid(row=0, column=1)

        self.__todo_list_top_frame.columnconfigure(0, weight=1)

        self.__todo_list = ttk.Treeview(frame, show='tree', height=12)
        self.__todo_list.grid(
            row=1, column=0, rowspan=3, sticky=tk.NSEW, padx=(0,8), pady=(0,8)
        )

        self.__todo_list.bind('<<TreeviewSelect>>', self.__show_selection)

        self.__todo_list_scroll = ttk.Scrollbar(
            frame, command=self.__todo_list.yview, orient='vertical'
        )

        self.__todo_list_scroll.grid(
            row=1, column=1, rowspan=3, sticky=tk.NS, padx=(0,8), pady=(0,8)
        )

        self.__todo_list.configure(yscrollcommand=self.__todo_list_scroll.set)

        self.__todo_task_label = ttk.Label(frame, text='Task')
        self.__todo_task_label.grid(row=0, column=2, pady=(0,8), sticky=tk.W)

        self.__todo_task = ttk.Entry(frame)
        self.__todo_task.grid(row=1, column=2, sticky=tk.EW, pady=(0,8))

        self.__todo_desc_label = ttk.Label(frame, text='Description')
        self.__todo_desc_label.grid(row=2, column=2, pady=(0,8), sticky=tk.W)

        self.__todo_description = tk.Text(
            frame, width=40, height=10, wrap='word', padx=4, pady=4
        )

        self.__todo_description.grid(
            row=3, column=2, sticky=tk.NSEW, pady=(0,8)
        )

        self.__todo_list_bot_frame = ttk.Frame(frame)
        self.__todo_list_bot_frame.grid(row=4, column=0, sticky=tk.NSEW)

        self.__todo_add = ttk.Button(
            self.__todo_list_bot_frame, text='Add', command=self.__list_add
        )

        self.__todo_add.grid(row=0, column=0, sticky=tk.E, padx=(0,4))

        self.__todo_rem = ttk.Button(
            self.__todo_list_bot_frame, text='Remove', command=self.__list_rem
        )

        self.__todo_rem.grid(row=0, column=1, sticky=tk.W, padx=(4,0))

        self.__todo_list_bot_frame.columnconfigure(0, weight=1)
        self.__todo_list_bot_frame.columnconfigure(1, weight=1)

        self.__todo_task_bot_frame = ttk.Frame(frame)
        self.__todo_task_bot_frame.grid(row=4, column=2, sticky=tk.NSEW)

        self.__todo_task_ok = ttk.Button(
            self.__todo_task_bot_frame, text='Ok', command=self.__add_ok
        )

        self.__todo_task_ok.grid(row=0, column=0, sticky=tk.E, padx=(0,4))

        self.__todo_task_cancel = ttk.Button(
            self.__todo_task_bot_frame, text='Cancel', command=self.__add_cancel
        )

        self.__todo_task_cancel.grid(row=0, column=1, sticky=tk.W, padx=(4,0))

        self.__todo_task_bot_frame.columnconfigure(0, weight=1)
        self.__todo_task_bot_frame.columnconfigure(1, weight=1)
        self.__todo_task_bot_frame.grid_remove()

        frame.rowconfigure(3, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(2, weight=1)

    def __task_clear(self): self.__todo_task.delete('0', 'end')

    def __task_descr_clear(self): self.__todo_description.delete('0.0', 'end')

    def __list_clear(self):
        for task in self.__tasks: self.__todo_list.delete(task)
        self.__tasks = {}
        self.__show_selection()

    def __list_add(self):
        self.__todo_list_bot_frame.grid_remove()
        self.__todo_task_bot_frame.grid()

        self.__task_clear()
        self.__task_descr_clear()

    def __list_rem(self):
        sel = self.__todo_list.selection()

        if len(sel) == 1:
            self.__tasks.pop(sel[0])
            self.__todo_list.delete(sel[0])
            self.__show_selection()

    def __show_selection(self, event=None):
        self.__task_clear()
        self.__task_descr_clear()

        sel = self.__todo_list.selection()

        if len(sel) == 1:
            self.__todo_task.insert('0', sel[0])
            self.__todo_description.insert('0.0', self.__tasks[sel[0]])

    def __add_ok(self):
        self.__todo_list_bot_frame.grid()
        self.__todo_task_bot_frame.grid_remove()

        task = self.__todo_task.get().strip()
        description = self.__todo_description.get('0.0', 'end')

        if len(task) == 0:
            self.__show_selection()
            return

        self.__todo_list.insert('', 'end', iid=task, text=task)
        self.__tasks[task] = description
        self.__todo_list.selection_set(task)
        self.__show_selection()

    def __add_cancel(self):
        self.__todo_list_bot_frame.grid()
        self.__todo_task_bot_frame.grid_remove()
        self.__show_selection()

class Toolbar(GridPlaceable):
    def __init__(self, *args, button_labels=None, button_icons=None, **kwargs):
        self.__button_labels = button_labels
        self.__button_icons = button_icons
        self.__buttons = {}
        GridPlaceable.__init__(self, *args, **kwargs)
        
    def initialise(self, frame):
        if self.__button_labels == None: return

        frame.grid_configure(padx=(0,16))
        index=0
        self.__icons = []
        
        for text in self.__button_labels:
            image = None
            
            if self.__button_icons != None:
                name = self.__button_icons[index]
                path = 'icons/' + name + '.png'
                
                try:
                    image = tk.PhotoImage(file=path)
                    self.__icons.append(image) # Save reference, else GC'd
                except: pass


            button = ttk.Button(frame, text=text, image=image)
            button.grid(pady=(0,8))
            self.__buttons[text] = button
            index += 1

    def set_listener(self, button, listener):
        if button in self.__buttons:
            self.__buttons[button].configure(command=listener)
            return True

        return False

class AppMonitor(GridPlaceable):
    def initialise(self, frame):
        self.__container = ttk.Frame(frame)
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

        self.__app_list = ttk.Treeview(frame, height=8)
        self.__app_list.grid(row=1, padx=(0,8), sticky=tk.NSEW)

        self.__list_scroller = ttk.Scrollbar(
            frame, command=self.__app_list.yview, orient='vertical'
        )

        self.__list_scroller.grid(row=1, column=1, sticky=tk.NS)

        self.__app_list.configure(yscrollcommand=self.__list_scroller.set)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.grid_configure(pady=(0,16))

        self.__app_list_iids = []

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

class AppList:
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

class AppEdit:
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

class AboutBox(GridPlaceable):
    def initialise(self, frame):
        iframe = ttk.Frame(frame)
        iframe.grid()

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        l1 = ttk.Label(iframe, text=config.app_name)
        l1.grid(pady=(0,8))
        
        l2 = ttk.Label(iframe, text='Version ' + config.app_version)
        l2.grid(pady=(0,8))

        l3 = ttk.Label(iframe, text='https://githhub.com/sivasankarankb/breaks')
        l3.grid(pady=(0,8))

        lcopy = ttk.Label(iframe, text='Copyright (C) 2020-2022 Sivasankaran K B')
        lcopy.grid(pady=(0,20))

        license_txt ='''\
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation.'''

        llicense = ttk.Label(iframe, text=license_txt)
        llicense.grid(pady=(0,20))

        l4 = ttk.Label(iframe, text='-- Contributors --')
        l4.grid(pady=(0,20))

        ll = ttk.Label(iframe, text='Rabeeba Ibrahim')
        ll.grid(pady=(0,8))

        ll = ttk.Label(iframe, text='Shasna Shemsudheen')
        ll.grid(pady=(0,8))

        ll = ttk.Label(iframe, text='Krishnapriya T R')
        ll.grid(pady=(0,16))

        ll = ttk.Label(iframe, text='Serin V Simpson')
        ll.grid(pady=(0,8))

        ll = ttk.Label(iframe, text='Sudharsanan K B')
        ll.grid(pady=(0,8))

        iframe.columnconfigure(0, weight=1)
