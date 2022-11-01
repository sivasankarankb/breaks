import tkinter as tk
from tkinter import ttk

class Toolbar:
    def __init__(self, master, button_labels, button_icons):
        self.__buttons = {}
        self.__icons = []
        
        for label, icon in zip(button_labels, button_icons):
            try:
                image = tk.PhotoImage(file='icons/' + icon + '.png')
                self.__icons.append(image) # Save reference, else GC'd
            
            except: image = None

            button = ttk.Button(master, text=label, image=image)
            button.grid(pady=(0,8))
            self.__buttons[label] = button
    
    def set_listener(self, button, listener):
        if button in self.__buttons:
            self.__buttons[button].configure(command=listener)
            return True

        return False
