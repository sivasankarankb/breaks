
# ui.py - (Graphical) User Interface stuff

import tkinter as tk
import tkinter.simpledialog as tkdlg
from tkinter import ttk

import config
import persistance

class App:
    def __setup_window(self):
        self.__tk.minsize(width = 300, height = 0)
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

        self.initialise(frame)

    def initialise(self, frame): pass

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

    def get_integer(self, message, title=''):
        value = tkdlg.askstring(title, message)

        try: return int(value)
        except: return None


class TimeGraph(GridPlaceable):
    def initialise(self, frame): self.__create_widgets(frame)

    def __create_widgets(self, frame):
        self.__canvas = tk.Canvas(frame, width=1, height=16)
        self.__canvas.grid(sticky=tk.NSEW)

        #frame.grid_configure(sticky=tk.EW)
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
    def initialise(self, frame): self.__create_widgets(frame)

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

        self.__todo_task_label = ttk.Label(frame, text='Task')
        self.__todo_task_label.grid(row=0, column=1, pady=(0,8), sticky=tk.W)

        self.__todo_task = ttk.Entry(frame)
        self.__todo_task.grid(row=1, column=1, sticky=tk.EW, pady=(0,8))

        self.__todo_desc_label = ttk.Label(frame, text='Description')
        self.__todo_desc_label.grid(row=2, column=1, pady=(0,8), sticky=tk.W)

        self.__todo_description = tk.Text(
            frame, width=40, height=10, wrap='word', padx=4, pady=4
        )

        self.__todo_description.grid(
            row=3, column=1, sticky=tk.NSEW, pady=(0,8)
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
        self.__todo_task_bot_frame.grid(row=4, column=1, sticky=tk.NSEW)

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
        frame.columnconfigure(1, weight=1)

    def __task_clear(self): self.__todo_task.delete('0', 'end')

    def __task_descr_clear(self): self.__todo_description.delete('0.0', 'end')

    def __list_clear(self): pass

    def __list_add(self):
        self.__todo_list_bot_frame.grid_remove()
        self.__todo_task_bot_frame.grid()
        
        self.__task_clear()
        self.__task_descr_clear()

    def __list_rem(self): pass

    def __add_ok(self):
        self.__todo_list_bot_frame.grid()
        self.__todo_task_bot_frame.grid_remove()

    def __add_cancel(self):
        self.__todo_list_bot_frame.grid()
        self.__todo_task_bot_frame.grid_remove()
