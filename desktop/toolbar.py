import tkinter as tk
from tkinter import ttk

from hidable_frame import HidableFrame

class Toolbar(HidableFrame):
    def __init__(self, *args, button_labels=None, button_icons=None, **kwargs):
        self.__button_labels = button_labels
        self.__button_icons = button_icons
        self.__buttons = {}
        HidableFrame.__init__(self, *args, **kwargs)
        
    def initialise(self, frame):
        if self.__button_labels == None: return

        frame.grid_configure(padx=(0,16))
        index=0
        self.__icons = []
        
        for text in self.__button_labels:
            image = None
            
            if self.__button_icons != None:
                name = self.__button_icons[index]
                path = 'icons/' + name + '.png'
                
                try:
                    image = tk.PhotoImage(file=path)
                    self.__icons.append(image) # Save reference, else GC'd
                except: pass


            button = ttk.Button(frame, text=text, image=image)
            button.grid(pady=(0,8))
            self.__buttons[text] = button
            index += 1

    def set_listener(self, button, listener):
        if button in self.__buttons:
            self.__buttons[button].configure(command=listener)
            return True

        return False
