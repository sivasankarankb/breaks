from tkinter import ttk

import config

class AboutBox:
    def __init__(self, master):
        frame = ttk.Frame(master)
        frame.grid()

        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        
        l1 = ttk.Label(frame, text=config.app_name)
        l1.grid(pady=(0,8))
        
        l2 = ttk.Label(frame, text='Version ' + config.app_version)
        l2.grid(pady=(0,8))

        l3 = ttk.Label(frame, text='https://githhub.com/sivasankarankb/breaks')
        l3.grid(pady=(0,8))

        lcopy = ttk.Label(frame, text='Copyright (C) 2020-2022 Sivasankaran K B')
        lcopy.grid(pady=(0,20))

        license_txt ='''\
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation.'''

        llicense = ttk.Label(frame, text=license_txt)
        llicense.grid(pady=(0,20))

        l4 = ttk.Label(frame, text='-- Contributors --')
        l4.grid(pady=(0,20))

        ll = ttk.Label(frame, text='Rabeeba Ibrahim')
        ll.grid(pady=(0,8))

        ll = ttk.Label(frame, text='Shasna Shemsudheen')
        ll.grid(pady=(0,8))

        ll = ttk.Label(frame, text='Krishnapriya T R')
        ll.grid(pady=(0,16))

        ll = ttk.Label(frame, text='Serin V Simpson')
        ll.grid(pady=(0,8))

        ll = ttk.Label(frame, text='Sudharsanan K B')
        ll.grid(pady=(0,8))

        frame.columnconfigure(0, weight=1)
