import tkinter as tk
import tkinter.simpledialog as tkdlg
from tkinter import ttk

import timers
import settings

from notifier import Notifier
from hidable_frame import HidableFrame

class WorkTimer:
    def __init__(self, ui):
        self.__ui = ui
        self.__ui.set_time_text('Ready?')
        self.__ui.set_timer_set_button_text('Set')

        self.__ui.set_timer_set_button_listener(
          self.__timer_set_button_listener
        )

        self.__ui.set_timer_button_text('Let\'s begin!')
        self.__ui.set_timer_button_listener(self.__timer_button_listener)

        self.__timer_button_state = 'init'

    def __timer_button_listener(self):
        if self.__timer_button_state == 'init':
            self.__ui.set_timer_button_text('Take a break.')

            self.__countdown_timer = timers.Countdown(
                settings.work_period, self.__timer_done
            )

            self.__countdown_timer.set_progress_callback(self.__timer_update)
            self.__countdown_timer.start()
            self.__timer_button_state = 'break'

        elif self.__timer_button_state == 'begin':
            self.__ui.set_timer_button_text('Take a break.')

            self.__countdown_timer = timers.Countdown(
                settings.work_period, self.__timer_done
            )

            self.__countdown_timer.set_progress_callback(self.__timer_update)
            self.__countdown_timer.start()
            self.__timer_button_state = 'break'

        elif self.__timer_button_state == 'break':
            self.__ui.set_timer_button_text('Let\'s work!')

            if not self.__countdown_timer.completed():
                self.__countdown_timer.cancel()
                self.__ui.set_time_text('Done')

            self.__countdown_timer = None
            self.__timer_button_state = 'begin'

    def __timer_set_button_listener(self):
        dur = self.__ui.get_integer("Timer interval in minutes:", int(settings.work_period//60))

        if dur != None and dur > 0: settings.work_period = dur * 60

    def __timer_done(self):
        self.__ui.set_time_text('Done')
        Notifier.notify('Take a break.')

    def __timer_update(self, seconds):
        minutes = seconds // 60
        self.__ui.set_time_text( str(minutes) + ' minute(s) left')

    def cleanup(self): pass


class WorkTimerUI(HidableFrame):
    def initialise(self, frame): self.__create_widgets(frame)

    def __create_widgets(self, frame):
        iframe = ttk.Frame(frame, padding=8, borderwidth=1, relief='solid')
        iframe.grid(sticky=tk.NSEW)

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        frame = iframe

        self.__timer_time = ttk.Label(frame)
        self.__timer_time.grid(row=0, column=0)

        self.__timer_set_button = ttk.Button(
            frame, command=self.__click_timer_set_button
        )

        self.__timer_set_button.grid(row=0, column=1, padx=(0,8))
        self.__timer_set_button_listener = None

        self.__timer_button = ttk.Button(
            frame, command=self.__click_timer_button
        )
        self.__timer_button.grid(row=0, column=2)
        self.__timer_button_listener = None

        frame.columnconfigure(0, weight = 1)

    def __click_timer_button(self):
        if self.__timer_button_listener != None: self.__timer_button_listener()

    def __click_timer_set_button(self):
        if self.__timer_set_button_listener != None:
            self.__timer_set_button_listener()

    def set_time_text(self, txt): self.__timer_time.config(text = txt)

    def set_timer_button_text(self, txt): self.__timer_button.config(text = txt)

    def set_timer_button_listener(self, listener = None):
        self.__timer_button_listener = listener

    def set_timer_set_button_text(self, txt):
        self.__timer_set_button.config(text = txt)

    def set_timer_set_button_listener(self, listener = None):
        self.__timer_set_button_listener = listener

    def get_integer(self, message, default='0', title=''):
        value = tkdlg.askstring(title, message, initialvalue=default)

        try: return int(value)
        except: return None
