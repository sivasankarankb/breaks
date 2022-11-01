import pathlib
import json
import config

class AppMonitorData:
    def load(self):
        try: d = open(str(pathlib.Path(config.data_dir) / 'app_monitor.json'))
        except: return None

        try: data = json.load(d)
        except: return None
        
        d.close()
        return data

    def save(self, data):
        try: d = open(
            str(pathlib.Path(config.data_dir) / 'app_monitor.json'), 'wt'
        )

        except: return False

        try: json.dump(data, d)
        except: return False
        
        d.close()
        return True