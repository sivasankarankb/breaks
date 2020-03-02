
# ui.py - (Graphical) User Interface stuff

import tkinter as tk
from tkinter import ttk

import config

class AppUI_tkinter(ttk.Frame):
    def __init__(self, master = None):
        ttk.Frame.__init__(self, master)
        self.__top_level_window = self.winfo_toplevel()

        self.master.title(config.app_name)
        self.__setup_window()
        self.__create_widgets()

        self.__top_level_window.protocol("WM_DELETE_WINDOW", self.__exit)

    def __setup_window(self):
        self.__top_level_window.minsize(width = 300, height = 150)
        self.__top_level_window.rowconfigure(0, weight = 1)
        self.__top_level_window.columnconfigure(0, weight = 1)
        self.grid(sticky = tk.N + tk.S + tk.E + tk.W)

    def __create_widgets(self):
        self.__timer_time = ttk.Label(self)
        self.__timer_time.grid()

        self.__timer_button = ttk.Button(self, command=self.__click_timer_button)
        self.__timer_button.grid()
        self.__timer_button_listener = None

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)

    def __click_timer_button(self):
        if self.__timer_button_listener != None:
            self.__timer_button_listener()

    def __exit(self):
        self.__top_level_window.destroy()

    def start(self):
        self.mainloop()

    def set_time_text(self, txt):
        self.__timer_time.config(text = txt)

    def set_timer_button_text(self, txt):
        self.__timer_button.config(text = txt)

    def set_timer_button_listener(self, listener = None):
        self.__timer_button_listener = listener

    def hide_main_window(self):
        self.__top_level_window.withdraw()

    def minimise_main_window(self):
        self.__top_level_window.iconify()

    def show_main_window(self):
        self.__top_level_window.deiconify()
