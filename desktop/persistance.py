
# persistance.py - Saves and loads application data

import timers
import shelve

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
        if self.__ended or not self.__begun: return

        self.record_event('end')
        self.__end_timestamp = timers.timestamp()
        self.__ended = True

        try: storage = shelve.open('workdata.shelf')
        except: storage = None

        if storage != None:
            data = (
                self.__begin_timestamp, self.__events, self.__end_timestamp
            )

            if 'workday' in storage: storage['workday'].append(data)
            else: storage['workday'] = [data]

            storage.close()

        else: pass #TODO: Handle this elegantly (maybe).

    def load(self, index=None):
        try: storage = shelve.open('workdata.shelf', 'r')
        except: storage = None

        if storage != None and 'workday' in storage:

            if index != None and len(storage['workday']) > index:
                data = storage['workday'][index]

            elif index == None: data = storage['workday'][:]

            else: data = None

            storage.close()
            return data
