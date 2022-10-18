from tkinter import ttk

import config
from hidable_frame import HidableFrame

class AboutBox(HidableFrame):
    def initialise(self, frame):
        iframe = ttk.Frame(frame)
        iframe.grid()

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        l1 = ttk.Label(iframe, text=config.app_name)
        l1.grid(pady=(0,8))
        
        l2 = ttk.Label(iframe, text='Version ' + config.app_version)
        l2.grid(pady=(0,8))

        l3 = ttk.Label(iframe, text='https://githhub.com/sivasankarankb/breaks')
        l3.grid(pady=(0,8))

        lcopy = ttk.Label(iframe, text='Copyright (C) 2020-2022 Sivasankaran K B')
        lcopy.grid(pady=(0,20))

        license_txt ='''\
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation.'''

        llicense = ttk.Label(iframe, text=license_txt)
        llicense.grid(pady=(0,20))

        l4 = ttk.Label(iframe, text='-- Contributors --')
        l4.grid(pady=(0,20))

        ll = ttk.Label(iframe, text='Rabeeba Ibrahim')
        ll.grid(pady=(0,8))

        ll = ttk.Label(iframe, text='Shasna Shemsudheen')
        ll.grid(pady=(0,8))

        ll = ttk.Label(iframe, text='Krishnapriya T R')
        ll.grid(pady=(0,16))

        ll = ttk.Label(iframe, text='Serin V Simpson')
        ll.grid(pady=(0,8))

        ll = ttk.Label(iframe, text='Sudharsanan K B')
        ll.grid(pady=(0,8))

        iframe.columnconfigure(0, weight=1)
