
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
