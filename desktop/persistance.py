
# persistance.py - Saves and loads application data

import timers

class WorkData:
    def __init__(self):
        self.__lap_timer = timers.Lap()
        self.__events = []
        self.__begun = False
        self.__ended = False

    def begin(self):
        if self.__begun: return

        self.__lap_timer.start()
        self.__begin_timestamp = timers.timestamp()
        self.__begun = True

    def record_event(self, label, data=None):
        self.__events.append((label, data, self.__lap_timer.lap()))

    def end(self):
        if self.__ended: return

        self.record_event('end')
        self.__end_timestamp = timers.timestamp()
        self.__ended = True

    def save(self): pass

    def load(self, start_time, stop_time): pass

    def load_single(self, start_time): pass
