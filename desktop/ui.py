
# ui.py - (Graphical) User Interface stuff

import tkinter as tk
from tkinter import ttk

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
