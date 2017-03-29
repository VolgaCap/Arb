import ctypes
import xroad.lib as lib


class Timer(object):

    @staticmethod
    def __on_timer(ctx):
        self = ctypes.cast(ctx, ctypes.py_object).value
        self.__fn(self)

    def __init__(self, fn):
        self.__on_timer_fun = lib.on_timer_handler(Timer.__on_timer)
        self.__fn = fn
        cback = lib.TimerCallbackCTypes(ctypes.py_object(self), self.__on_timer_fun)
        self.__timer = lib.common().xroad_timer_create(cback)
        self.__started = False

    @property
    def started(self):
        return self.__started

    def start(self, start, periodic=0):
        lib.common().xroad_timer_start_repeat(self.__timer, start, periodic)
        self.__started = True

    def stop(self):
        lib.common().xroad_timer_stop(self.__timer)
        self.__started = False

    def __del__(self):
        if self.__timer:
            lib.common().xroad_timer_destroy(self.__timer)


class XroadError(Exception):
    pass

# vim:et:sts=4:sw=4
