##
# @file lib.py
# @author Dmitry S. Melnikov, dmitryme@gmail.com

import ctypes
import os
from xroad.xtypes import Str, Path
from xroad.mdata_ctypes import ServerCallbackCTypes,ClientCallbackCTypes, ChannelCallbackCTypes
from xroad.order_ctypes import OrderCallbackCTypes


class EpollEventDataCTypes(ctypes.Structure):
    _fields_ = [('ptr', ctypes.c_void_p),
                ('fd', ctypes.c_int32),
                ('u32', ctypes.c_uint32),
                ('u64', ctypes.c_uint64)]


class EpollEventCTypes(ctypes.Structure):
    _fields_ = [('events', ctypes.c_uint32),
                ('data', EpollEventDataCTypes)]

on_timer_handler = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
on_signal_handler = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)
on_epoll_event_handler = ctypes.CFUNCTYPE(None, ctypes.POINTER(EpollEventCTypes))


class TimerCallbackCTypes(ctypes.Structure):
    _fields_ = [('ctx', ctypes.py_object),
                ('on_timer', on_timer_handler)]


class SignalCallbackCTypes(ctypes.Structure):
    _fields_ = [('ctx', ctypes.py_object),
                ('on_signal', on_signal_handler)]


__libnode = None
__libcommon = None
__liblogger = None
__libidb = None
__libmdata_engine = None
__liborder = None
__libui = None


def node():
    if __libnode is None:
        raise RuntimeError("do lib.init() first")
    return __libnode


def common():
    if __libcommon is None:
        raise RuntimeError("do lib.init() first")
    return __libcommon


def logger():
    if __liblogger is None:
        raise RuntimeError("do lib.init() first")
    return __liblogger


def idb():
    if __libidb is None:
        raise RuntimeError("do lib.init() first")
    return __libidb


def mdata_engine():
    if __libmdata_engine is None:
        raise RuntimeError("do lib.init() first")
    return __libmdata_engine


def order():
    if __liborder is None:
        raise RuntimeError("do lib.init() first")
    return __liborder


def ui():
    if __libui is None:
        raise RuntimeError("do lib.init() first")
    return __libui


def init():
    global __libnode
    __libnode = ctypes.CDLL(os.path.join(os.environ["XROAD_ROOT_DIR"], "sdk/lib/libnode.so"), ctypes.RTLD_GLOBAL)
    __libnode.xroad_registry_get.restype = ctypes.c_void_p
    __libnode.xroad_registry_get_by_name.restype = ctypes.c_void_p
    __libnode.xroad_registry_get_by_name.argtypes = [Str]
    __libnode.xroad_registry_get_by_id.restype = ctypes.c_void_p
    __libnode.xroad_registry_get_by_id.argtypes = [ctypes.c_ushort]
    __libnode.xroad_registry_get_by_pid.restype = ctypes.c_void_p
    __libnode.xroad_registry_get_by_pid.argtypes = [ctypes.c_int]
    __libnode.xroad_node_get_data.restype = ctypes.c_void_p
    __libnode.xroad_node_get_home_dir.restype = ctypes.POINTER(Path)
    __libnode.xroad_node_get_cfg.restype = ctypes.c_void_p
    __libnode.xroad_node_create_cursor.argtypes = [ctypes.c_int]
    __libnode.xroad_node_create_cursor.restype = ctypes.c_void_p
    __libnode.xroad_node_cursor_get_first.restype = ctypes.c_void_p
    __libnode.xroad_node_cursor_get_first.argtypes = [ctypes.c_void_p]
    __libnode.xroad_node_cursor_get_next.restype = ctypes.c_void_p
    __libnode.xroad_node_cursor_get_next.argtypes = [ctypes.c_void_p]
    __libnode.xroad_node_cursor_get_last.restype = ctypes.c_void_p
    __libnode.xroad_node_cursor_get_last.argtypes = [ctypes.c_void_p]
    __libnode.xroad_node_cursor_get_prev.restype = ctypes.c_void_p
    __libnode.xroad_node_cursor_get_prev.argtypes = [ctypes.c_void_p]
    __libnode.xroad_node_cursor_offset.restype = ctypes.c_void_p
    __libnode.xroad_node_cursor_offset.argtypes = [ctypes.c_void_p, ctypes.c_long]
    __libnode.xroad_node_get_object.argtypes = [ctypes.c_int, ctypes.c_long]
    __libnode.xroad_node_get_object.restype = ctypes.c_void_p
    __libnode.xroad_object_get_type.argtypes = [ctypes.c_void_p]
    __libnode.xroad_object_get_type.restype = ctypes.c_int
    __libnode.xroad_node_shrink_cache.argtypes = [ctypes.c_int, ctypes.c_long]
    __libnode.xroad_object_get_type.argtypes = [ctypes.c_void_p]
    __libnode.xroad_object_get_type.restype = ctypes.c_int
    __libnode.xroad_node_create_object.argtypes = [ctypes.c_int]
    __libnode.xroad_node_create_object.restype = ctypes.c_void_p
    __libnode.xroad_node_get_object_count.argtypes = [ctypes.c_int]
    __libnode.xroad_node_get_object_count.restype = ctypes.c_int64
    __libnode.xroad_node_get_epoll_fd.restype = ctypes.c_int
    __libnode.xroad_node_add_epoll.argtypes = [ctypes.c_int32, on_epoll_event_handler]
    __libnode.xroad_node_add_epoll.restype = ctypes.c_int
    __libnode.xroad_node_mod_epoll.argtypes = [ctypes.c_int32, on_epoll_event_handler]
    __libnode.xroad_node_mod_epoll.restype = ctypes.c_int
    __libnode.xroad_node_del_epoll.argtypes = [ctypes.c_int32, on_epoll_event_handler]
    __libnode.xroad_node_del_epoll.restype = ctypes.c_int
    __libnode.xroad_node_receive.argtypes = [ctypes.c_int64]
    __libnode.xroad_node_receive.restype = ctypes.c_int32
    __libnode.xroad_node_get_version.restype = ctypes.c_void_p
    __libnode.xroad_node_is_initialized.restype = ctypes.c_bool

    global __libcommon
    __libcommon = ctypes.CDLL(os.path.join(os.environ["XROAD_ROOT_DIR"], "sdk/lib/libcommon.so"), ctypes.RTLD_GLOBAL)
    __libcommon.xroad_xml_get_root.restype = ctypes.c_void_p
    __libcommon.xroad_xml_get_root.argtypes = [ctypes.c_void_p]
    __libcommon.xroad_xml_get_tag.restype = ctypes.c_void_p
    __libcommon.xroad_xml_get_tag.argtypes = [ctypes.c_void_p, Str]
    __libcommon.xroad_xml_has_tag.restype = ctypes.c_int32
    __libcommon.xroad_xml_has_tag.argtypes = [ctypes.c_void_p, Str]
    __libcommon.xroad_xml_has_attr.restype = ctypes.c_int32
    __libcommon.xroad_xml_has_attr.argtypes = [ctypes.c_void_p, Str]
    __libcommon.xroad_xml_get_name.argtypes = [ctypes.c_void_p]
    __libcommon.xroad_xml_get_name.restype = Str
    __libcommon.xroad_xml_get_text.argtypes = [ctypes.c_void_p]
    __libcommon.xroad_xml_get_text.restype = Str
    __libcommon.xroad_xml_get_attr_s.restype = Str
    __libcommon.xroad_xml_get_attr_s.argtypes = [ctypes.c_void_p, Str]
    __libcommon.xroad_xml_get_attr_i.restype = ctypes.c_int
    __libcommon.xroad_xml_get_attr_i.argtypes = [ctypes.c_void_p, Str]
    __libcommon.xroad_xml_get_attr_d.restype = ctypes.c_double
    __libcommon.xroad_xml_get_attr_d.argtypes = [ctypes.c_void_p, Str]
    __libcommon.xroad_timer_create.restype = ctypes.c_void_p
    __libcommon.xroad_timer_create.argtypes = [TimerCallbackCTypes]
    __libcommon.xroad_timer_start_repeat.restype = ctypes.c_void_p
    __libcommon.xroad_timer_start_repeat.argtypes = [ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint64]
    __libcommon.xroad_signal_create.restype = ctypes.c_void_p
    __libcommon.xroad_signal_create.argtypes = [SignalCallbackCTypes]
    __libcommon.xroad_xml_get_variable.restype = Str
    __libcommon.xroad_xml_get_variable.argtypes = [ctypes.c_void_p, Str]

    __libcommon.xroad_xml_get_first.restype = ctypes.c_void_p
    __libcommon.xroad_xml_get_first.argtypes = [ctypes.c_void_p]

    __libcommon.xroad_xml_get_next.restype = ctypes.c_void_p
    __libcommon.xroad_xml_get_next.argtypes = [ctypes.c_void_p, Str]

    __libcommon.xroad_signal_catch.restype = ctypes.c_int
    __libcommon.xroad_signal_catch.argtypes = [ctypes.c_void_p, ctypes.c_int]
    __libcommon.xroad_signal_destroy.argtypes = [ctypes.c_void_p]
    __libcommon.xroad_signal_free.argtypes = [ctypes.c_void_p, ctypes.c_int]

    global __liblogger
    __liblogger = ctypes.CDLL(os.path.join(os.environ['XROAD_ROOT_DIR'], 'sdk/lib/liblogger.so'), ctypes.RTLD_GLOBAL)
    __liblogger.xroad_logx.argtypes = [ctypes.c_void_p, ctypes.c_int32, Str, ctypes.c_char_p]
    __liblogger.xroad_vlogx.argtypes = [ctypes.c_void_p, ctypes.c_int32, Str, ctypes.c_char_p]
    __liblogger.xroad_logger_get_level.argtypes = [ctypes.c_void_p]
    __liblogger.xroad_logger_get_level.restype = ctypes.c_int32
    __liblogger.xroad_logger_get.argtypes = [Str]
    __liblogger.xroad_logger_get.restype = ctypes.c_void_p

    global __libidb
    __libidb = ctypes.CDLL(os.path.join(os.environ['XROAD_ROOT_DIR'], 'sdk/lib/libinstrdb.so'), ctypes.RTLD_GLOBAL)
    __libidb.instrdb_get_by_id.restype = ctypes.c_void_p
    __libidb.instrdb_get_by_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
    __libidb.instrdb_get_by_alias.restype = ctypes.c_void_p
    __libidb.instrdb_get_by_alias.argtypes = [ctypes.c_void_p, Str]
    __libidb.instrdb_get_by_name.restype = ctypes.c_void_p
    __libidb.instrdb_get_by_name.argtypes = [ctypes.c_void_p, Str, Str]
    __libidb.instrdb_get_by_name.restype = ctypes.c_void_p
    __libidb.instrdb_add.argtypes = [ctypes.c_void_p, Str, Str, Str, Str]
    __libidb.instrdb_add.restype = ctypes.c_void_p

    global __libmdata_engine
    __libmdata_engine = ctypes.CDLL(os.path.join(os.environ['XROAD_ROOT_DIR'], 'sdk/lib/libmdata.so'), ctypes.RTLD_GLOBAL)
    __libmdata_engine.mdata_engine_client_create.restype = ctypes.c_void_p
    __libmdata_engine.mdata_engine_client_create.argtypes = [ctypes.c_void_p, ClientCallbackCTypes]
    __libmdata_engine.mdata_engine_create.restype = ctypes.c_void_p
    __libmdata_engine.mdata_engine_create.argtypes = [ctypes.c_void_p, ServerCallbackCTypes, ClientCallbackCTypes]
    __libmdata_engine.mdata_engine_start.restype = ctypes.c_int
    __libmdata_engine.mdata_engine_start.argtypes = [ctypes.c_void_p]
    __libmdata_engine.mdata_engine_stop.argtypes = [ctypes.c_void_p]
    __libmdata_engine.mdata_engine_destroy.argtypes = [ctypes.c_void_p]
    __libmdata_engine.mdata_engine_subscribe.restype = ctypes.c_int
    __libmdata_engine.mdata_engine_subscribe.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ChannelCallbackCTypes]
    __libmdata_engine.mdata_engine_send.restype = ctypes.c_int
    __libmdata_engine.mdata_engine_send.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]

    global __liborder
    __liborder = ctypes.CDLL(os.path.join(os.environ['XROAD_ROOT_DIR'], 'sdk/lib/liborder.so'), ctypes.RTLD_GLOBAL)
    __liborder.order_create.restype = ctypes.c_void_p
    __liborder.order_create.argtypes = [Str, OrderCallbackCTypes, ctypes.c_void_p, Str, Str,
                                        ctypes.c_int, ctypes.c_long, ctypes.c_double, Str, ctypes.py_object,
                                        ctypes.POINTER(Str)]
    __liborder.order_destroy.argtypes = [ctypes.c_void_p]
    __liborder.order_send.restype = ctypes.c_int
    __liborder.order_send.argtypes = [ctypes.c_void_p]
    __liborder.order_cancel.restype = ctypes.c_int
    __liborder.order_cancel.argtypes = [ctypes.c_void_p]
    __liborder.order_replace.restype = ctypes.c_int
    __liborder.order_replace.argtypes = [ctypes.c_void_p, ctypes.c_long, ctypes.c_double, ctypes.c_int]
    __liborder.order_reset.argtypes = [ctypes.c_void_p]
    __liborder.order_on_node_object.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
    __liborder.order_get_name.restype = Str
    __liborder.order_get_name.argtypes = [ctypes.c_void_p]
    __liborder.order_get_instr.restype = ctypes.c_void_p
    __liborder.order_get_instr.argtypes = [ctypes.c_void_p]
    __liborder.order_get_side.restype = ctypes.c_int
    __liborder.order_get_side.argtypes = [ctypes.c_void_p]
    __liborder.order_get_qty.restype = ctypes.c_long
    __liborder.order_get_qty.argtypes = [ctypes.c_void_p]
    __liborder.order_get_price.restype = ctypes.c_double
    __liborder.order_get_price.argtypes = [ctypes.c_void_p]
    __liborder.order_get_ctx.restype = ctypes.c_void_p
    __liborder.order_get_ctx.argtypes = [ctypes.c_void_p]
    __liborder.order_get_state.restype = ctypes.c_int
    __liborder.order_get_state.argtypes = [ctypes.c_void_p]
    __liborder.order_get_total_qty.restype = ctypes.c_ulong
    __liborder.order_get_total_qty.argtypes = [ctypes.c_void_p]
    __liborder.order_get_avg_price.restype = ctypes.c_double
    __liborder.order_print.argtypes = [ctypes.c_void_p]
    __liborder.order_print.restype = Str
    __liborder.order_get_avg_price.argtypes = [ctypes.c_void_p]
    __liborder.order_get_xorder.argtypes = [ctypes.c_void_p]
    __liborder.order_get_xorder.restype = ctypes.c_void_p
    __liborder.order_set_opt.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_void_p]
    __liborder.order_set_opt.restype = ctypes.c_int

    global __libui
    __libui = ctypes.CDLL(os.path.join(os.environ['XROAD_ROOT_DIR'], 'sdk/lib/libui.so'), ctypes.RTLD_GLOBAL)
    __libui.ui_create.restype = ctypes.c_void_p
    __libui.ui_create.argtypes = [ctypes.c_void_p]
    __libui.ui_destroy.argtypes = [ctypes.c_void_p]
    __libui.ui_get_field.restype = ctypes.c_void_p
    __libui.ui_get_field.argtypes = [ctypes.c_void_p, ctypes.c_ushort, Str]
    __libui.ui_get_int32.restype = ctypes.c_long
    __libui.ui_get_int32.argtypes = [ctypes.c_void_p, ctypes.c_ushort, Str]
    __libui.ui_get_int64.restype = ctypes.c_long
    __libui.ui_get_int64.argtypes = [ctypes.c_void_p, ctypes.c_ushort, Str]
    __libui.ui_get_double.restype = ctypes.c_double
    __libui.ui_get_double.argtypes = [ctypes.c_void_p, ctypes.c_ushort, Str]
    __libui.ui_get_str.restype = Str
    __libui.ui_get_str.argtypes = [ctypes.c_void_p, ctypes.c_ushort, Str]

# vim:et:sts=4:sw=4
