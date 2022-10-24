import tkinter as tk
from tkinter import ttk

from .app_list import AppListUI
from .app_edit import AppEditUI

class AppMonitorUI:
    def __init__(self, master):
        self.__container = ttk.Frame(master)
        self.__container.grid(column=0, columnspan=2, pady=(0,16))        
        
        self.__add_button = ttk.Button(self.__container, text='Add')
        self.__add_button.grid(row=0, column=0, padx=(0,8))

        self.__edit_button = ttk.Button(
            self.__container, text='Edit', command=self.__edit_click
        )
        
        self.__edit_button.grid(row=0, column=1, padx=(0,8))
        self.__edit_button_listener = None

        self.__remove_button = ttk.Button(
            self.__container, text='Remove', command=self.__remove_click
        )
        
        self.__remove_button.grid(row=0, column=2)
        self.__remove_button_listener = None

        self.__app_list = ttk.Treeview(master, height=8)
        self.__app_list.grid(row=1, padx=(0,8), sticky=tk.NSEW)

        self.__list_scroller = ttk.Scrollbar(
            master, command=self.__app_list.yview, orient='vertical'
        )

        self.__list_scroller.grid(row=1, column=1, sticky=tk.NS)

        self.__app_list.configure(yscrollcommand=self.__list_scroller.set)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.grid_configure(pady=(0,16))

        self.__app_list_iids = []

        self.__app_list_dlg = None
        self.__app_list_ok_listener = None

        self.__edit_app_dlg = None
        self.__edit_app_ok_listener = None

    def set_add_listener(self, listener=None):
        self.__add_button.configure(command=listener)

    def set_edit_listener(self, listener=None):
        self.__edit_button_listener = listener

    def set_remove_listener(self, listener=None):
        self.__remove_button_listener = listener

    def set_list_headings(self, headings):
        self.__app_list.configure(columns=headings[1:])
        self.__app_list.heading('#0', text=headings[0])
        for heading in headings[1:]:
            self.__app_list.heading(heading, text=heading)

    def set_list_content(self, content=[], idix=0, clear=True):
        if len(self.__app_list_iids) > 0 :
            old_iids = self.__app_list_iids[:]

        else: old_iids = []
            
        self.__app_list_iids = []

        for item in content:
            if item[idix] not in old_iids:
                self.__app_list.insert(
                    '', 'end', iid=item[idix], text=item[0], values=item[1:]
                )

            else:
                self.__app_list.item(item[idix], text=item[0], values=item[1:])
                old_iids.remove(item[idix])

            self.__app_list_iids.append(item[idix])

        if len(old_iids) > 0 and clear:
            for old_app in old_iids: self.__app_list.delete(old_app)

    def set_list_col_width(self, col, width):
        try: col = '#' + str(int(col))
        except: pass
        self.__app_list.column(col, width=width)

    def __selection_listener(self, listener):
        selection = self.__app_list.selection()
        
        if len(selection) == 1 and listener != None: listener(selection[0])

    def __edit_click(self):
        self.__selection_listener(self.__edit_button_listener)
    
    def __remove_click(self):
        self.__selection_listener(self.__remove_button_listener)

    def show_app_list(self):
        self.__app_list_dlg = AppListUI(self.__container)

    def set_app_list_ok_listener(self, listener):
        if self.__app_list_dlg != None:
            self.__app_list_dlg.set_ok_listener(self.__handle_app_list_ok)
            self.__app_list_ok_listener = listener

    def __handle_app_list_ok(self, *args, **kwargs):
        if self.__app_list_ok_listener != None:
            self.__app_list_ok_listener(*args, **kwargs)

        self.__app_list_dlg = None
        self.__app_list_ok_listener = None

    def show_edit_app(self, *defaults):
        self.__edit_app_dlg = AppEditUI(self.__container)
        self.__edit_app_dlg.set_default_values(*defaults)

    def set_edit_app_ok_listener(self, listener):
        if self.__edit_app_dlg != None:
            self.__edit_app_dlg.set_ok_listener(self.__handle_edit_app_ok)
            self.__edit_app_ok_listener = listener

    def __handle_edit_app_ok(self, *args, **kwargs):
        if self.__edit_app_ok_listener != None:
            self.__edit_app_ok_listener(*args, **kwargs)

        self.__edit_app_dlg = None
        self.__edit_app_ok_listener = None
