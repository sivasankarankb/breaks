import tkinter as tk
from tkinter import ttk

class AppEditUI:
    def __init__(self, master=None):
        self.__window = tk.Toplevel(master=master)
        self.__window.rowconfigure(0, weight=1)
        self.__window.columnconfigure(0, weight=1)

        self.__window.title('Edit App Entry')
        self.__window.minsize(width=400, height=220)
        
        container = ttk.Frame(self.__window)
        container.grid(
            row=0, column=0, padx=16, pady=16
        )

        name_label = ttk.Label(
            container, text='App friendly name'
        )

        name_label.grid(
            row=0, column=0, padx=(0,16), pady=(0,32), sticky=tk.E
        )

        self.__name_text = ttk.Entry(container, width=30)
        self.__name_text.grid(row=0, column=1, sticky=tk.EW, pady=(0,32))

        # ---

        time_limit_label = ttk.Label(
            container, text='App usage limit'
        )

        time_limit_label.grid(
            row=1, column=0, padx=(0,16), pady=(0,16), sticky=tk.E
        )

        time_limit_frame = ttk.Frame(container)
        time_limit_frame.grid(row=1, column=1, pady=(0,16), sticky=tk.EW)


        self.__time_hrs = ttk.Entry(time_limit_frame, width=4)
        self.__time_hrs.grid(row=0, column=0, padx=(0,8))

        time_hrs_label = ttk.Label(
            time_limit_frame, text='hours'
        )
        
        time_hrs_label.grid(row=0, column=1, padx=(0,8), sticky=tk.W)

        self.__time_min = ttk.Entry(time_limit_frame, width=4)
        self.__time_min.grid(row=0, column=2, padx=(0,8))

        time_min_label = ttk.Label(
            time_limit_frame, text='minutes'
        )
        time_min_label.grid(row=0, column=3)

        container.columnconfigure(1, weight=1)
        time_limit_frame.columnconfigure(1, weight=1)
        
        # ---

        limit_toggle_frame = ttk.Frame(container)
        limit_toggle_frame.grid(
            row=2, column=1, pady=(0,8), sticky=tk.EW
        )

        limit_toggle = tk.StringVar(value='off')
        self.__limit_toggle_var = limit_toggle

        limit_radio_on = ttk.Radiobutton(
            limit_toggle_frame, variable=limit_toggle,
            value='on', text='Enabled', command=self.__limit_toggled
        )

        limit_radio_on.grid(row=0, column=0, padx=(0,8), sticky=tk.W)

        limit_radio_off = ttk.Radiobutton(
            limit_toggle_frame, variable=limit_toggle,
            value='off', text='Disabled', command=self.__limit_toggled
        )

        limit_radio_off.grid(row=0, column=1)
        self.__limit_toggled()

        # ---

        ok_button = ttk.Button(
            container, text='Ok', command=self.__ok_click
        )

        ok_button.grid(row=3, column=1, sticky=tk.E, pady=(24,0))
        self.__ok_button_listener = None
        self.__app_identity = None
        
    def __limit_toggled(self):
        if self.__limit_toggle_var.get() == 'on':
            self.__time_min.state(('!disabled',))
            self.__time_hrs.state(('!disabled',))
        else:
            self.__time_min.state(('disabled',))
            self.__time_hrs.state(('disabled',))

    def __ok_click(self):
        if self.__ok_button_listener != None:
            name = self.__name_text.get().strip()
            limit = None
            
            if self.__limit_toggle_var.get() == 'on':
                try: hrs = int(self.__time_hrs.get().strip())
                except: hrs = 0
                
                try: mins = int(self.__time_min.get().strip())
                except: mins = 0

                if hrs > -1 and mins > -1 and (hrs != 0 or mins != 0):
                    limit = (hrs * 60 + mins) * 60

            self.__ok_button_listener(name, limit, self.__app_identity)

        self.__window.destroy()

    def set_default_values(self, name, limit=None, identity=None):
        self.__app_identity = identity
        last = len(self.__name_text.get())

        if last > 0: self.__name_text.delete(0, last)

        self.__name_text.insert(0, name.strip())
        last = len(self.__time_hrs.get())
            
        if last > 0: self.__time_hrs.delete(0, last)
            
        last = len(self.__time_min.get())
            
        if last > 0: self.__time_min.delete(0, last)

        if limit == None:
            self.__limit_toggle_var.set('off')
            self.__limit_toggled()
            self.__time_hrs.insert(0, '0')
            self.__time_min.insert(0, '0')

        else:
            mins = int(limit) // 60
            hrs = int(mins // 60)
            mins =int(mins % 60)
            self.__limit_toggle_var.set('on')
            self.__limit_toggled()
            self.__time_hrs.insert(0, str(hrs))
            self.__time_min.insert(0, str(mins))

    def set_ok_listener(self, listener): self.__ok_button_listener = listener
