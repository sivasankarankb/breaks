import tkinter as tk
from tkinter import ttk

from ui import GridPlaceable

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