import tkinter as tk
from tkinter import ttk

class DoingNow:
    def __init__(self, master):
        doing_now_label = ttk.Label(master, text='Doing now:')

        doing_now_label.grid(
            row=0, column=0, sticky=tk.W, pady=(0,8)
        )

        clear_button = ttk.Button(
            master, text='Clear', command=self.__clear_click
        )

        clear_button.grid(row=0, column=1, sticky=tk.E, pady=(0,8))

        self.__current_task = tk.Text(
            master, width=40, height=6, wrap='word', padx=4, pady=4
        )

        self.__current_task.grid(sticky=tk.NSEW, columnspan=2)

        master.rowconfigure(1, weight=1)
        master.columnconfigure(0, weight=1)

    def __clear_click(self): self.__current_task.delete('0.0', 'end')