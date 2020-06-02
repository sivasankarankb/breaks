
# ui.py - (Graphical) User Interface stuff

import tkinter as tk
from tkinter import ttk

import config

class App:
    def __setup_window(self):
        self.__tk.minsize(width = 300, height = 150)
        self.__tk.rowconfigure(0, weight = 1)
        self.__tk.columnconfigure(0, weight = 1)

    def __init__(self):
        self.__tk = tk.Tk()
        self.__tk.title(config.app_name)
        self.__tk.protocol("WM_DELETE_WINDOW", self.__exit)

        self.__setup_window()

    def start(self): self.__tk.mainloop()

    def get_top_level_window(self): return self.__tk

    def minimise_main_window(self): self.__tk.iconify()

    def hide_main_window(self): self.__tk.withdraw()

    def show_main_window(self): self.__tk.deiconify()

    def __exit(self): self.__tk.destroy()

class GridPlaceable:
    def __init__(self, master = None, row=None, column=None):
        params = {}
        if row != None: params['row'] = row
        if column != None: params['column'] = column

        frame = ttk.Frame(master)
        frame.grid(sticky=tk.NSEW, **params)

        self.create_widgets(frame)

class WorkTimer(GridPlaceable):
    def create_widgets(self, frame):
        self.__timer_time = ttk.Label(frame)
        self.__timer_time.grid()

        self.__timer_button = ttk.Button(
            frame, command=self.__click_timer_button
        )
        self.__timer_button.grid()
        self.__timer_button_listener = None

        frame.rowconfigure(0, weight = 1)
        frame.rowconfigure(1, weight = 1)
        frame.columnconfigure(0, weight = 1)

    def __click_timer_button(self):
        if self.__timer_button_listener != None: self.__timer_button_listener()

    def set_time_text(self, txt): self.__timer_time.config(text = txt)

    def set_timer_button_text(self, txt):
        self.__timer_button.config(text = txt)

    def set_timer_button_listener(self, listener = None):
        self.__timer_button_listener = listener

class TimeGraph(GridPlaceable):
    def create_widgets(self, frame):
        frame.grid_configure(sticky=tk.EW)
        frame.columnconfigure(0, weight=1)

        self.__canvas = tk.Canvas(frame, height=32)
        self.__canvas.grid(sticky=tk.EW)

        self.__graph_data = []
        self.draw()

        frame.bind('<Configure>', self.__canvas_reconfigure, add=True)

    def __canvas_reconfigure(self, event):
        params = str(event).split()[2:]

        for param in params:
            key, value = param.split('=')
            if key == 'width': self.draw(value)

    def set_data(self, data, normalise=True):
        total = 0
        for item in data: total += item[0]

        if normalise:
            normalised = []
            for item in data: normalised.append((item[0] / total, item[1]))

        else: normalised = data

        self.__graph_data = normalised

    def set_height(self, height): self.__canvas['height'] = height

    def draw(self, width=None):
        try:
            for item in self.__graph_ids: self.__canvas.delete(item)
        except: pass

        self.__graph_ids = []

        x1, y1 = 3, 3
        y2 = int(self.__canvas['height']) - 3
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
    def create_widgets(self, frame):
        pass
