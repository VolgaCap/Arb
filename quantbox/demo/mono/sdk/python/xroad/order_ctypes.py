##
# @file order_ctypes.py
# @author Dmitry S. Melnikov, dmitryme@gmail.com

import ctypes
from xroad.xtypes import Str


on_activate = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
on_before_send = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
on_trade = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_long, ctypes.c_double)
on_canceled = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
on_unexpected_canceled = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
on_expired = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
on_destroyed = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
on_replaced = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
on_rejected = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, Str)
on_cancel_rejected = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, Str)
on_replace_rejected = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, Str)


class OrderCallbackCTypes(ctypes.Structure):
    _fields_ = [("on_activate", on_activate),
                ("on_before_send", on_before_send),
                ("on_trade", on_trade),
                ("on_canceled", on_canceled),
                ("on_unexpected_canceled", on_unexpected_canceled),
                ("on_expired", on_expired),
                ("on_destroyed", on_destroyed),
                ("on_replaced", on_replaced),
                ("on_rejected", on_rejected),
                ("on_cancel_rejected", on_cancel_rejected),
                ("on_on_replace_rejected",  on_replace_rejected)]
# vim:et:sts=4:sw=4
