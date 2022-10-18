import tkinter as tk
from tkinter import ttk

from ui import GridPlaceable

class ToDoList(GridPlaceable):
    def initialise(self, frame):
        self.__tasks = {}
        self.__create_widgets(frame)

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

        self.__todo_list.bind('<<TreeviewSelect>>', self.__show_selection)

        self.__todo_list_scroll = ttk.Scrollbar(
            frame, command=self.__todo_list.yview, orient='vertical'
        )

        self.__todo_list_scroll.grid(
            row=1, column=1, rowspan=3, sticky=tk.NS, padx=(0,8), pady=(0,8)
        )

        self.__todo_list.configure(yscrollcommand=self.__todo_list_scroll.set)

        self.__todo_task_label = ttk.Label(frame, text='Task')
        self.__todo_task_label.grid(row=0, column=2, pady=(0,8), sticky=tk.W)

        self.__todo_task = ttk.Entry(frame)
        self.__todo_task.grid(row=1, column=2, sticky=tk.EW, pady=(0,8))

        self.__todo_desc_label = ttk.Label(frame, text='Description')
        self.__todo_desc_label.grid(row=2, column=2, pady=(0,8), sticky=tk.W)

        self.__todo_description = tk.Text(
            frame, width=40, height=10, wrap='word', padx=4, pady=4
        )

        self.__todo_description.grid(
            row=3, column=2, sticky=tk.NSEW, pady=(0,8)
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
        self.__todo_task_bot_frame.grid(row=4, column=2, sticky=tk.NSEW)

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
        frame.columnconfigure(2, weight=1)

    def __task_clear(self): self.__todo_task.delete('0', 'end')

    def __task_descr_clear(self): self.__todo_description.delete('0.0', 'end')

    def __list_clear(self):
        for task in self.__tasks: self.__todo_list.delete(task)
        self.__tasks = {}
        self.__show_selection()

    def __list_add(self):
        self.__todo_list_bot_frame.grid_remove()
        self.__todo_task_bot_frame.grid()

        self.__task_clear()
        self.__task_descr_clear()

    def __list_rem(self):
        sel = self.__todo_list.selection()

        if len(sel) == 1:
            self.__tasks.pop(sel[0])
            self.__todo_list.delete(sel[0])
            self.__show_selection()

    def __show_selection(self, event=None):
        self.__task_clear()
        self.__task_descr_clear()

        sel = self.__todo_list.selection()

        if len(sel) == 1:
            self.__todo_task.insert('0', sel[0])
            self.__todo_description.insert('0.0', self.__tasks[sel[0]])

    def __add_ok(self):
        self.__todo_list_bot_frame.grid()
        self.__todo_task_bot_frame.grid_remove()

        task = self.__todo_task.get().strip()
        description = self.__todo_description.get('0.0', 'end')

        if len(task) == 0:
            self.__show_selection()
            return

        self.__todo_list.insert('', 'end', iid=task, text=task)
        self.__tasks[task] = description
        self.__todo_list.selection_set(task)
        self.__show_selection()

    def __add_cancel(self):
        self.__todo_list_bot_frame.grid()
        self.__todo_task_bot_frame.grid_remove()
        self.__show_selection()
