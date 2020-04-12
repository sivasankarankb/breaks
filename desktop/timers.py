
# timers.py - Custom timers

import threading
import time
import math

class Indeterminate:
    def __init__(self, progress, granularity=60.0):
        self.__progress_callback = progress
        self.__progress_granularity = granularity
        self.reset()

    def start(self):
        if self.__started: return

        self.__started = True
        self.__time_started = time.monotonic()
        self.__update()

    def __update(self):
        if not self.__started:
            self.__timer_task = None
            return

        error = self.time_passed_accurate() % self.__progress_granularity
        duration = math.ceil(self.__progress_granularity - error)
        self.__timer_task = threading.Timer(duration, self.__update)
        self.__timer_task.start()

        if self.__progress_callback != None:
            self.__progress_callback(self.time_passed())

    def time_passed(self):
        interval = self.time_passed_accurate()
        error = interval % self.__progress_granularity
        return int(interval - error)

    def time_passed_accurate(self):
        if self.__started:
            delta = time.monotonic() - self.__time_started
            return self.__time_previous + delta

        else: return self.__time_previous

    def stop(self):
        if not self.__started: return

        self.__started = False
        time_stopped = time.monotonic()

        if self.__timer_task != None:
            self.__timer_task.cancel()
            self.__timer_task = None

        self.__time_previous += time_stopped - self.__time_started

    def reset(self):
        self.__started = False
        self.__time_started = 0
        self.__time_previous = 0
        self.__timer_task = None

class Countdown:
    def __init__(self, seconds, done, granularity=60.0):
        self.__duration = seconds
        self.__done_callback = done
        self.__started = False
        self.__completed = False

        self.__timer = Indeterminate(
            progress=self.__update, granularity=granularity
        )

    def start(self):
        if not self.__started:
            self.__started = True
            self.__timer.start()

    def __update(self, time_passed):
        if not self.__started: return

        remaining = self.__duration - time_passed
        if remaining < 0: remaining = 0

        if self.__progress_callback != None:
            self.__progress_callback(remaining)

        if remaining == 0:
            self.__completed = True
            self.__started = False
            self.__timer.stop()

            if self.__done_callback != None: self.__done_callback()

    def cancel(self):
        if self.__started:
            self.__timer.stop()
            self.__timer = None
            self.__started = False

    def completed(self):
        return self.__completed

    def set_progress_callback(self, progress=None):
        self.__progress_callback = progress

class Lap:
    def __init__(self): self.__lapmoment = None

    def start(self): self.__lapmoment = time.monotonic()

    def lap(self):
        last = self.__lapmoment

        if last == None: return 0

        self.__lapmoment = time.monotonic()
        return self.__lapmoment - last
