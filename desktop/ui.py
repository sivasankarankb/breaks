
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
    def __init__(self, master = None):
        self.__frame = ttk.Frame(master)
        self.__frame.grid(sticky = tk.N + tk.S + tk.E + tk.W)
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
