
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

class WorkTimer:
    def __init__(self, master = None, row=None, column=None):
        params = {}
        if row != None: params['row'] = row
        if column != None: params['column'] = column

        self.__frame = ttk.Frame(master)
        self.__frame.grid(sticky = tk.N + tk.S + tk.E + tk.W, **params)
        self.__create_widgets()

    def __create_widgets(self):
        self.__timer_time = ttk.Label(self.__frame)
        self.__timer_time.grid()

        self.__timer_button = ttk.Button(
            self.__frame, command=self.__click_timer_button
        )
        self.__timer_button.grid()
        self.__timer_button_listener = None

        self.__frame.rowconfigure(0, weight = 1)
        self.__frame.rowconfigure(1, weight = 1)
        self.__frame.columnconfigure(0, weight = 1)

    def __click_timer_button(self):
        if self.__timer_button_listener != None: self.__timer_button_listener()

    def set_time_text(self, txt): self.__timer_time.config(text = txt)

    def set_timer_button_text(self, txt):
        self.__timer_button.config(text = txt)

    def set_timer_button_listener(self, listener = None):
        self.__timer_button_listener = listener

class TimeGraph():
    def __init__(self, master=None, row=None, column=None):
        params = {}
        if row != None: params['row'] = row
        if column != None: params['column'] = column

        self.__frame = ttk.Frame(master)
        self.__frame.grid(sticky=tk.E + tk.W, **params)

        self.__create_widgets()

    def __create_widgets(self):
        self.__frame.columnconfigure(0, weight=1)

        self.__canvas = tk.Canvas(self.__frame, height=32)
        self.__canvas.grid(sticky=tk.E + tk.W)

        self.__graph_data = []
        self.draw_graph()

    def set_graph_data(self, data, normalise=True):
        total = 0
        for item in data: total += item[0]

        if normalise:
            normalised = []
            for item in data: normalised.append((item[0] / total, item[1]))

        else: normalised = data

        self.__graph_data = normalised

    def draw_graph(self):
        try:
            for item in self.__graph_ids: self.__canvas.delete(item)
        except: pass

        self.__graph_ids = []

        x1, y1 = 3, 3
        y2 = int(self.__canvas['height']) - 3
        width = int(self.__canvas['width']) - 5

        for point in self.__graph_data:
            x2 = x1 + (width * point[0])
            fill = point[1]
            item = self.__canvas.create_rectangle(x1, y1, x2, y2, fill=fill)

            self.__graph_ids.append(item)
            x1 = x2
