import tkinter as tk
from tkinter import ttk

class Toolbar:
    def __init__(self, master, button_labels=None, button_icons=None):
        self.__buttons = {}
        
        if button_labels == None: return

        index=0
        self.__icons = []
        
        for text in button_labels:
            image = None
            
            if button_icons != None:
                name = button_icons[index]
                path = 'icons/' + name + '.png'
                
                try:
                    image = tk.PhotoImage(file=path)
                    self.__icons.append(image) # Save reference, else GC'd
                except: pass


            button = ttk.Button(master, text=text, image=image)
            button.grid(pady=(0,8))
            self.__buttons[text] = button
            index += 1
    
    def set_listener(self, button, listener):
        if button in self.__buttons:
            self.__buttons[button].configure(command=listener)
            return True

        return False
