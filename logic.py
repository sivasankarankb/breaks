
# logic.py - Core logic

import plyer

from timers import CountdownTimer
import config
import settings

class Notifier:
    def notify(message):
        plyer.notification.notify(title=config.app_name, message=message)

class AppLogic:
    def __init__(self, ui):
        self.__ui = ui
        self.__ui.set_time_text('Ready')
        self.__ui.set_timer_button_text('Let\'s work!')
        self.__ui.set_timer_button_listener(self.__timer_button_listener)

        self.__timer_button_state = False

    def __timer_button_listener(self):
        self.__timer_button_state = not self.__timer_button_state
        
        if self.__timer_button_state:
            self.__ui.set_timer_button_text('Take a break.')
            
            self.__countdown_timer = CountdownTimer(settings.work_period, self.__timer_done)
            self.__countdown_timer.set_progress_callback(self.__timer_update)
            self.__countdown_timer.start()

        else:
            self.__ui.set_timer_button_text('Let\'s work!')

            if not self.__countdown_timer.completed():
                self.__countdown_timer.cancel()
                self.__ui.set_time_text('Done')

            self.__countdown_timer = None

    def __timer_done(self):
        self.__ui.set_time_text('Done')
        Notifier.notify('Take a break.')

    def __timer_update(self, minutes):
        self.__ui.set_time_text( str(minutes) + ' minute(s) left')
