import psutil

class Process:
    def __init__(self, pid, path, label, created):
        self.__pid = pid
        self.__path = path
        self.__label = label
        self.__created = created

    def get_pid(self): return self.__pid

    def get_path(self): return self.__path

    def get_label(self): return self.__label

    def get_created(self): return self.__created


class ProcessInfo:
    def get_process_ids(self): return psutil.pids()

    def get_info_of(self, pid):
        try: p = psutil.Process(pid).as_dict(
            ['pid', 'exe', 'name', 'create_time']
        )

        except: pass
        
        else: return Process(
            pid=p['pid'], path=p['exe'], label=p['name'],
            created=p['create_time']
        )
