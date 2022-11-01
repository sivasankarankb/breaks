import tkinter as tk
from tkinter import ttk

from .process_info import ProcessInfo

class AppListUI:
    def __refresh_list(self):
        try:
            if len(self.__app_ids) > 0:
                for app in self.__app_ids: self.__process_list.delete(app)

        except: pass

        self.__app_ids = []
        apps = {}

        for pid in self.__proc_info.get_process_ids():
            p = self.__proc_info.get_info_of(pid)
            
            if p == None: continue
            
            path = p.get_path()
            
            if path == None or len(path) == 0: continue
                
            apps[path] = p
            self.__app_ids.append(path)

        sorted_apps = list(apps.values())
        sorted_apps.sort(key=lambda p: p.get_created(), reverse=True)

        for p in sorted_apps:
            self.__process_list.insert(
                '', 'end', iid=p.get_path(),
                text=p.get_label(), values=[p.get_path()]
            )
        
    def __init__(self, master=None):
        self.__window = tk.Toplevel(master=master)
        self.__window.rowconfigure(0, weight=1)
        self.__window.columnconfigure(0, weight=1)

        self.__window.title('Select App')
        self.__window.minsize(width=480, height=450)
        
        container = ttk.Frame(self.__window)
        container.grid(
            row=0, column=0, sticky=tk.NSEW, padx=16, pady=16
        )
        
        message = ttk.Label(
            container, text='Select an app to add.'
        )
        
        message.grid(pady=(0,8), sticky=tk.W)

        self.__process_list = ttk.Treeview(
            container, height=16, columns=['path']
        )

        self.__process_list.heading('#0', text='Application')
        self.__process_list.heading('#1', text='Path')

        self.__process_list.column('#0', width=120, stretch=False)
        self.__process_list.column('#1', anchor=tk.W)
        
        self.__process_list.grid(
            row=1, column=0, pady=(0,8), sticky=tk.NSEW
        )

        list_scroll_right = ttk.Scrollbar(
            container, orient='vertical'
        )

        list_scroll_right.grid(
            row=1, column=1, pady=(0,8), sticky=tk.NS
        )

        self.__process_list.configure(yscrollcommand=list_scroll_right.set)
        list_scroll_right.configure(command=self.__process_list.yview)
        

        ok_button = ttk.Button(
            container, text='Ok', command=self.__ok_click
        )

        ok_button.grid(row=3, column=0, columnspan=2, sticky=tk.E)

        self.__ok_button_listener = None

        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)

        self.__proc_info = ProcessInfo()
        self.__refresh_list()

    def __ok_click(self):
        selection = self.__process_list.selection()
        if len(selection) != 1: return

        if self.__ok_button_listener != None:
            exe = selection[0]
            name = self.__process_list.item(exe, 'text')
            self.__ok_button_listener(name, exe)

        self.__window.destroy()

    def set_ok_listener(self, listener=None):
        self.__ok_button_listener = listener
