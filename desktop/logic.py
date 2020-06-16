
# logic.py - Core logic

import plyer

import timers
import config
import settings
import persistance

class Notifier:
    def notify(message):
        plyer.notification.notify(title=config.app_name, message=message)

class WorkTimer:
    def __init__(self, ui):
        self.__ui = ui
        self.__ui.set_time_text('Ready?')
        self.__ui.set_timer_set_button_text('Set')

        self.__ui.set_timer_set_button_listener(
          self.__timer_set_button_listener
        )

        self.__ui.set_timer_button_text('Let\'s begin!')
        self.__ui.set_timer_button_listener(self.__timer_button_listener)

        self.__timer_button_state = 'init'
        self.__work_data = persistance.WorkData()

    def __timer_button_listener(self):
        if self.__timer_button_state == 'init':
            self.__work_data.begin()
            self.__ui.set_timer_button_text('Take a break.')

            self.__countdown_timer = timers.Countdown(
                settings.work_period, self.__timer_done
            )

            self.__countdown_timer.set_progress_callback(self.__timer_update)
            self.__countdown_timer.start()
            self.__timer_button_state = 'break'

        elif self.__timer_button_state == 'begin':
            self.__work_data.record_event('start-work')
            self.__ui.set_timer_button_text('Take a break.')

            self.__countdown_timer = timers.Countdown(
                settings.work_period, self.__timer_done
            )

            self.__countdown_timer.set_progress_callback(self.__timer_update)
            self.__countdown_timer.start()
            self.__timer_button_state = 'break'

        elif self.__timer_button_state == 'break':
            self.__work_data.record_event('take-break')
            self.__ui.set_timer_button_text('Let\'s work!')

            if not self.__countdown_timer.completed():
                self.__countdown_timer.cancel()
                self.__ui.set_time_text('Done')

            self.__countdown_timer = None
            self.__timer_button_state = 'begin'

    def __timer_set_button_listener(self):
        dur = self.__ui.get_integer("Duration:")

        if dur != None and dur > 0: settings.work_period = dur * 60

    def __timer_done(self):
        self.__work_data.record_event('time-up')
        self.__ui.set_time_text('Done')
        Notifier.notify('Take a break.')

    def __timer_update(self, seconds):
        minutes = seconds // 60
        self.__ui.set_time_text( str(minutes) + ' minute(s) left')

    def cleanup(self): self.__work_data.end()
