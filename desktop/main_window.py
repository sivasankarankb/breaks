import tkinter as tk
from tkinter import ttk

import config

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
