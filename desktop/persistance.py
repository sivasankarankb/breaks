
# persistance.py - Saves and loads application data

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


class AppMonitorData:
    def __init__(self):
        self.__persistance_dir = PersistanceDir()
        
    def load(self):
        return self.__persistance_dir.load_dict('monitor', 'mondata')

    def save(self, data):
        return self.__persistance_dir.save_dict('monitor', 'mondata', data)
