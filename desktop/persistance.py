
# persistance.py - Saves and loads application data

import timers
import shelve
import pathlib

class WorkData:
    def __create_persistance_dir(self):
        dir = pathlib.Path("data")

        if dir.exists() and not dir.is_dir(): dir.unlink()
        if not dir.exists(): dir.mkdir()

        self.__presistance_dir = dir.resolve()

    def __persistance_path(self, file):
        return str(self.__presistance_dir / file)

    def __init__(self):
        self.__lap_timer = timers.Lap()
        self.__events = []
        self.__begun = False
        self.__ended = False

        self.__create_persistance_dir()

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

        try: storage = shelve.open(self.__persistance_path('workdata.shelf'))
        except: storage = None

        if storage != None:
            data = (
                self.__begin_timestamp, self.__events, self.__end_timestamp
            )

            if 'workday' in storage:
                workdays = storage['workday']
                workdays.append(data)
                
                # This is how shelve works, assign to save to file.
                storage['workday'] = workdays

            else: storage['workday'] = [data]

            storage.close()

        else: pass #TODO: Handle this elegantly (maybe).

    def load(self, index=None):

        try: storage = shelve.open(
            self.__persistance_path('workdata.shelf'), 'r'
        )

        except: storage = None

        if storage != None and 'workday' in storage:

            if index == None: data = storage['workday'][:]

            elif len(storage['workday']) > index:
                data = storage['workday'][index]

            else: data = None

            storage.close()
            return data
