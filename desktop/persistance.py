
# persistance.py - Saves and loads application data

import timers
import shelve
import pathlib

class PersistanceDir:
    def __init__(self):
        self.__persistance_dir = None

    def __create_persistance_dir(self):
        dir = pathlib.Path("data")

        if dir.exists() and not dir.is_dir(): dir.unlink()

        if not dir.exists(): dir.mkdir()

        self.__presistance_dir = dir.resolve()

    def __path(self, file):
        if self.__persistance_dir == None: self.__create_persistance_dir()

        return str(self.__presistance_dir / file)

    def load_dict(self, file, key):
        try: storage = shelve.open(self.__path(file + '.shf'))
        
        except: return None

        if key in storage: data = storage[key]
            
        else: data = None

        storage.close()
        return data

    def save_dict(self, file, key, data):
        try: storage = shelve.open(self.__path(file + '.shf'))
        
        except: return False

        storage[key] = data
        storage.close()
        return True
            

class WorkData:
    def __init__(self):
        self.__lap_timer = timers.Lap()
        self.__events = []
        self.__begun = False
        self.__ended = False

        self.__persistance_dir = PersistanceDir()

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

        workdays = self.__persistance_dir.load_dict('workdata', 'workday')

        if workdays != None:
            workdays.append(data)

        else: workdays = [data]

        self.__persistance_dir.save_dict('workdata', 'workday', workdays)

    def load(self, index=None):

        workday = self.__persistance_dir.load_dict('workdata', 'workday')

        if workday != None:

            if index == None: data = workday

            elif len(workday) > index: data = workday[index]

            else: data = None

            return data

class AppMonitorData:
    def __init__(self):
        self.__persistance_dir = PersistanceDir()
        
    def load(self):
        return self.__persistance_dir.load_dict('monitor', 'mondata')

    def save(self, data):
        return self.__persistance_dir.save_dict('monitor', 'mondata', data)
