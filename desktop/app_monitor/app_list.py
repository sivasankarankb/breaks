import psutil
import tkinter as tk
from tkinter import ttk

class AppListUI:
    def __refresh_list(self):
        apps = {}

        for pid in psutil.pids():
            try: info = psutil.Process(pid).as_dict(['create_time', 'name', 'exe'])
            except: continue
            
            if info['exe'] == None or len(info['exe']) == 0: continue
                
            apps[info['exe']] = [info['create_time'], info['name'], info['exe']]


        try:
            if len(self.__app_ids) > 0:
                for app in self.__app_ids: self.__process_list.delete(app)

        except: pass

        self.__app_ids = list(apps.keys())
        list_entries = list(apps.values())
        list_entries.sort(key=lambda elt: elt[0], reverse=True)

        for entry in list_entries:
            self.__process_list.insert(
                '', 'end', iid=entry[2], text=entry[1], values=[entry[2]]
            )
        
    def __init__(self, master=None):
        self.__window = tk.Toplevel(master=master)
        self.__window.rowconfigure(0, weight=1)
        self.__window.columnconfigure(0, weight=1)

        self.__window.title('Select App')
        self.__window.minsize(width=480, height=450)
        
        self.__container = ttk.Frame(self.__window)
        self.__container.grid(
            row=0, column=0, sticky=tk.NSEW, padx=16, pady=16
        )
        
        self.__message = ttk.Label(
            self.__container, text='Select an app to add.'
        )
        
        self.__message.grid(pady=(0,8), sticky=tk.W)

        self.__process_list = ttk.Treeview(
            self.__container, height=16, columns=['path']
        )

        self.__process_list.heading('#0', text='Application')
        self.__process_list.heading('#1', text='Path')

        self.__process_list.column('#0', width=120, stretch=False)
        self.__process_list.column('#1', anchor=tk.W)
        
        self.__process_list.grid(
            row=1, column=0, pady=(0,8), sticky=tk.NSEW
        )

        self.__list_scroll_right = ttk.Scrollbar(
            self.__container, orient='vertical'
        )

        self.__list_scroll_right.grid(
            row=1, column=1, pady=(0,8), sticky=tk.NS
        )

        self.__process_list.configure(yscrollcommand=self.__list_scroll_right.set)
        self.__list_scroll_right.configure(command=self.__process_list.yview)
        

        self.__ok_button = ttk.Button(
            self.__container, text='Ok', command=self.__ok_click
        )

        self.__ok_button.grid(row=3, column=0, columnspan=2, sticky=tk.E)

        self.__ok_button_listener = None

        self.__container.rowconfigure(1, weight=1)
        self.__container.columnconfigure(0, weight=1)

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
