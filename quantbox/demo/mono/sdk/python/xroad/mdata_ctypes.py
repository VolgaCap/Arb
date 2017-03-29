##
# @file mdata.py
# @author Danil Krivopustov, krivopustovda@gmail.com

import ctypes
from enum import IntEnum


##
# describes type of data which interests client
class SubscriptionType(IntEnum):
    Book = 1,
    Trade = 2,
    Quote = 4,
    Common = 8,
    Snapshot = 16,  # receive snapshot
    Updates = 32    # receive regular updates


class BookLevelCTypes(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("price", ctypes.c_double),
                ("qty", ctypes.c_long)]


class SubscribeCTypes(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("instr_id", ctypes.c_ulong),
                ("mask", ctypes.c_int)]


class ResolveCTypes(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("alias", ctypes.c_char * 21)]


class Book_20CTypes(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("instr_id", ctypes.c_ulong),
                ("asks", BookLevelCTypes * 20),
                ("bids", BookLevelCTypes * 20),
                ("exch_ts", ctypes.c_ulong),
                ("ts", ctypes.c_ulong)]
#               ("rcv_ts", ctypes.c_ulong)]


class QuoteCTypes(ctypes.Structure):
    _pack_ = 4
    _fields_ = [('instr_id', ctypes.c_ulong),
                ("ask", BookLevelCTypes),
                ("bid", BookLevelCTypes),
                ("exch_ts", ctypes.c_ulong),
                ("ts",  ctypes.c_ulong),
                ("flag",  ctypes.c_uint)]
#               ("rcv_ts", ctypes.c_ulong)]


class SymbolCTypes(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("instr_id", ctypes.c_ulong),
                ("alias", ctypes.c_char * 21)]


class TradeCTypes(ctypes.Structure):
    _pack_ = 4
    _fields_ = [('instr_id', ctypes.c_ulong),
                ('price', ctypes.c_double),
                ('qty', ctypes.c_long),
                ("side", ctypes.c_int),
                ("exch_ts", ctypes.c_ulong),
                ("ts", ctypes.c_ulong)]
#               ("rcv_ts", ctypes.c_ulong  )]


class SubscribeResultCTypes(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("instr_id", ctypes.c_ulong),
                ("error_num", ctypes.c_int),
                ("mask", ctypes.c_int)]


class FeedStateCTypes(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("mask", ctypes.c_int),
                ("state", ctypes.c_int),
                ("instr_id", ctypes.c_ulong)]


class CommonInfoCTypes(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("instr_id", ctypes.c_ulong),
                ("flag", ctypes.c_int),
                ("oi", ctypes.c_double),
                ("min", ctypes.c_double),
                ("max", ctypes.c_double),
                ("open", ctypes.c_double),
                ("close", ctypes.c_double),
                ("high", ctypes.c_double),
                ("low", ctypes.c_double),
                ("last", ctypes.c_double),
                ("volume", ctypes.c_double),
                ("ts", ctypes.c_ulong),
                ("exch_ts", ctypes.c_ulong)]


on_mdata_resolve_type = ctypes.CFUNCTYPE(None, ctypes.POINTER(ResolveCTypes), ctypes.c_void_p)
on_mdata_subscribe_type = ctypes.CFUNCTYPE(None, ctypes.POINTER(SubscribeCTypes), ctypes.c_void_p)
on_mdata_symbol_type = ctypes.CFUNCTYPE(None, ctypes.POINTER(SymbolCTypes), ctypes.c_void_p)
on_mdata_subscribe_result_type = ctypes.CFUNCTYPE(None, ctypes.POINTER(SubscribeResultCTypes), ctypes.c_void_p)
on_mdata_feed_state_type = ctypes.CFUNCTYPE(None, ctypes.POINTER(FeedStateCTypes), ctypes.c_void_p)
on_mdata_mdata_type = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
on_mdata_connected_type = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
on_mdata_disconnected_type = ctypes.CFUNCTYPE(None, ctypes.c_void_p)

class ServerCallbackCTypes(ctypes.Structure):
    _fields_ = [("ctx", ctypes.py_object),
                ("on_resolve", on_mdata_resolve_type),
                ("on_subscribe", on_mdata_subscribe_type),
                ("on_connected", on_mdata_connected_type),
                ("on_disconnected", on_mdata_disconnected_type)]

class ClientCallbackCTypes(ctypes.Structure):
    _fields_ = [("ctx", ctypes.py_object),
                ("on_symbol", on_mdata_symbol_type),
                ("on_subscribe_result", on_mdata_subscribe_result_type),
                ("on_feed_state", on_mdata_feed_state_type),
                ("on_connected", on_mdata_connected_type),
                ("on_disconnected", on_mdata_disconnected_type)]


class ChannelCallbackCTypes(ctypes.Structure):
    _fields_ = [('ctx', ctypes.py_object),
                ('on_mdata', on_mdata_mdata_type)]

# vim:et:sts=4:sw=4
