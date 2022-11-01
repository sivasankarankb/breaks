import config
import plyer

class Notifier:
    def notify(self, message):
        plyer.notification.notify(title=config.app_name, message=message)