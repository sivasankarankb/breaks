
# timers.py - Custom timers

import threading

class CountdownTimer:
    def __init__(self, minutes, done):
        self.__minutes = minutes
        self.__done_callback = done
        self.__started = False
        self.__completed = False

    def start(self):
        if not self.__started:
            self.__started = True
            self.__update()

    def __update(self):
        if self.__started:
            if self.__minutes > 0:
                self.__timer_task = threading.Timer(60.0, self.__update)
                self.__timer_task.start()
                
                if self.__progress_callback != None:
                    self.__progress_callback(self.__minutes)

                self.__minutes = self.__minutes - 1

            else:
                self.__started = False
                self.__completed = True
                
                if self.__done_callback != None:
                    self.__done_callback()

    def cancel(self):
        if self.__started:
            if self.__timer_task != None:
                self.__timer_task.cancel()

            self.__timer_task = None
            self.__started = False

    def completed(self):
        return self.__completed

    def set_progress_callback(self, progress=None):
        self.__progress_callback = progress
