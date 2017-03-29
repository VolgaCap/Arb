import ctypes
import re
import binascii
from enum import IntEnum
from xroad import xtypes, lib
import logging
from xroad.common import XroadError


class ObjectType(IntEnum):
    start = 1
    stop = 2
    reconfig = 3
    activate = 4
    deactivate = 5
    date_changed = 6
    reset = 7
    alarm = 8
    exited = 9
    event = 10
    state = 11
    fix_session = 15
    order = 16
    pos = 17
    order_stat = 18
    iceberg = 19
    twap = 20
    pov = 21
    vwap = 22
    instr = 23
    tick_info = 24
    timesheet = 25
    mdstat = 102
    order_sql = 26
    cancel_sql = 27
    replace_sql = 28
    order_rabbit = 29
    rake = 30
    stealth = 31
    spread = 32
    leg = 33
    spread_trade = 34
    cgate_session = 35
    cgate_table = 36
    cgate_order = 37
    order_fix = 41
    exec_report_fix = 42
    cancel_reject_fix = 43
    reject_fix = 44
    cancel_fix = 45
    replace_fix = 46
    cancel = 50
    remove = 52
    replace = 53
    accepted = 70
    rejected = 71
    expired = 72
    canceled = 73
    trade = 74
    cancel_rejected = 75
    replace_rejected = 76
    replaced = 77
    removed = 78
    subscribe = 80
    unsubscribe = 81
    subscribe_res = 82
    opt_mm = 90
    field = 91
    trd_capt = 92
    rollover = 93
    mmaker = 94
    sniper = 95
    trd_capt_link_pos = 97
    order_log = 98
    pos_sum = 99
    resolve = 100
    resolve_ack = 101
    mdata_subs = 103
    trd_capt_move_pos = 104


##
# get object schema
def get_object_schema(object_type):
    schema = {"type" : object_type, "fields" : []}
    if object_type == ObjectType.start:
        return schema
    elif object_type == ObjectType.stop:
        return schema
    elif object_type == ObjectType.reconfig:
        return schema
    elif object_type == ObjectType.activate:
        return schema
    elif object_type == ObjectType.deactivate:
        return schema
    elif object_type == ObjectType.date_changed:
        return schema
    elif object_type == ObjectType.reset:
        schema["fields"].append({"name" : "hint", "type" : "int32"})
        return schema
    elif object_type == ObjectType.alarm:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "timestamp", "type" : "uint64"})
        schema["fields"].append({"name" : "level", "type" : "enum", "enum_name" : "AlarmLevel"})
        schema["fields"].append({"name" : "text", "type" : "string", "size" : 128})
        return schema
    elif object_type == ObjectType.exited:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "is_crashed", "type" : "int8"})
        return schema
    elif object_type == ObjectType.event:
        schema["fields"].append({"name" : "type", "type" : "string", "size" : 64})
        schema["fields"].append({"name" : "group", "type" : "string", "size" : 64})
        return schema
    elif object_type == ObjectType.state:
        schema["fields"].append({"name" : "status", "type" : "enum", "enum_name" : "NodeState"})
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        return schema
    elif object_type == ObjectType.fix_session:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "sender_comp_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "target_comp_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "tran_cnt", "type" : "int64"})
        schema["fields"].append({"name" : "expected_seqnum_in", "type" : "int64"})
        schema["fields"].append({"name" : "sent_seqnum_out", "type" : "int64"})
        schema["fields"].append({"name" : "status", "type" : "enum", "enum_name" : "FixSessionStatus"})
        schema["fields"].append({"name" : "order_fix", "type" : "object_ref"})
        schema["fields"].append({"name" : "cancel_fix", "type" : "object_ref"})
        schema["fields"].append({"name" : "replace_fix", "type" : "object_ref"})
        schema["fields"].append({"name" : "exec_report_fix", "type" : "object_ref"})
        schema["fields"].append({"name" : "cancel_reject_fix", "type" : "object_ref"})
        schema["fields"].append({"name" : "reject_fix", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.order:
        schema["fields"].append({"name" : "side", "type" : "enum", "enum_name" : "Side"})
        schema["fields"].append({"name" : "tif", "type" : "enum", "enum_name" : "Tif"})
        schema["fields"].append({"name" : "src_node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "dst_node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "ext_ref", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "status", "type" : "enum", "enum_name" : "OrderStatus"})
        schema["fields"].append({"name" : "sub_status", "type" : "int32"})
        schema["fields"].append({"name" : "sender", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "timestamp", "type" : "uint64"})
        schema["fields"].append({"name" : "account", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "client_code", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "sales", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "leaves_qty", "type" : "int64"})
        schema["fields"].append({"name" : "cum_qty", "type" : "int64"})
        schema["fields"].append({"name" : "type", "type" : "enum", "enum_name" : "OrdType"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "exp_date", "type" : "uint64"})
        schema["fields"].append({"name" : "flags", "type" : "int32"})
        schema["fields"].append({"name" : "snd_time", "type" : "uint64"})
        schema["fields"].append({"name" : "rcv_time", "type" : "uint64"})
        schema["fields"].append({"name" : "parent", "type" : "object_ref"})
        schema["fields"].append({"name" : "child", "type" : "object_ref"})
        schema["fields"].append({"name" : "algo", "type" : "object_ref"})
        schema["fields"].append({"name" : "hedge_cur", "type" : "enum", "enum_name" : "Currency"})
        return schema
    elif object_type == ObjectType.pos:
        schema["fields"].append({"name" : "sender", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        schema["fields"].append({"name" : "last_trd_capt_id", "type" : "int32"})
        schema["fields"].append({"name" : "first_import_trd_capt", "type" : "object_ref"})
        schema["fields"].append({"name" : "book", "type" : "string", "size" : 12})
        schema["fields"].append({"name" : "desk", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "total_buy", "type" : "int64"})
        schema["fields"].append({"name" : "total_sell", "type" : "int64"})
        schema["fields"].append({"name" : "avg_price", "type" : "double"})
        schema["fields"].append({"name" : "last_price", "type" : "double"})
        schema["fields"].append({"name" : "total_pnl", "type" : "double"})
        schema["fields"].append({"name" : "realize_pnl", "type" : "double"})
        schema["fields"].append({"name" : "unrealize_pnl", "type" : "double"})
        schema["fields"].append({"name" : "cost", "type" : "double"})
        schema["fields"].append({"name" : "exch_fee", "type" : "double"})
        schema["fields"].append({"name" : "pos_sum", "type" : "object_ref"})
        schema["fields"].append({"name" : "nkd", "type" : "double"})
        return schema
    elif object_type == ObjectType.order_stat:
        schema["fields"].append({"name" : "sender", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "order_cnt", "type" : "int32"})
        schema["fields"].append({"name" : "active_order_cnt", "type" : "int32"})
        schema["fields"].append({"name" : "lat_min", "type" : "int32"})
        schema["fields"].append({"name" : "lat_max", "type" : "int32"})
        schema["fields"].append({"name" : "lat_50", "type" : "int32"})
        schema["fields"].append({"name" : "lat_75", "type" : "int32"})
        schema["fields"].append({"name" : "lat_99", "type" : "int32"})
        schema["fields"].append({"name" : "lat_9999", "type" : "int32"})
        schema["fields"].append({"name" : "rtp_min", "type" : "int32"})
        schema["fields"].append({"name" : "rtp_max", "type" : "int32"})
        schema["fields"].append({"name" : "rtp_50", "type" : "int32"})
        schema["fields"].append({"name" : "rtp_75", "type" : "int32"})
        schema["fields"].append({"name" : "rtp_99", "type" : "int32"})
        schema["fields"].append({"name" : "rtp_9999", "type" : "int32"})
        return schema
    elif object_type == ObjectType.iceberg:
        schema["fields"].append({"name" : "display_qty", "type" : "int64"})
        return schema
    elif object_type == ObjectType.twap:
        schema["fields"].append({"name" : "start", "type" : "int32"})
        schema["fields"].append({"name" : "stop", "type" : "int32"})
        schema["fields"].append({"name" : "agression_level", "type" : "int32"})
        schema["fields"].append({"name" : "mid_time", "type" : "int32"})
        schema["fields"].append({"name" : "agression_time", "type" : "int32"})
        return schema
    elif object_type == ObjectType.pov:
        schema["fields"].append({"name" : "start", "type" : "int32"})
        schema["fields"].append({"name" : "stop", "type" : "int32"})
        schema["fields"].append({"name" : "agression_level", "type" : "int32"})
        schema["fields"].append({"name" : "mid_time", "type" : "int32"})
        schema["fields"].append({"name" : "agression_time", "type" : "int32"})
        schema["fields"].append({"name" : "period", "type" : "int32"})
        schema["fields"].append({"name" : "rate", "type" : "double"})
        schema["fields"].append({"name" : "display_qty", "type" : "int64"})
        return schema
    elif object_type == ObjectType.vwap:
        schema["fields"].append({"name" : "start", "type" : "int32"})
        schema["fields"].append({"name" : "stop", "type" : "int32"})
        schema["fields"].append({"name" : "agression_level", "type" : "int32"})
        schema["fields"].append({"name" : "mid_time", "type" : "int32"})
        schema["fields"].append({"name" : "agression_time", "type" : "int32"})
        schema["fields"].append({"name" : "price_move", "type" : "double"})
        return schema
    elif object_type == ObjectType.instr:
        schema["fields"].append({"name" : "alias", "type" : "string", "size" : 20})
        schema["fields"].append({"name" : "name", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "long_name", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "cqg_name", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "exch_id", "type" : "int64"})
        schema["fields"].append({"name" : "cls", "type" : "string", "size" : 20})
        schema["fields"].append({"name" : "exch", "type" : "enum", "enum_name" : "Exchange"})
        schema["fields"].append({"name" : "cfi", "type" : "string", "size" : 6})
        schema["fields"].append({"name" : "cur", "type" : "enum", "enum_name" : "Currency"})
        schema["fields"].append({"name" : "lot_size", "type" : "int32"})
        schema["fields"].append({"name" : "deleted", "type" : "int8"})
        schema["fields"].append({"name" : "strike", "type" : "double"})
        schema["fields"].append({"name" : "face_value", "type" : "double"})
        schema["fields"].append({"name" : "accrued_int", "type" : "double"})
        schema["fields"].append({"name" : "exp_dtime", "type" : "uint64"})
        schema["fields"].append({"name" : "callput", "type" : "enum", "enum_name" : "Callput"})
        schema["fields"].append({"name" : "isin", "type" : "string", "size" : 12})
        schema["fields"].append({"name" : "bb_source", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "bb_code", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "bb_figi", "type" : "string", "size" : 12})
        schema["fields"].append({"name" : "underlying", "type" : "object_ref"})
        schema["fields"].append({"name" : "leading", "type" : "object_ref"})
        schema["fields"].append({"name" : "tick_info", "type" : "object_ref"})
        schema["fields"].append({"name" : "timesheet", "type" : "object_ref"})
        schema["fields"].append({"name" : "mdstat", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.tick_info:
        schema["fields"].append({"name" : "price_min", "type" : "double"})
        schema["fields"].append({"name" : "price_max", "type" : "double"})
        schema["fields"].append({"name" : "size", "type" : "double"})
        schema["fields"].append({"name" : "value", "type" : "double"})
        schema["fields"].append({"name" : "precision", "type" : "int32"})
        schema["fields"].append({"name" : "next", "type" : "object_ref"})
        schema["fields"].append({"name" : "deleted", "type" : "int8"})
        return schema
    elif object_type == ObjectType.timesheet:
        schema["fields"].append({"name" : "start", "type" : "int64"})
        schema["fields"].append({"name" : "stop", "type" : "int64"})
        schema["fields"].append({"name" : "next", "type" : "object_ref"})
        schema["fields"].append({"name" : "deleted", "type" : "int8"})
        return schema
    elif object_type == ObjectType.mdstat:
        schema["fields"].append({"name" : "last_price", "type" : "double"})
        schema["fields"].append({"name" : "update_ts", "type" : "int64"})
        return schema
    elif object_type == ObjectType.order_sql:
        schema["fields"].append({"name" : "db_id", "type" : "int64"})
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        return schema
    elif object_type == ObjectType.cancel_sql:
        schema["fields"].append({"name" : "db_id", "type" : "int64"})
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        return schema
    elif object_type == ObjectType.replace_sql:
        schema["fields"].append({"name" : "db_id", "type" : "int64"})
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        return schema
    elif object_type == ObjectType.order_rabbit:
        schema["fields"].append({"name" : "side", "type" : "enum", "enum_name" : "Side"})
        schema["fields"].append({"name" : "tif", "type" : "enum", "enum_name" : "Tif"})
        schema["fields"].append({"name" : "src_node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "dst_node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "ext_ref", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "status", "type" : "enum", "enum_name" : "OrderStatus"})
        schema["fields"].append({"name" : "sub_status", "type" : "int32"})
        schema["fields"].append({"name" : "clord_id", "type" : "int64"})
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.rake:
        schema["fields"].append({"name" : "working_int", "type" : "int32"})
        schema["fields"].append({"name" : "book_depth", "type" : "int32"})
        schema["fields"].append({"name" : "level_dist", "type" : "int32"})
        schema["fields"].append({"name" : "agression_level", "type" : "int32"})
        schema["fields"].append({"name" : "mid_time", "type" : "int32"})
        schema["fields"].append({"name" : "agression_time", "type" : "int32"})
        schema["fields"].append({"name" : "display_qty", "type" : "int64"})
        return schema
    elif object_type == ObjectType.stealth:
        schema["fields"].append({"name" : "working_int", "type" : "int32"})
        schema["fields"].append({"name" : "display_qty", "type" : "int32"})
        schema["fields"].append({"name" : "qty_shift", "type" : "double"})
        schema["fields"].append({"name" : "book_depth", "type" : "int32"})
        schema["fields"].append({"name" : "level_dist", "type" : "int32"})
        schema["fields"].append({"name" : "liq_price_shift", "type" : "double"})
        return schema
    elif object_type == ObjectType.spread:
        schema["fields"].append({"name" : "side", "type" : "enum", "enum_name" : "Side"})
        schema["fields"].append({"name" : "tif", "type" : "enum", "enum_name" : "Tif"})
        schema["fields"].append({"name" : "src_node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "dst_node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "ext_ref", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "status", "type" : "enum", "enum_name" : "OrderStatus"})
        schema["fields"].append({"name" : "sub_status", "type" : "int32"})
        schema["fields"].append({"name" : "sender", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "timestamp", "type" : "uint64"})
        schema["fields"].append({"name" : "type", "type" : "enum", "enum_name" : "OrdType"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "leaves_qty", "type" : "int64"})
        schema["fields"].append({"name" : "cum_qty", "type" : "int64"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "flags", "type" : "int32"})
        schema["fields"].append({"name" : "agression_level", "type" : "int32"})
        schema["fields"].append({"name" : "fill_timeout", "type" : "int32"})
        schema["fields"].append({"name" : "cancel_on_hang", "type" : "int8"})
        schema["fields"].append({"name" : "leg", "type" : "object_ref"})
        schema["fields"].append({"name" : "text", "type" : "string", "size" : 64})
        schema["fields"].append({"name" : "vwap_price", "type" : "double"})
        schema["fields"].append({"name" : "mdata_price", "type" : "double"})
        schema["fields"].append({"name" : "mdata_qty", "type" : "int64"})
        return schema
    elif object_type == ObjectType.leg:
        schema["fields"].append({"name" : "uniq_id", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "next", "type" : "object_ref"})
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "qty_ratio", "type" : "int32"})
        schema["fields"].append({"name" : "is_working", "type" : "int8"})
        schema["fields"].append({"name" : "vwap_price", "type" : "double"})
        return schema
    elif object_type == ObjectType.spread_trade:
        schema["fields"].append({"name" : "spread", "type" : "object_ref"})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        schema["fields"].append({"name" : "order_status", "type" : "enum", "enum_name" : "OrderStatus"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "leaves_qty", "type" : "int64"})
        schema["fields"].append({"name" : "cum_qty", "type" : "int64"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "trade", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.cgate_session:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "name", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "lifenum", "type" : "int64"})
        schema["fields"].append({"name" : "cgate_table", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.cgate_table:
        schema["fields"].append({"name" : "name", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "rev", "type" : "int64"})
        schema["fields"].append({"name" : "next", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.cgate_order:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "exch_id", "type" : "int64"})
        schema["fields"].append({"name" : "replace", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.order_fix:
        schema["fields"].append({"name" : "sender", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        schema["fields"].append({"name" : "seqnum", "type" : "int64"})
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "order_id", "type" : "int64"})
        schema["fields"].append({"name" : "status", "type" : "enum", "enum_name" : "OrderFixStatus"})
        schema["fields"].append({"name" : "clord_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "leaves_qty", "type" : "int64"})
        schema["fields"].append({"name" : "cum_qty", "type" : "int64"})
        schema["fields"].append({"name" : "display_qty", "type" : "int64"})
        schema["fields"].append({"name" : "crfix", "type" : "object_ref"})
        schema["fields"].append({"name" : "parent", "type" : "object_ref"})
        schema["fields"].append({"name" : "child", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.exec_report_fix:
        schema["fields"].append({"name" : "sender", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "order_id", "type" : "int64"})
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "seqnum", "type" : "int64"})
        schema["fields"].append({"name" : "clord_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "orig_clord_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "sec_clord_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "exec_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "exec_type", "type" : "enum", "enum_name" : "ExecType"})
        schema["fields"].append({"name" : "ofix", "type" : "object_ref"})
        schema["fields"].append({"name" : "order_status", "type" : "enum", "enum_name" : "OrderFixStatus"})
        schema["fields"].append({"name" : "side", "type" : "enum", "enum_name" : "Side"})
        schema["fields"].append({"name" : "symbol", "type" : "string", "size" : 20})
        schema["fields"].append({"name" : "cls", "type" : "string", "size" : 20})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "tif", "type" : "enum", "enum_name" : "Tif"})
        schema["fields"].append({"name" : "exp_date", "type" : "uint64"})
        schema["fields"].append({"name" : "last_qty", "type" : "int64"})
        schema["fields"].append({"name" : "leaves_qty", "type" : "int64"})
        schema["fields"].append({"name" : "cum_qty", "type" : "int64"})
        schema["fields"].append({"name" : "last_px", "type" : "double"})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        schema["fields"].append({"name" : "reason", "type" : "int32"})
        schema["fields"].append({"name" : "text", "type" : "string", "size" : 128})
        schema["fields"].append({"name" : "mleg_report_type", "type" : "enum", "enum_name" : "MlegReportType"})
        return schema
    elif object_type == ObjectType.cancel_reject_fix:
        schema["fields"].append({"name" : "sender", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "crfix", "type" : "object_ref"})
        schema["fields"].append({"name" : "seqnum", "type" : "int64"})
        schema["fields"].append({"name" : "status", "type" : "enum", "enum_name" : "OrderFixStatus"})
        schema["fields"].append({"name" : "clord_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "sec_clord_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "orig_clord_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "response_to", "type" : "enum", "enum_name" : "RejResponseTo"})
        schema["fields"].append({"name" : "reason", "type" : "int32"})
        schema["fields"].append({"name" : "text", "type" : "string", "size" : 128})
        return schema
    elif object_type == ObjectType.reject_fix:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "seqnum", "type" : "int64"})
        schema["fields"].append({"name" : "ref_seqnum", "type" : "int64"})
        schema["fields"].append({"name" : "reason", "type" : "int32"})
        schema["fields"].append({"name" : "text", "type" : "string", "size" : 128})
        return schema
    elif object_type == ObjectType.cancel_fix:
        schema["fields"].append({"name" : "ofix", "type" : "object_ref"})
        schema["fields"].append({"name" : "seqnum", "type" : "int64"})
        schema["fields"].append({"name" : "clord_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "orig_clord_id", "type" : "string", "size" : 32})
        return schema
    elif object_type == ObjectType.replace_fix:
        schema["fields"].append({"name" : "ofix", "type" : "object_ref"})
        schema["fields"].append({"name" : "seqnum", "type" : "int64"})
        schema["fields"].append({"name" : "clord_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "orig_clord_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        return schema
    elif object_type == ObjectType.cancel:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.remove:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.replace:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "hedge_cur", "type" : "enum", "enum_name" : "Currency"})
        schema["fields"].append({"name" : "algo", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.accepted:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        schema["fields"].append({"name" : "exch_id", "type" : "int64"})
        schema["fields"].append({"name" : "order_status", "type" : "enum", "enum_name" : "OrderStatus"})
        return schema
    elif object_type == ObjectType.rejected:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        schema["fields"].append({"name" : "reason", "type" : "enum", "enum_name" : "RejReason"})
        schema["fields"].append({"name" : "text", "type" : "string", "size" : 128})
        return schema
    elif object_type == ObjectType.expired:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        return schema
    elif object_type == ObjectType.canceled:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        return schema
    elif object_type == ObjectType.trade:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        schema["fields"].append({"name" : "exch_id", "type" : "int64"})
        schema["fields"].append({"name" : "opp_order", "type" : "object_ref"})
        schema["fields"].append({"name" : "order_status", "type" : "enum", "enum_name" : "OrderStatus"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "leaves_qty", "type" : "int64"})
        schema["fields"].append({"name" : "cum_qty", "type" : "int64"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "next", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.cancel_rejected:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "order_status", "type" : "enum", "enum_name" : "OrderStatus"})
        schema["fields"].append({"name" : "reason", "type" : "enum", "enum_name" : "RejReason"})
        schema["fields"].append({"name" : "text", "type" : "string", "size" : 128})
        return schema
    elif object_type == ObjectType.replace_rejected:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "order_status", "type" : "enum", "enum_name" : "OrderStatus"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "leaves_qty", "type" : "int64"})
        schema["fields"].append({"name" : "cum_qty", "type" : "int64"})
        schema["fields"].append({"name" : "reason", "type" : "enum", "enum_name" : "RejReason"})
        schema["fields"].append({"name" : "text", "type" : "string", "size" : 128})
        return schema
    elif object_type == ObjectType.replaced:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        schema["fields"].append({"name" : "order_status", "type" : "enum", "enum_name" : "OrderStatus"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "leaves_qty", "type" : "int64"})
        schema["fields"].append({"name" : "cum_qty", "type" : "int64"})
        return schema
    elif object_type == ObjectType.removed:
        schema["fields"].append({"name" : "order", "type" : "object_ref"})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        return schema
    elif object_type == ObjectType.subscribe:
        schema["fields"].append({"name" : "src_node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.unsubscribe:
        schema["fields"].append({"name" : "src_node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.subscribe_res:
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        schema["fields"].append({"name" : "result", "type" : "enum", "enum_name" : "SubsResult"})
        return schema
    elif object_type == ObjectType.opt_mm:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        schema["fields"].append({"name" : "enabled", "type" : "int8"})
        schema["fields"].append({"name" : "deleted", "type" : "int8"})
        schema["fields"].append({"name" : "bid_enabled", "type" : "int8"})
        schema["fields"].append({"name" : "bid_state", "type" : "enum", "enum_name" : "OptMmState"})
        schema["fields"].append({"name" : "ask_enabled", "type" : "int8"})
        schema["fields"].append({"name" : "ask_state", "type" : "enum", "enum_name" : "OptMmState"})
        schema["fields"].append({"name" : "premium", "type" : "double"})
        schema["fields"].append({"name" : "delta", "type" : "double"})
        schema["fields"].append({"name" : "volatility", "type" : "double"})
        schema["fields"].append({"name" : "rate", "type" : "double"})
        schema["fields"].append({"name" : "time_rate", "type" : "double"})
        schema["fields"].append({"name" : "fut_mid_price", "type" : "double"})
        schema["fields"].append({"name" : "mid_price", "type" : "double"})
        schema["fields"].append({"name" : "bid_size", "type" : "int64"})
        schema["fields"].append({"name" : "ask_size", "type" : "int64"})
        schema["fields"].append({"name" : "lower", "type" : "int64"})
        schema["fields"].append({"name" : "higher", "type" : "int64"})
        schema["fields"].append({"name" : "position", "type" : "int64"})
        schema["fields"].append({"name" : "pos_keep", "type" : "int64"})
        schema["fields"].append({"name" : "bid_spread", "type" : "double"})
        schema["fields"].append({"name" : "ask_spread", "type" : "double"})
        schema["fields"].append({"name" : "sensitivity", "type" : "double"})
        schema["fields"].append({"name" : "shift", "type" : "double"})
        schema["fields"].append({"name" : "shift_vol", "type" : "double"})
        schema["fields"].append({"name" : "calc_mid", "type" : "enum", "enum_name" : "CalcMid"})
        schema["fields"].append({"name" : "bid_text", "type" : "string", "size" : 64})
        schema["fields"].append({"name" : "ask_text", "type" : "string", "size" : 64})
        return schema
    elif object_type == ObjectType.field:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "name", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "type", "type" : "enum", "enum_name" : "FieldType"})
        schema["fields"].append({"name" : "value", "type" : "binary", "size" : 128})
        schema["fields"].append({"name" : "deleted", "type" : "int8"})
        return schema
    elif object_type == ObjectType.trd_capt:
        schema["fields"].append({"name" : "tradeno", "type" : "uint64"})
        schema["fields"].append({"name" : "orderno", "type" : "uint64"})
        schema["fields"].append({"name" : "trade", "type" : "object_ref"})
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        schema["fields"].append({"name" : "side", "type" : "enum", "enum_name" : "Side"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "qty_items", "type" : "int64"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "account", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "client_code", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "exch_fee", "type" : "double"})
        schema["fields"].append({"name" : "book", "type" : "string", "size" : 12})
        schema["fields"].append({"name" : "otc_id", "type" : "int64"})
        schema["fields"].append({"name" : "counterparty", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "deleted", "type" : "int8"})
        schema["fields"].append({"name" : "face_value", "type" : "double"})
        schema["fields"].append({"name" : "accrued_int", "type" : "double"})
        return schema
    elif object_type == ObjectType.rollover:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "start_ts", "type" : "uint64"})
        schema["fields"].append({"name" : "index", "type" : "double"})
        schema["fields"].append({"name" : "leg1_alias", "type" : "string", "size" : 20})
        schema["fields"].append({"name" : "leg1_side", "type" : "enum", "enum_name" : "Side"})
        schema["fields"].append({"name" : "leg1_state", "type" : "int32"})
        schema["fields"].append({"name" : "leg1_reason", "type" : "string", "size" : 128})
        schema["fields"].append({"name" : "leg1_price", "type" : "double"})
        schema["fields"].append({"name" : "leg1_qty", "type" : "int64"})
        schema["fields"].append({"name" : "leg1_cum_qty", "type" : "int64"})
        schema["fields"].append({"name" : "leg2_alias", "type" : "string", "size" : 20})
        schema["fields"].append({"name" : "leg2_side", "type" : "enum", "enum_name" : "Side"})
        schema["fields"].append({"name" : "leg2_state", "type" : "int32"})
        schema["fields"].append({"name" : "leg2_reason", "type" : "string", "size" : 128})
        schema["fields"].append({"name" : "leg2_price", "type" : "double"})
        schema["fields"].append({"name" : "leg2_qty", "type" : "int64"})
        schema["fields"].append({"name" : "leg2_cum_qty", "type" : "int64"})
        return schema
    elif object_type == ObjectType.mmaker:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "start_ts", "type" : "uint64"})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        schema["fields"].append({"name" : "active_side", "type" : "enum", "enum_name" : "Side"})
        schema["fields"].append({"name" : "best_bid", "type" : "double"})
        schema["fields"].append({"name" : "last_trade", "type" : "enum", "enum_name" : "Side"})
        schema["fields"].append({"name" : "total_buy", "type" : "int64"})
        schema["fields"].append({"name" : "total_sell", "type" : "int64"})
        schema["fields"].append({"name" : "bids", "type" : "binary", "size" : 480})
        schema["fields"].append({"name" : "asks", "type" : "binary", "size" : 480})
        return schema
    elif object_type == ObjectType.sniper:
        return schema
    elif object_type == ObjectType.trd_capt_link_pos:
        schema["fields"].append({"name" : "trd_capt", "type" : "object_ref"})
        schema["fields"].append({"name" : "pos", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.order_log:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "exec_id", "type" : "string", "size" : 32})
        schema["fields"].append({"name" : "orderno", "type" : "uint64"})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        schema["fields"].append({"name" : "side", "type" : "enum", "enum_name" : "Side"})
        schema["fields"].append({"name" : "qty", "type" : "int64"})
        schema["fields"].append({"name" : "leaves_qty", "type" : "int64"})
        schema["fields"].append({"name" : "cum_qty", "type" : "int64"})
        schema["fields"].append({"name" : "price", "type" : "double"})
        schema["fields"].append({"name" : "exec_type", "type" : "enum", "enum_name" : "ExecType"})
        schema["fields"].append({"name" : "status", "type" : "enum", "enum_name" : "OrderStatus"})
        schema["fields"].append({"name" : "account", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "client_code", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "tran_time", "type" : "int64"})
        return schema
    elif object_type == ObjectType.pos_sum:
        schema["fields"].append({"name" : "sender", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "book", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "desk", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "realize_pnl", "type" : "double"})
        schema["fields"].append({"name" : "unrealize_pnl", "type" : "double"})
        schema["fields"].append({"name" : "exch_fee", "type" : "double"})
        return schema
    elif object_type == ObjectType.resolve:
        schema["fields"].append({"name" : "req_id", "type" : "string", "size" : 36})
        schema["fields"].append({"name" : "alias", "type" : "string", "size" : 20})
        schema["fields"].append({"name" : "from_node", "type" : "uint16"})
        schema["fields"].append({"name" : "isin", "type" : "string", "size" : 12})
        schema["fields"].append({"name" : "bb_source", "type" : "string", "size" : 16})
        schema["fields"].append({"name" : "bb_code", "type" : "string", "size" : 32})
        return schema
    elif object_type == ObjectType.resolve_ack:
        schema["fields"].append({"name" : "req_id", "type" : "string", "size" : 36})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        return schema
    elif object_type == ObjectType.mdata_subs:
        schema["fields"].append({"name" : "node_id", "type" : "uint16"})
        schema["fields"].append({"name" : "req_id", "type" : "string", "size" : 36})
        schema["fields"].append({"name" : "instr", "type" : "object_ref"})
        schema["fields"].append({"name" : "state", "type" : "enum", "enum_name" : "MdataSubsState"})
        schema["fields"].append({"name" : "ref_cnt", "type" : "int32"})
        return schema
    elif object_type == ObjectType.trd_capt_move_pos:
        schema["fields"].append({"name" : "trd_capt_to", "type" : "object_ref"})
        schema["fields"].append({"name" : "trd_capt_from", "type" : "object_ref"})
        return schema


class BrokenRefError(Exception):
    pass


##
# convert string (object_type, id) into tuple
def str_to_tuple(ref):
    res = re.match(r"\(\s*([a-z_0-9]+)\s*,\s*(\d+)\s*\)", ref)
    if res is None:
        raise ValueError("wrong object reference {0}".format(ref))
    (otype, obj_id) = res.group(1, 2)
    return (ObjectType(int(otype)), int(obj_id))


def create_object(obj_type):
    ptr = lib.node().xroad_node_create_object(obj_type)
    return ptr_to_object(ptr, True)


def ptr_to_object(ptr, delete_it=False):
    obj_type = ObjectType(lib.node().xroad_object_get_type(ptr))
    if obj_type == ObjectType.start:
        return Start(ptr, delete_it)
    elif obj_type == ObjectType.stop:
        return Stop(ptr, delete_it)
    elif obj_type == ObjectType.reconfig:
        return Reconfig(ptr, delete_it)
    elif obj_type == ObjectType.activate:
        return Activate(ptr, delete_it)
    elif obj_type == ObjectType.deactivate:
        return Deactivate(ptr, delete_it)
    elif obj_type == ObjectType.date_changed:
        return DateChanged(ptr, delete_it)
    elif obj_type == ObjectType.reset:
        return Reset(ptr, delete_it)
    elif obj_type == ObjectType.alarm:
        return Alarm(ptr, delete_it)
    elif obj_type == ObjectType.exited:
        return Exited(ptr, delete_it)
    elif obj_type == ObjectType.event:
        return Event(ptr, delete_it)
    elif obj_type == ObjectType.state:
        return State(ptr, delete_it)
    elif obj_type == ObjectType.fix_session:
        return FixSession(ptr)
    elif obj_type == ObjectType.order:
        return Order(ptr)
    elif obj_type == ObjectType.pos:
        return Pos(ptr)
    elif obj_type == ObjectType.order_stat:
        return OrderStat(ptr)
    elif obj_type == ObjectType.iceberg:
        return Iceberg(ptr)
    elif obj_type == ObjectType.twap:
        return Twap(ptr)
    elif obj_type == ObjectType.pov:
        return Pov(ptr)
    elif obj_type == ObjectType.vwap:
        return Vwap(ptr)
    elif obj_type == ObjectType.instr:
        return Instr(ptr)
    elif obj_type == ObjectType.tick_info:
        return TickInfo(ptr)
    elif obj_type == ObjectType.timesheet:
        return Timesheet(ptr)
    elif obj_type == ObjectType.mdstat:
        return Mdstat(ptr)
    elif obj_type == ObjectType.order_sql:
        return OrderSql(ptr)
    elif obj_type == ObjectType.cancel_sql:
        return CancelSql(ptr)
    elif obj_type == ObjectType.replace_sql:
        return ReplaceSql(ptr)
    elif obj_type == ObjectType.order_rabbit:
        return OrderRabbit(ptr)
    elif obj_type == ObjectType.rake:
        return Rake(ptr)
    elif obj_type == ObjectType.stealth:
        return Stealth(ptr)
    elif obj_type == ObjectType.spread:
        return Spread(ptr)
    elif obj_type == ObjectType.leg:
        return Leg(ptr)
    elif obj_type == ObjectType.spread_trade:
        return SpreadTrade(ptr)
    elif obj_type == ObjectType.cgate_session:
        return CgateSession(ptr)
    elif obj_type == ObjectType.cgate_table:
        return CgateTable(ptr)
    elif obj_type == ObjectType.cgate_order:
        return CgateOrder(ptr)
    elif obj_type == ObjectType.order_fix:
        return OrderFix(ptr)
    elif obj_type == ObjectType.exec_report_fix:
        return ExecReportFix(ptr)
    elif obj_type == ObjectType.cancel_reject_fix:
        return CancelRejectFix(ptr)
    elif obj_type == ObjectType.reject_fix:
        return RejectFix(ptr)
    elif obj_type == ObjectType.cancel_fix:
        return CancelFix(ptr)
    elif obj_type == ObjectType.replace_fix:
        return ReplaceFix(ptr)
    elif obj_type == ObjectType.cancel:
        return Cancel(ptr, delete_it)
    elif obj_type == ObjectType.remove:
        return Remove(ptr, delete_it)
    elif obj_type == ObjectType.replace:
        return Replace(ptr)
    elif obj_type == ObjectType.accepted:
        return Accepted(ptr, delete_it)
    elif obj_type == ObjectType.rejected:
        return Rejected(ptr, delete_it)
    elif obj_type == ObjectType.expired:
        return Expired(ptr, delete_it)
    elif obj_type == ObjectType.canceled:
        return Canceled(ptr, delete_it)
    elif obj_type == ObjectType.trade:
        return Trade(ptr)
    elif obj_type == ObjectType.cancel_rejected:
        return CancelRejected(ptr, delete_it)
    elif obj_type == ObjectType.replace_rejected:
        return ReplaceRejected(ptr, delete_it)
    elif obj_type == ObjectType.replaced:
        return Replaced(ptr, delete_it)
    elif obj_type == ObjectType.removed:
        return Removed(ptr, delete_it)
    elif obj_type == ObjectType.subscribe:
        return Subscribe(ptr, delete_it)
    elif obj_type == ObjectType.unsubscribe:
        return Unsubscribe(ptr, delete_it)
    elif obj_type == ObjectType.subscribe_res:
        return SubscribeRes(ptr, delete_it)
    elif obj_type == ObjectType.opt_mm:
        return OptMm(ptr)
    elif obj_type == ObjectType.field:
        return Field(ptr)
    elif obj_type == ObjectType.trd_capt:
        return TrdCapt(ptr)
    elif obj_type == ObjectType.rollover:
        return Rollover(ptr)
    elif obj_type == ObjectType.mmaker:
        return Mmaker(ptr)
    elif obj_type == ObjectType.sniper:
        return Sniper(ptr)
    elif obj_type == ObjectType.trd_capt_link_pos:
        return TrdCaptLinkPos(ptr)
    elif obj_type == ObjectType.order_log:
        return OrderLog(ptr)
    elif obj_type == ObjectType.pos_sum:
        return PosSum(ptr)
    elif obj_type == ObjectType.resolve:
        return Resolve(ptr)
    elif obj_type == ObjectType.resolve_ack:
        return ResolveAck(ptr, delete_it)
    elif obj_type == ObjectType.mdata_subs:
        return MdataSubs(ptr)
    elif obj_type == ObjectType.trd_capt_move_pos:
        return TrdCaptMovePos(ptr)
    raise TypeError("unknown object type")


def printable_tables():
    return ["fix_session"
           , "order"
           , "pos"
           , "order_stat"
           , "iceberg"
           , "twap"
           , "pov"
           , "vwap"
           , "instr"
           , "tick_info"
           , "timesheet"
           , "mdstat"
           , "order_sql"
           , "cancel_sql"
           , "replace_sql"
           , "order_rabbit"
           , "rake"
           , "stealth"
           , "spread"
           , "leg"
           , "spread_trade"
           , "cgate_session"
           , "cgate_table"
           , "cgate_order"
           , "order_fix"
           , "exec_report_fix"
           , "cancel_reject_fix"
           , "reject_fix"
           , "cancel_fix"
           , "replace_fix"
           , "replace"
           , "trade"
           , "opt_mm"
           , "field"
           , "trd_capt"
           , "rollover"
           , "mmaker"
           , "sniper"
           , "trd_capt_link_pos"
           , "order_log"
           , "pos_sum"
           , "resolve"
           , "mdata_subs"
           , "trd_capt_move_pos"]


class Start(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_start_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_start_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_start_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_start_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.start

    @property
    def is_valid(self):
        lib.node().xroad_start_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_start_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_start_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_start_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_start_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_start_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_start_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_start_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_start_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Start(lib.node().xroad_start_clone(self.__ptr))


class Stop(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_stop_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stop_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_stop_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_stop_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.stop

    @property
    def is_valid(self):
        lib.node().xroad_stop_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_stop_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_stop_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_stop_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_stop_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_stop_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_stop_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_stop_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_stop_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Stop(lib.node().xroad_stop_clone(self.__ptr))


class Reconfig(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_reconfig_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reconfig_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_reconfig_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_reconfig_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.reconfig

    @property
    def is_valid(self):
        lib.node().xroad_reconfig_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_reconfig_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_reconfig_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_reconfig_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_reconfig_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_reconfig_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_reconfig_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_reconfig_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_reconfig_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Reconfig(lib.node().xroad_reconfig_clone(self.__ptr))


class Activate(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_activate_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_activate_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_activate_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_activate_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.activate

    @property
    def is_valid(self):
        lib.node().xroad_activate_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_activate_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_activate_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_activate_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_activate_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_activate_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_activate_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_activate_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_activate_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Activate(lib.node().xroad_activate_clone(self.__ptr))


class Deactivate(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_deactivate_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_deactivate_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_deactivate_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_deactivate_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.deactivate

    @property
    def is_valid(self):
        lib.node().xroad_deactivate_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_deactivate_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_deactivate_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_deactivate_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_deactivate_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_deactivate_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_deactivate_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_deactivate_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_deactivate_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Deactivate(lib.node().xroad_deactivate_clone(self.__ptr))


class DateChanged(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_date_changed_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_date_changed_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_date_changed_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_date_changed_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.date_changed

    @property
    def is_valid(self):
        lib.node().xroad_date_changed_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_date_changed_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_date_changed_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_date_changed_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_date_changed_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_date_changed_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_date_changed_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_date_changed_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_date_changed_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return DateChanged(lib.node().xroad_date_changed_clone(self.__ptr))


class Reset(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_reset_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reset_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_reset_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_reset_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.reset

    @property
    def is_valid(self):
        lib.node().xroad_reset_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_reset_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_reset_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_reset_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_reset_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_reset_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_reset_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_reset_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_reset_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Reset(lib.node().xroad_reset_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "hint":
            self.hint = int(value) if value is not None else value

    @property
    def hint(self):
        lib.node().xroad_reset_hint_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_reset_hint_is_set(self.__ptr):
            lib.node().xroad_reset_get_hint.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reset_get_hint.restype = ctypes.c_int
            return lib.node().xroad_reset_get_hint(self.__ptr)
        else:
            return None

    @hint.setter
    def hint(self, value):
        if value is not None:
            lib.node().xroad_reset_set_hint.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_reset_set_hint(self.__ptr, value)
        else:
            lib.node().xroad_reset_reset_hint.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reset_reset_hint(self.__ptr)


class Alarm(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_alarm_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_alarm_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_alarm_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_alarm_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.alarm

    @property
    def is_valid(self):
        lib.node().xroad_alarm_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_alarm_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_alarm_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_alarm_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_alarm_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_alarm_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_alarm_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_alarm_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_alarm_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Alarm(lib.node().xroad_alarm_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "timestamp":
            self.timestamp = int(value) if value is not None else value
        elif field == "level":
            self.level = xtypes.AlarmLevel[value] if value is not None else value
        elif field == "text":
            self.text = str(value) if value is not None else value

    @property
    def node_id(self):
        lib.node().xroad_alarm_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_alarm_node_id_is_set(self.__ptr):
            lib.node().xroad_alarm_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_alarm_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_alarm_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_alarm_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_alarm_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_alarm_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_alarm_reset_node_id(self.__ptr)

    @property
    def timestamp(self):
        lib.node().xroad_alarm_timestamp_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_alarm_timestamp_is_set(self.__ptr):
            lib.node().xroad_alarm_get_timestamp.argtypes = [ctypes.c_void_p]
            lib.node().xroad_alarm_get_timestamp.restype = ctypes.c_ulong
            return lib.node().xroad_alarm_get_timestamp(self.__ptr)
        else:
            return None

    @timestamp.setter
    def timestamp(self, value):
        if value is not None:
            lib.node().xroad_alarm_set_timestamp.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_alarm_set_timestamp(self.__ptr, value)
        else:
            lib.node().xroad_alarm_reset_timestamp.argtypes = [ctypes.c_void_p]
            lib.node().xroad_alarm_reset_timestamp(self.__ptr)

    @property
    def level(self):
        lib.node().xroad_alarm_level_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_alarm_level_is_set(self.__ptr):
            lib.node().xroad_alarm_get_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_alarm_get_level.restype = ctypes.c_int
            return xtypes.AlarmLevel(lib.node().xroad_alarm_get_level(self.__ptr))
        else:
            return None

    @level.setter
    def level(self, value):
        if not isinstance(value, xtypes.AlarmLevel) and value is not None:
            raise TypeError("{0} has wrong type. must be AlarmLevel enum".format(value))
        if value is not None:
            lib.node().xroad_alarm_set_level.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_alarm_set_level(self.__ptr, value.value)
        else:
            lib.node().xroad_alarm_reset_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_alarm_reset_level(self.__ptr)

    @property
    def text(self):
        lib.node().xroad_alarm_text_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_alarm_text_is_set(self.__ptr):
            lib.node().xroad_alarm_get_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_alarm_get_text.restype = ctypes.POINTER(xtypes.AlarmText)
            res = lib.node().xroad_alarm_get_text(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @text.setter
    def text(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_alarm_set_text.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_alarm_set_text(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_alarm_reset_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_alarm_reset_text(self.__ptr)


class Exited(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_exited_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exited_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_exited_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_exited_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.exited

    @property
    def is_valid(self):
        lib.node().xroad_exited_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_exited_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_exited_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_exited_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_exited_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_exited_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_exited_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_exited_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_exited_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Exited(lib.node().xroad_exited_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "is_crashed":
            self.is_crashed = int(value) if value is not None else value

    @property
    def node_id(self):
        lib.node().xroad_exited_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exited_node_id_is_set(self.__ptr):
            lib.node().xroad_exited_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exited_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_exited_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_exited_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_exited_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_exited_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exited_reset_node_id(self.__ptr)

    @property
    def is_crashed(self):
        lib.node().xroad_exited_is_crashed_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exited_is_crashed_is_set(self.__ptr):
            lib.node().xroad_exited_get_is_crashed.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exited_get_is_crashed.restype = ctypes.c_byte
            return lib.node().xroad_exited_get_is_crashed(self.__ptr)
        else:
            return None

    @is_crashed.setter
    def is_crashed(self, value):
        if value is not None:
            lib.node().xroad_exited_set_is_crashed.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_exited_set_is_crashed(self.__ptr, value)
        else:
            lib.node().xroad_exited_reset_is_crashed.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exited_reset_is_crashed(self.__ptr)


class Event(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_event_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_event_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_event_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_event_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.event

    @property
    def is_valid(self):
        lib.node().xroad_event_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_event_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_event_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_event_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_event_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_event_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_event_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_event_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_event_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Event(lib.node().xroad_event_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "type":
            self.type = str(value) if value is not None else value
        elif field == "group":
            self.group = str(value) if value is not None else value

    @property
    def type(self):
        lib.node().xroad_event_type_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_event_type_is_set(self.__ptr):
            lib.node().xroad_event_get_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_event_get_type.restype = ctypes.POINTER(xtypes.ShortText)
            res = lib.node().xroad_event_get_type(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @type.setter
    def type(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_event_set_type.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_event_set_type(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_event_reset_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_event_reset_type(self.__ptr)

    @property
    def group(self):
        lib.node().xroad_event_group_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_event_group_is_set(self.__ptr):
            lib.node().xroad_event_get_group.argtypes = [ctypes.c_void_p]
            lib.node().xroad_event_get_group.restype = ctypes.POINTER(xtypes.ShortText)
            res = lib.node().xroad_event_get_group(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @group.setter
    def group(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_event_set_group.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_event_set_group(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_event_reset_group.argtypes = [ctypes.c_void_p]
            lib.node().xroad_event_reset_group(self.__ptr)


class State(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_state_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_state_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_state_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_state_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.state

    @property
    def is_valid(self):
        lib.node().xroad_state_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_state_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_state_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_state_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_state_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_state_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_state_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_state_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_state_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return State(lib.node().xroad_state_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "status":
            self.status = xtypes.NodeState[value] if value is not None else value
        elif field == "node_id":
            self.node_id = int(value) if value is not None else value

    @property
    def status(self):
        lib.node().xroad_state_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_state_status_is_set(self.__ptr):
            lib.node().xroad_state_get_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_state_get_status.restype = ctypes.c_int
            return xtypes.NodeState(lib.node().xroad_state_get_status(self.__ptr))
        else:
            return None

    @status.setter
    def status(self, value):
        if not isinstance(value, xtypes.NodeState) and value is not None:
            raise TypeError("{0} has wrong type. must be NodeState enum".format(value))
        if value is not None:
            lib.node().xroad_state_set_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_state_set_status(self.__ptr, value.value)
        else:
            lib.node().xroad_state_reset_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_state_reset_status(self.__ptr)

    @property
    def node_id(self):
        lib.node().xroad_state_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_state_node_id_is_set(self.__ptr):
            lib.node().xroad_state_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_state_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_state_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_state_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_state_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_state_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_state_reset_node_id(self.__ptr)


class FixSession(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_fix_session_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_fix_session_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.fix_session

    @property
    def is_valid(self):
        lib.node().xroad_fix_session_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_fix_session_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_fix_session_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_fix_session_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_fix_session_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_fix_session_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_fix_session_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_fix_session_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_fix_session_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return FixSession(lib.node().xroad_fix_session_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_fix_session_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_fix_session_get_id.restype = ctypes.c_long
        return lib.node().xroad_fix_session_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_fix_session_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_fix_session_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_fix_session_copy(self.__ptr, id)
        return FixSession(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.sender_comp_id
        if v is not None:
            fields["sender_comp_id"] = v
        v = self.target_comp_id
        if v is not None:
            fields["target_comp_id"] = v
        v = self.tran_cnt
        if v is not None:
            fields["tran_cnt"] = v
        v = self.expected_seqnum_in
        if v is not None:
            fields["expected_seqnum_in"] = v
        v = self.sent_seqnum_out
        if v is not None:
            fields["sent_seqnum_out"] = v
        v = self.status
        if v is not None:
            fields["status"] = v.name
        v = self.order_fix
        if v is not None:
            fields["order_fix"] = "({0},{1})".format(v.object_type, v.id)
        v = self.cancel_fix
        if v is not None:
            fields["cancel_fix"] = "({0},{1})".format(v.object_type, v.id)
        v = self.replace_fix
        if v is not None:
            fields["replace_fix"] = "({0},{1})".format(v.object_type, v.id)
        v = self.exec_report_fix
        if v is not None:
            fields["exec_report_fix"] = "({0},{1})".format(v.object_type, v.id)
        v = self.cancel_reject_fix
        if v is not None:
            fields["cancel_reject_fix"] = "({0},{1})".format(v.object_type, v.id)
        v = self.reject_fix
        if v is not None:
            fields["reject_fix"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "sender_comp_id":
            self.sender_comp_id = str(value) if value is not None else value
        elif field == "target_comp_id":
            self.target_comp_id = str(value) if value is not None else value
        elif field == "tran_cnt":
            self.tran_cnt = int(value) if value is not None else value
        elif field == "expected_seqnum_in":
            self.expected_seqnum_in = int(value) if value is not None else value
        elif field == "sent_seqnum_out":
            self.sent_seqnum_out = int(value) if value is not None else value
        elif field == "status":
            self.status = xtypes.FixSessionStatus[value] if value is not None else value
        elif field == "order_fix":
            if hasattr(value, "ptr"):
                self.order_fix = value
            else:
                self.order_fix = str_to_tuple(value)
        elif field == "cancel_fix":
            if hasattr(value, "ptr"):
                self.cancel_fix = value
            else:
                self.cancel_fix = str_to_tuple(value)
        elif field == "replace_fix":
            if hasattr(value, "ptr"):
                self.replace_fix = value
            else:
                self.replace_fix = str_to_tuple(value)
        elif field == "exec_report_fix":
            if hasattr(value, "ptr"):
                self.exec_report_fix = value
            else:
                self.exec_report_fix = str_to_tuple(value)
        elif field == "cancel_reject_fix":
            if hasattr(value, "ptr"):
                self.cancel_reject_fix = value
            else:
                self.cancel_reject_fix = str_to_tuple(value)
        elif field == "reject_fix":
            if hasattr(value, "ptr"):
                self.reject_fix = value
            else:
                self.reject_fix = str_to_tuple(value)

    @property
    def node_id(self):
        lib.node().xroad_fix_session_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_node_id_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_fix_session_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_fix_session_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_fix_session_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_fix_session_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_node_id(self.__ptr)

    @property
    def sender_comp_id(self):
        lib.node().xroad_fix_session_sender_comp_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_sender_comp_id_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_sender_comp_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_sender_comp_id.restype = ctypes.POINTER(xtypes.SenderCompId)
            res = lib.node().xroad_fix_session_get_sender_comp_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sender_comp_id.setter
    def sender_comp_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_fix_session_set_sender_comp_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_fix_session_set_sender_comp_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_fix_session_reset_sender_comp_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_sender_comp_id(self.__ptr)

    @property
    def target_comp_id(self):
        lib.node().xroad_fix_session_target_comp_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_target_comp_id_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_target_comp_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_target_comp_id.restype = ctypes.POINTER(xtypes.SenderCompId)
            res = lib.node().xroad_fix_session_get_target_comp_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @target_comp_id.setter
    def target_comp_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_fix_session_set_target_comp_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_fix_session_set_target_comp_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_fix_session_reset_target_comp_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_target_comp_id(self.__ptr)

    @property
    def tran_cnt(self):
        lib.node().xroad_fix_session_tran_cnt_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_tran_cnt_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_tran_cnt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_tran_cnt.restype = ctypes.c_long
            return lib.node().xroad_fix_session_get_tran_cnt(self.__ptr)
        else:
            return None

    @tran_cnt.setter
    def tran_cnt(self, value):
        if value is not None:
            lib.node().xroad_fix_session_set_tran_cnt.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_fix_session_set_tran_cnt(self.__ptr, value)
        else:
            lib.node().xroad_fix_session_reset_tran_cnt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_tran_cnt(self.__ptr)

    @property
    def expected_seqnum_in(self):
        lib.node().xroad_fix_session_expected_seqnum_in_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_expected_seqnum_in_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_expected_seqnum_in.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_expected_seqnum_in.restype = ctypes.c_long
            return lib.node().xroad_fix_session_get_expected_seqnum_in(self.__ptr)
        else:
            return None

    @expected_seqnum_in.setter
    def expected_seqnum_in(self, value):
        if value is not None:
            lib.node().xroad_fix_session_set_expected_seqnum_in.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_fix_session_set_expected_seqnum_in(self.__ptr, value)
        else:
            lib.node().xroad_fix_session_reset_expected_seqnum_in.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_expected_seqnum_in(self.__ptr)

    @property
    def sent_seqnum_out(self):
        lib.node().xroad_fix_session_sent_seqnum_out_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_sent_seqnum_out_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_sent_seqnum_out.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_sent_seqnum_out.restype = ctypes.c_long
            return lib.node().xroad_fix_session_get_sent_seqnum_out(self.__ptr)
        else:
            return None

    @sent_seqnum_out.setter
    def sent_seqnum_out(self, value):
        if value is not None:
            lib.node().xroad_fix_session_set_sent_seqnum_out.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_fix_session_set_sent_seqnum_out(self.__ptr, value)
        else:
            lib.node().xroad_fix_session_reset_sent_seqnum_out.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_sent_seqnum_out(self.__ptr)

    @property
    def status(self):
        lib.node().xroad_fix_session_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_status_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_status.restype = ctypes.c_int
            return xtypes.FixSessionStatus(lib.node().xroad_fix_session_get_status(self.__ptr))
        else:
            return None

    @status.setter
    def status(self, value):
        if not isinstance(value, xtypes.FixSessionStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be FixSessionStatus enum".format(value))
        if value is not None:
            lib.node().xroad_fix_session_set_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_fix_session_set_status(self.__ptr, value.value)
        else:
            lib.node().xroad_fix_session_reset_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_status(self.__ptr)

    @property
    def order_fix(self):
        lib.node().xroad_fix_session_order_fix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_order_fix_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_order_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_order_fix.restype = ctypes.c_void_p
            obj = lib.node().xroad_fix_session_get_order_fix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order_fix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order_fix.setter
    def order_fix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_fix_session_set_order_fix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_fix_session_set_order_fix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_fix_session_set_order_fix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_fix_session_set_order_fix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_fix_session_reset_order_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_order_fix(self.__ptr)

    @property
    def cancel_fix(self):
        lib.node().xroad_fix_session_cancel_fix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_cancel_fix_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_cancel_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_cancel_fix.restype = ctypes.c_void_p
            obj = lib.node().xroad_fix_session_get_cancel_fix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference cancel_fix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @cancel_fix.setter
    def cancel_fix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_fix_session_set_cancel_fix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_fix_session_set_cancel_fix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_fix_session_set_cancel_fix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_fix_session_set_cancel_fix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_fix_session_reset_cancel_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_cancel_fix(self.__ptr)

    @property
    def replace_fix(self):
        lib.node().xroad_fix_session_replace_fix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_replace_fix_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_replace_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_replace_fix.restype = ctypes.c_void_p
            obj = lib.node().xroad_fix_session_get_replace_fix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference replace_fix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @replace_fix.setter
    def replace_fix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_fix_session_set_replace_fix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_fix_session_set_replace_fix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_fix_session_set_replace_fix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_fix_session_set_replace_fix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_fix_session_reset_replace_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_replace_fix(self.__ptr)

    @property
    def exec_report_fix(self):
        lib.node().xroad_fix_session_exec_report_fix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_exec_report_fix_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_exec_report_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_exec_report_fix.restype = ctypes.c_void_p
            obj = lib.node().xroad_fix_session_get_exec_report_fix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference exec_report_fix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @exec_report_fix.setter
    def exec_report_fix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_fix_session_set_exec_report_fix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_fix_session_set_exec_report_fix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_fix_session_set_exec_report_fix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_fix_session_set_exec_report_fix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_fix_session_reset_exec_report_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_exec_report_fix(self.__ptr)

    @property
    def cancel_reject_fix(self):
        lib.node().xroad_fix_session_cancel_reject_fix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_cancel_reject_fix_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_cancel_reject_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_cancel_reject_fix.restype = ctypes.c_void_p
            obj = lib.node().xroad_fix_session_get_cancel_reject_fix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference cancel_reject_fix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @cancel_reject_fix.setter
    def cancel_reject_fix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_fix_session_set_cancel_reject_fix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_fix_session_set_cancel_reject_fix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_fix_session_set_cancel_reject_fix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_fix_session_set_cancel_reject_fix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_fix_session_reset_cancel_reject_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_cancel_reject_fix(self.__ptr)

    @property
    def reject_fix(self):
        lib.node().xroad_fix_session_reject_fix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_fix_session_reject_fix_is_set(self.__ptr):
            lib.node().xroad_fix_session_get_reject_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_get_reject_fix.restype = ctypes.c_void_p
            obj = lib.node().xroad_fix_session_get_reject_fix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference reject_fix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @reject_fix.setter
    def reject_fix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_fix_session_set_reject_fix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_fix_session_set_reject_fix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_fix_session_set_reject_fix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_fix_session_set_reject_fix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_fix_session_reset_reject_fix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_fix_session_reset_reject_fix(self.__ptr)


class Order(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_order_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_order_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.order

    @property
    def is_valid(self):
        lib.node().xroad_order_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_order_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_order_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_order_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_order_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_order_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_order_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_order_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Order(lib.node().xroad_order_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_order_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_get_id.restype = ctypes.c_long
        return lib.node().xroad_order_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_order_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_order_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_order_copy(self.__ptr, id)
        return Order(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.side
        if v is not None:
            fields["side"] = v.name
        v = self.tif
        if v is not None:
            fields["tif"] = v.name
        v = self.src_node_id
        if v is not None:
            fields["src_node_id"] = v
        v = self.dst_node_id
        if v is not None:
            fields["dst_node_id"] = v
        v = self.ext_ref
        if v is not None:
            fields["ext_ref"] = v
        v = self.status
        if v is not None:
            fields["status"] = v.name
        v = self.sub_status
        if v is not None:
            fields["sub_status"] = v
        v = self.sender
        if v is not None:
            fields["sender"] = v
        v = self.timestamp
        if v is not None:
            fields["timestamp"] = v
        v = self.account
        if v is not None:
            fields["account"] = v
        v = self.client_code
        if v is not None:
            fields["client_code"] = v
        v = self.sales
        if v is not None:
            fields["sales"] = v
        v = self.instr
        if v is not None:
            fields["instr"] = "({0},{1})".format(v.object_type, v.id)
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.leaves_qty
        if v is not None:
            fields["leaves_qty"] = v
        v = self.cum_qty
        if v is not None:
            fields["cum_qty"] = v
        v = self.type
        if v is not None:
            fields["type"] = v.name
        v = self.price
        if v is not None:
            fields["price"] = v
        v = self.exp_date
        if v is not None:
            fields["exp_date"] = v
        v = self.flags
        if v is not None:
            fields["flags"] = v
        v = self.snd_time
        if v is not None:
            fields["snd_time"] = v
        v = self.rcv_time
        if v is not None:
            fields["rcv_time"] = v
        v = self.parent
        if v is not None:
            fields["parent"] = "({0},{1})".format(v.object_type, v.id)
        v = self.child
        if v is not None:
            fields["child"] = "({0},{1})".format(v.object_type, v.id)
        v = self.algo
        if v is not None:
            fields["algo"] = "({0},{1})".format(v.object_type, v.id)
        v = self.hedge_cur
        if v is not None:
            fields["hedge_cur"] = v.name
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "side":
            self.side = xtypes.Side[value] if value is not None else value
        elif field == "tif":
            self.tif = xtypes.Tif[value] if value is not None else value
        elif field == "src_node_id":
            self.src_node_id = int(value) if value is not None else value
        elif field == "dst_node_id":
            self.dst_node_id = int(value) if value is not None else value
        elif field == "ext_ref":
            self.ext_ref = str(value) if value is not None else value
        elif field == "status":
            self.status = xtypes.OrderStatus[value] if value is not None else value
        elif field == "sub_status":
            self.sub_status = int(value) if value is not None else value
        elif field == "sender":
            self.sender = str(value) if value is not None else value
        elif field == "timestamp":
            self.timestamp = int(value) if value is not None else value
        elif field == "account":
            self.account = str(value) if value is not None else value
        elif field == "client_code":
            self.client_code = str(value) if value is not None else value
        elif field == "sales":
            self.sales = str(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "leaves_qty":
            self.leaves_qty = int(value) if value is not None else value
        elif field == "cum_qty":
            self.cum_qty = int(value) if value is not None else value
        elif field == "type":
            self.type = xtypes.OrdType[value] if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "exp_date":
            self.exp_date = int(value) if value is not None else value
        elif field == "flags":
            self.flags = int(value) if value is not None else value
        elif field == "snd_time":
            self.snd_time = int(value) if value is not None else value
        elif field == "rcv_time":
            self.rcv_time = int(value) if value is not None else value
        elif field == "parent":
            if hasattr(value, "ptr"):
                self.parent = value
            else:
                self.parent = str_to_tuple(value)
        elif field == "child":
            if hasattr(value, "ptr"):
                self.child = value
            else:
                self.child = str_to_tuple(value)
        elif field == "algo":
            if hasattr(value, "ptr"):
                self.algo = value
            else:
                self.algo = str_to_tuple(value)
        elif field == "hedge_cur":
            self.hedge_cur = xtypes.Currency[value] if value is not None else value

    @property
    def side(self):
        lib.node().xroad_order_side_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_side_is_set(self.__ptr):
            lib.node().xroad_order_get_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_side.restype = ctypes.c_int
            return xtypes.Side(lib.node().xroad_order_get_side(self.__ptr))
        else:
            return None

    @side.setter
    def side(self, value):
        if not isinstance(value, xtypes.Side) and value is not None:
            raise TypeError("{0} has wrong type. must be Side enum".format(value))
        if value is not None:
            lib.node().xroad_order_set_side.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_set_side(self.__ptr, value.value)
        else:
            lib.node().xroad_order_reset_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_side(self.__ptr)

    @property
    def tif(self):
        lib.node().xroad_order_tif_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_tif_is_set(self.__ptr):
            lib.node().xroad_order_get_tif.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_tif.restype = ctypes.c_int
            return xtypes.Tif(lib.node().xroad_order_get_tif(self.__ptr))
        else:
            return None

    @tif.setter
    def tif(self, value):
        if not isinstance(value, xtypes.Tif) and value is not None:
            raise TypeError("{0} has wrong type. must be Tif enum".format(value))
        if value is not None:
            lib.node().xroad_order_set_tif.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_set_tif(self.__ptr, value.value)
        else:
            lib.node().xroad_order_reset_tif.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_tif(self.__ptr)

    @property
    def src_node_id(self):
        lib.node().xroad_order_src_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_src_node_id_is_set(self.__ptr):
            lib.node().xroad_order_get_src_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_src_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_order_get_src_node_id(self.__ptr)
        else:
            return None

    @src_node_id.setter
    def src_node_id(self, value):
        if value is not None:
            lib.node().xroad_order_set_src_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_order_set_src_node_id(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_src_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_src_node_id(self.__ptr)

    @property
    def dst_node_id(self):
        lib.node().xroad_order_dst_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_dst_node_id_is_set(self.__ptr):
            lib.node().xroad_order_get_dst_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_dst_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_order_get_dst_node_id(self.__ptr)
        else:
            return None

    @dst_node_id.setter
    def dst_node_id(self, value):
        if value is not None:
            lib.node().xroad_order_set_dst_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_order_set_dst_node_id(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_dst_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_dst_node_id(self.__ptr)

    @property
    def ext_ref(self):
        lib.node().xroad_order_ext_ref_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_ext_ref_is_set(self.__ptr):
            lib.node().xroad_order_get_ext_ref.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_ext_ref.restype = ctypes.POINTER(xtypes.ExtRef)
            res = lib.node().xroad_order_get_ext_ref(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @ext_ref.setter
    def ext_ref(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_set_ext_ref.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_set_ext_ref(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_reset_ext_ref.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_ext_ref(self.__ptr)

    @property
    def status(self):
        lib.node().xroad_order_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_status_is_set(self.__ptr):
            lib.node().xroad_order_get_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_status.restype = ctypes.c_int
            return xtypes.OrderStatus(lib.node().xroad_order_get_status(self.__ptr))
        else:
            return None

    @status.setter
    def status(self, value):
        if not isinstance(value, xtypes.OrderStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderStatus enum".format(value))
        if value is not None:
            lib.node().xroad_order_set_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_set_status(self.__ptr, value.value)
        else:
            lib.node().xroad_order_reset_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_status(self.__ptr)

    @property
    def sub_status(self):
        lib.node().xroad_order_sub_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_sub_status_is_set(self.__ptr):
            lib.node().xroad_order_get_sub_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_sub_status.restype = ctypes.c_int
            return lib.node().xroad_order_get_sub_status(self.__ptr)
        else:
            return None

    @sub_status.setter
    def sub_status(self, value):
        if value is not None:
            lib.node().xroad_order_set_sub_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_set_sub_status(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_sub_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_sub_status(self.__ptr)

    @property
    def sender(self):
        lib.node().xroad_order_sender_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_sender_is_set(self.__ptr):
            lib.node().xroad_order_get_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_sender.restype = ctypes.POINTER(xtypes.Sender)
            res = lib.node().xroad_order_get_sender(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sender.setter
    def sender(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_set_sender.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_set_sender(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_reset_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_sender(self.__ptr)

    @property
    def timestamp(self):
        lib.node().xroad_order_timestamp_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_timestamp_is_set(self.__ptr):
            lib.node().xroad_order_get_timestamp.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_timestamp.restype = ctypes.c_ulong
            return lib.node().xroad_order_get_timestamp(self.__ptr)
        else:
            return None

    @timestamp.setter
    def timestamp(self, value):
        if value is not None:
            lib.node().xroad_order_set_timestamp.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_order_set_timestamp(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_timestamp.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_timestamp(self.__ptr)

    @property
    def account(self):
        lib.node().xroad_order_account_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_account_is_set(self.__ptr):
            lib.node().xroad_order_get_account.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_account.restype = ctypes.POINTER(xtypes.Account)
            res = lib.node().xroad_order_get_account(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @account.setter
    def account(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_set_account.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_set_account(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_reset_account.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_account(self.__ptr)

    @property
    def client_code(self):
        lib.node().xroad_order_client_code_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_client_code_is_set(self.__ptr):
            lib.node().xroad_order_get_client_code.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_client_code.restype = ctypes.POINTER(xtypes.ClientCode)
            res = lib.node().xroad_order_get_client_code(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @client_code.setter
    def client_code(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_set_client_code.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_set_client_code(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_reset_client_code.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_client_code(self.__ptr)

    @property
    def sales(self):
        lib.node().xroad_order_sales_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_sales_is_set(self.__ptr):
            lib.node().xroad_order_get_sales.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_sales.restype = ctypes.POINTER(xtypes.Sales)
            res = lib.node().xroad_order_get_sales(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sales.setter
    def sales(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_set_sales.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_set_sales(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_reset_sales.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_sales(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_order_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_instr_is_set(self.__ptr):
            lib.node().xroad_order_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_instr(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_order_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_qty_is_set(self.__ptr):
            lib.node().xroad_order_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_qty.restype = ctypes.c_long
            return lib.node().xroad_order_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_order_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_qty(self.__ptr)

    @property
    def leaves_qty(self):
        lib.node().xroad_order_leaves_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_leaves_qty_is_set(self.__ptr):
            lib.node().xroad_order_get_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_leaves_qty.restype = ctypes.c_long
            return lib.node().xroad_order_get_leaves_qty(self.__ptr)
        else:
            return None

    @leaves_qty.setter
    def leaves_qty(self, value):
        if value is not None:
            lib.node().xroad_order_set_leaves_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_set_leaves_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_leaves_qty(self.__ptr)

    @property
    def cum_qty(self):
        lib.node().xroad_order_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_cum_qty_is_set(self.__ptr):
            lib.node().xroad_order_get_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_order_get_cum_qty(self.__ptr)
        else:
            return None

    @cum_qty.setter
    def cum_qty(self, value):
        if value is not None:
            lib.node().xroad_order_set_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_set_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_cum_qty(self.__ptr)

    @property
    def type(self):
        lib.node().xroad_order_type_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_type_is_set(self.__ptr):
            lib.node().xroad_order_get_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_type.restype = ctypes.c_int
            return xtypes.OrdType(lib.node().xroad_order_get_type(self.__ptr))
        else:
            return None

    @type.setter
    def type(self, value):
        if not isinstance(value, xtypes.OrdType) and value is not None:
            raise TypeError("{0} has wrong type. must be OrdType enum".format(value))
        if value is not None:
            lib.node().xroad_order_set_type.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_set_type(self.__ptr, value.value)
        else:
            lib.node().xroad_order_reset_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_type(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_order_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_price_is_set(self.__ptr):
            lib.node().xroad_order_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_price.restype = ctypes.c_double
            return lib.node().xroad_order_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_order_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_order_set_price(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_price(self.__ptr)

    @property
    def exp_date(self):
        lib.node().xroad_order_exp_date_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_exp_date_is_set(self.__ptr):
            lib.node().xroad_order_get_exp_date.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_exp_date.restype = ctypes.c_ulong
            return lib.node().xroad_order_get_exp_date(self.__ptr)
        else:
            return None

    @exp_date.setter
    def exp_date(self, value):
        if value is not None:
            lib.node().xroad_order_set_exp_date.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_order_set_exp_date(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_exp_date.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_exp_date(self.__ptr)

    @property
    def flags(self):
        lib.node().xroad_order_flags_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_flags_is_set(self.__ptr):
            lib.node().xroad_order_get_flags.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_flags.restype = ctypes.c_int
            return lib.node().xroad_order_get_flags(self.__ptr)
        else:
            return None

    @flags.setter
    def flags(self, value):
        if value is not None:
            lib.node().xroad_order_set_flags.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_set_flags(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_flags.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_flags(self.__ptr)

    @property
    def snd_time(self):
        lib.node().xroad_order_snd_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_snd_time_is_set(self.__ptr):
            lib.node().xroad_order_get_snd_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_snd_time.restype = ctypes.c_ulong
            return lib.node().xroad_order_get_snd_time(self.__ptr)
        else:
            return None

    @snd_time.setter
    def snd_time(self, value):
        if value is not None:
            lib.node().xroad_order_set_snd_time.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_order_set_snd_time(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_snd_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_snd_time(self.__ptr)

    @property
    def rcv_time(self):
        lib.node().xroad_order_rcv_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_rcv_time_is_set(self.__ptr):
            lib.node().xroad_order_get_rcv_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_rcv_time.restype = ctypes.c_ulong
            return lib.node().xroad_order_get_rcv_time(self.__ptr)
        else:
            return None

    @rcv_time.setter
    def rcv_time(self, value):
        if value is not None:
            lib.node().xroad_order_set_rcv_time.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_order_set_rcv_time(self.__ptr, value)
        else:
            lib.node().xroad_order_reset_rcv_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_rcv_time(self.__ptr)

    @property
    def parent(self):
        lib.node().xroad_order_parent_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_parent_is_set(self.__ptr):
            lib.node().xroad_order_get_parent.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_parent.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_get_parent(self.__ptr)
            if not obj:
                raise BrokenRefError("reference parent is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @parent.setter
    def parent(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_set_parent.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_set_parent(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_set_parent_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_set_parent_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_reset_parent.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_parent(self.__ptr)

    @property
    def child(self):
        lib.node().xroad_order_child_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_child_is_set(self.__ptr):
            lib.node().xroad_order_get_child.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_child.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_get_child(self.__ptr)
            if not obj:
                raise BrokenRefError("reference child is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @child.setter
    def child(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_set_child.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_set_child(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_set_child_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_set_child_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_reset_child.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_child(self.__ptr)

    @property
    def algo(self):
        lib.node().xroad_order_algo_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_algo_is_set(self.__ptr):
            lib.node().xroad_order_get_algo.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_algo.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_get_algo(self.__ptr)
            if not obj:
                raise BrokenRefError("reference algo is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @algo.setter
    def algo(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_set_algo.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_set_algo(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_set_algo_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_set_algo_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_reset_algo.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_algo(self.__ptr)

    @property
    def hedge_cur(self):
        lib.node().xroad_order_hedge_cur_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_hedge_cur_is_set(self.__ptr):
            lib.node().xroad_order_get_hedge_cur.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_get_hedge_cur.restype = ctypes.c_int
            return xtypes.Currency(lib.node().xroad_order_get_hedge_cur(self.__ptr))
        else:
            return None

    @hedge_cur.setter
    def hedge_cur(self, value):
        if not isinstance(value, xtypes.Currency) and value is not None:
            raise TypeError("{0} has wrong type. must be Currency enum".format(value))
        if value is not None:
            lib.node().xroad_order_set_hedge_cur.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_set_hedge_cur(self.__ptr, value.value)
        else:
            lib.node().xroad_order_reset_hedge_cur.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_reset_hedge_cur(self.__ptr)


class Pos(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_pos_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_pos_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.pos

    @property
    def is_valid(self):
        lib.node().xroad_pos_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_pos_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_pos_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_pos_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_pos_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_pos_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_pos_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_pos_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_pos_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Pos(lib.node().xroad_pos_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_pos_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_pos_get_id.restype = ctypes.c_long
        return lib.node().xroad_pos_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_pos_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_pos_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_pos_copy(self.__ptr, id)
        return Pos(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.sender
        if v is not None:
            fields["sender"] = v
        v = self.instr
        if v is not None:
            fields["instr"] = "({0},{1})".format(v.object_type, v.id)
        v = self.last_trd_capt_id
        if v is not None:
            fields["last_trd_capt_id"] = v
        v = self.first_import_trd_capt
        if v is not None:
            fields["first_import_trd_capt"] = "({0},{1})".format(v.object_type, v.id)
        v = self.book
        if v is not None:
            fields["book"] = v
        v = self.desk
        if v is not None:
            fields["desk"] = v
        v = self.total_buy
        if v is not None:
            fields["total_buy"] = v
        v = self.total_sell
        if v is not None:
            fields["total_sell"] = v
        v = self.avg_price
        if v is not None:
            fields["avg_price"] = v
        v = self.last_price
        if v is not None:
            fields["last_price"] = v
        v = self.total_pnl
        if v is not None:
            fields["total_pnl"] = v
        v = self.realize_pnl
        if v is not None:
            fields["realize_pnl"] = v
        v = self.unrealize_pnl
        if v is not None:
            fields["unrealize_pnl"] = v
        v = self.cost
        if v is not None:
            fields["cost"] = v
        v = self.exch_fee
        if v is not None:
            fields["exch_fee"] = v
        v = self.pos_sum
        if v is not None:
            fields["pos_sum"] = "({0},{1})".format(v.object_type, v.id)
        v = self.nkd
        if v is not None:
            fields["nkd"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "sender":
            self.sender = str(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)
        elif field == "last_trd_capt_id":
            self.last_trd_capt_id = int(value) if value is not None else value
        elif field == "first_import_trd_capt":
            if hasattr(value, "ptr"):
                self.first_import_trd_capt = value
            else:
                self.first_import_trd_capt = str_to_tuple(value)
        elif field == "book":
            self.book = str(value) if value is not None else value
        elif field == "desk":
            self.desk = str(value) if value is not None else value
        elif field == "total_buy":
            self.total_buy = int(value) if value is not None else value
        elif field == "total_sell":
            self.total_sell = int(value) if value is not None else value
        elif field == "avg_price":
            self.avg_price = float(value) if value is not None else value
        elif field == "last_price":
            self.last_price = float(value) if value is not None else value
        elif field == "total_pnl":
            self.total_pnl = float(value) if value is not None else value
        elif field == "realize_pnl":
            self.realize_pnl = float(value) if value is not None else value
        elif field == "unrealize_pnl":
            self.unrealize_pnl = float(value) if value is not None else value
        elif field == "cost":
            self.cost = float(value) if value is not None else value
        elif field == "exch_fee":
            self.exch_fee = float(value) if value is not None else value
        elif field == "pos_sum":
            if hasattr(value, "ptr"):
                self.pos_sum = value
            else:
                self.pos_sum = str_to_tuple(value)
        elif field == "nkd":
            self.nkd = float(value) if value is not None else value

    @property
    def sender(self):
        lib.node().xroad_pos_sender_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_sender_is_set(self.__ptr):
            lib.node().xroad_pos_get_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_sender.restype = ctypes.POINTER(xtypes.Sender)
            res = lib.node().xroad_pos_get_sender(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sender.setter
    def sender(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_pos_set_sender.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_pos_set_sender(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_pos_reset_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_sender(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_pos_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_instr_is_set(self.__ptr):
            lib.node().xroad_pos_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_pos_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_pos_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_pos_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_pos_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_pos_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_pos_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_instr(self.__ptr)

    @property
    def last_trd_capt_id(self):
        lib.node().xroad_pos_last_trd_capt_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_last_trd_capt_id_is_set(self.__ptr):
            lib.node().xroad_pos_get_last_trd_capt_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_last_trd_capt_id.restype = ctypes.c_int
            return lib.node().xroad_pos_get_last_trd_capt_id(self.__ptr)
        else:
            return None

    @last_trd_capt_id.setter
    def last_trd_capt_id(self, value):
        if value is not None:
            lib.node().xroad_pos_set_last_trd_capt_id.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_pos_set_last_trd_capt_id(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_last_trd_capt_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_last_trd_capt_id(self.__ptr)

    @property
    def first_import_trd_capt(self):
        lib.node().xroad_pos_first_import_trd_capt_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_first_import_trd_capt_is_set(self.__ptr):
            lib.node().xroad_pos_get_first_import_trd_capt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_first_import_trd_capt.restype = ctypes.c_void_p
            obj = lib.node().xroad_pos_get_first_import_trd_capt(self.__ptr)
            if not obj:
                raise BrokenRefError("reference first_import_trd_capt is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @first_import_trd_capt.setter
    def first_import_trd_capt(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_pos_set_first_import_trd_capt.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_pos_set_first_import_trd_capt(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_pos_set_first_import_trd_capt_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_pos_set_first_import_trd_capt_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_pos_reset_first_import_trd_capt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_first_import_trd_capt(self.__ptr)

    @property
    def book(self):
        lib.node().xroad_pos_book_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_book_is_set(self.__ptr):
            lib.node().xroad_pos_get_book.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_book.restype = ctypes.POINTER(xtypes.Book)
            res = lib.node().xroad_pos_get_book(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @book.setter
    def book(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_pos_set_book.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_pos_set_book(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_pos_reset_book.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_book(self.__ptr)

    @property
    def desk(self):
        lib.node().xroad_pos_desk_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_desk_is_set(self.__ptr):
            lib.node().xroad_pos_get_desk.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_desk.restype = ctypes.POINTER(xtypes.Desk)
            res = lib.node().xroad_pos_get_desk(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @desk.setter
    def desk(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_pos_set_desk.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_pos_set_desk(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_pos_reset_desk.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_desk(self.__ptr)

    @property
    def total_buy(self):
        lib.node().xroad_pos_total_buy_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_total_buy_is_set(self.__ptr):
            lib.node().xroad_pos_get_total_buy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_total_buy.restype = ctypes.c_long
            return lib.node().xroad_pos_get_total_buy(self.__ptr)
        else:
            return None

    @total_buy.setter
    def total_buy(self, value):
        if value is not None:
            lib.node().xroad_pos_set_total_buy.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_pos_set_total_buy(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_total_buy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_total_buy(self.__ptr)

    @property
    def total_sell(self):
        lib.node().xroad_pos_total_sell_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_total_sell_is_set(self.__ptr):
            lib.node().xroad_pos_get_total_sell.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_total_sell.restype = ctypes.c_long
            return lib.node().xroad_pos_get_total_sell(self.__ptr)
        else:
            return None

    @total_sell.setter
    def total_sell(self, value):
        if value is not None:
            lib.node().xroad_pos_set_total_sell.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_pos_set_total_sell(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_total_sell.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_total_sell(self.__ptr)

    @property
    def avg_price(self):
        lib.node().xroad_pos_avg_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_avg_price_is_set(self.__ptr):
            lib.node().xroad_pos_get_avg_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_avg_price.restype = ctypes.c_double
            return lib.node().xroad_pos_get_avg_price(self.__ptr)
        else:
            return None

    @avg_price.setter
    def avg_price(self, value):
        if value is not None:
            lib.node().xroad_pos_set_avg_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_set_avg_price(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_avg_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_avg_price(self.__ptr)

    @property
    def last_price(self):
        lib.node().xroad_pos_last_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_last_price_is_set(self.__ptr):
            lib.node().xroad_pos_get_last_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_last_price.restype = ctypes.c_double
            return lib.node().xroad_pos_get_last_price(self.__ptr)
        else:
            return None

    @last_price.setter
    def last_price(self, value):
        if value is not None:
            lib.node().xroad_pos_set_last_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_set_last_price(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_last_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_last_price(self.__ptr)

    @property
    def total_pnl(self):
        lib.node().xroad_pos_total_pnl_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_total_pnl_is_set(self.__ptr):
            lib.node().xroad_pos_get_total_pnl.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_total_pnl.restype = ctypes.c_double
            return lib.node().xroad_pos_get_total_pnl(self.__ptr)
        else:
            return None

    @total_pnl.setter
    def total_pnl(self, value):
        if value is not None:
            lib.node().xroad_pos_set_total_pnl.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_set_total_pnl(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_total_pnl.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_total_pnl(self.__ptr)

    @property
    def realize_pnl(self):
        lib.node().xroad_pos_realize_pnl_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_realize_pnl_is_set(self.__ptr):
            lib.node().xroad_pos_get_realize_pnl.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_realize_pnl.restype = ctypes.c_double
            return lib.node().xroad_pos_get_realize_pnl(self.__ptr)
        else:
            return None

    @realize_pnl.setter
    def realize_pnl(self, value):
        if value is not None:
            lib.node().xroad_pos_set_realize_pnl.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_set_realize_pnl(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_realize_pnl.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_realize_pnl(self.__ptr)

    @property
    def unrealize_pnl(self):
        lib.node().xroad_pos_unrealize_pnl_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_unrealize_pnl_is_set(self.__ptr):
            lib.node().xroad_pos_get_unrealize_pnl.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_unrealize_pnl.restype = ctypes.c_double
            return lib.node().xroad_pos_get_unrealize_pnl(self.__ptr)
        else:
            return None

    @unrealize_pnl.setter
    def unrealize_pnl(self, value):
        if value is not None:
            lib.node().xroad_pos_set_unrealize_pnl.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_set_unrealize_pnl(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_unrealize_pnl.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_unrealize_pnl(self.__ptr)

    @property
    def cost(self):
        lib.node().xroad_pos_cost_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_cost_is_set(self.__ptr):
            lib.node().xroad_pos_get_cost.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_cost.restype = ctypes.c_double
            return lib.node().xroad_pos_get_cost(self.__ptr)
        else:
            return None

    @cost.setter
    def cost(self, value):
        if value is not None:
            lib.node().xroad_pos_set_cost.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_set_cost(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_cost.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_cost(self.__ptr)

    @property
    def exch_fee(self):
        lib.node().xroad_pos_exch_fee_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_exch_fee_is_set(self.__ptr):
            lib.node().xroad_pos_get_exch_fee.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_exch_fee.restype = ctypes.c_double
            return lib.node().xroad_pos_get_exch_fee(self.__ptr)
        else:
            return None

    @exch_fee.setter
    def exch_fee(self, value):
        if value is not None:
            lib.node().xroad_pos_set_exch_fee.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_set_exch_fee(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_exch_fee.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_exch_fee(self.__ptr)

    @property
    def pos_sum(self):
        lib.node().xroad_pos_pos_sum_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_pos_sum_is_set(self.__ptr):
            lib.node().xroad_pos_get_pos_sum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_pos_sum.restype = ctypes.c_void_p
            obj = lib.node().xroad_pos_get_pos_sum(self.__ptr)
            if not obj:
                raise BrokenRefError("reference pos_sum is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @pos_sum.setter
    def pos_sum(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_pos_set_pos_sum.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_pos_set_pos_sum(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_pos_set_pos_sum_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_pos_set_pos_sum_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_pos_reset_pos_sum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_pos_sum(self.__ptr)

    @property
    def nkd(self):
        lib.node().xroad_pos_nkd_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_nkd_is_set(self.__ptr):
            lib.node().xroad_pos_get_nkd.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_get_nkd.restype = ctypes.c_double
            return lib.node().xroad_pos_get_nkd(self.__ptr)
        else:
            return None

    @nkd.setter
    def nkd(self, value):
        if value is not None:
            lib.node().xroad_pos_set_nkd.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_set_nkd(self.__ptr, value)
        else:
            lib.node().xroad_pos_reset_nkd.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_reset_nkd(self.__ptr)


class OrderStat(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_order_stat_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_order_stat_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.order_stat

    @property
    def is_valid(self):
        lib.node().xroad_order_stat_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_order_stat_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_order_stat_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_order_stat_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_order_stat_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_order_stat_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_order_stat_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_order_stat_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_stat_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return OrderStat(lib.node().xroad_order_stat_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_order_stat_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_stat_get_id.restype = ctypes.c_long
        return lib.node().xroad_order_stat_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_order_stat_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_order_stat_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_order_stat_copy(self.__ptr, id)
        return OrderStat(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.sender
        if v is not None:
            fields["sender"] = v
        v = self.order_cnt
        if v is not None:
            fields["order_cnt"] = v
        v = self.active_order_cnt
        if v is not None:
            fields["active_order_cnt"] = v
        v = self.lat_min
        if v is not None:
            fields["lat_min"] = v
        v = self.lat_max
        if v is not None:
            fields["lat_max"] = v
        v = self.lat_50
        if v is not None:
            fields["lat_50"] = v
        v = self.lat_75
        if v is not None:
            fields["lat_75"] = v
        v = self.lat_99
        if v is not None:
            fields["lat_99"] = v
        v = self.lat_9999
        if v is not None:
            fields["lat_9999"] = v
        v = self.rtp_min
        if v is not None:
            fields["rtp_min"] = v
        v = self.rtp_max
        if v is not None:
            fields["rtp_max"] = v
        v = self.rtp_50
        if v is not None:
            fields["rtp_50"] = v
        v = self.rtp_75
        if v is not None:
            fields["rtp_75"] = v
        v = self.rtp_99
        if v is not None:
            fields["rtp_99"] = v
        v = self.rtp_9999
        if v is not None:
            fields["rtp_9999"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "sender":
            self.sender = str(value) if value is not None else value
        elif field == "order_cnt":
            self.order_cnt = int(value) if value is not None else value
        elif field == "active_order_cnt":
            self.active_order_cnt = int(value) if value is not None else value
        elif field == "lat_min":
            self.lat_min = int(value) if value is not None else value
        elif field == "lat_max":
            self.lat_max = int(value) if value is not None else value
        elif field == "lat_50":
            self.lat_50 = int(value) if value is not None else value
        elif field == "lat_75":
            self.lat_75 = int(value) if value is not None else value
        elif field == "lat_99":
            self.lat_99 = int(value) if value is not None else value
        elif field == "lat_9999":
            self.lat_9999 = int(value) if value is not None else value
        elif field == "rtp_min":
            self.rtp_min = int(value) if value is not None else value
        elif field == "rtp_max":
            self.rtp_max = int(value) if value is not None else value
        elif field == "rtp_50":
            self.rtp_50 = int(value) if value is not None else value
        elif field == "rtp_75":
            self.rtp_75 = int(value) if value is not None else value
        elif field == "rtp_99":
            self.rtp_99 = int(value) if value is not None else value
        elif field == "rtp_9999":
            self.rtp_9999 = int(value) if value is not None else value

    @property
    def sender(self):
        lib.node().xroad_order_stat_sender_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_sender_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_sender.restype = ctypes.POINTER(xtypes.Sender)
            res = lib.node().xroad_order_stat_get_sender(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sender.setter
    def sender(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_stat_set_sender.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_stat_set_sender(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_stat_reset_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_sender(self.__ptr)

    @property
    def order_cnt(self):
        lib.node().xroad_order_stat_order_cnt_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_order_cnt_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_order_cnt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_order_cnt.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_order_cnt(self.__ptr)
        else:
            return None

    @order_cnt.setter
    def order_cnt(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_order_cnt.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_order_cnt(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_order_cnt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_order_cnt(self.__ptr)

    @property
    def active_order_cnt(self):
        lib.node().xroad_order_stat_active_order_cnt_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_active_order_cnt_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_active_order_cnt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_active_order_cnt.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_active_order_cnt(self.__ptr)
        else:
            return None

    @active_order_cnt.setter
    def active_order_cnt(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_active_order_cnt.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_active_order_cnt(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_active_order_cnt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_active_order_cnt(self.__ptr)

    @property
    def lat_min(self):
        lib.node().xroad_order_stat_lat_min_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_lat_min_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_lat_min.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_lat_min.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_lat_min(self.__ptr)
        else:
            return None

    @lat_min.setter
    def lat_min(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_lat_min.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_lat_min(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_lat_min.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_lat_min(self.__ptr)

    @property
    def lat_max(self):
        lib.node().xroad_order_stat_lat_max_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_lat_max_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_lat_max.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_lat_max.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_lat_max(self.__ptr)
        else:
            return None

    @lat_max.setter
    def lat_max(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_lat_max.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_lat_max(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_lat_max.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_lat_max(self.__ptr)

    @property
    def lat_50(self):
        lib.node().xroad_order_stat_lat_50_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_lat_50_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_lat_50.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_lat_50.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_lat_50(self.__ptr)
        else:
            return None

    @lat_50.setter
    def lat_50(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_lat_50.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_lat_50(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_lat_50.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_lat_50(self.__ptr)

    @property
    def lat_75(self):
        lib.node().xroad_order_stat_lat_75_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_lat_75_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_lat_75.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_lat_75.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_lat_75(self.__ptr)
        else:
            return None

    @lat_75.setter
    def lat_75(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_lat_75.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_lat_75(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_lat_75.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_lat_75(self.__ptr)

    @property
    def lat_99(self):
        lib.node().xroad_order_stat_lat_99_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_lat_99_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_lat_99.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_lat_99.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_lat_99(self.__ptr)
        else:
            return None

    @lat_99.setter
    def lat_99(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_lat_99.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_lat_99(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_lat_99.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_lat_99(self.__ptr)

    @property
    def lat_9999(self):
        lib.node().xroad_order_stat_lat_9999_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_lat_9999_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_lat_9999.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_lat_9999.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_lat_9999(self.__ptr)
        else:
            return None

    @lat_9999.setter
    def lat_9999(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_lat_9999.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_lat_9999(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_lat_9999.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_lat_9999(self.__ptr)

    @property
    def rtp_min(self):
        lib.node().xroad_order_stat_rtp_min_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_rtp_min_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_rtp_min.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_rtp_min.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_rtp_min(self.__ptr)
        else:
            return None

    @rtp_min.setter
    def rtp_min(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_rtp_min.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_rtp_min(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_rtp_min.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_rtp_min(self.__ptr)

    @property
    def rtp_max(self):
        lib.node().xroad_order_stat_rtp_max_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_rtp_max_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_rtp_max.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_rtp_max.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_rtp_max(self.__ptr)
        else:
            return None

    @rtp_max.setter
    def rtp_max(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_rtp_max.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_rtp_max(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_rtp_max.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_rtp_max(self.__ptr)

    @property
    def rtp_50(self):
        lib.node().xroad_order_stat_rtp_50_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_rtp_50_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_rtp_50.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_rtp_50.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_rtp_50(self.__ptr)
        else:
            return None

    @rtp_50.setter
    def rtp_50(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_rtp_50.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_rtp_50(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_rtp_50.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_rtp_50(self.__ptr)

    @property
    def rtp_75(self):
        lib.node().xroad_order_stat_rtp_75_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_rtp_75_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_rtp_75.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_rtp_75.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_rtp_75(self.__ptr)
        else:
            return None

    @rtp_75.setter
    def rtp_75(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_rtp_75.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_rtp_75(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_rtp_75.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_rtp_75(self.__ptr)

    @property
    def rtp_99(self):
        lib.node().xroad_order_stat_rtp_99_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_rtp_99_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_rtp_99.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_rtp_99.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_rtp_99(self.__ptr)
        else:
            return None

    @rtp_99.setter
    def rtp_99(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_rtp_99.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_rtp_99(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_rtp_99.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_rtp_99(self.__ptr)

    @property
    def rtp_9999(self):
        lib.node().xroad_order_stat_rtp_9999_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_stat_rtp_9999_is_set(self.__ptr):
            lib.node().xroad_order_stat_get_rtp_9999.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_get_rtp_9999.restype = ctypes.c_int
            return lib.node().xroad_order_stat_get_rtp_9999(self.__ptr)
        else:
            return None

    @rtp_9999.setter
    def rtp_9999(self, value):
        if value is not None:
            lib.node().xroad_order_stat_set_rtp_9999.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_stat_set_rtp_9999(self.__ptr, value)
        else:
            lib.node().xroad_order_stat_reset_rtp_9999.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_stat_reset_rtp_9999(self.__ptr)


class Iceberg(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_iceberg_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_iceberg_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.iceberg

    @property
    def is_valid(self):
        lib.node().xroad_iceberg_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_iceberg_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_iceberg_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_iceberg_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_iceberg_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_iceberg_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_iceberg_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_iceberg_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_iceberg_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Iceberg(lib.node().xroad_iceberg_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_iceberg_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_iceberg_get_id.restype = ctypes.c_long
        return lib.node().xroad_iceberg_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_iceberg_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_iceberg_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_iceberg_copy(self.__ptr, id)
        return Iceberg(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.display_qty
        if v is not None:
            fields["display_qty"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "display_qty":
            self.display_qty = int(value) if value is not None else value

    @property
    def display_qty(self):
        lib.node().xroad_iceberg_display_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_iceberg_display_qty_is_set(self.__ptr):
            lib.node().xroad_iceberg_get_display_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_iceberg_get_display_qty.restype = ctypes.c_long
            return lib.node().xroad_iceberg_get_display_qty(self.__ptr)
        else:
            return None

    @display_qty.setter
    def display_qty(self, value):
        if value is not None:
            lib.node().xroad_iceberg_set_display_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_iceberg_set_display_qty(self.__ptr, value)
        else:
            lib.node().xroad_iceberg_reset_display_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_iceberg_reset_display_qty(self.__ptr)


class Twap(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_twap_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_twap_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.twap

    @property
    def is_valid(self):
        lib.node().xroad_twap_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_twap_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_twap_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_twap_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_twap_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_twap_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_twap_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_twap_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_twap_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Twap(lib.node().xroad_twap_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_twap_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_twap_get_id.restype = ctypes.c_long
        return lib.node().xroad_twap_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_twap_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_twap_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_twap_copy(self.__ptr, id)
        return Twap(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.start
        if v is not None:
            fields["start"] = v
        v = self.stop
        if v is not None:
            fields["stop"] = v
        v = self.agression_level
        if v is not None:
            fields["agression_level"] = v
        v = self.mid_time
        if v is not None:
            fields["mid_time"] = v
        v = self.agression_time
        if v is not None:
            fields["agression_time"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "start":
            self.start = int(value) if value is not None else value
        elif field == "stop":
            self.stop = int(value) if value is not None else value
        elif field == "agression_level":
            self.agression_level = int(value) if value is not None else value
        elif field == "mid_time":
            self.mid_time = int(value) if value is not None else value
        elif field == "agression_time":
            self.agression_time = int(value) if value is not None else value

    @property
    def start(self):
        lib.node().xroad_twap_start_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_twap_start_is_set(self.__ptr):
            lib.node().xroad_twap_get_start.argtypes = [ctypes.c_void_p]
            lib.node().xroad_twap_get_start.restype = ctypes.c_int
            return lib.node().xroad_twap_get_start(self.__ptr)
        else:
            return None

    @start.setter
    def start(self, value):
        if value is not None:
            lib.node().xroad_twap_set_start.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_twap_set_start(self.__ptr, value)
        else:
            lib.node().xroad_twap_reset_start.argtypes = [ctypes.c_void_p]
            lib.node().xroad_twap_reset_start(self.__ptr)

    @property
    def stop(self):
        lib.node().xroad_twap_stop_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_twap_stop_is_set(self.__ptr):
            lib.node().xroad_twap_get_stop.argtypes = [ctypes.c_void_p]
            lib.node().xroad_twap_get_stop.restype = ctypes.c_int
            return lib.node().xroad_twap_get_stop(self.__ptr)
        else:
            return None

    @stop.setter
    def stop(self, value):
        if value is not None:
            lib.node().xroad_twap_set_stop.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_twap_set_stop(self.__ptr, value)
        else:
            lib.node().xroad_twap_reset_stop.argtypes = [ctypes.c_void_p]
            lib.node().xroad_twap_reset_stop(self.__ptr)

    @property
    def agression_level(self):
        lib.node().xroad_twap_agression_level_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_twap_agression_level_is_set(self.__ptr):
            lib.node().xroad_twap_get_agression_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_twap_get_agression_level.restype = ctypes.c_int
            return lib.node().xroad_twap_get_agression_level(self.__ptr)
        else:
            return None

    @agression_level.setter
    def agression_level(self, value):
        if value is not None:
            lib.node().xroad_twap_set_agression_level.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_twap_set_agression_level(self.__ptr, value)
        else:
            lib.node().xroad_twap_reset_agression_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_twap_reset_agression_level(self.__ptr)

    @property
    def mid_time(self):
        lib.node().xroad_twap_mid_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_twap_mid_time_is_set(self.__ptr):
            lib.node().xroad_twap_get_mid_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_twap_get_mid_time.restype = ctypes.c_int
            return lib.node().xroad_twap_get_mid_time(self.__ptr)
        else:
            return None

    @mid_time.setter
    def mid_time(self, value):
        if value is not None:
            lib.node().xroad_twap_set_mid_time.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_twap_set_mid_time(self.__ptr, value)
        else:
            lib.node().xroad_twap_reset_mid_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_twap_reset_mid_time(self.__ptr)

    @property
    def agression_time(self):
        lib.node().xroad_twap_agression_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_twap_agression_time_is_set(self.__ptr):
            lib.node().xroad_twap_get_agression_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_twap_get_agression_time.restype = ctypes.c_int
            return lib.node().xroad_twap_get_agression_time(self.__ptr)
        else:
            return None

    @agression_time.setter
    def agression_time(self, value):
        if value is not None:
            lib.node().xroad_twap_set_agression_time.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_twap_set_agression_time(self.__ptr, value)
        else:
            lib.node().xroad_twap_reset_agression_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_twap_reset_agression_time(self.__ptr)


class Pov(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_pov_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_pov_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.pov

    @property
    def is_valid(self):
        lib.node().xroad_pov_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_pov_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_pov_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_pov_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_pov_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_pov_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_pov_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_pov_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_pov_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Pov(lib.node().xroad_pov_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_pov_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_pov_get_id.restype = ctypes.c_long
        return lib.node().xroad_pov_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_pov_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_pov_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_pov_copy(self.__ptr, id)
        return Pov(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.start
        if v is not None:
            fields["start"] = v
        v = self.stop
        if v is not None:
            fields["stop"] = v
        v = self.agression_level
        if v is not None:
            fields["agression_level"] = v
        v = self.mid_time
        if v is not None:
            fields["mid_time"] = v
        v = self.agression_time
        if v is not None:
            fields["agression_time"] = v
        v = self.period
        if v is not None:
            fields["period"] = v
        v = self.rate
        if v is not None:
            fields["rate"] = v
        v = self.display_qty
        if v is not None:
            fields["display_qty"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "start":
            self.start = int(value) if value is not None else value
        elif field == "stop":
            self.stop = int(value) if value is not None else value
        elif field == "agression_level":
            self.agression_level = int(value) if value is not None else value
        elif field == "mid_time":
            self.mid_time = int(value) if value is not None else value
        elif field == "agression_time":
            self.agression_time = int(value) if value is not None else value
        elif field == "period":
            self.period = int(value) if value is not None else value
        elif field == "rate":
            self.rate = float(value) if value is not None else value
        elif field == "display_qty":
            self.display_qty = int(value) if value is not None else value

    @property
    def start(self):
        lib.node().xroad_pov_start_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pov_start_is_set(self.__ptr):
            lib.node().xroad_pov_get_start.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_get_start.restype = ctypes.c_int
            return lib.node().xroad_pov_get_start(self.__ptr)
        else:
            return None

    @start.setter
    def start(self, value):
        if value is not None:
            lib.node().xroad_pov_set_start.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_pov_set_start(self.__ptr, value)
        else:
            lib.node().xroad_pov_reset_start.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_reset_start(self.__ptr)

    @property
    def stop(self):
        lib.node().xroad_pov_stop_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pov_stop_is_set(self.__ptr):
            lib.node().xroad_pov_get_stop.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_get_stop.restype = ctypes.c_int
            return lib.node().xroad_pov_get_stop(self.__ptr)
        else:
            return None

    @stop.setter
    def stop(self, value):
        if value is not None:
            lib.node().xroad_pov_set_stop.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_pov_set_stop(self.__ptr, value)
        else:
            lib.node().xroad_pov_reset_stop.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_reset_stop(self.__ptr)

    @property
    def agression_level(self):
        lib.node().xroad_pov_agression_level_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pov_agression_level_is_set(self.__ptr):
            lib.node().xroad_pov_get_agression_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_get_agression_level.restype = ctypes.c_int
            return lib.node().xroad_pov_get_agression_level(self.__ptr)
        else:
            return None

    @agression_level.setter
    def agression_level(self, value):
        if value is not None:
            lib.node().xroad_pov_set_agression_level.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_pov_set_agression_level(self.__ptr, value)
        else:
            lib.node().xroad_pov_reset_agression_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_reset_agression_level(self.__ptr)

    @property
    def mid_time(self):
        lib.node().xroad_pov_mid_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pov_mid_time_is_set(self.__ptr):
            lib.node().xroad_pov_get_mid_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_get_mid_time.restype = ctypes.c_int
            return lib.node().xroad_pov_get_mid_time(self.__ptr)
        else:
            return None

    @mid_time.setter
    def mid_time(self, value):
        if value is not None:
            lib.node().xroad_pov_set_mid_time.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_pov_set_mid_time(self.__ptr, value)
        else:
            lib.node().xroad_pov_reset_mid_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_reset_mid_time(self.__ptr)

    @property
    def agression_time(self):
        lib.node().xroad_pov_agression_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pov_agression_time_is_set(self.__ptr):
            lib.node().xroad_pov_get_agression_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_get_agression_time.restype = ctypes.c_int
            return lib.node().xroad_pov_get_agression_time(self.__ptr)
        else:
            return None

    @agression_time.setter
    def agression_time(self, value):
        if value is not None:
            lib.node().xroad_pov_set_agression_time.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_pov_set_agression_time(self.__ptr, value)
        else:
            lib.node().xroad_pov_reset_agression_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_reset_agression_time(self.__ptr)

    @property
    def period(self):
        lib.node().xroad_pov_period_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pov_period_is_set(self.__ptr):
            lib.node().xroad_pov_get_period.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_get_period.restype = ctypes.c_int
            return lib.node().xroad_pov_get_period(self.__ptr)
        else:
            return None

    @period.setter
    def period(self, value):
        if value is not None:
            lib.node().xroad_pov_set_period.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_pov_set_period(self.__ptr, value)
        else:
            lib.node().xroad_pov_reset_period.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_reset_period(self.__ptr)

    @property
    def rate(self):
        lib.node().xroad_pov_rate_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pov_rate_is_set(self.__ptr):
            lib.node().xroad_pov_get_rate.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_get_rate.restype = ctypes.c_double
            return lib.node().xroad_pov_get_rate(self.__ptr)
        else:
            return None

    @rate.setter
    def rate(self, value):
        if value is not None:
            lib.node().xroad_pov_set_rate.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pov_set_rate(self.__ptr, value)
        else:
            lib.node().xroad_pov_reset_rate.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_reset_rate(self.__ptr)

    @property
    def display_qty(self):
        lib.node().xroad_pov_display_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pov_display_qty_is_set(self.__ptr):
            lib.node().xroad_pov_get_display_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_get_display_qty.restype = ctypes.c_long
            return lib.node().xroad_pov_get_display_qty(self.__ptr)
        else:
            return None

    @display_qty.setter
    def display_qty(self, value):
        if value is not None:
            lib.node().xroad_pov_set_display_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_pov_set_display_qty(self.__ptr, value)
        else:
            lib.node().xroad_pov_reset_display_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pov_reset_display_qty(self.__ptr)


class Vwap(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_vwap_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_vwap_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.vwap

    @property
    def is_valid(self):
        lib.node().xroad_vwap_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_vwap_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_vwap_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_vwap_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_vwap_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_vwap_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_vwap_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_vwap_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_vwap_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Vwap(lib.node().xroad_vwap_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_vwap_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_vwap_get_id.restype = ctypes.c_long
        return lib.node().xroad_vwap_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_vwap_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_vwap_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_vwap_copy(self.__ptr, id)
        return Vwap(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.start
        if v is not None:
            fields["start"] = v
        v = self.stop
        if v is not None:
            fields["stop"] = v
        v = self.agression_level
        if v is not None:
            fields["agression_level"] = v
        v = self.mid_time
        if v is not None:
            fields["mid_time"] = v
        v = self.agression_time
        if v is not None:
            fields["agression_time"] = v
        v = self.price_move
        if v is not None:
            fields["price_move"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "start":
            self.start = int(value) if value is not None else value
        elif field == "stop":
            self.stop = int(value) if value is not None else value
        elif field == "agression_level":
            self.agression_level = int(value) if value is not None else value
        elif field == "mid_time":
            self.mid_time = int(value) if value is not None else value
        elif field == "agression_time":
            self.agression_time = int(value) if value is not None else value
        elif field == "price_move":
            self.price_move = float(value) if value is not None else value

    @property
    def start(self):
        lib.node().xroad_vwap_start_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_vwap_start_is_set(self.__ptr):
            lib.node().xroad_vwap_get_start.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_get_start.restype = ctypes.c_int
            return lib.node().xroad_vwap_get_start(self.__ptr)
        else:
            return None

    @start.setter
    def start(self, value):
        if value is not None:
            lib.node().xroad_vwap_set_start.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_vwap_set_start(self.__ptr, value)
        else:
            lib.node().xroad_vwap_reset_start.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_reset_start(self.__ptr)

    @property
    def stop(self):
        lib.node().xroad_vwap_stop_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_vwap_stop_is_set(self.__ptr):
            lib.node().xroad_vwap_get_stop.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_get_stop.restype = ctypes.c_int
            return lib.node().xroad_vwap_get_stop(self.__ptr)
        else:
            return None

    @stop.setter
    def stop(self, value):
        if value is not None:
            lib.node().xroad_vwap_set_stop.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_vwap_set_stop(self.__ptr, value)
        else:
            lib.node().xroad_vwap_reset_stop.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_reset_stop(self.__ptr)

    @property
    def agression_level(self):
        lib.node().xroad_vwap_agression_level_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_vwap_agression_level_is_set(self.__ptr):
            lib.node().xroad_vwap_get_agression_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_get_agression_level.restype = ctypes.c_int
            return lib.node().xroad_vwap_get_agression_level(self.__ptr)
        else:
            return None

    @agression_level.setter
    def agression_level(self, value):
        if value is not None:
            lib.node().xroad_vwap_set_agression_level.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_vwap_set_agression_level(self.__ptr, value)
        else:
            lib.node().xroad_vwap_reset_agression_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_reset_agression_level(self.__ptr)

    @property
    def mid_time(self):
        lib.node().xroad_vwap_mid_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_vwap_mid_time_is_set(self.__ptr):
            lib.node().xroad_vwap_get_mid_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_get_mid_time.restype = ctypes.c_int
            return lib.node().xroad_vwap_get_mid_time(self.__ptr)
        else:
            return None

    @mid_time.setter
    def mid_time(self, value):
        if value is not None:
            lib.node().xroad_vwap_set_mid_time.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_vwap_set_mid_time(self.__ptr, value)
        else:
            lib.node().xroad_vwap_reset_mid_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_reset_mid_time(self.__ptr)

    @property
    def agression_time(self):
        lib.node().xroad_vwap_agression_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_vwap_agression_time_is_set(self.__ptr):
            lib.node().xroad_vwap_get_agression_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_get_agression_time.restype = ctypes.c_int
            return lib.node().xroad_vwap_get_agression_time(self.__ptr)
        else:
            return None

    @agression_time.setter
    def agression_time(self, value):
        if value is not None:
            lib.node().xroad_vwap_set_agression_time.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_vwap_set_agression_time(self.__ptr, value)
        else:
            lib.node().xroad_vwap_reset_agression_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_reset_agression_time(self.__ptr)

    @property
    def price_move(self):
        lib.node().xroad_vwap_price_move_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_vwap_price_move_is_set(self.__ptr):
            lib.node().xroad_vwap_get_price_move.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_get_price_move.restype = ctypes.c_double
            return lib.node().xroad_vwap_get_price_move(self.__ptr)
        else:
            return None

    @price_move.setter
    def price_move(self, value):
        if value is not None:
            lib.node().xroad_vwap_set_price_move.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_vwap_set_price_move(self.__ptr, value)
        else:
            lib.node().xroad_vwap_reset_price_move.argtypes = [ctypes.c_void_p]
            lib.node().xroad_vwap_reset_price_move(self.__ptr)


class Instr(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_instr_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_instr_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.instr

    @property
    def is_valid(self):
        lib.node().xroad_instr_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_instr_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_instr_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_instr_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_instr_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_instr_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_instr_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_instr_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_instr_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Instr(lib.node().xroad_instr_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_instr_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_instr_get_id.restype = ctypes.c_long
        return lib.node().xroad_instr_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_instr_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_instr_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_instr_copy(self.__ptr, id)
        return Instr(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.alias
        if v is not None:
            fields["alias"] = v
        v = self.name
        if v is not None:
            fields["name"] = v
        v = self.long_name
        if v is not None:
            fields["long_name"] = v
        v = self.cqg_name
        if v is not None:
            fields["cqg_name"] = v
        v = self.exch_id
        if v is not None:
            fields["exch_id"] = v
        v = self.cls
        if v is not None:
            fields["cls"] = v
        v = self.exch
        if v is not None:
            fields["exch"] = v.name
        v = self.cfi
        if v is not None:
            fields["cfi"] = v
        v = self.cur
        if v is not None:
            fields["cur"] = v.name
        v = self.lot_size
        if v is not None:
            fields["lot_size"] = v
        v = self.deleted
        if v is not None:
            fields["deleted"] = v
        v = self.strike
        if v is not None:
            fields["strike"] = v
        v = self.face_value
        if v is not None:
            fields["face_value"] = v
        v = self.accrued_int
        if v is not None:
            fields["accrued_int"] = v
        v = self.exp_dtime
        if v is not None:
            fields["exp_dtime"] = v
        v = self.callput
        if v is not None:
            fields["callput"] = v.name
        v = self.isin
        if v is not None:
            fields["isin"] = v
        v = self.bb_source
        if v is not None:
            fields["bb_source"] = v
        v = self.bb_code
        if v is not None:
            fields["bb_code"] = v
        v = self.bb_figi
        if v is not None:
            fields["bb_figi"] = v
        v = self.underlying
        if v is not None:
            fields["underlying"] = "({0},{1})".format(v.object_type, v.id)
        v = self.leading
        if v is not None:
            fields["leading"] = "({0},{1})".format(v.object_type, v.id)
        v = self.tick_info
        if v is not None:
            fields["tick_info"] = "({0},{1})".format(v.object_type, v.id)
        v = self.timesheet
        if v is not None:
            fields["timesheet"] = "({0},{1})".format(v.object_type, v.id)
        v = self.mdstat
        if v is not None:
            fields["mdstat"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "alias":
            self.alias = str(value) if value is not None else value
        elif field == "name":
            self.name = str(value) if value is not None else value
        elif field == "long_name":
            self.long_name = str(value) if value is not None else value
        elif field == "cqg_name":
            self.cqg_name = str(value) if value is not None else value
        elif field == "exch_id":
            self.exch_id = int(value) if value is not None else value
        elif field == "cls":
            self.cls = str(value) if value is not None else value
        elif field == "exch":
            self.exch = xtypes.Exchange[value] if value is not None else value
        elif field == "cfi":
            self.cfi = str(value) if value is not None else value
        elif field == "cur":
            self.cur = xtypes.Currency[value] if value is not None else value
        elif field == "lot_size":
            self.lot_size = int(value) if value is not None else value
        elif field == "deleted":
            self.deleted = int(value) if value is not None else value
        elif field == "strike":
            self.strike = float(value) if value is not None else value
        elif field == "face_value":
            self.face_value = float(value) if value is not None else value
        elif field == "accrued_int":
            self.accrued_int = float(value) if value is not None else value
        elif field == "exp_dtime":
            self.exp_dtime = int(value) if value is not None else value
        elif field == "callput":
            self.callput = xtypes.Callput[value] if value is not None else value
        elif field == "isin":
            self.isin = str(value) if value is not None else value
        elif field == "bb_source":
            self.bb_source = str(value) if value is not None else value
        elif field == "bb_code":
            self.bb_code = str(value) if value is not None else value
        elif field == "bb_figi":
            self.bb_figi = str(value) if value is not None else value
        elif field == "underlying":
            if hasattr(value, "ptr"):
                self.underlying = value
            else:
                self.underlying = str_to_tuple(value)
        elif field == "leading":
            if hasattr(value, "ptr"):
                self.leading = value
            else:
                self.leading = str_to_tuple(value)
        elif field == "tick_info":
            if hasattr(value, "ptr"):
                self.tick_info = value
            else:
                self.tick_info = str_to_tuple(value)
        elif field == "timesheet":
            if hasattr(value, "ptr"):
                self.timesheet = value
            else:
                self.timesheet = str_to_tuple(value)
        elif field == "mdstat":
            if hasattr(value, "ptr"):
                self.mdstat = value
            else:
                self.mdstat = str_to_tuple(value)

    @property
    def alias(self):
        lib.node().xroad_instr_alias_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_alias_is_set(self.__ptr):
            lib.node().xroad_instr_get_alias.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_alias.restype = ctypes.POINTER(xtypes.Alias)
            res = lib.node().xroad_instr_get_alias(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @alias.setter
    def alias(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_instr_set_alias.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_instr_set_alias(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_instr_reset_alias.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_alias(self.__ptr)

    @property
    def name(self):
        lib.node().xroad_instr_name_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_name_is_set(self.__ptr):
            lib.node().xroad_instr_get_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_name.restype = ctypes.POINTER(xtypes.Name)
            res = lib.node().xroad_instr_get_name(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @name.setter
    def name(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_instr_set_name.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_instr_set_name(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_instr_reset_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_name(self.__ptr)

    @property
    def long_name(self):
        lib.node().xroad_instr_long_name_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_long_name_is_set(self.__ptr):
            lib.node().xroad_instr_get_long_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_long_name.restype = ctypes.POINTER(xtypes.Name)
            res = lib.node().xroad_instr_get_long_name(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @long_name.setter
    def long_name(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_instr_set_long_name.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_instr_set_long_name(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_instr_reset_long_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_long_name(self.__ptr)

    @property
    def cqg_name(self):
        lib.node().xroad_instr_cqg_name_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_cqg_name_is_set(self.__ptr):
            lib.node().xroad_instr_get_cqg_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_cqg_name.restype = ctypes.POINTER(xtypes.Name)
            res = lib.node().xroad_instr_get_cqg_name(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @cqg_name.setter
    def cqg_name(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_instr_set_cqg_name.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_instr_set_cqg_name(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_instr_reset_cqg_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_cqg_name(self.__ptr)

    @property
    def exch_id(self):
        lib.node().xroad_instr_exch_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_exch_id_is_set(self.__ptr):
            lib.node().xroad_instr_get_exch_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_exch_id.restype = ctypes.c_long
            return lib.node().xroad_instr_get_exch_id(self.__ptr)
        else:
            return None

    @exch_id.setter
    def exch_id(self, value):
        if value is not None:
            lib.node().xroad_instr_set_exch_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_instr_set_exch_id(self.__ptr, value)
        else:
            lib.node().xroad_instr_reset_exch_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_exch_id(self.__ptr)

    @property
    def cls(self):
        lib.node().xroad_instr_cls_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_cls_is_set(self.__ptr):
            lib.node().xroad_instr_get_cls.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_cls.restype = ctypes.POINTER(xtypes.Cls)
            res = lib.node().xroad_instr_get_cls(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @cls.setter
    def cls(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_instr_set_cls.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_instr_set_cls(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_instr_reset_cls.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_cls(self.__ptr)

    @property
    def exch(self):
        lib.node().xroad_instr_exch_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_exch_is_set(self.__ptr):
            lib.node().xroad_instr_get_exch.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_exch.restype = ctypes.c_int
            return xtypes.Exchange(lib.node().xroad_instr_get_exch(self.__ptr))
        else:
            return None

    @exch.setter
    def exch(self, value):
        if not isinstance(value, xtypes.Exchange) and value is not None:
            raise TypeError("{0} has wrong type. must be Exchange enum".format(value))
        if value is not None:
            lib.node().xroad_instr_set_exch.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_instr_set_exch(self.__ptr, value.value)
        else:
            lib.node().xroad_instr_reset_exch.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_exch(self.__ptr)

    @property
    def cfi(self):
        lib.node().xroad_instr_cfi_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_cfi_is_set(self.__ptr):
            lib.node().xroad_instr_get_cfi.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_cfi.restype = ctypes.POINTER(xtypes.Cfi)
            res = lib.node().xroad_instr_get_cfi(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @cfi.setter
    def cfi(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_instr_set_cfi.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_instr_set_cfi(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_instr_reset_cfi.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_cfi(self.__ptr)

    @property
    def cur(self):
        lib.node().xroad_instr_cur_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_cur_is_set(self.__ptr):
            lib.node().xroad_instr_get_cur.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_cur.restype = ctypes.c_int
            return xtypes.Currency(lib.node().xroad_instr_get_cur(self.__ptr))
        else:
            return None

    @cur.setter
    def cur(self, value):
        if not isinstance(value, xtypes.Currency) and value is not None:
            raise TypeError("{0} has wrong type. must be Currency enum".format(value))
        if value is not None:
            lib.node().xroad_instr_set_cur.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_instr_set_cur(self.__ptr, value.value)
        else:
            lib.node().xroad_instr_reset_cur.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_cur(self.__ptr)

    @property
    def lot_size(self):
        lib.node().xroad_instr_lot_size_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_lot_size_is_set(self.__ptr):
            lib.node().xroad_instr_get_lot_size.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_lot_size.restype = ctypes.c_int
            return lib.node().xroad_instr_get_lot_size(self.__ptr)
        else:
            return None

    @lot_size.setter
    def lot_size(self, value):
        if value is not None:
            lib.node().xroad_instr_set_lot_size.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_instr_set_lot_size(self.__ptr, value)
        else:
            lib.node().xroad_instr_reset_lot_size.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_lot_size(self.__ptr)

    @property
    def deleted(self):
        lib.node().xroad_instr_deleted_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_deleted_is_set(self.__ptr):
            lib.node().xroad_instr_get_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_deleted.restype = ctypes.c_byte
            return lib.node().xroad_instr_get_deleted(self.__ptr)
        else:
            return None

    @deleted.setter
    def deleted(self, value):
        if value is not None:
            lib.node().xroad_instr_set_deleted.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_instr_set_deleted(self.__ptr, value)
        else:
            lib.node().xroad_instr_reset_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_deleted(self.__ptr)

    @property
    def strike(self):
        lib.node().xroad_instr_strike_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_strike_is_set(self.__ptr):
            lib.node().xroad_instr_get_strike.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_strike.restype = ctypes.c_double
            return lib.node().xroad_instr_get_strike(self.__ptr)
        else:
            return None

    @strike.setter
    def strike(self, value):
        if value is not None:
            lib.node().xroad_instr_set_strike.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_instr_set_strike(self.__ptr, value)
        else:
            lib.node().xroad_instr_reset_strike.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_strike(self.__ptr)

    @property
    def face_value(self):
        lib.node().xroad_instr_face_value_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_face_value_is_set(self.__ptr):
            lib.node().xroad_instr_get_face_value.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_face_value.restype = ctypes.c_double
            return lib.node().xroad_instr_get_face_value(self.__ptr)
        else:
            return None

    @face_value.setter
    def face_value(self, value):
        if value is not None:
            lib.node().xroad_instr_set_face_value.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_instr_set_face_value(self.__ptr, value)
        else:
            lib.node().xroad_instr_reset_face_value.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_face_value(self.__ptr)

    @property
    def accrued_int(self):
        lib.node().xroad_instr_accrued_int_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_accrued_int_is_set(self.__ptr):
            lib.node().xroad_instr_get_accrued_int.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_accrued_int.restype = ctypes.c_double
            return lib.node().xroad_instr_get_accrued_int(self.__ptr)
        else:
            return None

    @accrued_int.setter
    def accrued_int(self, value):
        if value is not None:
            lib.node().xroad_instr_set_accrued_int.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_instr_set_accrued_int(self.__ptr, value)
        else:
            lib.node().xroad_instr_reset_accrued_int.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_accrued_int(self.__ptr)

    @property
    def exp_dtime(self):
        lib.node().xroad_instr_exp_dtime_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_exp_dtime_is_set(self.__ptr):
            lib.node().xroad_instr_get_exp_dtime.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_exp_dtime.restype = ctypes.c_ulong
            return lib.node().xroad_instr_get_exp_dtime(self.__ptr)
        else:
            return None

    @exp_dtime.setter
    def exp_dtime(self, value):
        if value is not None:
            lib.node().xroad_instr_set_exp_dtime.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_instr_set_exp_dtime(self.__ptr, value)
        else:
            lib.node().xroad_instr_reset_exp_dtime.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_exp_dtime(self.__ptr)

    @property
    def callput(self):
        lib.node().xroad_instr_callput_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_callput_is_set(self.__ptr):
            lib.node().xroad_instr_get_callput.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_callput.restype = ctypes.c_int
            return xtypes.Callput(lib.node().xroad_instr_get_callput(self.__ptr))
        else:
            return None

    @callput.setter
    def callput(self, value):
        if not isinstance(value, xtypes.Callput) and value is not None:
            raise TypeError("{0} has wrong type. must be Callput enum".format(value))
        if value is not None:
            lib.node().xroad_instr_set_callput.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_instr_set_callput(self.__ptr, value.value)
        else:
            lib.node().xroad_instr_reset_callput.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_callput(self.__ptr)

    @property
    def isin(self):
        lib.node().xroad_instr_isin_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_isin_is_set(self.__ptr):
            lib.node().xroad_instr_get_isin.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_isin.restype = ctypes.POINTER(xtypes.Isin)
            res = lib.node().xroad_instr_get_isin(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @isin.setter
    def isin(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_instr_set_isin.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_instr_set_isin(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_instr_reset_isin.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_isin(self.__ptr)

    @property
    def bb_source(self):
        lib.node().xroad_instr_bb_source_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_bb_source_is_set(self.__ptr):
            lib.node().xroad_instr_get_bb_source.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_bb_source.restype = ctypes.POINTER(xtypes.BbSource)
            res = lib.node().xroad_instr_get_bb_source(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @bb_source.setter
    def bb_source(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_instr_set_bb_source.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_instr_set_bb_source(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_instr_reset_bb_source.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_bb_source(self.__ptr)

    @property
    def bb_code(self):
        lib.node().xroad_instr_bb_code_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_bb_code_is_set(self.__ptr):
            lib.node().xroad_instr_get_bb_code.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_bb_code.restype = ctypes.POINTER(xtypes.BbCode)
            res = lib.node().xroad_instr_get_bb_code(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @bb_code.setter
    def bb_code(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_instr_set_bb_code.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_instr_set_bb_code(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_instr_reset_bb_code.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_bb_code(self.__ptr)

    @property
    def bb_figi(self):
        lib.node().xroad_instr_bb_figi_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_bb_figi_is_set(self.__ptr):
            lib.node().xroad_instr_get_bb_figi.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_bb_figi.restype = ctypes.POINTER(xtypes.BbFigi)
            res = lib.node().xroad_instr_get_bb_figi(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @bb_figi.setter
    def bb_figi(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_instr_set_bb_figi.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_instr_set_bb_figi(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_instr_reset_bb_figi.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_bb_figi(self.__ptr)

    @property
    def underlying(self):
        lib.node().xroad_instr_underlying_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_underlying_is_set(self.__ptr):
            lib.node().xroad_instr_get_underlying.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_underlying.restype = ctypes.c_void_p
            obj = lib.node().xroad_instr_get_underlying(self.__ptr)
            if not obj:
                raise BrokenRefError("reference underlying is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @underlying.setter
    def underlying(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_instr_set_underlying.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_instr_set_underlying(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_instr_set_underlying_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_instr_set_underlying_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_instr_reset_underlying.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_underlying(self.__ptr)

    @property
    def leading(self):
        lib.node().xroad_instr_leading_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_leading_is_set(self.__ptr):
            lib.node().xroad_instr_get_leading.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_leading.restype = ctypes.c_void_p
            obj = lib.node().xroad_instr_get_leading(self.__ptr)
            if not obj:
                raise BrokenRefError("reference leading is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @leading.setter
    def leading(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_instr_set_leading.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_instr_set_leading(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_instr_set_leading_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_instr_set_leading_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_instr_reset_leading.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_leading(self.__ptr)

    @property
    def tick_info(self):
        lib.node().xroad_instr_tick_info_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_tick_info_is_set(self.__ptr):
            lib.node().xroad_instr_get_tick_info.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_tick_info.restype = ctypes.c_void_p
            obj = lib.node().xroad_instr_get_tick_info(self.__ptr)
            if not obj:
                raise BrokenRefError("reference tick_info is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @tick_info.setter
    def tick_info(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_instr_set_tick_info.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_instr_set_tick_info(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_instr_set_tick_info_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_instr_set_tick_info_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_instr_reset_tick_info.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_tick_info(self.__ptr)

    @property
    def timesheet(self):
        lib.node().xroad_instr_timesheet_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_timesheet_is_set(self.__ptr):
            lib.node().xroad_instr_get_timesheet.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_timesheet.restype = ctypes.c_void_p
            obj = lib.node().xroad_instr_get_timesheet(self.__ptr)
            if not obj:
                raise BrokenRefError("reference timesheet is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @timesheet.setter
    def timesheet(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_instr_set_timesheet.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_instr_set_timesheet(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_instr_set_timesheet_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_instr_set_timesheet_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_instr_reset_timesheet.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_timesheet(self.__ptr)

    @property
    def mdstat(self):
        lib.node().xroad_instr_mdstat_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_instr_mdstat_is_set(self.__ptr):
            lib.node().xroad_instr_get_mdstat.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_get_mdstat.restype = ctypes.c_void_p
            obj = lib.node().xroad_instr_get_mdstat(self.__ptr)
            if not obj:
                raise BrokenRefError("reference mdstat is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @mdstat.setter
    def mdstat(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_instr_set_mdstat.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_instr_set_mdstat(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_instr_set_mdstat_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_instr_set_mdstat_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_instr_reset_mdstat.argtypes = [ctypes.c_void_p]
            lib.node().xroad_instr_reset_mdstat(self.__ptr)


class TickInfo(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_tick_info_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_tick_info_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.tick_info

    @property
    def is_valid(self):
        lib.node().xroad_tick_info_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_tick_info_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_tick_info_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_tick_info_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_tick_info_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_tick_info_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_tick_info_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_tick_info_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_tick_info_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return TickInfo(lib.node().xroad_tick_info_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_tick_info_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_tick_info_get_id.restype = ctypes.c_long
        return lib.node().xroad_tick_info_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_tick_info_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_tick_info_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_tick_info_copy(self.__ptr, id)
        return TickInfo(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.price_min
        if v is not None:
            fields["price_min"] = v
        v = self.price_max
        if v is not None:
            fields["price_max"] = v
        v = self.size
        if v is not None:
            fields["size"] = v
        v = self.value
        if v is not None:
            fields["value"] = v
        v = self.precision
        if v is not None:
            fields["precision"] = v
        v = self.next
        if v is not None:
            fields["next"] = "({0},{1})".format(v.object_type, v.id)
        v = self.deleted
        if v is not None:
            fields["deleted"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "price_min":
            self.price_min = float(value) if value is not None else value
        elif field == "price_max":
            self.price_max = float(value) if value is not None else value
        elif field == "size":
            self.size = float(value) if value is not None else value
        elif field == "value":
            self.value = float(value) if value is not None else value
        elif field == "precision":
            self.precision = int(value) if value is not None else value
        elif field == "next":
            if hasattr(value, "ptr"):
                self.next = value
            else:
                self.next = str_to_tuple(value)
        elif field == "deleted":
            self.deleted = int(value) if value is not None else value

    @property
    def price_min(self):
        lib.node().xroad_tick_info_price_min_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_tick_info_price_min_is_set(self.__ptr):
            lib.node().xroad_tick_info_get_price_min.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_get_price_min.restype = ctypes.c_double
            return lib.node().xroad_tick_info_get_price_min(self.__ptr)
        else:
            return None

    @price_min.setter
    def price_min(self, value):
        if value is not None:
            lib.node().xroad_tick_info_set_price_min.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_tick_info_set_price_min(self.__ptr, value)
        else:
            lib.node().xroad_tick_info_reset_price_min.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_reset_price_min(self.__ptr)

    @property
    def price_max(self):
        lib.node().xroad_tick_info_price_max_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_tick_info_price_max_is_set(self.__ptr):
            lib.node().xroad_tick_info_get_price_max.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_get_price_max.restype = ctypes.c_double
            return lib.node().xroad_tick_info_get_price_max(self.__ptr)
        else:
            return None

    @price_max.setter
    def price_max(self, value):
        if value is not None:
            lib.node().xroad_tick_info_set_price_max.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_tick_info_set_price_max(self.__ptr, value)
        else:
            lib.node().xroad_tick_info_reset_price_max.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_reset_price_max(self.__ptr)

    @property
    def size(self):
        lib.node().xroad_tick_info_size_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_tick_info_size_is_set(self.__ptr):
            lib.node().xroad_tick_info_get_size.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_get_size.restype = ctypes.c_double
            return lib.node().xroad_tick_info_get_size(self.__ptr)
        else:
            return None

    @size.setter
    def size(self, value):
        if value is not None:
            lib.node().xroad_tick_info_set_size.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_tick_info_set_size(self.__ptr, value)
        else:
            lib.node().xroad_tick_info_reset_size.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_reset_size(self.__ptr)

    @property
    def value(self):
        lib.node().xroad_tick_info_value_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_tick_info_value_is_set(self.__ptr):
            lib.node().xroad_tick_info_get_value.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_get_value.restype = ctypes.c_double
            return lib.node().xroad_tick_info_get_value(self.__ptr)
        else:
            return None

    @value.setter
    def value(self, value):
        if value is not None:
            lib.node().xroad_tick_info_set_value.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_tick_info_set_value(self.__ptr, value)
        else:
            lib.node().xroad_tick_info_reset_value.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_reset_value(self.__ptr)

    @property
    def precision(self):
        lib.node().xroad_tick_info_precision_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_tick_info_precision_is_set(self.__ptr):
            lib.node().xroad_tick_info_get_precision.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_get_precision.restype = ctypes.c_int
            return lib.node().xroad_tick_info_get_precision(self.__ptr)
        else:
            return None

    @precision.setter
    def precision(self, value):
        if value is not None:
            lib.node().xroad_tick_info_set_precision.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_tick_info_set_precision(self.__ptr, value)
        else:
            lib.node().xroad_tick_info_reset_precision.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_reset_precision(self.__ptr)

    @property
    def next(self):
        lib.node().xroad_tick_info_next_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_tick_info_next_is_set(self.__ptr):
            lib.node().xroad_tick_info_get_next.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_get_next.restype = ctypes.c_void_p
            obj = lib.node().xroad_tick_info_get_next(self.__ptr)
            if not obj:
                raise BrokenRefError("reference next is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @next.setter
    def next(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_tick_info_set_next.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_tick_info_set_next(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_tick_info_set_next_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_tick_info_set_next_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_tick_info_reset_next.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_reset_next(self.__ptr)

    @property
    def deleted(self):
        lib.node().xroad_tick_info_deleted_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_tick_info_deleted_is_set(self.__ptr):
            lib.node().xroad_tick_info_get_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_get_deleted.restype = ctypes.c_byte
            return lib.node().xroad_tick_info_get_deleted(self.__ptr)
        else:
            return None

    @deleted.setter
    def deleted(self, value):
        if value is not None:
            lib.node().xroad_tick_info_set_deleted.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_tick_info_set_deleted(self.__ptr, value)
        else:
            lib.node().xroad_tick_info_reset_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_tick_info_reset_deleted(self.__ptr)


class Timesheet(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_timesheet_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_timesheet_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.timesheet

    @property
    def is_valid(self):
        lib.node().xroad_timesheet_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_timesheet_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_timesheet_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_timesheet_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_timesheet_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_timesheet_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_timesheet_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_timesheet_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_timesheet_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Timesheet(lib.node().xroad_timesheet_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_timesheet_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_timesheet_get_id.restype = ctypes.c_long
        return lib.node().xroad_timesheet_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_timesheet_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_timesheet_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_timesheet_copy(self.__ptr, id)
        return Timesheet(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.start
        if v is not None:
            fields["start"] = v
        v = self.stop
        if v is not None:
            fields["stop"] = v
        v = self.next
        if v is not None:
            fields["next"] = "({0},{1})".format(v.object_type, v.id)
        v = self.deleted
        if v is not None:
            fields["deleted"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "start":
            self.start = int(value) if value is not None else value
        elif field == "stop":
            self.stop = int(value) if value is not None else value
        elif field == "next":
            if hasattr(value, "ptr"):
                self.next = value
            else:
                self.next = str_to_tuple(value)
        elif field == "deleted":
            self.deleted = int(value) if value is not None else value

    @property
    def start(self):
        lib.node().xroad_timesheet_start_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_timesheet_start_is_set(self.__ptr):
            lib.node().xroad_timesheet_get_start.argtypes = [ctypes.c_void_p]
            lib.node().xroad_timesheet_get_start.restype = ctypes.c_long
            return lib.node().xroad_timesheet_get_start(self.__ptr)
        else:
            return None

    @start.setter
    def start(self, value):
        if value is not None:
            lib.node().xroad_timesheet_set_start.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_timesheet_set_start(self.__ptr, value)
        else:
            lib.node().xroad_timesheet_reset_start.argtypes = [ctypes.c_void_p]
            lib.node().xroad_timesheet_reset_start(self.__ptr)

    @property
    def stop(self):
        lib.node().xroad_timesheet_stop_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_timesheet_stop_is_set(self.__ptr):
            lib.node().xroad_timesheet_get_stop.argtypes = [ctypes.c_void_p]
            lib.node().xroad_timesheet_get_stop.restype = ctypes.c_long
            return lib.node().xroad_timesheet_get_stop(self.__ptr)
        else:
            return None

    @stop.setter
    def stop(self, value):
        if value is not None:
            lib.node().xroad_timesheet_set_stop.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_timesheet_set_stop(self.__ptr, value)
        else:
            lib.node().xroad_timesheet_reset_stop.argtypes = [ctypes.c_void_p]
            lib.node().xroad_timesheet_reset_stop(self.__ptr)

    @property
    def next(self):
        lib.node().xroad_timesheet_next_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_timesheet_next_is_set(self.__ptr):
            lib.node().xroad_timesheet_get_next.argtypes = [ctypes.c_void_p]
            lib.node().xroad_timesheet_get_next.restype = ctypes.c_void_p
            obj = lib.node().xroad_timesheet_get_next(self.__ptr)
            if not obj:
                raise BrokenRefError("reference next is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @next.setter
    def next(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_timesheet_set_next.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_timesheet_set_next(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_timesheet_set_next_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_timesheet_set_next_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_timesheet_reset_next.argtypes = [ctypes.c_void_p]
            lib.node().xroad_timesheet_reset_next(self.__ptr)

    @property
    def deleted(self):
        lib.node().xroad_timesheet_deleted_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_timesheet_deleted_is_set(self.__ptr):
            lib.node().xroad_timesheet_get_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_timesheet_get_deleted.restype = ctypes.c_byte
            return lib.node().xroad_timesheet_get_deleted(self.__ptr)
        else:
            return None

    @deleted.setter
    def deleted(self, value):
        if value is not None:
            lib.node().xroad_timesheet_set_deleted.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_timesheet_set_deleted(self.__ptr, value)
        else:
            lib.node().xroad_timesheet_reset_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_timesheet_reset_deleted(self.__ptr)


class Mdstat(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_mdstat_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_mdstat_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.mdstat

    @property
    def is_valid(self):
        lib.node().xroad_mdstat_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_mdstat_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_mdstat_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_mdstat_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_mdstat_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_mdstat_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_mdstat_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_mdstat_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_mdstat_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Mdstat(lib.node().xroad_mdstat_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_mdstat_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_mdstat_get_id.restype = ctypes.c_long
        return lib.node().xroad_mdstat_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_mdstat_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_mdstat_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_mdstat_copy(self.__ptr, id)
        return Mdstat(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.last_price
        if v is not None:
            fields["last_price"] = v
        v = self.update_ts
        if v is not None:
            fields["update_ts"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "last_price":
            self.last_price = float(value) if value is not None else value
        elif field == "update_ts":
            self.update_ts = int(value) if value is not None else value

    @property
    def last_price(self):
        lib.node().xroad_mdstat_last_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mdstat_last_price_is_set(self.__ptr):
            lib.node().xroad_mdstat_get_last_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdstat_get_last_price.restype = ctypes.c_double
            return lib.node().xroad_mdstat_get_last_price(self.__ptr)
        else:
            return None

    @last_price.setter
    def last_price(self, value):
        if value is not None:
            lib.node().xroad_mdstat_set_last_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_mdstat_set_last_price(self.__ptr, value)
        else:
            lib.node().xroad_mdstat_reset_last_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdstat_reset_last_price(self.__ptr)

    @property
    def update_ts(self):
        lib.node().xroad_mdstat_update_ts_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mdstat_update_ts_is_set(self.__ptr):
            lib.node().xroad_mdstat_get_update_ts.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdstat_get_update_ts.restype = ctypes.c_long
            return lib.node().xroad_mdstat_get_update_ts(self.__ptr)
        else:
            return None

    @update_ts.setter
    def update_ts(self, value):
        if value is not None:
            lib.node().xroad_mdstat_set_update_ts.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_mdstat_set_update_ts(self.__ptr, value)
        else:
            lib.node().xroad_mdstat_reset_update_ts.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdstat_reset_update_ts(self.__ptr)


class OrderSql(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_order_sql_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_order_sql_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.order_sql

    @property
    def is_valid(self):
        lib.node().xroad_order_sql_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_order_sql_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_order_sql_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_order_sql_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_order_sql_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_order_sql_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_order_sql_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_order_sql_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_sql_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return OrderSql(lib.node().xroad_order_sql_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_order_sql_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_sql_get_id.restype = ctypes.c_long
        return lib.node().xroad_order_sql_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_order_sql_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_order_sql_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_order_sql_copy(self.__ptr, id)
        return OrderSql(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.db_id
        if v is not None:
            fields["db_id"] = v
        v = self.order
        if v is not None:
            fields["order"] = "({0},{1})".format(v.object_type, v.id)
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.price
        if v is not None:
            fields["price"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "db_id":
            self.db_id = int(value) if value is not None else value
        elif field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value

    @property
    def db_id(self):
        lib.node().xroad_order_sql_db_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_sql_db_id_is_set(self.__ptr):
            lib.node().xroad_order_sql_get_db_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_sql_get_db_id.restype = ctypes.c_long
            return lib.node().xroad_order_sql_get_db_id(self.__ptr)
        else:
            return None

    @db_id.setter
    def db_id(self, value):
        if value is not None:
            lib.node().xroad_order_sql_set_db_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_sql_set_db_id(self.__ptr, value)
        else:
            lib.node().xroad_order_sql_reset_db_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_sql_reset_db_id(self.__ptr)

    @property
    def order(self):
        lib.node().xroad_order_sql_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_sql_order_is_set(self.__ptr):
            lib.node().xroad_order_sql_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_sql_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_sql_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_sql_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_sql_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_sql_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_sql_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_sql_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_sql_reset_order(self.__ptr)

    @property
    def node_id(self):
        lib.node().xroad_order_sql_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_sql_node_id_is_set(self.__ptr):
            lib.node().xroad_order_sql_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_sql_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_order_sql_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_order_sql_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_order_sql_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_order_sql_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_sql_reset_node_id(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_order_sql_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_sql_qty_is_set(self.__ptr):
            lib.node().xroad_order_sql_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_sql_get_qty.restype = ctypes.c_long
            return lib.node().xroad_order_sql_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_order_sql_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_sql_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_sql_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_sql_reset_qty(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_order_sql_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_sql_price_is_set(self.__ptr):
            lib.node().xroad_order_sql_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_sql_get_price.restype = ctypes.c_double
            return lib.node().xroad_order_sql_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_order_sql_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_order_sql_set_price(self.__ptr, value)
        else:
            lib.node().xroad_order_sql_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_sql_reset_price(self.__ptr)


class CancelSql(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_cancel_sql_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_cancel_sql_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.cancel_sql

    @property
    def is_valid(self):
        lib.node().xroad_cancel_sql_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_cancel_sql_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_cancel_sql_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_cancel_sql_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_cancel_sql_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_cancel_sql_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_cancel_sql_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_cancel_sql_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cancel_sql_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return CancelSql(lib.node().xroad_cancel_sql_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_cancel_sql_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cancel_sql_get_id.restype = ctypes.c_long
        return lib.node().xroad_cancel_sql_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_cancel_sql_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_cancel_sql_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_cancel_sql_copy(self.__ptr, id)
        return CancelSql(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.db_id
        if v is not None:
            fields["db_id"] = v
        v = self.order
        if v is not None:
            fields["order"] = "({0},{1})".format(v.object_type, v.id)
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "db_id":
            self.db_id = int(value) if value is not None else value
        elif field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "node_id":
            self.node_id = int(value) if value is not None else value

    @property
    def db_id(self):
        lib.node().xroad_cancel_sql_db_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_sql_db_id_is_set(self.__ptr):
            lib.node().xroad_cancel_sql_get_db_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_sql_get_db_id.restype = ctypes.c_long
            return lib.node().xroad_cancel_sql_get_db_id(self.__ptr)
        else:
            return None

    @db_id.setter
    def db_id(self, value):
        if value is not None:
            lib.node().xroad_cancel_sql_set_db_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_cancel_sql_set_db_id(self.__ptr, value)
        else:
            lib.node().xroad_cancel_sql_reset_db_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_sql_reset_db_id(self.__ptr)

    @property
    def order(self):
        lib.node().xroad_cancel_sql_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_sql_order_is_set(self.__ptr):
            lib.node().xroad_cancel_sql_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_sql_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_cancel_sql_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_cancel_sql_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_cancel_sql_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_cancel_sql_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_cancel_sql_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_cancel_sql_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_sql_reset_order(self.__ptr)

    @property
    def node_id(self):
        lib.node().xroad_cancel_sql_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_sql_node_id_is_set(self.__ptr):
            lib.node().xroad_cancel_sql_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_sql_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_cancel_sql_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_cancel_sql_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_cancel_sql_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_cancel_sql_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_sql_reset_node_id(self.__ptr)


class ReplaceSql(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_replace_sql_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_replace_sql_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.replace_sql

    @property
    def is_valid(self):
        lib.node().xroad_replace_sql_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_replace_sql_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_replace_sql_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_replace_sql_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_replace_sql_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_replace_sql_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_replace_sql_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_replace_sql_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_replace_sql_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return ReplaceSql(lib.node().xroad_replace_sql_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_replace_sql_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_replace_sql_get_id.restype = ctypes.c_long
        return lib.node().xroad_replace_sql_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_replace_sql_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_replace_sql_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_replace_sql_copy(self.__ptr, id)
        return ReplaceSql(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.db_id
        if v is not None:
            fields["db_id"] = v
        v = self.order
        if v is not None:
            fields["order"] = "({0},{1})".format(v.object_type, v.id)
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "db_id":
            self.db_id = int(value) if value is not None else value
        elif field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "node_id":
            self.node_id = int(value) if value is not None else value

    @property
    def db_id(self):
        lib.node().xroad_replace_sql_db_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_sql_db_id_is_set(self.__ptr):
            lib.node().xroad_replace_sql_get_db_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_sql_get_db_id.restype = ctypes.c_long
            return lib.node().xroad_replace_sql_get_db_id(self.__ptr)
        else:
            return None

    @db_id.setter
    def db_id(self, value):
        if value is not None:
            lib.node().xroad_replace_sql_set_db_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replace_sql_set_db_id(self.__ptr, value)
        else:
            lib.node().xroad_replace_sql_reset_db_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_sql_reset_db_id(self.__ptr)

    @property
    def order(self):
        lib.node().xroad_replace_sql_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_sql_order_is_set(self.__ptr):
            lib.node().xroad_replace_sql_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_sql_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_replace_sql_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_replace_sql_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_replace_sql_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_replace_sql_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_replace_sql_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_replace_sql_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_sql_reset_order(self.__ptr)

    @property
    def node_id(self):
        lib.node().xroad_replace_sql_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_sql_node_id_is_set(self.__ptr):
            lib.node().xroad_replace_sql_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_sql_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_replace_sql_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_replace_sql_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_replace_sql_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_replace_sql_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_sql_reset_node_id(self.__ptr)


class OrderRabbit(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_order_rabbit_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_order_rabbit_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.order_rabbit

    @property
    def is_valid(self):
        lib.node().xroad_order_rabbit_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_order_rabbit_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_order_rabbit_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_order_rabbit_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_order_rabbit_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_order_rabbit_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_order_rabbit_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_order_rabbit_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_rabbit_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return OrderRabbit(lib.node().xroad_order_rabbit_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_order_rabbit_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_rabbit_get_id.restype = ctypes.c_long
        return lib.node().xroad_order_rabbit_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_order_rabbit_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_order_rabbit_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_order_rabbit_copy(self.__ptr, id)
        return OrderRabbit(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.side
        if v is not None:
            fields["side"] = v.name
        v = self.tif
        if v is not None:
            fields["tif"] = v.name
        v = self.src_node_id
        if v is not None:
            fields["src_node_id"] = v
        v = self.dst_node_id
        if v is not None:
            fields["dst_node_id"] = v
        v = self.ext_ref
        if v is not None:
            fields["ext_ref"] = v
        v = self.status
        if v is not None:
            fields["status"] = v.name
        v = self.sub_status
        if v is not None:
            fields["sub_status"] = v
        v = self.clord_id
        if v is not None:
            fields["clord_id"] = v
        v = self.order
        if v is not None:
            fields["order"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "side":
            self.side = xtypes.Side[value] if value is not None else value
        elif field == "tif":
            self.tif = xtypes.Tif[value] if value is not None else value
        elif field == "src_node_id":
            self.src_node_id = int(value) if value is not None else value
        elif field == "dst_node_id":
            self.dst_node_id = int(value) if value is not None else value
        elif field == "ext_ref":
            self.ext_ref = str(value) if value is not None else value
        elif field == "status":
            self.status = xtypes.OrderStatus[value] if value is not None else value
        elif field == "sub_status":
            self.sub_status = int(value) if value is not None else value
        elif field == "clord_id":
            self.clord_id = int(value) if value is not None else value
        elif field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)

    @property
    def side(self):
        lib.node().xroad_order_rabbit_side_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_rabbit_side_is_set(self.__ptr):
            lib.node().xroad_order_rabbit_get_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_get_side.restype = ctypes.c_int
            return xtypes.Side(lib.node().xroad_order_rabbit_get_side(self.__ptr))
        else:
            return None

    @side.setter
    def side(self, value):
        if not isinstance(value, xtypes.Side) and value is not None:
            raise TypeError("{0} has wrong type. must be Side enum".format(value))
        if value is not None:
            lib.node().xroad_order_rabbit_set_side.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_rabbit_set_side(self.__ptr, value.value)
        else:
            lib.node().xroad_order_rabbit_reset_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_reset_side(self.__ptr)

    @property
    def tif(self):
        lib.node().xroad_order_rabbit_tif_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_rabbit_tif_is_set(self.__ptr):
            lib.node().xroad_order_rabbit_get_tif.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_get_tif.restype = ctypes.c_int
            return xtypes.Tif(lib.node().xroad_order_rabbit_get_tif(self.__ptr))
        else:
            return None

    @tif.setter
    def tif(self, value):
        if not isinstance(value, xtypes.Tif) and value is not None:
            raise TypeError("{0} has wrong type. must be Tif enum".format(value))
        if value is not None:
            lib.node().xroad_order_rabbit_set_tif.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_rabbit_set_tif(self.__ptr, value.value)
        else:
            lib.node().xroad_order_rabbit_reset_tif.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_reset_tif(self.__ptr)

    @property
    def src_node_id(self):
        lib.node().xroad_order_rabbit_src_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_rabbit_src_node_id_is_set(self.__ptr):
            lib.node().xroad_order_rabbit_get_src_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_get_src_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_order_rabbit_get_src_node_id(self.__ptr)
        else:
            return None

    @src_node_id.setter
    def src_node_id(self, value):
        if value is not None:
            lib.node().xroad_order_rabbit_set_src_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_order_rabbit_set_src_node_id(self.__ptr, value)
        else:
            lib.node().xroad_order_rabbit_reset_src_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_reset_src_node_id(self.__ptr)

    @property
    def dst_node_id(self):
        lib.node().xroad_order_rabbit_dst_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_rabbit_dst_node_id_is_set(self.__ptr):
            lib.node().xroad_order_rabbit_get_dst_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_get_dst_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_order_rabbit_get_dst_node_id(self.__ptr)
        else:
            return None

    @dst_node_id.setter
    def dst_node_id(self, value):
        if value is not None:
            lib.node().xroad_order_rabbit_set_dst_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_order_rabbit_set_dst_node_id(self.__ptr, value)
        else:
            lib.node().xroad_order_rabbit_reset_dst_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_reset_dst_node_id(self.__ptr)

    @property
    def ext_ref(self):
        lib.node().xroad_order_rabbit_ext_ref_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_rabbit_ext_ref_is_set(self.__ptr):
            lib.node().xroad_order_rabbit_get_ext_ref.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_get_ext_ref.restype = ctypes.POINTER(xtypes.ExtRef)
            res = lib.node().xroad_order_rabbit_get_ext_ref(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @ext_ref.setter
    def ext_ref(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_rabbit_set_ext_ref.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_rabbit_set_ext_ref(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_rabbit_reset_ext_ref.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_reset_ext_ref(self.__ptr)

    @property
    def status(self):
        lib.node().xroad_order_rabbit_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_rabbit_status_is_set(self.__ptr):
            lib.node().xroad_order_rabbit_get_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_get_status.restype = ctypes.c_int
            return xtypes.OrderStatus(lib.node().xroad_order_rabbit_get_status(self.__ptr))
        else:
            return None

    @status.setter
    def status(self, value):
        if not isinstance(value, xtypes.OrderStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderStatus enum".format(value))
        if value is not None:
            lib.node().xroad_order_rabbit_set_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_rabbit_set_status(self.__ptr, value.value)
        else:
            lib.node().xroad_order_rabbit_reset_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_reset_status(self.__ptr)

    @property
    def sub_status(self):
        lib.node().xroad_order_rabbit_sub_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_rabbit_sub_status_is_set(self.__ptr):
            lib.node().xroad_order_rabbit_get_sub_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_get_sub_status.restype = ctypes.c_int
            return lib.node().xroad_order_rabbit_get_sub_status(self.__ptr)
        else:
            return None

    @sub_status.setter
    def sub_status(self, value):
        if value is not None:
            lib.node().xroad_order_rabbit_set_sub_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_rabbit_set_sub_status(self.__ptr, value)
        else:
            lib.node().xroad_order_rabbit_reset_sub_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_reset_sub_status(self.__ptr)

    @property
    def clord_id(self):
        lib.node().xroad_order_rabbit_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_rabbit_clord_id_is_set(self.__ptr):
            lib.node().xroad_order_rabbit_get_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_get_clord_id.restype = ctypes.c_long
            return lib.node().xroad_order_rabbit_get_clord_id(self.__ptr)
        else:
            return None

    @clord_id.setter
    def clord_id(self, value):
        if value is not None:
            lib.node().xroad_order_rabbit_set_clord_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_rabbit_set_clord_id(self.__ptr, value)
        else:
            lib.node().xroad_order_rabbit_reset_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_reset_clord_id(self.__ptr)

    @property
    def order(self):
        lib.node().xroad_order_rabbit_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_rabbit_order_is_set(self.__ptr):
            lib.node().xroad_order_rabbit_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_rabbit_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_rabbit_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_rabbit_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_rabbit_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_rabbit_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_rabbit_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_rabbit_reset_order(self.__ptr)


class Rake(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_rake_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_rake_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.rake

    @property
    def is_valid(self):
        lib.node().xroad_rake_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_rake_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_rake_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_rake_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_rake_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_rake_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_rake_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_rake_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_rake_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Rake(lib.node().xroad_rake_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_rake_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_rake_get_id.restype = ctypes.c_long
        return lib.node().xroad_rake_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_rake_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_rake_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_rake_copy(self.__ptr, id)
        return Rake(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.working_int
        if v is not None:
            fields["working_int"] = v
        v = self.book_depth
        if v is not None:
            fields["book_depth"] = v
        v = self.level_dist
        if v is not None:
            fields["level_dist"] = v
        v = self.agression_level
        if v is not None:
            fields["agression_level"] = v
        v = self.mid_time
        if v is not None:
            fields["mid_time"] = v
        v = self.agression_time
        if v is not None:
            fields["agression_time"] = v
        v = self.display_qty
        if v is not None:
            fields["display_qty"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "working_int":
            self.working_int = int(value) if value is not None else value
        elif field == "book_depth":
            self.book_depth = int(value) if value is not None else value
        elif field == "level_dist":
            self.level_dist = int(value) if value is not None else value
        elif field == "agression_level":
            self.agression_level = int(value) if value is not None else value
        elif field == "mid_time":
            self.mid_time = int(value) if value is not None else value
        elif field == "agression_time":
            self.agression_time = int(value) if value is not None else value
        elif field == "display_qty":
            self.display_qty = int(value) if value is not None else value

    @property
    def working_int(self):
        lib.node().xroad_rake_working_int_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rake_working_int_is_set(self.__ptr):
            lib.node().xroad_rake_get_working_int.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_get_working_int.restype = ctypes.c_int
            return lib.node().xroad_rake_get_working_int(self.__ptr)
        else:
            return None

    @working_int.setter
    def working_int(self, value):
        if value is not None:
            lib.node().xroad_rake_set_working_int.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rake_set_working_int(self.__ptr, value)
        else:
            lib.node().xroad_rake_reset_working_int.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_reset_working_int(self.__ptr)

    @property
    def book_depth(self):
        lib.node().xroad_rake_book_depth_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rake_book_depth_is_set(self.__ptr):
            lib.node().xroad_rake_get_book_depth.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_get_book_depth.restype = ctypes.c_int
            return lib.node().xroad_rake_get_book_depth(self.__ptr)
        else:
            return None

    @book_depth.setter
    def book_depth(self, value):
        if value is not None:
            lib.node().xroad_rake_set_book_depth.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rake_set_book_depth(self.__ptr, value)
        else:
            lib.node().xroad_rake_reset_book_depth.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_reset_book_depth(self.__ptr)

    @property
    def level_dist(self):
        lib.node().xroad_rake_level_dist_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rake_level_dist_is_set(self.__ptr):
            lib.node().xroad_rake_get_level_dist.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_get_level_dist.restype = ctypes.c_int
            return lib.node().xroad_rake_get_level_dist(self.__ptr)
        else:
            return None

    @level_dist.setter
    def level_dist(self, value):
        if value is not None:
            lib.node().xroad_rake_set_level_dist.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rake_set_level_dist(self.__ptr, value)
        else:
            lib.node().xroad_rake_reset_level_dist.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_reset_level_dist(self.__ptr)

    @property
    def agression_level(self):
        lib.node().xroad_rake_agression_level_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rake_agression_level_is_set(self.__ptr):
            lib.node().xroad_rake_get_agression_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_get_agression_level.restype = ctypes.c_int
            return lib.node().xroad_rake_get_agression_level(self.__ptr)
        else:
            return None

    @agression_level.setter
    def agression_level(self, value):
        if value is not None:
            lib.node().xroad_rake_set_agression_level.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rake_set_agression_level(self.__ptr, value)
        else:
            lib.node().xroad_rake_reset_agression_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_reset_agression_level(self.__ptr)

    @property
    def mid_time(self):
        lib.node().xroad_rake_mid_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rake_mid_time_is_set(self.__ptr):
            lib.node().xroad_rake_get_mid_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_get_mid_time.restype = ctypes.c_int
            return lib.node().xroad_rake_get_mid_time(self.__ptr)
        else:
            return None

    @mid_time.setter
    def mid_time(self, value):
        if value is not None:
            lib.node().xroad_rake_set_mid_time.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rake_set_mid_time(self.__ptr, value)
        else:
            lib.node().xroad_rake_reset_mid_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_reset_mid_time(self.__ptr)

    @property
    def agression_time(self):
        lib.node().xroad_rake_agression_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rake_agression_time_is_set(self.__ptr):
            lib.node().xroad_rake_get_agression_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_get_agression_time.restype = ctypes.c_int
            return lib.node().xroad_rake_get_agression_time(self.__ptr)
        else:
            return None

    @agression_time.setter
    def agression_time(self, value):
        if value is not None:
            lib.node().xroad_rake_set_agression_time.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rake_set_agression_time(self.__ptr, value)
        else:
            lib.node().xroad_rake_reset_agression_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_reset_agression_time(self.__ptr)

    @property
    def display_qty(self):
        lib.node().xroad_rake_display_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rake_display_qty_is_set(self.__ptr):
            lib.node().xroad_rake_get_display_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_get_display_qty.restype = ctypes.c_long
            return lib.node().xroad_rake_get_display_qty(self.__ptr)
        else:
            return None

    @display_qty.setter
    def display_qty(self, value):
        if value is not None:
            lib.node().xroad_rake_set_display_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_rake_set_display_qty(self.__ptr, value)
        else:
            lib.node().xroad_rake_reset_display_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rake_reset_display_qty(self.__ptr)


class Stealth(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_stealth_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_stealth_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.stealth

    @property
    def is_valid(self):
        lib.node().xroad_stealth_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_stealth_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_stealth_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_stealth_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_stealth_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_stealth_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_stealth_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_stealth_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_stealth_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Stealth(lib.node().xroad_stealth_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_stealth_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_stealth_get_id.restype = ctypes.c_long
        return lib.node().xroad_stealth_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_stealth_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_stealth_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_stealth_copy(self.__ptr, id)
        return Stealth(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.working_int
        if v is not None:
            fields["working_int"] = v
        v = self.display_qty
        if v is not None:
            fields["display_qty"] = v
        v = self.qty_shift
        if v is not None:
            fields["qty_shift"] = v
        v = self.book_depth
        if v is not None:
            fields["book_depth"] = v
        v = self.level_dist
        if v is not None:
            fields["level_dist"] = v
        v = self.liq_price_shift
        if v is not None:
            fields["liq_price_shift"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "working_int":
            self.working_int = int(value) if value is not None else value
        elif field == "display_qty":
            self.display_qty = int(value) if value is not None else value
        elif field == "qty_shift":
            self.qty_shift = float(value) if value is not None else value
        elif field == "book_depth":
            self.book_depth = int(value) if value is not None else value
        elif field == "level_dist":
            self.level_dist = int(value) if value is not None else value
        elif field == "liq_price_shift":
            self.liq_price_shift = float(value) if value is not None else value

    @property
    def working_int(self):
        lib.node().xroad_stealth_working_int_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_stealth_working_int_is_set(self.__ptr):
            lib.node().xroad_stealth_get_working_int.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_get_working_int.restype = ctypes.c_int
            return lib.node().xroad_stealth_get_working_int(self.__ptr)
        else:
            return None

    @working_int.setter
    def working_int(self, value):
        if value is not None:
            lib.node().xroad_stealth_set_working_int.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_stealth_set_working_int(self.__ptr, value)
        else:
            lib.node().xroad_stealth_reset_working_int.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_reset_working_int(self.__ptr)

    @property
    def display_qty(self):
        lib.node().xroad_stealth_display_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_stealth_display_qty_is_set(self.__ptr):
            lib.node().xroad_stealth_get_display_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_get_display_qty.restype = ctypes.c_int
            return lib.node().xroad_stealth_get_display_qty(self.__ptr)
        else:
            return None

    @display_qty.setter
    def display_qty(self, value):
        if value is not None:
            lib.node().xroad_stealth_set_display_qty.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_stealth_set_display_qty(self.__ptr, value)
        else:
            lib.node().xroad_stealth_reset_display_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_reset_display_qty(self.__ptr)

    @property
    def qty_shift(self):
        lib.node().xroad_stealth_qty_shift_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_stealth_qty_shift_is_set(self.__ptr):
            lib.node().xroad_stealth_get_qty_shift.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_get_qty_shift.restype = ctypes.c_double
            return lib.node().xroad_stealth_get_qty_shift(self.__ptr)
        else:
            return None

    @qty_shift.setter
    def qty_shift(self, value):
        if value is not None:
            lib.node().xroad_stealth_set_qty_shift.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_stealth_set_qty_shift(self.__ptr, value)
        else:
            lib.node().xroad_stealth_reset_qty_shift.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_reset_qty_shift(self.__ptr)

    @property
    def book_depth(self):
        lib.node().xroad_stealth_book_depth_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_stealth_book_depth_is_set(self.__ptr):
            lib.node().xroad_stealth_get_book_depth.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_get_book_depth.restype = ctypes.c_int
            return lib.node().xroad_stealth_get_book_depth(self.__ptr)
        else:
            return None

    @book_depth.setter
    def book_depth(self, value):
        if value is not None:
            lib.node().xroad_stealth_set_book_depth.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_stealth_set_book_depth(self.__ptr, value)
        else:
            lib.node().xroad_stealth_reset_book_depth.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_reset_book_depth(self.__ptr)

    @property
    def level_dist(self):
        lib.node().xroad_stealth_level_dist_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_stealth_level_dist_is_set(self.__ptr):
            lib.node().xroad_stealth_get_level_dist.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_get_level_dist.restype = ctypes.c_int
            return lib.node().xroad_stealth_get_level_dist(self.__ptr)
        else:
            return None

    @level_dist.setter
    def level_dist(self, value):
        if value is not None:
            lib.node().xroad_stealth_set_level_dist.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_stealth_set_level_dist(self.__ptr, value)
        else:
            lib.node().xroad_stealth_reset_level_dist.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_reset_level_dist(self.__ptr)

    @property
    def liq_price_shift(self):
        lib.node().xroad_stealth_liq_price_shift_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_stealth_liq_price_shift_is_set(self.__ptr):
            lib.node().xroad_stealth_get_liq_price_shift.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_get_liq_price_shift.restype = ctypes.c_double
            return lib.node().xroad_stealth_get_liq_price_shift(self.__ptr)
        else:
            return None

    @liq_price_shift.setter
    def liq_price_shift(self, value):
        if value is not None:
            lib.node().xroad_stealth_set_liq_price_shift.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_stealth_set_liq_price_shift(self.__ptr, value)
        else:
            lib.node().xroad_stealth_reset_liq_price_shift.argtypes = [ctypes.c_void_p]
            lib.node().xroad_stealth_reset_liq_price_shift(self.__ptr)


class Spread(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_spread_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_spread_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.spread

    @property
    def is_valid(self):
        lib.node().xroad_spread_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_spread_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_spread_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_spread_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_spread_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_spread_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_spread_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_spread_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_spread_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Spread(lib.node().xroad_spread_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_spread_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_spread_get_id.restype = ctypes.c_long
        return lib.node().xroad_spread_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_spread_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_spread_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_spread_copy(self.__ptr, id)
        return Spread(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.side
        if v is not None:
            fields["side"] = v.name
        v = self.tif
        if v is not None:
            fields["tif"] = v.name
        v = self.src_node_id
        if v is not None:
            fields["src_node_id"] = v
        v = self.dst_node_id
        if v is not None:
            fields["dst_node_id"] = v
        v = self.ext_ref
        if v is not None:
            fields["ext_ref"] = v
        v = self.status
        if v is not None:
            fields["status"] = v.name
        v = self.sub_status
        if v is not None:
            fields["sub_status"] = v
        v = self.sender
        if v is not None:
            fields["sender"] = v
        v = self.timestamp
        if v is not None:
            fields["timestamp"] = v
        v = self.type
        if v is not None:
            fields["type"] = v.name
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.leaves_qty
        if v is not None:
            fields["leaves_qty"] = v
        v = self.cum_qty
        if v is not None:
            fields["cum_qty"] = v
        v = self.price
        if v is not None:
            fields["price"] = v
        v = self.flags
        if v is not None:
            fields["flags"] = v
        v = self.agression_level
        if v is not None:
            fields["agression_level"] = v
        v = self.fill_timeout
        if v is not None:
            fields["fill_timeout"] = v
        v = self.cancel_on_hang
        if v is not None:
            fields["cancel_on_hang"] = v
        v = self.leg
        if v is not None:
            fields["leg"] = "({0},{1})".format(v.object_type, v.id)
        v = self.text
        if v is not None:
            fields["text"] = v
        v = self.vwap_price
        if v is not None:
            fields["vwap_price"] = v
        v = self.mdata_price
        if v is not None:
            fields["mdata_price"] = v
        v = self.mdata_qty
        if v is not None:
            fields["mdata_qty"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "side":
            self.side = xtypes.Side[value] if value is not None else value
        elif field == "tif":
            self.tif = xtypes.Tif[value] if value is not None else value
        elif field == "src_node_id":
            self.src_node_id = int(value) if value is not None else value
        elif field == "dst_node_id":
            self.dst_node_id = int(value) if value is not None else value
        elif field == "ext_ref":
            self.ext_ref = str(value) if value is not None else value
        elif field == "status":
            self.status = xtypes.OrderStatus[value] if value is not None else value
        elif field == "sub_status":
            self.sub_status = int(value) if value is not None else value
        elif field == "sender":
            self.sender = str(value) if value is not None else value
        elif field == "timestamp":
            self.timestamp = int(value) if value is not None else value
        elif field == "type":
            self.type = xtypes.OrdType[value] if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "leaves_qty":
            self.leaves_qty = int(value) if value is not None else value
        elif field == "cum_qty":
            self.cum_qty = int(value) if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "flags":
            self.flags = int(value) if value is not None else value
        elif field == "agression_level":
            self.agression_level = int(value) if value is not None else value
        elif field == "fill_timeout":
            self.fill_timeout = int(value) if value is not None else value
        elif field == "cancel_on_hang":
            self.cancel_on_hang = int(value) if value is not None else value
        elif field == "leg":
            if hasattr(value, "ptr"):
                self.leg = value
            else:
                self.leg = str_to_tuple(value)
        elif field == "text":
            self.text = str(value) if value is not None else value
        elif field == "vwap_price":
            self.vwap_price = float(value) if value is not None else value
        elif field == "mdata_price":
            self.mdata_price = float(value) if value is not None else value
        elif field == "mdata_qty":
            self.mdata_qty = int(value) if value is not None else value

    @property
    def side(self):
        lib.node().xroad_spread_side_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_side_is_set(self.__ptr):
            lib.node().xroad_spread_get_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_side.restype = ctypes.c_int
            return xtypes.Side(lib.node().xroad_spread_get_side(self.__ptr))
        else:
            return None

    @side.setter
    def side(self, value):
        if not isinstance(value, xtypes.Side) and value is not None:
            raise TypeError("{0} has wrong type. must be Side enum".format(value))
        if value is not None:
            lib.node().xroad_spread_set_side.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_spread_set_side(self.__ptr, value.value)
        else:
            lib.node().xroad_spread_reset_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_side(self.__ptr)

    @property
    def tif(self):
        lib.node().xroad_spread_tif_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_tif_is_set(self.__ptr):
            lib.node().xroad_spread_get_tif.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_tif.restype = ctypes.c_int
            return xtypes.Tif(lib.node().xroad_spread_get_tif(self.__ptr))
        else:
            return None

    @tif.setter
    def tif(self, value):
        if not isinstance(value, xtypes.Tif) and value is not None:
            raise TypeError("{0} has wrong type. must be Tif enum".format(value))
        if value is not None:
            lib.node().xroad_spread_set_tif.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_spread_set_tif(self.__ptr, value.value)
        else:
            lib.node().xroad_spread_reset_tif.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_tif(self.__ptr)

    @property
    def src_node_id(self):
        lib.node().xroad_spread_src_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_src_node_id_is_set(self.__ptr):
            lib.node().xroad_spread_get_src_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_src_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_spread_get_src_node_id(self.__ptr)
        else:
            return None

    @src_node_id.setter
    def src_node_id(self, value):
        if value is not None:
            lib.node().xroad_spread_set_src_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_spread_set_src_node_id(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_src_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_src_node_id(self.__ptr)

    @property
    def dst_node_id(self):
        lib.node().xroad_spread_dst_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_dst_node_id_is_set(self.__ptr):
            lib.node().xroad_spread_get_dst_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_dst_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_spread_get_dst_node_id(self.__ptr)
        else:
            return None

    @dst_node_id.setter
    def dst_node_id(self, value):
        if value is not None:
            lib.node().xroad_spread_set_dst_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_spread_set_dst_node_id(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_dst_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_dst_node_id(self.__ptr)

    @property
    def ext_ref(self):
        lib.node().xroad_spread_ext_ref_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_ext_ref_is_set(self.__ptr):
            lib.node().xroad_spread_get_ext_ref.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_ext_ref.restype = ctypes.POINTER(xtypes.ExtRef)
            res = lib.node().xroad_spread_get_ext_ref(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @ext_ref.setter
    def ext_ref(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_spread_set_ext_ref.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_spread_set_ext_ref(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_spread_reset_ext_ref.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_ext_ref(self.__ptr)

    @property
    def status(self):
        lib.node().xroad_spread_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_status_is_set(self.__ptr):
            lib.node().xroad_spread_get_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_status.restype = ctypes.c_int
            return xtypes.OrderStatus(lib.node().xroad_spread_get_status(self.__ptr))
        else:
            return None

    @status.setter
    def status(self, value):
        if not isinstance(value, xtypes.OrderStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderStatus enum".format(value))
        if value is not None:
            lib.node().xroad_spread_set_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_spread_set_status(self.__ptr, value.value)
        else:
            lib.node().xroad_spread_reset_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_status(self.__ptr)

    @property
    def sub_status(self):
        lib.node().xroad_spread_sub_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_sub_status_is_set(self.__ptr):
            lib.node().xroad_spread_get_sub_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_sub_status.restype = ctypes.c_int
            return lib.node().xroad_spread_get_sub_status(self.__ptr)
        else:
            return None

    @sub_status.setter
    def sub_status(self, value):
        if value is not None:
            lib.node().xroad_spread_set_sub_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_spread_set_sub_status(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_sub_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_sub_status(self.__ptr)

    @property
    def sender(self):
        lib.node().xroad_spread_sender_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_sender_is_set(self.__ptr):
            lib.node().xroad_spread_get_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_sender.restype = ctypes.POINTER(xtypes.Sender)
            res = lib.node().xroad_spread_get_sender(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sender.setter
    def sender(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_spread_set_sender.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_spread_set_sender(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_spread_reset_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_sender(self.__ptr)

    @property
    def timestamp(self):
        lib.node().xroad_spread_timestamp_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_timestamp_is_set(self.__ptr):
            lib.node().xroad_spread_get_timestamp.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_timestamp.restype = ctypes.c_ulong
            return lib.node().xroad_spread_get_timestamp(self.__ptr)
        else:
            return None

    @timestamp.setter
    def timestamp(self, value):
        if value is not None:
            lib.node().xroad_spread_set_timestamp.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_spread_set_timestamp(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_timestamp.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_timestamp(self.__ptr)

    @property
    def type(self):
        lib.node().xroad_spread_type_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_type_is_set(self.__ptr):
            lib.node().xroad_spread_get_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_type.restype = ctypes.c_int
            return xtypes.OrdType(lib.node().xroad_spread_get_type(self.__ptr))
        else:
            return None

    @type.setter
    def type(self, value):
        if not isinstance(value, xtypes.OrdType) and value is not None:
            raise TypeError("{0} has wrong type. must be OrdType enum".format(value))
        if value is not None:
            lib.node().xroad_spread_set_type.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_spread_set_type(self.__ptr, value.value)
        else:
            lib.node().xroad_spread_reset_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_type(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_spread_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_qty_is_set(self.__ptr):
            lib.node().xroad_spread_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_qty.restype = ctypes.c_long
            return lib.node().xroad_spread_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_spread_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_spread_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_qty(self.__ptr)

    @property
    def leaves_qty(self):
        lib.node().xroad_spread_leaves_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_leaves_qty_is_set(self.__ptr):
            lib.node().xroad_spread_get_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_leaves_qty.restype = ctypes.c_long
            return lib.node().xroad_spread_get_leaves_qty(self.__ptr)
        else:
            return None

    @leaves_qty.setter
    def leaves_qty(self, value):
        if value is not None:
            lib.node().xroad_spread_set_leaves_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_spread_set_leaves_qty(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_leaves_qty(self.__ptr)

    @property
    def cum_qty(self):
        lib.node().xroad_spread_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_cum_qty_is_set(self.__ptr):
            lib.node().xroad_spread_get_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_spread_get_cum_qty(self.__ptr)
        else:
            return None

    @cum_qty.setter
    def cum_qty(self, value):
        if value is not None:
            lib.node().xroad_spread_set_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_spread_set_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_cum_qty(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_spread_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_price_is_set(self.__ptr):
            lib.node().xroad_spread_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_price.restype = ctypes.c_double
            return lib.node().xroad_spread_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_spread_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_spread_set_price(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_price(self.__ptr)

    @property
    def flags(self):
        lib.node().xroad_spread_flags_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_flags_is_set(self.__ptr):
            lib.node().xroad_spread_get_flags.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_flags.restype = ctypes.c_int
            return lib.node().xroad_spread_get_flags(self.__ptr)
        else:
            return None

    @flags.setter
    def flags(self, value):
        if value is not None:
            lib.node().xroad_spread_set_flags.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_spread_set_flags(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_flags.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_flags(self.__ptr)

    @property
    def agression_level(self):
        lib.node().xroad_spread_agression_level_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_agression_level_is_set(self.__ptr):
            lib.node().xroad_spread_get_agression_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_agression_level.restype = ctypes.c_int
            return lib.node().xroad_spread_get_agression_level(self.__ptr)
        else:
            return None

    @agression_level.setter
    def agression_level(self, value):
        if value is not None:
            lib.node().xroad_spread_set_agression_level.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_spread_set_agression_level(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_agression_level.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_agression_level(self.__ptr)

    @property
    def fill_timeout(self):
        lib.node().xroad_spread_fill_timeout_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_fill_timeout_is_set(self.__ptr):
            lib.node().xroad_spread_get_fill_timeout.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_fill_timeout.restype = ctypes.c_int
            return lib.node().xroad_spread_get_fill_timeout(self.__ptr)
        else:
            return None

    @fill_timeout.setter
    def fill_timeout(self, value):
        if value is not None:
            lib.node().xroad_spread_set_fill_timeout.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_spread_set_fill_timeout(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_fill_timeout.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_fill_timeout(self.__ptr)

    @property
    def cancel_on_hang(self):
        lib.node().xroad_spread_cancel_on_hang_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_cancel_on_hang_is_set(self.__ptr):
            lib.node().xroad_spread_get_cancel_on_hang.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_cancel_on_hang.restype = ctypes.c_byte
            return lib.node().xroad_spread_get_cancel_on_hang(self.__ptr)
        else:
            return None

    @cancel_on_hang.setter
    def cancel_on_hang(self, value):
        if value is not None:
            lib.node().xroad_spread_set_cancel_on_hang.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_spread_set_cancel_on_hang(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_cancel_on_hang.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_cancel_on_hang(self.__ptr)

    @property
    def leg(self):
        lib.node().xroad_spread_leg_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_leg_is_set(self.__ptr):
            lib.node().xroad_spread_get_leg.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_leg.restype = ctypes.c_void_p
            obj = lib.node().xroad_spread_get_leg(self.__ptr)
            if not obj:
                raise BrokenRefError("reference leg is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @leg.setter
    def leg(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_spread_set_leg.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_spread_set_leg(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_spread_set_leg_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_spread_set_leg_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_spread_reset_leg.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_leg(self.__ptr)

    @property
    def text(self):
        lib.node().xroad_spread_text_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_text_is_set(self.__ptr):
            lib.node().xroad_spread_get_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_text.restype = ctypes.POINTER(xtypes.ShortText)
            res = lib.node().xroad_spread_get_text(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @text.setter
    def text(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_spread_set_text.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_spread_set_text(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_spread_reset_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_text(self.__ptr)

    @property
    def vwap_price(self):
        lib.node().xroad_spread_vwap_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_vwap_price_is_set(self.__ptr):
            lib.node().xroad_spread_get_vwap_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_vwap_price.restype = ctypes.c_double
            return lib.node().xroad_spread_get_vwap_price(self.__ptr)
        else:
            return None

    @vwap_price.setter
    def vwap_price(self, value):
        if value is not None:
            lib.node().xroad_spread_set_vwap_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_spread_set_vwap_price(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_vwap_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_vwap_price(self.__ptr)

    @property
    def mdata_price(self):
        lib.node().xroad_spread_mdata_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_mdata_price_is_set(self.__ptr):
            lib.node().xroad_spread_get_mdata_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_mdata_price.restype = ctypes.c_double
            return lib.node().xroad_spread_get_mdata_price(self.__ptr)
        else:
            return None

    @mdata_price.setter
    def mdata_price(self, value):
        if value is not None:
            lib.node().xroad_spread_set_mdata_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_spread_set_mdata_price(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_mdata_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_mdata_price(self.__ptr)

    @property
    def mdata_qty(self):
        lib.node().xroad_spread_mdata_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_mdata_qty_is_set(self.__ptr):
            lib.node().xroad_spread_get_mdata_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_get_mdata_qty.restype = ctypes.c_long
            return lib.node().xroad_spread_get_mdata_qty(self.__ptr)
        else:
            return None

    @mdata_qty.setter
    def mdata_qty(self, value):
        if value is not None:
            lib.node().xroad_spread_set_mdata_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_spread_set_mdata_qty(self.__ptr, value)
        else:
            lib.node().xroad_spread_reset_mdata_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_reset_mdata_qty(self.__ptr)


class Leg(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_leg_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_leg_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.leg

    @property
    def is_valid(self):
        lib.node().xroad_leg_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_leg_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_leg_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_leg_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_leg_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_leg_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_leg_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_leg_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_leg_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Leg(lib.node().xroad_leg_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_leg_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_leg_get_id.restype = ctypes.c_long
        return lib.node().xroad_leg_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_leg_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_leg_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_leg_copy(self.__ptr, id)
        return Leg(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.uniq_id
        if v is not None:
            fields["uniq_id"] = v
        v = self.next
        if v is not None:
            fields["next"] = "({0},{1})".format(v.object_type, v.id)
        v = self.order
        if v is not None:
            fields["order"] = "({0},{1})".format(v.object_type, v.id)
        v = self.qty_ratio
        if v is not None:
            fields["qty_ratio"] = v
        v = self.is_working
        if v is not None:
            fields["is_working"] = v
        v = self.vwap_price
        if v is not None:
            fields["vwap_price"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "uniq_id":
            self.uniq_id = str(value) if value is not None else value
        elif field == "next":
            if hasattr(value, "ptr"):
                self.next = value
            else:
                self.next = str_to_tuple(value)
        elif field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "qty_ratio":
            self.qty_ratio = int(value) if value is not None else value
        elif field == "is_working":
            self.is_working = int(value) if value is not None else value
        elif field == "vwap_price":
            self.vwap_price = float(value) if value is not None else value

    @property
    def uniq_id(self):
        lib.node().xroad_leg_uniq_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_leg_uniq_id_is_set(self.__ptr):
            lib.node().xroad_leg_get_uniq_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_get_uniq_id.restype = ctypes.POINTER(xtypes.UniqId)
            res = lib.node().xroad_leg_get_uniq_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @uniq_id.setter
    def uniq_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_leg_set_uniq_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_leg_set_uniq_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_leg_reset_uniq_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_reset_uniq_id(self.__ptr)

    @property
    def next(self):
        lib.node().xroad_leg_next_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_leg_next_is_set(self.__ptr):
            lib.node().xroad_leg_get_next.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_get_next.restype = ctypes.c_void_p
            obj = lib.node().xroad_leg_get_next(self.__ptr)
            if not obj:
                raise BrokenRefError("reference next is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @next.setter
    def next(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_leg_set_next.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_leg_set_next(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_leg_set_next_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_leg_set_next_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_leg_reset_next.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_reset_next(self.__ptr)

    @property
    def order(self):
        lib.node().xroad_leg_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_leg_order_is_set(self.__ptr):
            lib.node().xroad_leg_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_leg_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_leg_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_leg_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_leg_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_leg_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_leg_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_reset_order(self.__ptr)

    @property
    def qty_ratio(self):
        lib.node().xroad_leg_qty_ratio_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_leg_qty_ratio_is_set(self.__ptr):
            lib.node().xroad_leg_get_qty_ratio.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_get_qty_ratio.restype = ctypes.c_int
            return lib.node().xroad_leg_get_qty_ratio(self.__ptr)
        else:
            return None

    @qty_ratio.setter
    def qty_ratio(self, value):
        if value is not None:
            lib.node().xroad_leg_set_qty_ratio.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_leg_set_qty_ratio(self.__ptr, value)
        else:
            lib.node().xroad_leg_reset_qty_ratio.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_reset_qty_ratio(self.__ptr)

    @property
    def is_working(self):
        lib.node().xroad_leg_is_working_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_leg_is_working_is_set(self.__ptr):
            lib.node().xroad_leg_get_is_working.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_get_is_working.restype = ctypes.c_byte
            return lib.node().xroad_leg_get_is_working(self.__ptr)
        else:
            return None

    @is_working.setter
    def is_working(self, value):
        if value is not None:
            lib.node().xroad_leg_set_is_working.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_leg_set_is_working(self.__ptr, value)
        else:
            lib.node().xroad_leg_reset_is_working.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_reset_is_working(self.__ptr)

    @property
    def vwap_price(self):
        lib.node().xroad_leg_vwap_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_leg_vwap_price_is_set(self.__ptr):
            lib.node().xroad_leg_get_vwap_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_get_vwap_price.restype = ctypes.c_double
            return lib.node().xroad_leg_get_vwap_price(self.__ptr)
        else:
            return None

    @vwap_price.setter
    def vwap_price(self, value):
        if value is not None:
            lib.node().xroad_leg_set_vwap_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_leg_set_vwap_price(self.__ptr, value)
        else:
            lib.node().xroad_leg_reset_vwap_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_leg_reset_vwap_price(self.__ptr)


class SpreadTrade(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_spread_trade_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_spread_trade_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.spread_trade

    @property
    def is_valid(self):
        lib.node().xroad_spread_trade_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_spread_trade_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_spread_trade_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_spread_trade_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_spread_trade_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_spread_trade_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_spread_trade_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_spread_trade_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_spread_trade_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return SpreadTrade(lib.node().xroad_spread_trade_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_spread_trade_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_spread_trade_get_id.restype = ctypes.c_long
        return lib.node().xroad_spread_trade_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_spread_trade_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_spread_trade_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_spread_trade_copy(self.__ptr, id)
        return SpreadTrade(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.spread
        if v is not None:
            fields["spread"] = "({0},{1})".format(v.object_type, v.id)
        v = self.tran_time
        if v is not None:
            fields["tran_time"] = v
        v = self.order_status
        if v is not None:
            fields["order_status"] = v.name
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.leaves_qty
        if v is not None:
            fields["leaves_qty"] = v
        v = self.cum_qty
        if v is not None:
            fields["cum_qty"] = v
        v = self.price
        if v is not None:
            fields["price"] = v
        v = self.trade
        if v is not None:
            fields["trade"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "spread":
            if hasattr(value, "ptr"):
                self.spread = value
            else:
                self.spread = str_to_tuple(value)
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value
        elif field == "order_status":
            self.order_status = xtypes.OrderStatus[value] if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "leaves_qty":
            self.leaves_qty = int(value) if value is not None else value
        elif field == "cum_qty":
            self.cum_qty = int(value) if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "trade":
            if hasattr(value, "ptr"):
                self.trade = value
            else:
                self.trade = str_to_tuple(value)

    @property
    def spread(self):
        lib.node().xroad_spread_trade_spread_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_trade_spread_is_set(self.__ptr):
            lib.node().xroad_spread_trade_get_spread.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_get_spread.restype = ctypes.c_void_p
            obj = lib.node().xroad_spread_trade_get_spread(self.__ptr)
            if not obj:
                raise BrokenRefError("reference spread is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @spread.setter
    def spread(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_spread_trade_set_spread.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_spread_trade_set_spread(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_spread_trade_set_spread_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_spread_trade_set_spread_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_spread_trade_reset_spread.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_reset_spread(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_spread_trade_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_trade_tran_time_is_set(self.__ptr):
            lib.node().xroad_spread_trade_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_spread_trade_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_spread_trade_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_spread_trade_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_spread_trade_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_reset_tran_time(self.__ptr)

    @property
    def order_status(self):
        lib.node().xroad_spread_trade_order_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_trade_order_status_is_set(self.__ptr):
            lib.node().xroad_spread_trade_get_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_get_order_status.restype = ctypes.c_int
            return xtypes.OrderStatus(lib.node().xroad_spread_trade_get_order_status(self.__ptr))
        else:
            return None

    @order_status.setter
    def order_status(self, value):
        if not isinstance(value, xtypes.OrderStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderStatus enum".format(value))
        if value is not None:
            lib.node().xroad_spread_trade_set_order_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_spread_trade_set_order_status(self.__ptr, value.value)
        else:
            lib.node().xroad_spread_trade_reset_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_reset_order_status(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_spread_trade_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_trade_qty_is_set(self.__ptr):
            lib.node().xroad_spread_trade_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_get_qty.restype = ctypes.c_long
            return lib.node().xroad_spread_trade_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_spread_trade_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_spread_trade_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_spread_trade_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_reset_qty(self.__ptr)

    @property
    def leaves_qty(self):
        lib.node().xroad_spread_trade_leaves_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_trade_leaves_qty_is_set(self.__ptr):
            lib.node().xroad_spread_trade_get_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_get_leaves_qty.restype = ctypes.c_long
            return lib.node().xroad_spread_trade_get_leaves_qty(self.__ptr)
        else:
            return None

    @leaves_qty.setter
    def leaves_qty(self, value):
        if value is not None:
            lib.node().xroad_spread_trade_set_leaves_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_spread_trade_set_leaves_qty(self.__ptr, value)
        else:
            lib.node().xroad_spread_trade_reset_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_reset_leaves_qty(self.__ptr)

    @property
    def cum_qty(self):
        lib.node().xroad_spread_trade_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_trade_cum_qty_is_set(self.__ptr):
            lib.node().xroad_spread_trade_get_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_get_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_spread_trade_get_cum_qty(self.__ptr)
        else:
            return None

    @cum_qty.setter
    def cum_qty(self, value):
        if value is not None:
            lib.node().xroad_spread_trade_set_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_spread_trade_set_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_spread_trade_reset_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_reset_cum_qty(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_spread_trade_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_trade_price_is_set(self.__ptr):
            lib.node().xroad_spread_trade_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_get_price.restype = ctypes.c_double
            return lib.node().xroad_spread_trade_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_spread_trade_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_spread_trade_set_price(self.__ptr, value)
        else:
            lib.node().xroad_spread_trade_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_reset_price(self.__ptr)

    @property
    def trade(self):
        lib.node().xroad_spread_trade_trade_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_spread_trade_trade_is_set(self.__ptr):
            lib.node().xroad_spread_trade_get_trade.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_get_trade.restype = ctypes.c_void_p
            obj = lib.node().xroad_spread_trade_get_trade(self.__ptr)
            if not obj:
                raise BrokenRefError("reference trade is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @trade.setter
    def trade(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_spread_trade_set_trade.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_spread_trade_set_trade(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_spread_trade_set_trade_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_spread_trade_set_trade_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_spread_trade_reset_trade.argtypes = [ctypes.c_void_p]
            lib.node().xroad_spread_trade_reset_trade(self.__ptr)


class CgateSession(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_cgate_session_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_cgate_session_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.cgate_session

    @property
    def is_valid(self):
        lib.node().xroad_cgate_session_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_cgate_session_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_cgate_session_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_cgate_session_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_cgate_session_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_cgate_session_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_cgate_session_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_cgate_session_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cgate_session_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return CgateSession(lib.node().xroad_cgate_session_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_cgate_session_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cgate_session_get_id.restype = ctypes.c_long
        return lib.node().xroad_cgate_session_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_cgate_session_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_cgate_session_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_cgate_session_copy(self.__ptr, id)
        return CgateSession(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.name
        if v is not None:
            fields["name"] = v
        v = self.lifenum
        if v is not None:
            fields["lifenum"] = v
        v = self.cgate_table
        if v is not None:
            fields["cgate_table"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "name":
            self.name = str(value) if value is not None else value
        elif field == "lifenum":
            self.lifenum = int(value) if value is not None else value
        elif field == "cgate_table":
            if hasattr(value, "ptr"):
                self.cgate_table = value
            else:
                self.cgate_table = str_to_tuple(value)

    @property
    def node_id(self):
        lib.node().xroad_cgate_session_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_session_node_id_is_set(self.__ptr):
            lib.node().xroad_cgate_session_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_session_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_cgate_session_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_cgate_session_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_cgate_session_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_cgate_session_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_session_reset_node_id(self.__ptr)

    @property
    def name(self):
        lib.node().xroad_cgate_session_name_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_session_name_is_set(self.__ptr):
            lib.node().xroad_cgate_session_get_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_session_get_name.restype = ctypes.POINTER(xtypes.Name)
            res = lib.node().xroad_cgate_session_get_name(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @name.setter
    def name(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_cgate_session_set_name.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_cgate_session_set_name(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_cgate_session_reset_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_session_reset_name(self.__ptr)

    @property
    def lifenum(self):
        lib.node().xroad_cgate_session_lifenum_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_session_lifenum_is_set(self.__ptr):
            lib.node().xroad_cgate_session_get_lifenum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_session_get_lifenum.restype = ctypes.c_long
            return lib.node().xroad_cgate_session_get_lifenum(self.__ptr)
        else:
            return None

    @lifenum.setter
    def lifenum(self, value):
        if value is not None:
            lib.node().xroad_cgate_session_set_lifenum.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_cgate_session_set_lifenum(self.__ptr, value)
        else:
            lib.node().xroad_cgate_session_reset_lifenum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_session_reset_lifenum(self.__ptr)

    @property
    def cgate_table(self):
        lib.node().xroad_cgate_session_cgate_table_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_session_cgate_table_is_set(self.__ptr):
            lib.node().xroad_cgate_session_get_cgate_table.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_session_get_cgate_table.restype = ctypes.c_void_p
            obj = lib.node().xroad_cgate_session_get_cgate_table(self.__ptr)
            if not obj:
                raise BrokenRefError("reference cgate_table is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @cgate_table.setter
    def cgate_table(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_cgate_session_set_cgate_table.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_cgate_session_set_cgate_table(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_cgate_session_set_cgate_table_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_cgate_session_set_cgate_table_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_cgate_session_reset_cgate_table.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_session_reset_cgate_table(self.__ptr)


class CgateTable(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_cgate_table_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_cgate_table_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.cgate_table

    @property
    def is_valid(self):
        lib.node().xroad_cgate_table_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_cgate_table_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_cgate_table_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_cgate_table_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_cgate_table_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_cgate_table_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_cgate_table_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_cgate_table_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cgate_table_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return CgateTable(lib.node().xroad_cgate_table_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_cgate_table_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cgate_table_get_id.restype = ctypes.c_long
        return lib.node().xroad_cgate_table_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_cgate_table_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_cgate_table_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_cgate_table_copy(self.__ptr, id)
        return CgateTable(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.name
        if v is not None:
            fields["name"] = v
        v = self.rev
        if v is not None:
            fields["rev"] = v
        v = self.next
        if v is not None:
            fields["next"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "name":
            self.name = str(value) if value is not None else value
        elif field == "rev":
            self.rev = int(value) if value is not None else value
        elif field == "next":
            if hasattr(value, "ptr"):
                self.next = value
            else:
                self.next = str_to_tuple(value)

    @property
    def name(self):
        lib.node().xroad_cgate_table_name_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_table_name_is_set(self.__ptr):
            lib.node().xroad_cgate_table_get_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_table_get_name.restype = ctypes.POINTER(xtypes.Name)
            res = lib.node().xroad_cgate_table_get_name(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @name.setter
    def name(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_cgate_table_set_name.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_cgate_table_set_name(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_cgate_table_reset_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_table_reset_name(self.__ptr)

    @property
    def rev(self):
        lib.node().xroad_cgate_table_rev_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_table_rev_is_set(self.__ptr):
            lib.node().xroad_cgate_table_get_rev.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_table_get_rev.restype = ctypes.c_long
            return lib.node().xroad_cgate_table_get_rev(self.__ptr)
        else:
            return None

    @rev.setter
    def rev(self, value):
        if value is not None:
            lib.node().xroad_cgate_table_set_rev.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_cgate_table_set_rev(self.__ptr, value)
        else:
            lib.node().xroad_cgate_table_reset_rev.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_table_reset_rev(self.__ptr)

    @property
    def next(self):
        lib.node().xroad_cgate_table_next_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_table_next_is_set(self.__ptr):
            lib.node().xroad_cgate_table_get_next.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_table_get_next.restype = ctypes.c_void_p
            obj = lib.node().xroad_cgate_table_get_next(self.__ptr)
            if not obj:
                raise BrokenRefError("reference next is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @next.setter
    def next(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_cgate_table_set_next.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_cgate_table_set_next(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_cgate_table_set_next_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_cgate_table_set_next_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_cgate_table_reset_next.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_table_reset_next(self.__ptr)


class CgateOrder(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_cgate_order_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_cgate_order_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.cgate_order

    @property
    def is_valid(self):
        lib.node().xroad_cgate_order_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_cgate_order_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_cgate_order_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_cgate_order_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_cgate_order_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_cgate_order_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_cgate_order_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_cgate_order_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cgate_order_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return CgateOrder(lib.node().xroad_cgate_order_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_cgate_order_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cgate_order_get_id.restype = ctypes.c_long
        return lib.node().xroad_cgate_order_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_cgate_order_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_cgate_order_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_cgate_order_copy(self.__ptr, id)
        return CgateOrder(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.order
        if v is not None:
            fields["order"] = "({0},{1})".format(v.object_type, v.id)
        v = self.exch_id
        if v is not None:
            fields["exch_id"] = v
        v = self.replace
        if v is not None:
            fields["replace"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "exch_id":
            self.exch_id = int(value) if value is not None else value
        elif field == "replace":
            if hasattr(value, "ptr"):
                self.replace = value
            else:
                self.replace = str_to_tuple(value)

    @property
    def node_id(self):
        lib.node().xroad_cgate_order_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_order_node_id_is_set(self.__ptr):
            lib.node().xroad_cgate_order_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_order_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_cgate_order_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_cgate_order_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_cgate_order_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_cgate_order_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_order_reset_node_id(self.__ptr)

    @property
    def order(self):
        lib.node().xroad_cgate_order_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_order_order_is_set(self.__ptr):
            lib.node().xroad_cgate_order_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_order_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_cgate_order_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_cgate_order_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_cgate_order_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_cgate_order_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_cgate_order_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_cgate_order_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_order_reset_order(self.__ptr)

    @property
    def exch_id(self):
        lib.node().xroad_cgate_order_exch_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_order_exch_id_is_set(self.__ptr):
            lib.node().xroad_cgate_order_get_exch_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_order_get_exch_id.restype = ctypes.c_long
            return lib.node().xroad_cgate_order_get_exch_id(self.__ptr)
        else:
            return None

    @exch_id.setter
    def exch_id(self, value):
        if value is not None:
            lib.node().xroad_cgate_order_set_exch_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_cgate_order_set_exch_id(self.__ptr, value)
        else:
            lib.node().xroad_cgate_order_reset_exch_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_order_reset_exch_id(self.__ptr)

    @property
    def replace(self):
        lib.node().xroad_cgate_order_replace_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cgate_order_replace_is_set(self.__ptr):
            lib.node().xroad_cgate_order_get_replace.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_order_get_replace.restype = ctypes.c_void_p
            obj = lib.node().xroad_cgate_order_get_replace(self.__ptr)
            if not obj:
                raise BrokenRefError("reference replace is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @replace.setter
    def replace(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_cgate_order_set_replace.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_cgate_order_set_replace(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_cgate_order_set_replace_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_cgate_order_set_replace_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_cgate_order_reset_replace.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cgate_order_reset_replace(self.__ptr)


class OrderFix(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_order_fix_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_order_fix_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.order_fix

    @property
    def is_valid(self):
        lib.node().xroad_order_fix_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_order_fix_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_order_fix_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_order_fix_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_order_fix_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_order_fix_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_order_fix_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_order_fix_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_fix_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return OrderFix(lib.node().xroad_order_fix_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_order_fix_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_fix_get_id.restype = ctypes.c_long
        return lib.node().xroad_order_fix_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_order_fix_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_order_fix_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_order_fix_copy(self.__ptr, id)
        return OrderFix(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.sender
        if v is not None:
            fields["sender"] = v
        v = self.instr
        if v is not None:
            fields["instr"] = "({0},{1})".format(v.object_type, v.id)
        v = self.seqnum
        if v is not None:
            fields["seqnum"] = v
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.order
        if v is not None:
            fields["order"] = "({0},{1})".format(v.object_type, v.id)
        v = self.order_id
        if v is not None:
            fields["order_id"] = v
        v = self.status
        if v is not None:
            fields["status"] = v.name
        v = self.clord_id
        if v is not None:
            fields["clord_id"] = v
        v = self.price
        if v is not None:
            fields["price"] = v
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.leaves_qty
        if v is not None:
            fields["leaves_qty"] = v
        v = self.cum_qty
        if v is not None:
            fields["cum_qty"] = v
        v = self.display_qty
        if v is not None:
            fields["display_qty"] = v
        v = self.crfix
        if v is not None:
            fields["crfix"] = "({0},{1})".format(v.object_type, v.id)
        v = self.parent
        if v is not None:
            fields["parent"] = "({0},{1})".format(v.object_type, v.id)
        v = self.child
        if v is not None:
            fields["child"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "sender":
            self.sender = str(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)
        elif field == "seqnum":
            self.seqnum = int(value) if value is not None else value
        elif field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "order_id":
            self.order_id = int(value) if value is not None else value
        elif field == "status":
            self.status = xtypes.OrderFixStatus[value] if value is not None else value
        elif field == "clord_id":
            self.clord_id = str(value) if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "leaves_qty":
            self.leaves_qty = int(value) if value is not None else value
        elif field == "cum_qty":
            self.cum_qty = int(value) if value is not None else value
        elif field == "display_qty":
            self.display_qty = int(value) if value is not None else value
        elif field == "crfix":
            if hasattr(value, "ptr"):
                self.crfix = value
            else:
                self.crfix = str_to_tuple(value)
        elif field == "parent":
            if hasattr(value, "ptr"):
                self.parent = value
            else:
                self.parent = str_to_tuple(value)
        elif field == "child":
            if hasattr(value, "ptr"):
                self.child = value
            else:
                self.child = str_to_tuple(value)

    @property
    def sender(self):
        lib.node().xroad_order_fix_sender_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_sender_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_sender.restype = ctypes.POINTER(xtypes.Sender)
            res = lib.node().xroad_order_fix_get_sender(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sender.setter
    def sender(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_fix_set_sender.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_fix_set_sender(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_fix_reset_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_sender(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_order_fix_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_instr_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_fix_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_fix_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_fix_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_fix_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_fix_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_fix_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_instr(self.__ptr)

    @property
    def seqnum(self):
        lib.node().xroad_order_fix_seqnum_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_seqnum_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_seqnum.restype = ctypes.c_long
            return lib.node().xroad_order_fix_get_seqnum(self.__ptr)
        else:
            return None

    @seqnum.setter
    def seqnum(self, value):
        if value is not None:
            lib.node().xroad_order_fix_set_seqnum.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_fix_set_seqnum(self.__ptr, value)
        else:
            lib.node().xroad_order_fix_reset_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_seqnum(self.__ptr)

    @property
    def node_id(self):
        lib.node().xroad_order_fix_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_node_id_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_order_fix_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_order_fix_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_order_fix_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_order_fix_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_node_id(self.__ptr)

    @property
    def order(self):
        lib.node().xroad_order_fix_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_order_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_fix_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_fix_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_fix_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_fix_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_fix_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_fix_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_order(self.__ptr)

    @property
    def order_id(self):
        lib.node().xroad_order_fix_order_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_order_id_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_order_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_order_id.restype = ctypes.c_long
            return lib.node().xroad_order_fix_get_order_id(self.__ptr)
        else:
            return None

    @order_id.setter
    def order_id(self, value):
        if value is not None:
            lib.node().xroad_order_fix_set_order_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_fix_set_order_id(self.__ptr, value)
        else:
            lib.node().xroad_order_fix_reset_order_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_order_id(self.__ptr)

    @property
    def status(self):
        lib.node().xroad_order_fix_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_status_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_status.restype = ctypes.c_int
            return xtypes.OrderFixStatus(lib.node().xroad_order_fix_get_status(self.__ptr))
        else:
            return None

    @status.setter
    def status(self, value):
        if not isinstance(value, xtypes.OrderFixStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderFixStatus enum".format(value))
        if value is not None:
            lib.node().xroad_order_fix_set_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_fix_set_status(self.__ptr, value.value)
        else:
            lib.node().xroad_order_fix_reset_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_status(self.__ptr)

    @property
    def clord_id(self):
        lib.node().xroad_order_fix_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_clord_id_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_clord_id.restype = ctypes.POINTER(xtypes.ClordId)
            res = lib.node().xroad_order_fix_get_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @clord_id.setter
    def clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_fix_set_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_fix_set_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_fix_reset_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_clord_id(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_order_fix_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_price_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_price.restype = ctypes.c_double
            return lib.node().xroad_order_fix_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_order_fix_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_order_fix_set_price(self.__ptr, value)
        else:
            lib.node().xroad_order_fix_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_price(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_order_fix_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_qty_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_qty.restype = ctypes.c_long
            return lib.node().xroad_order_fix_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_order_fix_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_fix_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_fix_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_qty(self.__ptr)

    @property
    def leaves_qty(self):
        lib.node().xroad_order_fix_leaves_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_leaves_qty_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_leaves_qty.restype = ctypes.c_long
            return lib.node().xroad_order_fix_get_leaves_qty(self.__ptr)
        else:
            return None

    @leaves_qty.setter
    def leaves_qty(self, value):
        if value is not None:
            lib.node().xroad_order_fix_set_leaves_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_fix_set_leaves_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_fix_reset_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_leaves_qty(self.__ptr)

    @property
    def cum_qty(self):
        lib.node().xroad_order_fix_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_cum_qty_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_order_fix_get_cum_qty(self.__ptr)
        else:
            return None

    @cum_qty.setter
    def cum_qty(self, value):
        if value is not None:
            lib.node().xroad_order_fix_set_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_fix_set_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_fix_reset_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_cum_qty(self.__ptr)

    @property
    def display_qty(self):
        lib.node().xroad_order_fix_display_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_display_qty_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_display_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_display_qty.restype = ctypes.c_long
            return lib.node().xroad_order_fix_get_display_qty(self.__ptr)
        else:
            return None

    @display_qty.setter
    def display_qty(self, value):
        if value is not None:
            lib.node().xroad_order_fix_set_display_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_fix_set_display_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_fix_reset_display_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_display_qty(self.__ptr)

    @property
    def crfix(self):
        lib.node().xroad_order_fix_crfix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_crfix_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_crfix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_crfix.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_fix_get_crfix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference crfix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @crfix.setter
    def crfix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_fix_set_crfix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_fix_set_crfix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_fix_set_crfix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_fix_set_crfix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_fix_reset_crfix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_crfix(self.__ptr)

    @property
    def parent(self):
        lib.node().xroad_order_fix_parent_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_parent_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_parent.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_parent.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_fix_get_parent(self.__ptr)
            if not obj:
                raise BrokenRefError("reference parent is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @parent.setter
    def parent(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_fix_set_parent.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_fix_set_parent(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_fix_set_parent_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_fix_set_parent_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_fix_reset_parent.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_parent(self.__ptr)

    @property
    def child(self):
        lib.node().xroad_order_fix_child_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_fix_child_is_set(self.__ptr):
            lib.node().xroad_order_fix_get_child.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_get_child.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_fix_get_child(self.__ptr)
            if not obj:
                raise BrokenRefError("reference child is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @child.setter
    def child(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_fix_set_child.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_fix_set_child(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_fix_set_child_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_fix_set_child_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_fix_reset_child.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_fix_reset_child(self.__ptr)


class ExecReportFix(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_exec_report_fix_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_exec_report_fix_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.exec_report_fix

    @property
    def is_valid(self):
        lib.node().xroad_exec_report_fix_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_exec_report_fix_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_exec_report_fix_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_exec_report_fix_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_exec_report_fix_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_exec_report_fix_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_exec_report_fix_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_exec_report_fix_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_exec_report_fix_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return ExecReportFix(lib.node().xroad_exec_report_fix_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_exec_report_fix_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_exec_report_fix_get_id.restype = ctypes.c_long
        return lib.node().xroad_exec_report_fix_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_exec_report_fix_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_exec_report_fix_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_exec_report_fix_copy(self.__ptr, id)
        return ExecReportFix(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.sender
        if v is not None:
            fields["sender"] = v
        v = self.order_id
        if v is not None:
            fields["order_id"] = v
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.seqnum
        if v is not None:
            fields["seqnum"] = v
        v = self.clord_id
        if v is not None:
            fields["clord_id"] = v
        v = self.orig_clord_id
        if v is not None:
            fields["orig_clord_id"] = v
        v = self.sec_clord_id
        if v is not None:
            fields["sec_clord_id"] = v
        v = self.exec_id
        if v is not None:
            fields["exec_id"] = v
        v = self.exec_type
        if v is not None:
            fields["exec_type"] = v.name
        v = self.ofix
        if v is not None:
            fields["ofix"] = "({0},{1})".format(v.object_type, v.id)
        v = self.order_status
        if v is not None:
            fields["order_status"] = v.name
        v = self.side
        if v is not None:
            fields["side"] = v.name
        v = self.symbol
        if v is not None:
            fields["symbol"] = v
        v = self.cls
        if v is not None:
            fields["cls"] = v
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.price
        if v is not None:
            fields["price"] = v
        v = self.tif
        if v is not None:
            fields["tif"] = v.name
        v = self.exp_date
        if v is not None:
            fields["exp_date"] = v
        v = self.last_qty
        if v is not None:
            fields["last_qty"] = v
        v = self.leaves_qty
        if v is not None:
            fields["leaves_qty"] = v
        v = self.cum_qty
        if v is not None:
            fields["cum_qty"] = v
        v = self.last_px
        if v is not None:
            fields["last_px"] = v
        v = self.tran_time
        if v is not None:
            fields["tran_time"] = v
        v = self.reason
        if v is not None:
            fields["reason"] = v
        v = self.text
        if v is not None:
            fields["text"] = v
        v = self.mleg_report_type
        if v is not None:
            fields["mleg_report_type"] = v.name
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "sender":
            self.sender = str(value) if value is not None else value
        elif field == "order_id":
            self.order_id = int(value) if value is not None else value
        elif field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "seqnum":
            self.seqnum = int(value) if value is not None else value
        elif field == "clord_id":
            self.clord_id = str(value) if value is not None else value
        elif field == "orig_clord_id":
            self.orig_clord_id = str(value) if value is not None else value
        elif field == "sec_clord_id":
            self.sec_clord_id = str(value) if value is not None else value
        elif field == "exec_id":
            self.exec_id = str(value) if value is not None else value
        elif field == "exec_type":
            self.exec_type = xtypes.ExecType[value] if value is not None else value
        elif field == "ofix":
            if hasattr(value, "ptr"):
                self.ofix = value
            else:
                self.ofix = str_to_tuple(value)
        elif field == "order_status":
            self.order_status = xtypes.OrderFixStatus[value] if value is not None else value
        elif field == "side":
            self.side = xtypes.Side[value] if value is not None else value
        elif field == "symbol":
            self.symbol = str(value) if value is not None else value
        elif field == "cls":
            self.cls = str(value) if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "tif":
            self.tif = xtypes.Tif[value] if value is not None else value
        elif field == "exp_date":
            self.exp_date = int(value) if value is not None else value
        elif field == "last_qty":
            self.last_qty = int(value) if value is not None else value
        elif field == "leaves_qty":
            self.leaves_qty = int(value) if value is not None else value
        elif field == "cum_qty":
            self.cum_qty = int(value) if value is not None else value
        elif field == "last_px":
            self.last_px = float(value) if value is not None else value
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value
        elif field == "reason":
            self.reason = int(value) if value is not None else value
        elif field == "text":
            self.text = str(value) if value is not None else value
        elif field == "mleg_report_type":
            self.mleg_report_type = xtypes.MlegReportType[value] if value is not None else value

    @property
    def sender(self):
        lib.node().xroad_exec_report_fix_sender_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_sender_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_sender.restype = ctypes.POINTER(xtypes.Sender)
            res = lib.node().xroad_exec_report_fix_get_sender(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sender.setter
    def sender(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_sender.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_exec_report_fix_set_sender(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_exec_report_fix_reset_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_sender(self.__ptr)

    @property
    def order_id(self):
        lib.node().xroad_exec_report_fix_order_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_order_id_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_order_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_order_id.restype = ctypes.c_long
            return lib.node().xroad_exec_report_fix_get_order_id(self.__ptr)
        else:
            return None

    @order_id.setter
    def order_id(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_order_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_exec_report_fix_set_order_id(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_order_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_order_id(self.__ptr)

    @property
    def node_id(self):
        lib.node().xroad_exec_report_fix_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_node_id_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_exec_report_fix_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_exec_report_fix_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_node_id(self.__ptr)

    @property
    def seqnum(self):
        lib.node().xroad_exec_report_fix_seqnum_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_seqnum_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_seqnum.restype = ctypes.c_long
            return lib.node().xroad_exec_report_fix_get_seqnum(self.__ptr)
        else:
            return None

    @seqnum.setter
    def seqnum(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_seqnum.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_exec_report_fix_set_seqnum(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_seqnum(self.__ptr)

    @property
    def clord_id(self):
        lib.node().xroad_exec_report_fix_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_clord_id_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_clord_id.restype = ctypes.POINTER(xtypes.ClordId)
            res = lib.node().xroad_exec_report_fix_get_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @clord_id.setter
    def clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_exec_report_fix_set_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_exec_report_fix_reset_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_clord_id(self.__ptr)

    @property
    def orig_clord_id(self):
        lib.node().xroad_exec_report_fix_orig_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_orig_clord_id_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_orig_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_orig_clord_id.restype = ctypes.POINTER(xtypes.ClordId)
            res = lib.node().xroad_exec_report_fix_get_orig_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @orig_clord_id.setter
    def orig_clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_orig_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_exec_report_fix_set_orig_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_exec_report_fix_reset_orig_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_orig_clord_id(self.__ptr)

    @property
    def sec_clord_id(self):
        lib.node().xroad_exec_report_fix_sec_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_sec_clord_id_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_sec_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_sec_clord_id.restype = ctypes.POINTER(xtypes.ExtRef)
            res = lib.node().xroad_exec_report_fix_get_sec_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sec_clord_id.setter
    def sec_clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_sec_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_exec_report_fix_set_sec_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_exec_report_fix_reset_sec_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_sec_clord_id(self.__ptr)

    @property
    def exec_id(self):
        lib.node().xroad_exec_report_fix_exec_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_exec_id_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_exec_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_exec_id.restype = ctypes.POINTER(xtypes.ExecId)
            res = lib.node().xroad_exec_report_fix_get_exec_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @exec_id.setter
    def exec_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_exec_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_exec_report_fix_set_exec_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_exec_report_fix_reset_exec_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_exec_id(self.__ptr)

    @property
    def exec_type(self):
        lib.node().xroad_exec_report_fix_exec_type_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_exec_type_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_exec_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_exec_type.restype = ctypes.c_int
            return xtypes.ExecType(lib.node().xroad_exec_report_fix_get_exec_type(self.__ptr))
        else:
            return None

    @exec_type.setter
    def exec_type(self, value):
        if not isinstance(value, xtypes.ExecType) and value is not None:
            raise TypeError("{0} has wrong type. must be ExecType enum".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_exec_type.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_exec_report_fix_set_exec_type(self.__ptr, value.value)
        else:
            lib.node().xroad_exec_report_fix_reset_exec_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_exec_type(self.__ptr)

    @property
    def ofix(self):
        lib.node().xroad_exec_report_fix_ofix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_ofix_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_ofix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_ofix.restype = ctypes.c_void_p
            obj = lib.node().xroad_exec_report_fix_get_ofix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference ofix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @ofix.setter
    def ofix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_exec_report_fix_set_ofix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_exec_report_fix_set_ofix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_exec_report_fix_set_ofix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_exec_report_fix_set_ofix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_exec_report_fix_reset_ofix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_ofix(self.__ptr)

    @property
    def order_status(self):
        lib.node().xroad_exec_report_fix_order_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_order_status_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_order_status.restype = ctypes.c_int
            return xtypes.OrderFixStatus(lib.node().xroad_exec_report_fix_get_order_status(self.__ptr))
        else:
            return None

    @order_status.setter
    def order_status(self, value):
        if not isinstance(value, xtypes.OrderFixStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderFixStatus enum".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_order_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_exec_report_fix_set_order_status(self.__ptr, value.value)
        else:
            lib.node().xroad_exec_report_fix_reset_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_order_status(self.__ptr)

    @property
    def side(self):
        lib.node().xroad_exec_report_fix_side_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_side_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_side.restype = ctypes.c_int
            return xtypes.Side(lib.node().xroad_exec_report_fix_get_side(self.__ptr))
        else:
            return None

    @side.setter
    def side(self, value):
        if not isinstance(value, xtypes.Side) and value is not None:
            raise TypeError("{0} has wrong type. must be Side enum".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_side.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_exec_report_fix_set_side(self.__ptr, value.value)
        else:
            lib.node().xroad_exec_report_fix_reset_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_side(self.__ptr)

    @property
    def symbol(self):
        lib.node().xroad_exec_report_fix_symbol_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_symbol_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_symbol.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_symbol.restype = ctypes.POINTER(xtypes.Alias)
            res = lib.node().xroad_exec_report_fix_get_symbol(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @symbol.setter
    def symbol(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_symbol.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_exec_report_fix_set_symbol(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_exec_report_fix_reset_symbol.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_symbol(self.__ptr)

    @property
    def cls(self):
        lib.node().xroad_exec_report_fix_cls_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_cls_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_cls.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_cls.restype = ctypes.POINTER(xtypes.Cls)
            res = lib.node().xroad_exec_report_fix_get_cls(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @cls.setter
    def cls(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_cls.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_exec_report_fix_set_cls(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_exec_report_fix_reset_cls.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_cls(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_exec_report_fix_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_qty_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_qty.restype = ctypes.c_long
            return lib.node().xroad_exec_report_fix_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_exec_report_fix_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_qty(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_exec_report_fix_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_price_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_price.restype = ctypes.c_double
            return lib.node().xroad_exec_report_fix_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_exec_report_fix_set_price(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_price(self.__ptr)

    @property
    def tif(self):
        lib.node().xroad_exec_report_fix_tif_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_tif_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_tif.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_tif.restype = ctypes.c_int
            return xtypes.Tif(lib.node().xroad_exec_report_fix_get_tif(self.__ptr))
        else:
            return None

    @tif.setter
    def tif(self, value):
        if not isinstance(value, xtypes.Tif) and value is not None:
            raise TypeError("{0} has wrong type. must be Tif enum".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_tif.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_exec_report_fix_set_tif(self.__ptr, value.value)
        else:
            lib.node().xroad_exec_report_fix_reset_tif.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_tif(self.__ptr)

    @property
    def exp_date(self):
        lib.node().xroad_exec_report_fix_exp_date_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_exp_date_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_exp_date.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_exp_date.restype = ctypes.c_ulong
            return lib.node().xroad_exec_report_fix_get_exp_date(self.__ptr)
        else:
            return None

    @exp_date.setter
    def exp_date(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_exp_date.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_exec_report_fix_set_exp_date(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_exp_date.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_exp_date(self.__ptr)

    @property
    def last_qty(self):
        lib.node().xroad_exec_report_fix_last_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_last_qty_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_last_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_last_qty.restype = ctypes.c_long
            return lib.node().xroad_exec_report_fix_get_last_qty(self.__ptr)
        else:
            return None

    @last_qty.setter
    def last_qty(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_last_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_exec_report_fix_set_last_qty(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_last_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_last_qty(self.__ptr)

    @property
    def leaves_qty(self):
        lib.node().xroad_exec_report_fix_leaves_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_leaves_qty_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_leaves_qty.restype = ctypes.c_long
            return lib.node().xroad_exec_report_fix_get_leaves_qty(self.__ptr)
        else:
            return None

    @leaves_qty.setter
    def leaves_qty(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_leaves_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_exec_report_fix_set_leaves_qty(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_leaves_qty(self.__ptr)

    @property
    def cum_qty(self):
        lib.node().xroad_exec_report_fix_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_cum_qty_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_exec_report_fix_get_cum_qty(self.__ptr)
        else:
            return None

    @cum_qty.setter
    def cum_qty(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_exec_report_fix_set_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_cum_qty(self.__ptr)

    @property
    def last_px(self):
        lib.node().xroad_exec_report_fix_last_px_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_last_px_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_last_px.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_last_px.restype = ctypes.c_double
            return lib.node().xroad_exec_report_fix_get_last_px(self.__ptr)
        else:
            return None

    @last_px.setter
    def last_px(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_last_px.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_exec_report_fix_set_last_px(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_last_px.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_last_px(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_exec_report_fix_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_tran_time_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_exec_report_fix_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_exec_report_fix_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_tran_time(self.__ptr)

    @property
    def reason(self):
        lib.node().xroad_exec_report_fix_reason_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_reason_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_reason.restype = ctypes.c_int
            return lib.node().xroad_exec_report_fix_get_reason(self.__ptr)
        else:
            return None

    @reason.setter
    def reason(self, value):
        if value is not None:
            lib.node().xroad_exec_report_fix_set_reason.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_exec_report_fix_set_reason(self.__ptr, value)
        else:
            lib.node().xroad_exec_report_fix_reset_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_reason(self.__ptr)

    @property
    def text(self):
        lib.node().xroad_exec_report_fix_text_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_text_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_text.restype = ctypes.POINTER(xtypes.Text)
            res = lib.node().xroad_exec_report_fix_get_text(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @text.setter
    def text(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_text.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_exec_report_fix_set_text(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_exec_report_fix_reset_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_text(self.__ptr)

    @property
    def mleg_report_type(self):
        lib.node().xroad_exec_report_fix_mleg_report_type_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_exec_report_fix_mleg_report_type_is_set(self.__ptr):
            lib.node().xroad_exec_report_fix_get_mleg_report_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_get_mleg_report_type.restype = ctypes.c_int
            return xtypes.MlegReportType(lib.node().xroad_exec_report_fix_get_mleg_report_type(self.__ptr))
        else:
            return None

    @mleg_report_type.setter
    def mleg_report_type(self, value):
        if not isinstance(value, xtypes.MlegReportType) and value is not None:
            raise TypeError("{0} has wrong type. must be MlegReportType enum".format(value))
        if value is not None:
            lib.node().xroad_exec_report_fix_set_mleg_report_type.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_exec_report_fix_set_mleg_report_type(self.__ptr, value.value)
        else:
            lib.node().xroad_exec_report_fix_reset_mleg_report_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_exec_report_fix_reset_mleg_report_type(self.__ptr)


class CancelRejectFix(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_cancel_reject_fix_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_cancel_reject_fix_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.cancel_reject_fix

    @property
    def is_valid(self):
        lib.node().xroad_cancel_reject_fix_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_cancel_reject_fix_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_cancel_reject_fix_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_cancel_reject_fix_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_cancel_reject_fix_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_cancel_reject_fix_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_cancel_reject_fix_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_cancel_reject_fix_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cancel_reject_fix_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return CancelRejectFix(lib.node().xroad_cancel_reject_fix_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_cancel_reject_fix_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cancel_reject_fix_get_id.restype = ctypes.c_long
        return lib.node().xroad_cancel_reject_fix_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_cancel_reject_fix_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_cancel_reject_fix_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_cancel_reject_fix_copy(self.__ptr, id)
        return CancelRejectFix(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.sender
        if v is not None:
            fields["sender"] = v
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.crfix
        if v is not None:
            fields["crfix"] = "({0},{1})".format(v.object_type, v.id)
        v = self.seqnum
        if v is not None:
            fields["seqnum"] = v
        v = self.status
        if v is not None:
            fields["status"] = v.name
        v = self.clord_id
        if v is not None:
            fields["clord_id"] = v
        v = self.sec_clord_id
        if v is not None:
            fields["sec_clord_id"] = v
        v = self.orig_clord_id
        if v is not None:
            fields["orig_clord_id"] = v
        v = self.response_to
        if v is not None:
            fields["response_to"] = v.name
        v = self.reason
        if v is not None:
            fields["reason"] = v
        v = self.text
        if v is not None:
            fields["text"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "sender":
            self.sender = str(value) if value is not None else value
        elif field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "crfix":
            if hasattr(value, "ptr"):
                self.crfix = value
            else:
                self.crfix = str_to_tuple(value)
        elif field == "seqnum":
            self.seqnum = int(value) if value is not None else value
        elif field == "status":
            self.status = xtypes.OrderFixStatus[value] if value is not None else value
        elif field == "clord_id":
            self.clord_id = str(value) if value is not None else value
        elif field == "sec_clord_id":
            self.sec_clord_id = str(value) if value is not None else value
        elif field == "orig_clord_id":
            self.orig_clord_id = str(value) if value is not None else value
        elif field == "response_to":
            self.response_to = xtypes.RejResponseTo[value] if value is not None else value
        elif field == "reason":
            self.reason = int(value) if value is not None else value
        elif field == "text":
            self.text = str(value) if value is not None else value

    @property
    def sender(self):
        lib.node().xroad_cancel_reject_fix_sender_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_sender_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_sender.restype = ctypes.POINTER(xtypes.Sender)
            res = lib.node().xroad_cancel_reject_fix_get_sender(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sender.setter
    def sender(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_cancel_reject_fix_set_sender.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_cancel_reject_fix_set_sender(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_cancel_reject_fix_reset_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_sender(self.__ptr)

    @property
    def node_id(self):
        lib.node().xroad_cancel_reject_fix_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_node_id_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_cancel_reject_fix_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_cancel_reject_fix_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_cancel_reject_fix_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_cancel_reject_fix_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_node_id(self.__ptr)

    @property
    def crfix(self):
        lib.node().xroad_cancel_reject_fix_crfix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_crfix_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_crfix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_crfix.restype = ctypes.c_void_p
            obj = lib.node().xroad_cancel_reject_fix_get_crfix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference crfix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @crfix.setter
    def crfix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_cancel_reject_fix_set_crfix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_cancel_reject_fix_set_crfix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_cancel_reject_fix_set_crfix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_cancel_reject_fix_set_crfix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_cancel_reject_fix_reset_crfix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_crfix(self.__ptr)

    @property
    def seqnum(self):
        lib.node().xroad_cancel_reject_fix_seqnum_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_seqnum_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_seqnum.restype = ctypes.c_long
            return lib.node().xroad_cancel_reject_fix_get_seqnum(self.__ptr)
        else:
            return None

    @seqnum.setter
    def seqnum(self, value):
        if value is not None:
            lib.node().xroad_cancel_reject_fix_set_seqnum.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_cancel_reject_fix_set_seqnum(self.__ptr, value)
        else:
            lib.node().xroad_cancel_reject_fix_reset_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_seqnum(self.__ptr)

    @property
    def status(self):
        lib.node().xroad_cancel_reject_fix_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_status_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_status.restype = ctypes.c_int
            return xtypes.OrderFixStatus(lib.node().xroad_cancel_reject_fix_get_status(self.__ptr))
        else:
            return None

    @status.setter
    def status(self, value):
        if not isinstance(value, xtypes.OrderFixStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderFixStatus enum".format(value))
        if value is not None:
            lib.node().xroad_cancel_reject_fix_set_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_cancel_reject_fix_set_status(self.__ptr, value.value)
        else:
            lib.node().xroad_cancel_reject_fix_reset_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_status(self.__ptr)

    @property
    def clord_id(self):
        lib.node().xroad_cancel_reject_fix_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_clord_id_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_clord_id.restype = ctypes.POINTER(xtypes.ClordId)
            res = lib.node().xroad_cancel_reject_fix_get_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @clord_id.setter
    def clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_cancel_reject_fix_set_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_cancel_reject_fix_set_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_cancel_reject_fix_reset_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_clord_id(self.__ptr)

    @property
    def sec_clord_id(self):
        lib.node().xroad_cancel_reject_fix_sec_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_sec_clord_id_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_sec_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_sec_clord_id.restype = ctypes.POINTER(xtypes.ExtRef)
            res = lib.node().xroad_cancel_reject_fix_get_sec_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sec_clord_id.setter
    def sec_clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_cancel_reject_fix_set_sec_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_cancel_reject_fix_set_sec_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_cancel_reject_fix_reset_sec_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_sec_clord_id(self.__ptr)

    @property
    def orig_clord_id(self):
        lib.node().xroad_cancel_reject_fix_orig_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_orig_clord_id_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_orig_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_orig_clord_id.restype = ctypes.POINTER(xtypes.ClordId)
            res = lib.node().xroad_cancel_reject_fix_get_orig_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @orig_clord_id.setter
    def orig_clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_cancel_reject_fix_set_orig_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_cancel_reject_fix_set_orig_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_cancel_reject_fix_reset_orig_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_orig_clord_id(self.__ptr)

    @property
    def response_to(self):
        lib.node().xroad_cancel_reject_fix_response_to_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_response_to_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_response_to.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_response_to.restype = ctypes.c_int
            return xtypes.RejResponseTo(lib.node().xroad_cancel_reject_fix_get_response_to(self.__ptr))
        else:
            return None

    @response_to.setter
    def response_to(self, value):
        if not isinstance(value, xtypes.RejResponseTo) and value is not None:
            raise TypeError("{0} has wrong type. must be RejResponseTo enum".format(value))
        if value is not None:
            lib.node().xroad_cancel_reject_fix_set_response_to.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_cancel_reject_fix_set_response_to(self.__ptr, value.value)
        else:
            lib.node().xroad_cancel_reject_fix_reset_response_to.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_response_to(self.__ptr)

    @property
    def reason(self):
        lib.node().xroad_cancel_reject_fix_reason_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_reason_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_reason.restype = ctypes.c_int
            return lib.node().xroad_cancel_reject_fix_get_reason(self.__ptr)
        else:
            return None

    @reason.setter
    def reason(self, value):
        if value is not None:
            lib.node().xroad_cancel_reject_fix_set_reason.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_cancel_reject_fix_set_reason(self.__ptr, value)
        else:
            lib.node().xroad_cancel_reject_fix_reset_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_reason(self.__ptr)

    @property
    def text(self):
        lib.node().xroad_cancel_reject_fix_text_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_reject_fix_text_is_set(self.__ptr):
            lib.node().xroad_cancel_reject_fix_get_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_get_text.restype = ctypes.POINTER(xtypes.Text)
            res = lib.node().xroad_cancel_reject_fix_get_text(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @text.setter
    def text(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_cancel_reject_fix_set_text.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_cancel_reject_fix_set_text(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_cancel_reject_fix_reset_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reject_fix_reset_text(self.__ptr)


class RejectFix(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_reject_fix_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_reject_fix_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.reject_fix

    @property
    def is_valid(self):
        lib.node().xroad_reject_fix_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_reject_fix_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_reject_fix_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_reject_fix_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_reject_fix_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_reject_fix_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_reject_fix_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_reject_fix_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_reject_fix_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return RejectFix(lib.node().xroad_reject_fix_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_reject_fix_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_reject_fix_get_id.restype = ctypes.c_long
        return lib.node().xroad_reject_fix_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_reject_fix_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_reject_fix_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_reject_fix_copy(self.__ptr, id)
        return RejectFix(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.seqnum
        if v is not None:
            fields["seqnum"] = v
        v = self.ref_seqnum
        if v is not None:
            fields["ref_seqnum"] = v
        v = self.reason
        if v is not None:
            fields["reason"] = v
        v = self.text
        if v is not None:
            fields["text"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "seqnum":
            self.seqnum = int(value) if value is not None else value
        elif field == "ref_seqnum":
            self.ref_seqnum = int(value) if value is not None else value
        elif field == "reason":
            self.reason = int(value) if value is not None else value
        elif field == "text":
            self.text = str(value) if value is not None else value

    @property
    def node_id(self):
        lib.node().xroad_reject_fix_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_reject_fix_node_id_is_set(self.__ptr):
            lib.node().xroad_reject_fix_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reject_fix_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_reject_fix_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_reject_fix_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_reject_fix_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_reject_fix_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reject_fix_reset_node_id(self.__ptr)

    @property
    def seqnum(self):
        lib.node().xroad_reject_fix_seqnum_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_reject_fix_seqnum_is_set(self.__ptr):
            lib.node().xroad_reject_fix_get_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reject_fix_get_seqnum.restype = ctypes.c_long
            return lib.node().xroad_reject_fix_get_seqnum(self.__ptr)
        else:
            return None

    @seqnum.setter
    def seqnum(self, value):
        if value is not None:
            lib.node().xroad_reject_fix_set_seqnum.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_reject_fix_set_seqnum(self.__ptr, value)
        else:
            lib.node().xroad_reject_fix_reset_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reject_fix_reset_seqnum(self.__ptr)

    @property
    def ref_seqnum(self):
        lib.node().xroad_reject_fix_ref_seqnum_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_reject_fix_ref_seqnum_is_set(self.__ptr):
            lib.node().xroad_reject_fix_get_ref_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reject_fix_get_ref_seqnum.restype = ctypes.c_long
            return lib.node().xroad_reject_fix_get_ref_seqnum(self.__ptr)
        else:
            return None

    @ref_seqnum.setter
    def ref_seqnum(self, value):
        if value is not None:
            lib.node().xroad_reject_fix_set_ref_seqnum.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_reject_fix_set_ref_seqnum(self.__ptr, value)
        else:
            lib.node().xroad_reject_fix_reset_ref_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reject_fix_reset_ref_seqnum(self.__ptr)

    @property
    def reason(self):
        lib.node().xroad_reject_fix_reason_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_reject_fix_reason_is_set(self.__ptr):
            lib.node().xroad_reject_fix_get_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reject_fix_get_reason.restype = ctypes.c_int
            return lib.node().xroad_reject_fix_get_reason(self.__ptr)
        else:
            return None

    @reason.setter
    def reason(self, value):
        if value is not None:
            lib.node().xroad_reject_fix_set_reason.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_reject_fix_set_reason(self.__ptr, value)
        else:
            lib.node().xroad_reject_fix_reset_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reject_fix_reset_reason(self.__ptr)

    @property
    def text(self):
        lib.node().xroad_reject_fix_text_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_reject_fix_text_is_set(self.__ptr):
            lib.node().xroad_reject_fix_get_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reject_fix_get_text.restype = ctypes.POINTER(xtypes.Text)
            res = lib.node().xroad_reject_fix_get_text(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @text.setter
    def text(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_reject_fix_set_text.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_reject_fix_set_text(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_reject_fix_reset_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_reject_fix_reset_text(self.__ptr)


class CancelFix(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_cancel_fix_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_cancel_fix_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.cancel_fix

    @property
    def is_valid(self):
        lib.node().xroad_cancel_fix_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_cancel_fix_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_cancel_fix_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_cancel_fix_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_cancel_fix_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_cancel_fix_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_cancel_fix_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_cancel_fix_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cancel_fix_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return CancelFix(lib.node().xroad_cancel_fix_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_cancel_fix_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cancel_fix_get_id.restype = ctypes.c_long
        return lib.node().xroad_cancel_fix_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_cancel_fix_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_cancel_fix_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_cancel_fix_copy(self.__ptr, id)
        return CancelFix(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.ofix
        if v is not None:
            fields["ofix"] = "({0},{1})".format(v.object_type, v.id)
        v = self.seqnum
        if v is not None:
            fields["seqnum"] = v
        v = self.clord_id
        if v is not None:
            fields["clord_id"] = v
        v = self.orig_clord_id
        if v is not None:
            fields["orig_clord_id"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "ofix":
            if hasattr(value, "ptr"):
                self.ofix = value
            else:
                self.ofix = str_to_tuple(value)
        elif field == "seqnum":
            self.seqnum = int(value) if value is not None else value
        elif field == "clord_id":
            self.clord_id = str(value) if value is not None else value
        elif field == "orig_clord_id":
            self.orig_clord_id = str(value) if value is not None else value

    @property
    def ofix(self):
        lib.node().xroad_cancel_fix_ofix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_fix_ofix_is_set(self.__ptr):
            lib.node().xroad_cancel_fix_get_ofix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_fix_get_ofix.restype = ctypes.c_void_p
            obj = lib.node().xroad_cancel_fix_get_ofix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference ofix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @ofix.setter
    def ofix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_cancel_fix_set_ofix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_cancel_fix_set_ofix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_cancel_fix_set_ofix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_cancel_fix_set_ofix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_cancel_fix_reset_ofix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_fix_reset_ofix(self.__ptr)

    @property
    def seqnum(self):
        lib.node().xroad_cancel_fix_seqnum_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_fix_seqnum_is_set(self.__ptr):
            lib.node().xroad_cancel_fix_get_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_fix_get_seqnum.restype = ctypes.c_long
            return lib.node().xroad_cancel_fix_get_seqnum(self.__ptr)
        else:
            return None

    @seqnum.setter
    def seqnum(self, value):
        if value is not None:
            lib.node().xroad_cancel_fix_set_seqnum.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_cancel_fix_set_seqnum(self.__ptr, value)
        else:
            lib.node().xroad_cancel_fix_reset_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_fix_reset_seqnum(self.__ptr)

    @property
    def clord_id(self):
        lib.node().xroad_cancel_fix_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_fix_clord_id_is_set(self.__ptr):
            lib.node().xroad_cancel_fix_get_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_fix_get_clord_id.restype = ctypes.POINTER(xtypes.ClordId)
            res = lib.node().xroad_cancel_fix_get_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @clord_id.setter
    def clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_cancel_fix_set_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_cancel_fix_set_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_cancel_fix_reset_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_fix_reset_clord_id(self.__ptr)

    @property
    def orig_clord_id(self):
        lib.node().xroad_cancel_fix_orig_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_fix_orig_clord_id_is_set(self.__ptr):
            lib.node().xroad_cancel_fix_get_orig_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_fix_get_orig_clord_id.restype = ctypes.POINTER(xtypes.ClordId)
            res = lib.node().xroad_cancel_fix_get_orig_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @orig_clord_id.setter
    def orig_clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_cancel_fix_set_orig_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_cancel_fix_set_orig_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_cancel_fix_reset_orig_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_fix_reset_orig_clord_id(self.__ptr)


class ReplaceFix(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_replace_fix_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_replace_fix_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.replace_fix

    @property
    def is_valid(self):
        lib.node().xroad_replace_fix_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_replace_fix_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_replace_fix_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_replace_fix_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_replace_fix_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_replace_fix_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_replace_fix_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_replace_fix_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_replace_fix_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return ReplaceFix(lib.node().xroad_replace_fix_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_replace_fix_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_replace_fix_get_id.restype = ctypes.c_long
        return lib.node().xroad_replace_fix_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_replace_fix_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_replace_fix_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_replace_fix_copy(self.__ptr, id)
        return ReplaceFix(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.ofix
        if v is not None:
            fields["ofix"] = "({0},{1})".format(v.object_type, v.id)
        v = self.seqnum
        if v is not None:
            fields["seqnum"] = v
        v = self.clord_id
        if v is not None:
            fields["clord_id"] = v
        v = self.orig_clord_id
        if v is not None:
            fields["orig_clord_id"] = v
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.price
        if v is not None:
            fields["price"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "ofix":
            if hasattr(value, "ptr"):
                self.ofix = value
            else:
                self.ofix = str_to_tuple(value)
        elif field == "seqnum":
            self.seqnum = int(value) if value is not None else value
        elif field == "clord_id":
            self.clord_id = str(value) if value is not None else value
        elif field == "orig_clord_id":
            self.orig_clord_id = str(value) if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value

    @property
    def ofix(self):
        lib.node().xroad_replace_fix_ofix_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_fix_ofix_is_set(self.__ptr):
            lib.node().xroad_replace_fix_get_ofix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_get_ofix.restype = ctypes.c_void_p
            obj = lib.node().xroad_replace_fix_get_ofix(self.__ptr)
            if not obj:
                raise BrokenRefError("reference ofix is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @ofix.setter
    def ofix(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_replace_fix_set_ofix.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_replace_fix_set_ofix(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_replace_fix_set_ofix_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_replace_fix_set_ofix_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_replace_fix_reset_ofix.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_reset_ofix(self.__ptr)

    @property
    def seqnum(self):
        lib.node().xroad_replace_fix_seqnum_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_fix_seqnum_is_set(self.__ptr):
            lib.node().xroad_replace_fix_get_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_get_seqnum.restype = ctypes.c_long
            return lib.node().xroad_replace_fix_get_seqnum(self.__ptr)
        else:
            return None

    @seqnum.setter
    def seqnum(self, value):
        if value is not None:
            lib.node().xroad_replace_fix_set_seqnum.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replace_fix_set_seqnum(self.__ptr, value)
        else:
            lib.node().xroad_replace_fix_reset_seqnum.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_reset_seqnum(self.__ptr)

    @property
    def clord_id(self):
        lib.node().xroad_replace_fix_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_fix_clord_id_is_set(self.__ptr):
            lib.node().xroad_replace_fix_get_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_get_clord_id.restype = ctypes.POINTER(xtypes.ClordId)
            res = lib.node().xroad_replace_fix_get_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @clord_id.setter
    def clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_replace_fix_set_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_replace_fix_set_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_replace_fix_reset_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_reset_clord_id(self.__ptr)

    @property
    def orig_clord_id(self):
        lib.node().xroad_replace_fix_orig_clord_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_fix_orig_clord_id_is_set(self.__ptr):
            lib.node().xroad_replace_fix_get_orig_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_get_orig_clord_id.restype = ctypes.POINTER(xtypes.ClordId)
            res = lib.node().xroad_replace_fix_get_orig_clord_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @orig_clord_id.setter
    def orig_clord_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_replace_fix_set_orig_clord_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_replace_fix_set_orig_clord_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_replace_fix_reset_orig_clord_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_reset_orig_clord_id(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_replace_fix_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_fix_qty_is_set(self.__ptr):
            lib.node().xroad_replace_fix_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_get_qty.restype = ctypes.c_long
            return lib.node().xroad_replace_fix_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_replace_fix_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replace_fix_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_replace_fix_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_reset_qty(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_replace_fix_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_fix_price_is_set(self.__ptr):
            lib.node().xroad_replace_fix_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_get_price.restype = ctypes.c_double
            return lib.node().xroad_replace_fix_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_replace_fix_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_replace_fix_set_price(self.__ptr, value)
        else:
            lib.node().xroad_replace_fix_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_fix_reset_price(self.__ptr)


class Cancel(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_cancel_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_cancel_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_cancel_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.cancel

    @property
    def is_valid(self):
        lib.node().xroad_cancel_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_cancel_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_cancel_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_cancel_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_cancel_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_cancel_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_cancel_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_cancel_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cancel_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Cancel(lib.node().xroad_cancel_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)

    @property
    def order(self):
        lib.node().xroad_cancel_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_order_is_set(self.__ptr):
            lib.node().xroad_cancel_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_cancel_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_cancel_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_cancel_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_cancel_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_cancel_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_cancel_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_reset_order(self.__ptr)


class Remove(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_remove_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_remove_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_remove_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_remove_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.remove

    @property
    def is_valid(self):
        lib.node().xroad_remove_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_remove_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_remove_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_remove_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_remove_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_remove_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_remove_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_remove_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_remove_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Remove(lib.node().xroad_remove_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)

    @property
    def order(self):
        lib.node().xroad_remove_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_remove_order_is_set(self.__ptr):
            lib.node().xroad_remove_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_remove_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_remove_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_remove_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_remove_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_remove_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_remove_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_remove_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_remove_reset_order(self.__ptr)


class Replace(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_replace_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_replace_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.replace

    @property
    def is_valid(self):
        lib.node().xroad_replace_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_replace_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_replace_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_replace_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_replace_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_replace_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_replace_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_replace_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_replace_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Replace(lib.node().xroad_replace_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_replace_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_replace_get_id.restype = ctypes.c_long
        return lib.node().xroad_replace_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_replace_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_replace_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_replace_copy(self.__ptr, id)
        return Replace(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.order
        if v is not None:
            fields["order"] = "({0},{1})".format(v.object_type, v.id)
        v = self.price
        if v is not None:
            fields["price"] = v
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.hedge_cur
        if v is not None:
            fields["hedge_cur"] = v.name
        v = self.algo
        if v is not None:
            fields["algo"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "hedge_cur":
            self.hedge_cur = xtypes.Currency[value] if value is not None else value
        elif field == "algo":
            if hasattr(value, "ptr"):
                self.algo = value
            else:
                self.algo = str_to_tuple(value)

    @property
    def order(self):
        lib.node().xroad_replace_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_order_is_set(self.__ptr):
            lib.node().xroad_replace_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_replace_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_replace_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_replace_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_replace_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_replace_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_replace_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_reset_order(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_replace_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_price_is_set(self.__ptr):
            lib.node().xroad_replace_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_get_price.restype = ctypes.c_double
            return lib.node().xroad_replace_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_replace_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_replace_set_price(self.__ptr, value)
        else:
            lib.node().xroad_replace_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_reset_price(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_replace_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_qty_is_set(self.__ptr):
            lib.node().xroad_replace_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_get_qty.restype = ctypes.c_long
            return lib.node().xroad_replace_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_replace_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replace_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_replace_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_reset_qty(self.__ptr)

    @property
    def hedge_cur(self):
        lib.node().xroad_replace_hedge_cur_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_hedge_cur_is_set(self.__ptr):
            lib.node().xroad_replace_get_hedge_cur.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_get_hedge_cur.restype = ctypes.c_int
            return xtypes.Currency(lib.node().xroad_replace_get_hedge_cur(self.__ptr))
        else:
            return None

    @hedge_cur.setter
    def hedge_cur(self, value):
        if not isinstance(value, xtypes.Currency) and value is not None:
            raise TypeError("{0} has wrong type. must be Currency enum".format(value))
        if value is not None:
            lib.node().xroad_replace_set_hedge_cur.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_replace_set_hedge_cur(self.__ptr, value.value)
        else:
            lib.node().xroad_replace_reset_hedge_cur.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_reset_hedge_cur(self.__ptr)

    @property
    def algo(self):
        lib.node().xroad_replace_algo_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_algo_is_set(self.__ptr):
            lib.node().xroad_replace_get_algo.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_get_algo.restype = ctypes.c_void_p
            obj = lib.node().xroad_replace_get_algo(self.__ptr)
            if not obj:
                raise BrokenRefError("reference algo is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @algo.setter
    def algo(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_replace_set_algo.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_replace_set_algo(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_replace_set_algo_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_replace_set_algo_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_replace_reset_algo.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_reset_algo(self.__ptr)


class Accepted(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_accepted_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_accepted_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_accepted_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_accepted_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.accepted

    @property
    def is_valid(self):
        lib.node().xroad_accepted_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_accepted_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_accepted_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_accepted_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_accepted_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_accepted_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_accepted_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_accepted_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_accepted_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Accepted(lib.node().xroad_accepted_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value
        elif field == "exch_id":
            self.exch_id = int(value) if value is not None else value
        elif field == "order_status":
            self.order_status = xtypes.OrderStatus[value] if value is not None else value

    @property
    def order(self):
        lib.node().xroad_accepted_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_accepted_order_is_set(self.__ptr):
            lib.node().xroad_accepted_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_accepted_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_accepted_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_accepted_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_accepted_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_accepted_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_accepted_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_accepted_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_accepted_reset_order(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_accepted_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_accepted_tran_time_is_set(self.__ptr):
            lib.node().xroad_accepted_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_accepted_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_accepted_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_accepted_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_accepted_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_accepted_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_accepted_reset_tran_time(self.__ptr)

    @property
    def exch_id(self):
        lib.node().xroad_accepted_exch_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_accepted_exch_id_is_set(self.__ptr):
            lib.node().xroad_accepted_get_exch_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_accepted_get_exch_id.restype = ctypes.c_long
            return lib.node().xroad_accepted_get_exch_id(self.__ptr)
        else:
            return None

    @exch_id.setter
    def exch_id(self, value):
        if value is not None:
            lib.node().xroad_accepted_set_exch_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_accepted_set_exch_id(self.__ptr, value)
        else:
            lib.node().xroad_accepted_reset_exch_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_accepted_reset_exch_id(self.__ptr)

    @property
    def order_status(self):
        lib.node().xroad_accepted_order_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_accepted_order_status_is_set(self.__ptr):
            lib.node().xroad_accepted_get_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_accepted_get_order_status.restype = ctypes.c_int
            return xtypes.OrderStatus(lib.node().xroad_accepted_get_order_status(self.__ptr))
        else:
            return None

    @order_status.setter
    def order_status(self, value):
        if not isinstance(value, xtypes.OrderStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderStatus enum".format(value))
        if value is not None:
            lib.node().xroad_accepted_set_order_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_accepted_set_order_status(self.__ptr, value.value)
        else:
            lib.node().xroad_accepted_reset_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_accepted_reset_order_status(self.__ptr)


class Rejected(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_rejected_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rejected_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_rejected_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_rejected_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.rejected

    @property
    def is_valid(self):
        lib.node().xroad_rejected_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_rejected_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_rejected_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_rejected_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_rejected_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_rejected_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_rejected_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_rejected_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_rejected_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Rejected(lib.node().xroad_rejected_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value
        elif field == "reason":
            self.reason = xtypes.RejReason[value] if value is not None else value
        elif field == "text":
            self.text = str(value) if value is not None else value

    @property
    def order(self):
        lib.node().xroad_rejected_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rejected_order_is_set(self.__ptr):
            lib.node().xroad_rejected_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rejected_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_rejected_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_rejected_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_rejected_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_rejected_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_rejected_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_rejected_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rejected_reset_order(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_rejected_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rejected_tran_time_is_set(self.__ptr):
            lib.node().xroad_rejected_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rejected_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_rejected_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_rejected_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_rejected_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_rejected_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rejected_reset_tran_time(self.__ptr)

    @property
    def reason(self):
        lib.node().xroad_rejected_reason_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rejected_reason_is_set(self.__ptr):
            lib.node().xroad_rejected_get_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rejected_get_reason.restype = ctypes.c_int
            return xtypes.RejReason(lib.node().xroad_rejected_get_reason(self.__ptr))
        else:
            return None

    @reason.setter
    def reason(self, value):
        if not isinstance(value, xtypes.RejReason) and value is not None:
            raise TypeError("{0} has wrong type. must be RejReason enum".format(value))
        if value is not None:
            lib.node().xroad_rejected_set_reason.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rejected_set_reason(self.__ptr, value.value)
        else:
            lib.node().xroad_rejected_reset_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rejected_reset_reason(self.__ptr)

    @property
    def text(self):
        lib.node().xroad_rejected_text_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rejected_text_is_set(self.__ptr):
            lib.node().xroad_rejected_get_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rejected_get_text.restype = ctypes.POINTER(xtypes.Text)
            res = lib.node().xroad_rejected_get_text(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @text.setter
    def text(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_rejected_set_text.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_rejected_set_text(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_rejected_reset_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rejected_reset_text(self.__ptr)


class Expired(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_expired_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_expired_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_expired_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_expired_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.expired

    @property
    def is_valid(self):
        lib.node().xroad_expired_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_expired_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_expired_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_expired_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_expired_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_expired_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_expired_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_expired_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_expired_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Expired(lib.node().xroad_expired_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value

    @property
    def order(self):
        lib.node().xroad_expired_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_expired_order_is_set(self.__ptr):
            lib.node().xroad_expired_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_expired_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_expired_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_expired_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_expired_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_expired_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_expired_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_expired_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_expired_reset_order(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_expired_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_expired_tran_time_is_set(self.__ptr):
            lib.node().xroad_expired_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_expired_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_expired_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_expired_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_expired_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_expired_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_expired_reset_tran_time(self.__ptr)


class Canceled(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_canceled_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_canceled_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_canceled_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_canceled_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.canceled

    @property
    def is_valid(self):
        lib.node().xroad_canceled_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_canceled_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_canceled_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_canceled_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_canceled_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_canceled_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_canceled_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_canceled_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_canceled_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Canceled(lib.node().xroad_canceled_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value

    @property
    def order(self):
        lib.node().xroad_canceled_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_canceled_order_is_set(self.__ptr):
            lib.node().xroad_canceled_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_canceled_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_canceled_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_canceled_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_canceled_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_canceled_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_canceled_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_canceled_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_canceled_reset_order(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_canceled_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_canceled_tran_time_is_set(self.__ptr):
            lib.node().xroad_canceled_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_canceled_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_canceled_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_canceled_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_canceled_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_canceled_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_canceled_reset_tran_time(self.__ptr)


class Trade(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_trade_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_trade_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.trade

    @property
    def is_valid(self):
        lib.node().xroad_trade_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_trade_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_trade_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_trade_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_trade_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_trade_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_trade_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_trade_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_trade_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Trade(lib.node().xroad_trade_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_trade_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_trade_get_id.restype = ctypes.c_long
        return lib.node().xroad_trade_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_trade_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_trade_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_trade_copy(self.__ptr, id)
        return Trade(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.order
        if v is not None:
            fields["order"] = "({0},{1})".format(v.object_type, v.id)
        v = self.tran_time
        if v is not None:
            fields["tran_time"] = v
        v = self.exch_id
        if v is not None:
            fields["exch_id"] = v
        v = self.opp_order
        if v is not None:
            fields["opp_order"] = "({0},{1})".format(v.object_type, v.id)
        v = self.order_status
        if v is not None:
            fields["order_status"] = v.name
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.leaves_qty
        if v is not None:
            fields["leaves_qty"] = v
        v = self.cum_qty
        if v is not None:
            fields["cum_qty"] = v
        v = self.price
        if v is not None:
            fields["price"] = v
        v = self.next
        if v is not None:
            fields["next"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value
        elif field == "exch_id":
            self.exch_id = int(value) if value is not None else value
        elif field == "opp_order":
            if hasattr(value, "ptr"):
                self.opp_order = value
            else:
                self.opp_order = str_to_tuple(value)
        elif field == "order_status":
            self.order_status = xtypes.OrderStatus[value] if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "leaves_qty":
            self.leaves_qty = int(value) if value is not None else value
        elif field == "cum_qty":
            self.cum_qty = int(value) if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "next":
            if hasattr(value, "ptr"):
                self.next = value
            else:
                self.next = str_to_tuple(value)

    @property
    def order(self):
        lib.node().xroad_trade_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trade_order_is_set(self.__ptr):
            lib.node().xroad_trade_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_trade_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_trade_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_trade_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_trade_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_trade_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_trade_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_reset_order(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_trade_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trade_tran_time_is_set(self.__ptr):
            lib.node().xroad_trade_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_trade_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_trade_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_trade_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_trade_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_reset_tran_time(self.__ptr)

    @property
    def exch_id(self):
        lib.node().xroad_trade_exch_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trade_exch_id_is_set(self.__ptr):
            lib.node().xroad_trade_get_exch_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_get_exch_id.restype = ctypes.c_long
            return lib.node().xroad_trade_get_exch_id(self.__ptr)
        else:
            return None

    @exch_id.setter
    def exch_id(self, value):
        if value is not None:
            lib.node().xroad_trade_set_exch_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_trade_set_exch_id(self.__ptr, value)
        else:
            lib.node().xroad_trade_reset_exch_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_reset_exch_id(self.__ptr)

    @property
    def opp_order(self):
        lib.node().xroad_trade_opp_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trade_opp_order_is_set(self.__ptr):
            lib.node().xroad_trade_get_opp_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_get_opp_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_trade_get_opp_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference opp_order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @opp_order.setter
    def opp_order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_trade_set_opp_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_trade_set_opp_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_trade_set_opp_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_trade_set_opp_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_trade_reset_opp_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_reset_opp_order(self.__ptr)

    @property
    def order_status(self):
        lib.node().xroad_trade_order_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trade_order_status_is_set(self.__ptr):
            lib.node().xroad_trade_get_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_get_order_status.restype = ctypes.c_int
            return xtypes.OrderStatus(lib.node().xroad_trade_get_order_status(self.__ptr))
        else:
            return None

    @order_status.setter
    def order_status(self, value):
        if not isinstance(value, xtypes.OrderStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderStatus enum".format(value))
        if value is not None:
            lib.node().xroad_trade_set_order_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_trade_set_order_status(self.__ptr, value.value)
        else:
            lib.node().xroad_trade_reset_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_reset_order_status(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_trade_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trade_qty_is_set(self.__ptr):
            lib.node().xroad_trade_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_get_qty.restype = ctypes.c_long
            return lib.node().xroad_trade_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_trade_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_trade_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_trade_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_reset_qty(self.__ptr)

    @property
    def leaves_qty(self):
        lib.node().xroad_trade_leaves_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trade_leaves_qty_is_set(self.__ptr):
            lib.node().xroad_trade_get_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_get_leaves_qty.restype = ctypes.c_long
            return lib.node().xroad_trade_get_leaves_qty(self.__ptr)
        else:
            return None

    @leaves_qty.setter
    def leaves_qty(self, value):
        if value is not None:
            lib.node().xroad_trade_set_leaves_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_trade_set_leaves_qty(self.__ptr, value)
        else:
            lib.node().xroad_trade_reset_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_reset_leaves_qty(self.__ptr)

    @property
    def cum_qty(self):
        lib.node().xroad_trade_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trade_cum_qty_is_set(self.__ptr):
            lib.node().xroad_trade_get_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_get_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_trade_get_cum_qty(self.__ptr)
        else:
            return None

    @cum_qty.setter
    def cum_qty(self, value):
        if value is not None:
            lib.node().xroad_trade_set_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_trade_set_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_trade_reset_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_reset_cum_qty(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_trade_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trade_price_is_set(self.__ptr):
            lib.node().xroad_trade_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_get_price.restype = ctypes.c_double
            return lib.node().xroad_trade_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_trade_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_trade_set_price(self.__ptr, value)
        else:
            lib.node().xroad_trade_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_reset_price(self.__ptr)

    @property
    def next(self):
        lib.node().xroad_trade_next_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trade_next_is_set(self.__ptr):
            lib.node().xroad_trade_get_next.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_get_next.restype = ctypes.c_void_p
            obj = lib.node().xroad_trade_get_next(self.__ptr)
            if not obj:
                raise BrokenRefError("reference next is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @next.setter
    def next(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_trade_set_next.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_trade_set_next(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_trade_set_next_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_trade_set_next_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_trade_reset_next.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trade_reset_next(self.__ptr)


class CancelRejected(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_cancel_rejected_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_rejected_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_cancel_rejected_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_cancel_rejected_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.cancel_rejected

    @property
    def is_valid(self):
        lib.node().xroad_cancel_rejected_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_cancel_rejected_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_cancel_rejected_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_cancel_rejected_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_cancel_rejected_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_cancel_rejected_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_cancel_rejected_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_cancel_rejected_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_cancel_rejected_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return CancelRejected(lib.node().xroad_cancel_rejected_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "order_status":
            self.order_status = xtypes.OrderStatus[value] if value is not None else value
        elif field == "reason":
            self.reason = xtypes.RejReason[value] if value is not None else value
        elif field == "text":
            self.text = str(value) if value is not None else value

    @property
    def order(self):
        lib.node().xroad_cancel_rejected_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_rejected_order_is_set(self.__ptr):
            lib.node().xroad_cancel_rejected_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_rejected_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_cancel_rejected_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_cancel_rejected_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_cancel_rejected_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_cancel_rejected_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_cancel_rejected_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_cancel_rejected_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_rejected_reset_order(self.__ptr)

    @property
    def order_status(self):
        lib.node().xroad_cancel_rejected_order_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_rejected_order_status_is_set(self.__ptr):
            lib.node().xroad_cancel_rejected_get_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_rejected_get_order_status.restype = ctypes.c_int
            return xtypes.OrderStatus(lib.node().xroad_cancel_rejected_get_order_status(self.__ptr))
        else:
            return None

    @order_status.setter
    def order_status(self, value):
        if not isinstance(value, xtypes.OrderStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderStatus enum".format(value))
        if value is not None:
            lib.node().xroad_cancel_rejected_set_order_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_cancel_rejected_set_order_status(self.__ptr, value.value)
        else:
            lib.node().xroad_cancel_rejected_reset_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_rejected_reset_order_status(self.__ptr)

    @property
    def reason(self):
        lib.node().xroad_cancel_rejected_reason_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_rejected_reason_is_set(self.__ptr):
            lib.node().xroad_cancel_rejected_get_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_rejected_get_reason.restype = ctypes.c_int
            return xtypes.RejReason(lib.node().xroad_cancel_rejected_get_reason(self.__ptr))
        else:
            return None

    @reason.setter
    def reason(self, value):
        if not isinstance(value, xtypes.RejReason) and value is not None:
            raise TypeError("{0} has wrong type. must be RejReason enum".format(value))
        if value is not None:
            lib.node().xroad_cancel_rejected_set_reason.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_cancel_rejected_set_reason(self.__ptr, value.value)
        else:
            lib.node().xroad_cancel_rejected_reset_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_rejected_reset_reason(self.__ptr)

    @property
    def text(self):
        lib.node().xroad_cancel_rejected_text_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_cancel_rejected_text_is_set(self.__ptr):
            lib.node().xroad_cancel_rejected_get_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_rejected_get_text.restype = ctypes.POINTER(xtypes.Text)
            res = lib.node().xroad_cancel_rejected_get_text(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @text.setter
    def text(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_cancel_rejected_set_text.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_cancel_rejected_set_text(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_cancel_rejected_reset_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_cancel_rejected_reset_text(self.__ptr)


class ReplaceRejected(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_replace_rejected_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_replace_rejected_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_replace_rejected_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.replace_rejected

    @property
    def is_valid(self):
        lib.node().xroad_replace_rejected_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_replace_rejected_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_replace_rejected_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_replace_rejected_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_replace_rejected_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_replace_rejected_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_replace_rejected_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_replace_rejected_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_replace_rejected_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return ReplaceRejected(lib.node().xroad_replace_rejected_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "order_status":
            self.order_status = xtypes.OrderStatus[value] if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "leaves_qty":
            self.leaves_qty = int(value) if value is not None else value
        elif field == "cum_qty":
            self.cum_qty = int(value) if value is not None else value
        elif field == "reason":
            self.reason = xtypes.RejReason[value] if value is not None else value
        elif field == "text":
            self.text = str(value) if value is not None else value

    @property
    def order(self):
        lib.node().xroad_replace_rejected_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_rejected_order_is_set(self.__ptr):
            lib.node().xroad_replace_rejected_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_replace_rejected_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_replace_rejected_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_replace_rejected_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_replace_rejected_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_replace_rejected_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_replace_rejected_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_reset_order(self.__ptr)

    @property
    def order_status(self):
        lib.node().xroad_replace_rejected_order_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_rejected_order_status_is_set(self.__ptr):
            lib.node().xroad_replace_rejected_get_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_get_order_status.restype = ctypes.c_int
            return xtypes.OrderStatus(lib.node().xroad_replace_rejected_get_order_status(self.__ptr))
        else:
            return None

    @order_status.setter
    def order_status(self, value):
        if not isinstance(value, xtypes.OrderStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderStatus enum".format(value))
        if value is not None:
            lib.node().xroad_replace_rejected_set_order_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_replace_rejected_set_order_status(self.__ptr, value.value)
        else:
            lib.node().xroad_replace_rejected_reset_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_reset_order_status(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_replace_rejected_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_rejected_price_is_set(self.__ptr):
            lib.node().xroad_replace_rejected_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_get_price.restype = ctypes.c_double
            return lib.node().xroad_replace_rejected_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_replace_rejected_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_replace_rejected_set_price(self.__ptr, value)
        else:
            lib.node().xroad_replace_rejected_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_reset_price(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_replace_rejected_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_rejected_qty_is_set(self.__ptr):
            lib.node().xroad_replace_rejected_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_get_qty.restype = ctypes.c_long
            return lib.node().xroad_replace_rejected_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_replace_rejected_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replace_rejected_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_replace_rejected_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_reset_qty(self.__ptr)

    @property
    def leaves_qty(self):
        lib.node().xroad_replace_rejected_leaves_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_rejected_leaves_qty_is_set(self.__ptr):
            lib.node().xroad_replace_rejected_get_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_get_leaves_qty.restype = ctypes.c_long
            return lib.node().xroad_replace_rejected_get_leaves_qty(self.__ptr)
        else:
            return None

    @leaves_qty.setter
    def leaves_qty(self, value):
        if value is not None:
            lib.node().xroad_replace_rejected_set_leaves_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replace_rejected_set_leaves_qty(self.__ptr, value)
        else:
            lib.node().xroad_replace_rejected_reset_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_reset_leaves_qty(self.__ptr)

    @property
    def cum_qty(self):
        lib.node().xroad_replace_rejected_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_rejected_cum_qty_is_set(self.__ptr):
            lib.node().xroad_replace_rejected_get_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_get_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_replace_rejected_get_cum_qty(self.__ptr)
        else:
            return None

    @cum_qty.setter
    def cum_qty(self, value):
        if value is not None:
            lib.node().xroad_replace_rejected_set_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replace_rejected_set_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_replace_rejected_reset_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_reset_cum_qty(self.__ptr)

    @property
    def reason(self):
        lib.node().xroad_replace_rejected_reason_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_rejected_reason_is_set(self.__ptr):
            lib.node().xroad_replace_rejected_get_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_get_reason.restype = ctypes.c_int
            return xtypes.RejReason(lib.node().xroad_replace_rejected_get_reason(self.__ptr))
        else:
            return None

    @reason.setter
    def reason(self, value):
        if not isinstance(value, xtypes.RejReason) and value is not None:
            raise TypeError("{0} has wrong type. must be RejReason enum".format(value))
        if value is not None:
            lib.node().xroad_replace_rejected_set_reason.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_replace_rejected_set_reason(self.__ptr, value.value)
        else:
            lib.node().xroad_replace_rejected_reset_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_reset_reason(self.__ptr)

    @property
    def text(self):
        lib.node().xroad_replace_rejected_text_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replace_rejected_text_is_set(self.__ptr):
            lib.node().xroad_replace_rejected_get_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_get_text.restype = ctypes.POINTER(xtypes.Text)
            res = lib.node().xroad_replace_rejected_get_text(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @text.setter
    def text(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_replace_rejected_set_text.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_replace_rejected_set_text(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_replace_rejected_reset_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replace_rejected_reset_text(self.__ptr)


class Replaced(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_replaced_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_replaced_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_replaced_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.replaced

    @property
    def is_valid(self):
        lib.node().xroad_replaced_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_replaced_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_replaced_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_replaced_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_replaced_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_replaced_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_replaced_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_replaced_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_replaced_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Replaced(lib.node().xroad_replaced_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value
        elif field == "order_status":
            self.order_status = xtypes.OrderStatus[value] if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "leaves_qty":
            self.leaves_qty = int(value) if value is not None else value
        elif field == "cum_qty":
            self.cum_qty = int(value) if value is not None else value

    @property
    def order(self):
        lib.node().xroad_replaced_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replaced_order_is_set(self.__ptr):
            lib.node().xroad_replaced_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_replaced_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_replaced_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_replaced_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_replaced_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_replaced_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_replaced_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_reset_order(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_replaced_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replaced_tran_time_is_set(self.__ptr):
            lib.node().xroad_replaced_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_replaced_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_replaced_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replaced_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_replaced_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_reset_tran_time(self.__ptr)

    @property
    def order_status(self):
        lib.node().xroad_replaced_order_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replaced_order_status_is_set(self.__ptr):
            lib.node().xroad_replaced_get_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_get_order_status.restype = ctypes.c_int
            return xtypes.OrderStatus(lib.node().xroad_replaced_get_order_status(self.__ptr))
        else:
            return None

    @order_status.setter
    def order_status(self, value):
        if not isinstance(value, xtypes.OrderStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderStatus enum".format(value))
        if value is not None:
            lib.node().xroad_replaced_set_order_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_replaced_set_order_status(self.__ptr, value.value)
        else:
            lib.node().xroad_replaced_reset_order_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_reset_order_status(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_replaced_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replaced_price_is_set(self.__ptr):
            lib.node().xroad_replaced_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_get_price.restype = ctypes.c_double
            return lib.node().xroad_replaced_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_replaced_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_replaced_set_price(self.__ptr, value)
        else:
            lib.node().xroad_replaced_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_reset_price(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_replaced_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replaced_qty_is_set(self.__ptr):
            lib.node().xroad_replaced_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_get_qty.restype = ctypes.c_long
            return lib.node().xroad_replaced_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_replaced_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replaced_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_replaced_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_reset_qty(self.__ptr)

    @property
    def leaves_qty(self):
        lib.node().xroad_replaced_leaves_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replaced_leaves_qty_is_set(self.__ptr):
            lib.node().xroad_replaced_get_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_get_leaves_qty.restype = ctypes.c_long
            return lib.node().xroad_replaced_get_leaves_qty(self.__ptr)
        else:
            return None

    @leaves_qty.setter
    def leaves_qty(self, value):
        if value is not None:
            lib.node().xroad_replaced_set_leaves_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replaced_set_leaves_qty(self.__ptr, value)
        else:
            lib.node().xroad_replaced_reset_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_reset_leaves_qty(self.__ptr)

    @property
    def cum_qty(self):
        lib.node().xroad_replaced_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_replaced_cum_qty_is_set(self.__ptr):
            lib.node().xroad_replaced_get_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_get_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_replaced_get_cum_qty(self.__ptr)
        else:
            return None

    @cum_qty.setter
    def cum_qty(self, value):
        if value is not None:
            lib.node().xroad_replaced_set_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_replaced_set_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_replaced_reset_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_replaced_reset_cum_qty(self.__ptr)


class Removed(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_removed_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_removed_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_removed_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_removed_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.removed

    @property
    def is_valid(self):
        lib.node().xroad_removed_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_removed_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_removed_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_removed_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_removed_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_removed_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_removed_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_removed_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_removed_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Removed(lib.node().xroad_removed_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "order":
            if hasattr(value, "ptr"):
                self.order = value
            else:
                self.order = str_to_tuple(value)
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value

    @property
    def order(self):
        lib.node().xroad_removed_order_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_removed_order_is_set(self.__ptr):
            lib.node().xroad_removed_get_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_removed_get_order.restype = ctypes.c_void_p
            obj = lib.node().xroad_removed_get_order(self.__ptr)
            if not obj:
                raise BrokenRefError("reference order is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @order.setter
    def order(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_removed_set_order.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_removed_set_order(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_removed_set_order_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_removed_set_order_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_removed_reset_order.argtypes = [ctypes.c_void_p]
            lib.node().xroad_removed_reset_order(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_removed_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_removed_tran_time_is_set(self.__ptr):
            lib.node().xroad_removed_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_removed_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_removed_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_removed_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_removed_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_removed_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_removed_reset_tran_time(self.__ptr)


class Subscribe(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_subscribe_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_subscribe_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_subscribe_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_subscribe_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.subscribe

    @property
    def is_valid(self):
        lib.node().xroad_subscribe_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_subscribe_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_subscribe_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_subscribe_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_subscribe_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_subscribe_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_subscribe_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_subscribe_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_subscribe_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Subscribe(lib.node().xroad_subscribe_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "src_node_id":
            self.src_node_id = int(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)

    @property
    def src_node_id(self):
        lib.node().xroad_subscribe_src_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_subscribe_src_node_id_is_set(self.__ptr):
            lib.node().xroad_subscribe_get_src_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_subscribe_get_src_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_subscribe_get_src_node_id(self.__ptr)
        else:
            return None

    @src_node_id.setter
    def src_node_id(self, value):
        if value is not None:
            lib.node().xroad_subscribe_set_src_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_subscribe_set_src_node_id(self.__ptr, value)
        else:
            lib.node().xroad_subscribe_reset_src_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_subscribe_reset_src_node_id(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_subscribe_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_subscribe_instr_is_set(self.__ptr):
            lib.node().xroad_subscribe_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_subscribe_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_subscribe_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_subscribe_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_subscribe_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_subscribe_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_subscribe_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_subscribe_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_subscribe_reset_instr(self.__ptr)


class Unsubscribe(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_unsubscribe_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_unsubscribe_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_unsubscribe_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_unsubscribe_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.unsubscribe

    @property
    def is_valid(self):
        lib.node().xroad_unsubscribe_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_unsubscribe_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_unsubscribe_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_unsubscribe_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_unsubscribe_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_unsubscribe_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_unsubscribe_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_unsubscribe_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_unsubscribe_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Unsubscribe(lib.node().xroad_unsubscribe_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "src_node_id":
            self.src_node_id = int(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)

    @property
    def src_node_id(self):
        lib.node().xroad_unsubscribe_src_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_unsubscribe_src_node_id_is_set(self.__ptr):
            lib.node().xroad_unsubscribe_get_src_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_unsubscribe_get_src_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_unsubscribe_get_src_node_id(self.__ptr)
        else:
            return None

    @src_node_id.setter
    def src_node_id(self, value):
        if value is not None:
            lib.node().xroad_unsubscribe_set_src_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_unsubscribe_set_src_node_id(self.__ptr, value)
        else:
            lib.node().xroad_unsubscribe_reset_src_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_unsubscribe_reset_src_node_id(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_unsubscribe_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_unsubscribe_instr_is_set(self.__ptr):
            lib.node().xroad_unsubscribe_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_unsubscribe_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_unsubscribe_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_unsubscribe_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_unsubscribe_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_unsubscribe_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_unsubscribe_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_unsubscribe_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_unsubscribe_reset_instr(self.__ptr)


class SubscribeRes(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_subscribe_res_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_subscribe_res_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_subscribe_res_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_subscribe_res_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.subscribe_res

    @property
    def is_valid(self):
        lib.node().xroad_subscribe_res_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_subscribe_res_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_subscribe_res_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_subscribe_res_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_subscribe_res_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_subscribe_res_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_subscribe_res_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_subscribe_res_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_subscribe_res_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return SubscribeRes(lib.node().xroad_subscribe_res_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)
        elif field == "result":
            self.result = xtypes.SubsResult[value] if value is not None else value

    @property
    def instr(self):
        lib.node().xroad_subscribe_res_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_subscribe_res_instr_is_set(self.__ptr):
            lib.node().xroad_subscribe_res_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_subscribe_res_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_subscribe_res_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_subscribe_res_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_subscribe_res_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_subscribe_res_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_subscribe_res_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_subscribe_res_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_subscribe_res_reset_instr(self.__ptr)

    @property
    def result(self):
        lib.node().xroad_subscribe_res_result_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_subscribe_res_result_is_set(self.__ptr):
            lib.node().xroad_subscribe_res_get_result.argtypes = [ctypes.c_void_p]
            lib.node().xroad_subscribe_res_get_result.restype = ctypes.c_int
            return xtypes.SubsResult(lib.node().xroad_subscribe_res_get_result(self.__ptr))
        else:
            return None

    @result.setter
    def result(self, value):
        if not isinstance(value, xtypes.SubsResult) and value is not None:
            raise TypeError("{0} has wrong type. must be SubsResult enum".format(value))
        if value is not None:
            lib.node().xroad_subscribe_res_set_result.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_subscribe_res_set_result(self.__ptr, value.value)
        else:
            lib.node().xroad_subscribe_res_reset_result.argtypes = [ctypes.c_void_p]
            lib.node().xroad_subscribe_res_reset_result(self.__ptr)


class OptMm(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_opt_mm_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_opt_mm_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.opt_mm

    @property
    def is_valid(self):
        lib.node().xroad_opt_mm_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_opt_mm_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_opt_mm_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_opt_mm_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_opt_mm_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_opt_mm_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_opt_mm_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_opt_mm_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_opt_mm_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return OptMm(lib.node().xroad_opt_mm_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_opt_mm_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_opt_mm_get_id.restype = ctypes.c_long
        return lib.node().xroad_opt_mm_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_opt_mm_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_opt_mm_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_opt_mm_copy(self.__ptr, id)
        return OptMm(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.instr
        if v is not None:
            fields["instr"] = "({0},{1})".format(v.object_type, v.id)
        v = self.enabled
        if v is not None:
            fields["enabled"] = v
        v = self.deleted
        if v is not None:
            fields["deleted"] = v
        v = self.bid_enabled
        if v is not None:
            fields["bid_enabled"] = v
        v = self.bid_state
        if v is not None:
            fields["bid_state"] = v.name
        v = self.ask_enabled
        if v is not None:
            fields["ask_enabled"] = v
        v = self.ask_state
        if v is not None:
            fields["ask_state"] = v.name
        v = self.premium
        if v is not None:
            fields["premium"] = v
        v = self.delta
        if v is not None:
            fields["delta"] = v
        v = self.volatility
        if v is not None:
            fields["volatility"] = v
        v = self.rate
        if v is not None:
            fields["rate"] = v
        v = self.time_rate
        if v is not None:
            fields["time_rate"] = v
        v = self.fut_mid_price
        if v is not None:
            fields["fut_mid_price"] = v
        v = self.mid_price
        if v is not None:
            fields["mid_price"] = v
        v = self.bid_size
        if v is not None:
            fields["bid_size"] = v
        v = self.ask_size
        if v is not None:
            fields["ask_size"] = v
        v = self.lower
        if v is not None:
            fields["lower"] = v
        v = self.higher
        if v is not None:
            fields["higher"] = v
        v = self.position
        if v is not None:
            fields["position"] = v
        v = self.pos_keep
        if v is not None:
            fields["pos_keep"] = v
        v = self.bid_spread
        if v is not None:
            fields["bid_spread"] = v
        v = self.ask_spread
        if v is not None:
            fields["ask_spread"] = v
        v = self.sensitivity
        if v is not None:
            fields["sensitivity"] = v
        v = self.shift
        if v is not None:
            fields["shift"] = v
        v = self.shift_vol
        if v is not None:
            fields["shift_vol"] = v
        v = self.calc_mid
        if v is not None:
            fields["calc_mid"] = v.name
        v = self.bid_text
        if v is not None:
            fields["bid_text"] = v
        v = self.ask_text
        if v is not None:
            fields["ask_text"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)
        elif field == "enabled":
            self.enabled = int(value) if value is not None else value
        elif field == "deleted":
            self.deleted = int(value) if value is not None else value
        elif field == "bid_enabled":
            self.bid_enabled = int(value) if value is not None else value
        elif field == "bid_state":
            self.bid_state = xtypes.OptMmState[value] if value is not None else value
        elif field == "ask_enabled":
            self.ask_enabled = int(value) if value is not None else value
        elif field == "ask_state":
            self.ask_state = xtypes.OptMmState[value] if value is not None else value
        elif field == "premium":
            self.premium = float(value) if value is not None else value
        elif field == "delta":
            self.delta = float(value) if value is not None else value
        elif field == "volatility":
            self.volatility = float(value) if value is not None else value
        elif field == "rate":
            self.rate = float(value) if value is not None else value
        elif field == "time_rate":
            self.time_rate = float(value) if value is not None else value
        elif field == "fut_mid_price":
            self.fut_mid_price = float(value) if value is not None else value
        elif field == "mid_price":
            self.mid_price = float(value) if value is not None else value
        elif field == "bid_size":
            self.bid_size = int(value) if value is not None else value
        elif field == "ask_size":
            self.ask_size = int(value) if value is not None else value
        elif field == "lower":
            self.lower = int(value) if value is not None else value
        elif field == "higher":
            self.higher = int(value) if value is not None else value
        elif field == "position":
            self.position = int(value) if value is not None else value
        elif field == "pos_keep":
            self.pos_keep = int(value) if value is not None else value
        elif field == "bid_spread":
            self.bid_spread = float(value) if value is not None else value
        elif field == "ask_spread":
            self.ask_spread = float(value) if value is not None else value
        elif field == "sensitivity":
            self.sensitivity = float(value) if value is not None else value
        elif field == "shift":
            self.shift = float(value) if value is not None else value
        elif field == "shift_vol":
            self.shift_vol = float(value) if value is not None else value
        elif field == "calc_mid":
            self.calc_mid = xtypes.CalcMid[value] if value is not None else value
        elif field == "bid_text":
            self.bid_text = str(value) if value is not None else value
        elif field == "ask_text":
            self.ask_text = str(value) if value is not None else value

    @property
    def node_id(self):
        lib.node().xroad_opt_mm_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_node_id_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_opt_mm_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_opt_mm_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_node_id(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_opt_mm_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_instr_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_opt_mm_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_opt_mm_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_opt_mm_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_opt_mm_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_opt_mm_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_opt_mm_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_instr(self.__ptr)

    @property
    def enabled(self):
        lib.node().xroad_opt_mm_enabled_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_enabled_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_enabled.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_enabled.restype = ctypes.c_byte
            return lib.node().xroad_opt_mm_get_enabled(self.__ptr)
        else:
            return None

    @enabled.setter
    def enabled(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_enabled.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_opt_mm_set_enabled(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_enabled.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_enabled(self.__ptr)

    @property
    def deleted(self):
        lib.node().xroad_opt_mm_deleted_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_deleted_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_deleted.restype = ctypes.c_byte
            return lib.node().xroad_opt_mm_get_deleted(self.__ptr)
        else:
            return None

    @deleted.setter
    def deleted(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_deleted.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_opt_mm_set_deleted(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_deleted(self.__ptr)

    @property
    def bid_enabled(self):
        lib.node().xroad_opt_mm_bid_enabled_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_bid_enabled_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_bid_enabled.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_bid_enabled.restype = ctypes.c_byte
            return lib.node().xroad_opt_mm_get_bid_enabled(self.__ptr)
        else:
            return None

    @bid_enabled.setter
    def bid_enabled(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_bid_enabled.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_opt_mm_set_bid_enabled(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_bid_enabled.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_bid_enabled(self.__ptr)

    @property
    def bid_state(self):
        lib.node().xroad_opt_mm_bid_state_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_bid_state_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_bid_state.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_bid_state.restype = ctypes.c_int
            return xtypes.OptMmState(lib.node().xroad_opt_mm_get_bid_state(self.__ptr))
        else:
            return None

    @bid_state.setter
    def bid_state(self, value):
        if not isinstance(value, xtypes.OptMmState) and value is not None:
            raise TypeError("{0} has wrong type. must be OptMmState enum".format(value))
        if value is not None:
            lib.node().xroad_opt_mm_set_bid_state.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_opt_mm_set_bid_state(self.__ptr, value.value)
        else:
            lib.node().xroad_opt_mm_reset_bid_state.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_bid_state(self.__ptr)

    @property
    def ask_enabled(self):
        lib.node().xroad_opt_mm_ask_enabled_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_ask_enabled_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_ask_enabled.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_ask_enabled.restype = ctypes.c_byte
            return lib.node().xroad_opt_mm_get_ask_enabled(self.__ptr)
        else:
            return None

    @ask_enabled.setter
    def ask_enabled(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_ask_enabled.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_opt_mm_set_ask_enabled(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_ask_enabled.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_ask_enabled(self.__ptr)

    @property
    def ask_state(self):
        lib.node().xroad_opt_mm_ask_state_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_ask_state_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_ask_state.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_ask_state.restype = ctypes.c_int
            return xtypes.OptMmState(lib.node().xroad_opt_mm_get_ask_state(self.__ptr))
        else:
            return None

    @ask_state.setter
    def ask_state(self, value):
        if not isinstance(value, xtypes.OptMmState) and value is not None:
            raise TypeError("{0} has wrong type. must be OptMmState enum".format(value))
        if value is not None:
            lib.node().xroad_opt_mm_set_ask_state.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_opt_mm_set_ask_state(self.__ptr, value.value)
        else:
            lib.node().xroad_opt_mm_reset_ask_state.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_ask_state(self.__ptr)

    @property
    def premium(self):
        lib.node().xroad_opt_mm_premium_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_premium_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_premium.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_premium.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_premium(self.__ptr)
        else:
            return None

    @premium.setter
    def premium(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_premium.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_premium(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_premium.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_premium(self.__ptr)

    @property
    def delta(self):
        lib.node().xroad_opt_mm_delta_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_delta_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_delta.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_delta.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_delta(self.__ptr)
        else:
            return None

    @delta.setter
    def delta(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_delta.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_delta(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_delta.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_delta(self.__ptr)

    @property
    def volatility(self):
        lib.node().xroad_opt_mm_volatility_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_volatility_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_volatility.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_volatility.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_volatility(self.__ptr)
        else:
            return None

    @volatility.setter
    def volatility(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_volatility.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_volatility(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_volatility.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_volatility(self.__ptr)

    @property
    def rate(self):
        lib.node().xroad_opt_mm_rate_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_rate_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_rate.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_rate.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_rate(self.__ptr)
        else:
            return None

    @rate.setter
    def rate(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_rate.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_rate(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_rate.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_rate(self.__ptr)

    @property
    def time_rate(self):
        lib.node().xroad_opt_mm_time_rate_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_time_rate_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_time_rate.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_time_rate.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_time_rate(self.__ptr)
        else:
            return None

    @time_rate.setter
    def time_rate(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_time_rate.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_time_rate(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_time_rate.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_time_rate(self.__ptr)

    @property
    def fut_mid_price(self):
        lib.node().xroad_opt_mm_fut_mid_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_fut_mid_price_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_fut_mid_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_fut_mid_price.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_fut_mid_price(self.__ptr)
        else:
            return None

    @fut_mid_price.setter
    def fut_mid_price(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_fut_mid_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_fut_mid_price(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_fut_mid_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_fut_mid_price(self.__ptr)

    @property
    def mid_price(self):
        lib.node().xroad_opt_mm_mid_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_mid_price_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_mid_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_mid_price.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_mid_price(self.__ptr)
        else:
            return None

    @mid_price.setter
    def mid_price(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_mid_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_mid_price(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_mid_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_mid_price(self.__ptr)

    @property
    def bid_size(self):
        lib.node().xroad_opt_mm_bid_size_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_bid_size_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_bid_size.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_bid_size.restype = ctypes.c_long
            return lib.node().xroad_opt_mm_get_bid_size(self.__ptr)
        else:
            return None

    @bid_size.setter
    def bid_size(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_bid_size.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_opt_mm_set_bid_size(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_bid_size.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_bid_size(self.__ptr)

    @property
    def ask_size(self):
        lib.node().xroad_opt_mm_ask_size_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_ask_size_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_ask_size.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_ask_size.restype = ctypes.c_long
            return lib.node().xroad_opt_mm_get_ask_size(self.__ptr)
        else:
            return None

    @ask_size.setter
    def ask_size(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_ask_size.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_opt_mm_set_ask_size(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_ask_size.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_ask_size(self.__ptr)

    @property
    def lower(self):
        lib.node().xroad_opt_mm_lower_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_lower_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_lower.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_lower.restype = ctypes.c_long
            return lib.node().xroad_opt_mm_get_lower(self.__ptr)
        else:
            return None

    @lower.setter
    def lower(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_lower.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_opt_mm_set_lower(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_lower.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_lower(self.__ptr)

    @property
    def higher(self):
        lib.node().xroad_opt_mm_higher_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_higher_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_higher.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_higher.restype = ctypes.c_long
            return lib.node().xroad_opt_mm_get_higher(self.__ptr)
        else:
            return None

    @higher.setter
    def higher(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_higher.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_opt_mm_set_higher(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_higher.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_higher(self.__ptr)

    @property
    def position(self):
        lib.node().xroad_opt_mm_position_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_position_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_position.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_position.restype = ctypes.c_long
            return lib.node().xroad_opt_mm_get_position(self.__ptr)
        else:
            return None

    @position.setter
    def position(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_position.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_opt_mm_set_position(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_position.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_position(self.__ptr)

    @property
    def pos_keep(self):
        lib.node().xroad_opt_mm_pos_keep_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_pos_keep_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_pos_keep.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_pos_keep.restype = ctypes.c_long
            return lib.node().xroad_opt_mm_get_pos_keep(self.__ptr)
        else:
            return None

    @pos_keep.setter
    def pos_keep(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_pos_keep.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_opt_mm_set_pos_keep(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_pos_keep.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_pos_keep(self.__ptr)

    @property
    def bid_spread(self):
        lib.node().xroad_opt_mm_bid_spread_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_bid_spread_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_bid_spread.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_bid_spread.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_bid_spread(self.__ptr)
        else:
            return None

    @bid_spread.setter
    def bid_spread(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_bid_spread.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_bid_spread(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_bid_spread.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_bid_spread(self.__ptr)

    @property
    def ask_spread(self):
        lib.node().xroad_opt_mm_ask_spread_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_ask_spread_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_ask_spread.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_ask_spread.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_ask_spread(self.__ptr)
        else:
            return None

    @ask_spread.setter
    def ask_spread(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_ask_spread.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_ask_spread(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_ask_spread.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_ask_spread(self.__ptr)

    @property
    def sensitivity(self):
        lib.node().xroad_opt_mm_sensitivity_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_sensitivity_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_sensitivity.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_sensitivity.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_sensitivity(self.__ptr)
        else:
            return None

    @sensitivity.setter
    def sensitivity(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_sensitivity.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_sensitivity(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_sensitivity.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_sensitivity(self.__ptr)

    @property
    def shift(self):
        lib.node().xroad_opt_mm_shift_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_shift_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_shift.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_shift.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_shift(self.__ptr)
        else:
            return None

    @shift.setter
    def shift(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_shift.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_shift(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_shift.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_shift(self.__ptr)

    @property
    def shift_vol(self):
        lib.node().xroad_opt_mm_shift_vol_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_shift_vol_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_shift_vol.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_shift_vol.restype = ctypes.c_double
            return lib.node().xroad_opt_mm_get_shift_vol(self.__ptr)
        else:
            return None

    @shift_vol.setter
    def shift_vol(self, value):
        if value is not None:
            lib.node().xroad_opt_mm_set_shift_vol.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_opt_mm_set_shift_vol(self.__ptr, value)
        else:
            lib.node().xroad_opt_mm_reset_shift_vol.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_shift_vol(self.__ptr)

    @property
    def calc_mid(self):
        lib.node().xroad_opt_mm_calc_mid_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_calc_mid_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_calc_mid.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_calc_mid.restype = ctypes.c_int
            return xtypes.CalcMid(lib.node().xroad_opt_mm_get_calc_mid(self.__ptr))
        else:
            return None

    @calc_mid.setter
    def calc_mid(self, value):
        if not isinstance(value, xtypes.CalcMid) and value is not None:
            raise TypeError("{0} has wrong type. must be CalcMid enum".format(value))
        if value is not None:
            lib.node().xroad_opt_mm_set_calc_mid.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_opt_mm_set_calc_mid(self.__ptr, value.value)
        else:
            lib.node().xroad_opt_mm_reset_calc_mid.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_calc_mid(self.__ptr)

    @property
    def bid_text(self):
        lib.node().xroad_opt_mm_bid_text_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_bid_text_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_bid_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_bid_text.restype = ctypes.POINTER(xtypes.ShortText)
            res = lib.node().xroad_opt_mm_get_bid_text(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @bid_text.setter
    def bid_text(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_opt_mm_set_bid_text.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_opt_mm_set_bid_text(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_opt_mm_reset_bid_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_bid_text(self.__ptr)

    @property
    def ask_text(self):
        lib.node().xroad_opt_mm_ask_text_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_opt_mm_ask_text_is_set(self.__ptr):
            lib.node().xroad_opt_mm_get_ask_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_get_ask_text.restype = ctypes.POINTER(xtypes.ShortText)
            res = lib.node().xroad_opt_mm_get_ask_text(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @ask_text.setter
    def ask_text(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_opt_mm_set_ask_text.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_opt_mm_set_ask_text(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_opt_mm_reset_ask_text.argtypes = [ctypes.c_void_p]
            lib.node().xroad_opt_mm_reset_ask_text(self.__ptr)


class Field(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_field_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_field_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.field

    @property
    def is_valid(self):
        lib.node().xroad_field_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_field_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_field_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_field_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_field_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_field_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_field_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_field_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_field_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Field(lib.node().xroad_field_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_field_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_field_get_id.restype = ctypes.c_long
        return lib.node().xroad_field_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_field_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_field_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_field_copy(self.__ptr, id)
        return Field(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.name
        if v is not None:
            fields["name"] = v
        v = self.type
        if v is not None:
            fields["type"] = v.name
        v = self.value
        if v is not None:
            try:
                fields["value"] = binascii.b2a_hex(v).decode("utf-8")
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(binascii.b2a_hex(v), self.__class__))
                return ''
        v = self.deleted
        if v is not None:
            fields["deleted"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "name":
            self.name = str(value) if value is not None else value
        elif field == "type":
            self.type = xtypes.FieldType[value] if value is not None else value
        elif field == "value":
            self.value = binascii.unhexlify(value.replace(" ", "")) if value is not None else value
        elif field == "deleted":
            self.deleted = int(value) if value is not None else value

    @property
    def node_id(self):
        lib.node().xroad_field_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_field_node_id_is_set(self.__ptr):
            lib.node().xroad_field_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_field_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_field_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_field_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_field_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_field_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_field_reset_node_id(self.__ptr)

    @property
    def name(self):
        lib.node().xroad_field_name_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_field_name_is_set(self.__ptr):
            lib.node().xroad_field_get_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_field_get_name.restype = ctypes.POINTER(xtypes.FieldName)
            res = lib.node().xroad_field_get_name(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @name.setter
    def name(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_field_set_name.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_field_set_name(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_field_reset_name.argtypes = [ctypes.c_void_p]
            lib.node().xroad_field_reset_name(self.__ptr)

    @property
    def type(self):
        lib.node().xroad_field_type_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_field_type_is_set(self.__ptr):
            lib.node().xroad_field_get_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_field_get_type.restype = ctypes.c_int
            return xtypes.FieldType(lib.node().xroad_field_get_type(self.__ptr))
        else:
            return None

    @type.setter
    def type(self, value):
        if not isinstance(value, xtypes.FieldType) and value is not None:
            raise TypeError("{0} has wrong type. must be FieldType enum".format(value))
        if value is not None:
            lib.node().xroad_field_set_type.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_field_set_type(self.__ptr, value.value)
        else:
            lib.node().xroad_field_reset_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_field_reset_type(self.__ptr)

    @property
    def value(self):
        lib.node().xroad_field_value_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_field_value_is_set(self.__ptr):
            lib.node().xroad_field_get_value.argtypes = [ctypes.c_void_p]
            lib.node().xroad_field_get_value.restype = ctypes.POINTER(xtypes.FieldValue)
            res = lib.node().xroad_field_get_value(self.__ptr)
            return bytes(res.contents.data[:res.contents.len])
        else:
            return None

    @value.setter
    def value(self, value):
        if value is not None and not isinstance(value, bytes):
            raise TypeError("{0} has wrong type. must be bytes".format(value))
        if value is not None:
            lib.node().xroad_field_set_value.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]
            lib.node().xroad_field_set_value(self.__ptr, value, len(value))
        else:
            lib.node().xroad_field_reset_value.argtypes = [ctypes.c_void_p]
            lib.node().xroad_field_reset_value(self.__ptr)

    @property
    def deleted(self):
        lib.node().xroad_field_deleted_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_field_deleted_is_set(self.__ptr):
            lib.node().xroad_field_get_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_field_get_deleted.restype = ctypes.c_byte
            return lib.node().xroad_field_get_deleted(self.__ptr)
        else:
            return None

    @deleted.setter
    def deleted(self, value):
        if value is not None:
            lib.node().xroad_field_set_deleted.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_field_set_deleted(self.__ptr, value)
        else:
            lib.node().xroad_field_reset_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_field_reset_deleted(self.__ptr)


class TrdCapt(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_trd_capt_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_trd_capt_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.trd_capt

    @property
    def is_valid(self):
        lib.node().xroad_trd_capt_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_trd_capt_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_trd_capt_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_trd_capt_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_trd_capt_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_trd_capt_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_trd_capt_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_trd_capt_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_trd_capt_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return TrdCapt(lib.node().xroad_trd_capt_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_trd_capt_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_trd_capt_get_id.restype = ctypes.c_long
        return lib.node().xroad_trd_capt_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_trd_capt_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_trd_capt_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_trd_capt_copy(self.__ptr, id)
        return TrdCapt(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.tradeno
        if v is not None:
            fields["tradeno"] = v
        v = self.orderno
        if v is not None:
            fields["orderno"] = v
        v = self.trade
        if v is not None:
            fields["trade"] = "({0},{1})".format(v.object_type, v.id)
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.instr
        if v is not None:
            fields["instr"] = "({0},{1})".format(v.object_type, v.id)
        v = self.tran_time
        if v is not None:
            fields["tran_time"] = v
        v = self.side
        if v is not None:
            fields["side"] = v.name
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.qty_items
        if v is not None:
            fields["qty_items"] = v
        v = self.price
        if v is not None:
            fields["price"] = v
        v = self.account
        if v is not None:
            fields["account"] = v
        v = self.client_code
        if v is not None:
            fields["client_code"] = v
        v = self.exch_fee
        if v is not None:
            fields["exch_fee"] = v
        v = self.book
        if v is not None:
            fields["book"] = v
        v = self.otc_id
        if v is not None:
            fields["otc_id"] = v
        v = self.counterparty
        if v is not None:
            fields["counterparty"] = v
        v = self.deleted
        if v is not None:
            fields["deleted"] = v
        v = self.face_value
        if v is not None:
            fields["face_value"] = v
        v = self.accrued_int
        if v is not None:
            fields["accrued_int"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "tradeno":
            self.tradeno = int(value) if value is not None else value
        elif field == "orderno":
            self.orderno = int(value) if value is not None else value
        elif field == "trade":
            if hasattr(value, "ptr"):
                self.trade = value
            else:
                self.trade = str_to_tuple(value)
        elif field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value
        elif field == "side":
            self.side = xtypes.Side[value] if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "qty_items":
            self.qty_items = int(value) if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "account":
            self.account = str(value) if value is not None else value
        elif field == "client_code":
            self.client_code = str(value) if value is not None else value
        elif field == "exch_fee":
            self.exch_fee = float(value) if value is not None else value
        elif field == "book":
            self.book = str(value) if value is not None else value
        elif field == "otc_id":
            self.otc_id = int(value) if value is not None else value
        elif field == "counterparty":
            self.counterparty = str(value) if value is not None else value
        elif field == "deleted":
            self.deleted = int(value) if value is not None else value
        elif field == "face_value":
            self.face_value = float(value) if value is not None else value
        elif field == "accrued_int":
            self.accrued_int = float(value) if value is not None else value

    @property
    def tradeno(self):
        lib.node().xroad_trd_capt_tradeno_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_tradeno_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_tradeno.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_tradeno.restype = ctypes.c_ulong
            return lib.node().xroad_trd_capt_get_tradeno(self.__ptr)
        else:
            return None

    @tradeno.setter
    def tradeno(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_tradeno.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_trd_capt_set_tradeno(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_tradeno.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_tradeno(self.__ptr)

    @property
    def orderno(self):
        lib.node().xroad_trd_capt_orderno_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_orderno_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_orderno.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_orderno.restype = ctypes.c_ulong
            return lib.node().xroad_trd_capt_get_orderno(self.__ptr)
        else:
            return None

    @orderno.setter
    def orderno(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_orderno.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_trd_capt_set_orderno(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_orderno.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_orderno(self.__ptr)

    @property
    def trade(self):
        lib.node().xroad_trd_capt_trade_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_trade_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_trade.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_trade.restype = ctypes.c_void_p
            obj = lib.node().xroad_trd_capt_get_trade(self.__ptr)
            if not obj:
                raise BrokenRefError("reference trade is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @trade.setter
    def trade(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_trd_capt_set_trade.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_trd_capt_set_trade(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_trd_capt_set_trade_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_trd_capt_set_trade_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_trd_capt_reset_trade.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_trade(self.__ptr)

    @property
    def node_id(self):
        lib.node().xroad_trd_capt_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_node_id_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_trd_capt_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_trd_capt_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_node_id(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_trd_capt_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_instr_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_trd_capt_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_trd_capt_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_trd_capt_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_trd_capt_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_trd_capt_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_trd_capt_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_instr(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_trd_capt_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_tran_time_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_trd_capt_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_trd_capt_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_tran_time(self.__ptr)

    @property
    def side(self):
        lib.node().xroad_trd_capt_side_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_side_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_side.restype = ctypes.c_int
            return xtypes.Side(lib.node().xroad_trd_capt_get_side(self.__ptr))
        else:
            return None

    @side.setter
    def side(self, value):
        if not isinstance(value, xtypes.Side) and value is not None:
            raise TypeError("{0} has wrong type. must be Side enum".format(value))
        if value is not None:
            lib.node().xroad_trd_capt_set_side.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_trd_capt_set_side(self.__ptr, value.value)
        else:
            lib.node().xroad_trd_capt_reset_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_side(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_trd_capt_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_qty_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_qty.restype = ctypes.c_long
            return lib.node().xroad_trd_capt_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_trd_capt_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_qty(self.__ptr)

    @property
    def qty_items(self):
        lib.node().xroad_trd_capt_qty_items_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_qty_items_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_qty_items.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_qty_items.restype = ctypes.c_long
            return lib.node().xroad_trd_capt_get_qty_items(self.__ptr)
        else:
            return None

    @qty_items.setter
    def qty_items(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_qty_items.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_trd_capt_set_qty_items(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_qty_items.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_qty_items(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_trd_capt_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_price_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_price.restype = ctypes.c_double
            return lib.node().xroad_trd_capt_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_trd_capt_set_price(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_price(self.__ptr)

    @property
    def account(self):
        lib.node().xroad_trd_capt_account_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_account_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_account.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_account.restype = ctypes.POINTER(xtypes.Account)
            res = lib.node().xroad_trd_capt_get_account(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @account.setter
    def account(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_trd_capt_set_account.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_trd_capt_set_account(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_trd_capt_reset_account.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_account(self.__ptr)

    @property
    def client_code(self):
        lib.node().xroad_trd_capt_client_code_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_client_code_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_client_code.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_client_code.restype = ctypes.POINTER(xtypes.ClientCode)
            res = lib.node().xroad_trd_capt_get_client_code(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @client_code.setter
    def client_code(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_trd_capt_set_client_code.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_trd_capt_set_client_code(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_trd_capt_reset_client_code.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_client_code(self.__ptr)

    @property
    def exch_fee(self):
        lib.node().xroad_trd_capt_exch_fee_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_exch_fee_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_exch_fee.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_exch_fee.restype = ctypes.c_double
            return lib.node().xroad_trd_capt_get_exch_fee(self.__ptr)
        else:
            return None

    @exch_fee.setter
    def exch_fee(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_exch_fee.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_trd_capt_set_exch_fee(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_exch_fee.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_exch_fee(self.__ptr)

    @property
    def book(self):
        lib.node().xroad_trd_capt_book_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_book_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_book.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_book.restype = ctypes.POINTER(xtypes.Book)
            res = lib.node().xroad_trd_capt_get_book(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @book.setter
    def book(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_trd_capt_set_book.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_trd_capt_set_book(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_trd_capt_reset_book.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_book(self.__ptr)

    @property
    def otc_id(self):
        lib.node().xroad_trd_capt_otc_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_otc_id_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_otc_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_otc_id.restype = ctypes.c_long
            return lib.node().xroad_trd_capt_get_otc_id(self.__ptr)
        else:
            return None

    @otc_id.setter
    def otc_id(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_otc_id.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_trd_capt_set_otc_id(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_otc_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_otc_id(self.__ptr)

    @property
    def counterparty(self):
        lib.node().xroad_trd_capt_counterparty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_counterparty_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_counterparty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_counterparty.restype = ctypes.POINTER(xtypes.Name)
            res = lib.node().xroad_trd_capt_get_counterparty(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @counterparty.setter
    def counterparty(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_trd_capt_set_counterparty.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_trd_capt_set_counterparty(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_trd_capt_reset_counterparty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_counterparty(self.__ptr)

    @property
    def deleted(self):
        lib.node().xroad_trd_capt_deleted_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_deleted_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_deleted.restype = ctypes.c_byte
            return lib.node().xroad_trd_capt_get_deleted(self.__ptr)
        else:
            return None

    @deleted.setter
    def deleted(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_deleted.argtypes = [ctypes.c_void_p, ctypes.c_byte]
            lib.node().xroad_trd_capt_set_deleted(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_deleted.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_deleted(self.__ptr)

    @property
    def face_value(self):
        lib.node().xroad_trd_capt_face_value_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_face_value_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_face_value.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_face_value.restype = ctypes.c_double
            return lib.node().xroad_trd_capt_get_face_value(self.__ptr)
        else:
            return None

    @face_value.setter
    def face_value(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_face_value.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_trd_capt_set_face_value(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_face_value.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_face_value(self.__ptr)

    @property
    def accrued_int(self):
        lib.node().xroad_trd_capt_accrued_int_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_accrued_int_is_set(self.__ptr):
            lib.node().xroad_trd_capt_get_accrued_int.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_get_accrued_int.restype = ctypes.c_double
            return lib.node().xroad_trd_capt_get_accrued_int(self.__ptr)
        else:
            return None

    @accrued_int.setter
    def accrued_int(self, value):
        if value is not None:
            lib.node().xroad_trd_capt_set_accrued_int.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_trd_capt_set_accrued_int(self.__ptr, value)
        else:
            lib.node().xroad_trd_capt_reset_accrued_int.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_reset_accrued_int(self.__ptr)


class Rollover(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_rollover_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_rollover_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.rollover

    @property
    def is_valid(self):
        lib.node().xroad_rollover_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_rollover_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_rollover_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_rollover_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_rollover_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_rollover_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_rollover_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_rollover_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_rollover_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Rollover(lib.node().xroad_rollover_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_rollover_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_rollover_get_id.restype = ctypes.c_long
        return lib.node().xroad_rollover_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_rollover_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_rollover_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_rollover_copy(self.__ptr, id)
        return Rollover(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.start_ts
        if v is not None:
            fields["start_ts"] = v
        v = self.index
        if v is not None:
            fields["index"] = v
        v = self.leg1_alias
        if v is not None:
            fields["leg1_alias"] = v
        v = self.leg1_side
        if v is not None:
            fields["leg1_side"] = v.name
        v = self.leg1_state
        if v is not None:
            fields["leg1_state"] = v
        v = self.leg1_reason
        if v is not None:
            fields["leg1_reason"] = v
        v = self.leg1_price
        if v is not None:
            fields["leg1_price"] = v
        v = self.leg1_qty
        if v is not None:
            fields["leg1_qty"] = v
        v = self.leg1_cum_qty
        if v is not None:
            fields["leg1_cum_qty"] = v
        v = self.leg2_alias
        if v is not None:
            fields["leg2_alias"] = v
        v = self.leg2_side
        if v is not None:
            fields["leg2_side"] = v.name
        v = self.leg2_state
        if v is not None:
            fields["leg2_state"] = v
        v = self.leg2_reason
        if v is not None:
            fields["leg2_reason"] = v
        v = self.leg2_price
        if v is not None:
            fields["leg2_price"] = v
        v = self.leg2_qty
        if v is not None:
            fields["leg2_qty"] = v
        v = self.leg2_cum_qty
        if v is not None:
            fields["leg2_cum_qty"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "start_ts":
            self.start_ts = int(value) if value is not None else value
        elif field == "index":
            self.index = float(value) if value is not None else value
        elif field == "leg1_alias":
            self.leg1_alias = str(value) if value is not None else value
        elif field == "leg1_side":
            self.leg1_side = xtypes.Side[value] if value is not None else value
        elif field == "leg1_state":
            self.leg1_state = int(value) if value is not None else value
        elif field == "leg1_reason":
            self.leg1_reason = str(value) if value is not None else value
        elif field == "leg1_price":
            self.leg1_price = float(value) if value is not None else value
        elif field == "leg1_qty":
            self.leg1_qty = int(value) if value is not None else value
        elif field == "leg1_cum_qty":
            self.leg1_cum_qty = int(value) if value is not None else value
        elif field == "leg2_alias":
            self.leg2_alias = str(value) if value is not None else value
        elif field == "leg2_side":
            self.leg2_side = xtypes.Side[value] if value is not None else value
        elif field == "leg2_state":
            self.leg2_state = int(value) if value is not None else value
        elif field == "leg2_reason":
            self.leg2_reason = str(value) if value is not None else value
        elif field == "leg2_price":
            self.leg2_price = float(value) if value is not None else value
        elif field == "leg2_qty":
            self.leg2_qty = int(value) if value is not None else value
        elif field == "leg2_cum_qty":
            self.leg2_cum_qty = int(value) if value is not None else value

    @property
    def node_id(self):
        lib.node().xroad_rollover_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_node_id_is_set(self.__ptr):
            lib.node().xroad_rollover_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_rollover_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_rollover_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_node_id(self.__ptr)

    @property
    def start_ts(self):
        lib.node().xroad_rollover_start_ts_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_start_ts_is_set(self.__ptr):
            lib.node().xroad_rollover_get_start_ts.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_start_ts.restype = ctypes.c_ulong
            return lib.node().xroad_rollover_get_start_ts(self.__ptr)
        else:
            return None

    @start_ts.setter
    def start_ts(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_start_ts.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_rollover_set_start_ts(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_start_ts.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_start_ts(self.__ptr)

    @property
    def index(self):
        lib.node().xroad_rollover_index_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_index_is_set(self.__ptr):
            lib.node().xroad_rollover_get_index.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_index.restype = ctypes.c_double
            return lib.node().xroad_rollover_get_index(self.__ptr)
        else:
            return None

    @index.setter
    def index(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_index.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_rollover_set_index(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_index.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_index(self.__ptr)

    @property
    def leg1_alias(self):
        lib.node().xroad_rollover_leg1_alias_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg1_alias_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg1_alias.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg1_alias.restype = ctypes.POINTER(xtypes.Alias)
            res = lib.node().xroad_rollover_get_leg1_alias(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @leg1_alias.setter
    def leg1_alias(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_rollover_set_leg1_alias.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_rollover_set_leg1_alias(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_rollover_reset_leg1_alias.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg1_alias(self.__ptr)

    @property
    def leg1_side(self):
        lib.node().xroad_rollover_leg1_side_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg1_side_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg1_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg1_side.restype = ctypes.c_int
            return xtypes.Side(lib.node().xroad_rollover_get_leg1_side(self.__ptr))
        else:
            return None

    @leg1_side.setter
    def leg1_side(self, value):
        if not isinstance(value, xtypes.Side) and value is not None:
            raise TypeError("{0} has wrong type. must be Side enum".format(value))
        if value is not None:
            lib.node().xroad_rollover_set_leg1_side.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rollover_set_leg1_side(self.__ptr, value.value)
        else:
            lib.node().xroad_rollover_reset_leg1_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg1_side(self.__ptr)

    @property
    def leg1_state(self):
        lib.node().xroad_rollover_leg1_state_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg1_state_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg1_state.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg1_state.restype = ctypes.c_int
            return lib.node().xroad_rollover_get_leg1_state(self.__ptr)
        else:
            return None

    @leg1_state.setter
    def leg1_state(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_leg1_state.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rollover_set_leg1_state(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_leg1_state.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg1_state(self.__ptr)

    @property
    def leg1_reason(self):
        lib.node().xroad_rollover_leg1_reason_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg1_reason_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg1_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg1_reason.restype = ctypes.POINTER(xtypes.Text)
            res = lib.node().xroad_rollover_get_leg1_reason(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @leg1_reason.setter
    def leg1_reason(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_rollover_set_leg1_reason.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_rollover_set_leg1_reason(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_rollover_reset_leg1_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg1_reason(self.__ptr)

    @property
    def leg1_price(self):
        lib.node().xroad_rollover_leg1_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg1_price_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg1_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg1_price.restype = ctypes.c_double
            return lib.node().xroad_rollover_get_leg1_price(self.__ptr)
        else:
            return None

    @leg1_price.setter
    def leg1_price(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_leg1_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_rollover_set_leg1_price(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_leg1_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg1_price(self.__ptr)

    @property
    def leg1_qty(self):
        lib.node().xroad_rollover_leg1_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg1_qty_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg1_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg1_qty.restype = ctypes.c_long
            return lib.node().xroad_rollover_get_leg1_qty(self.__ptr)
        else:
            return None

    @leg1_qty.setter
    def leg1_qty(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_leg1_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_rollover_set_leg1_qty(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_leg1_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg1_qty(self.__ptr)

    @property
    def leg1_cum_qty(self):
        lib.node().xroad_rollover_leg1_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg1_cum_qty_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg1_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg1_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_rollover_get_leg1_cum_qty(self.__ptr)
        else:
            return None

    @leg1_cum_qty.setter
    def leg1_cum_qty(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_leg1_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_rollover_set_leg1_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_leg1_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg1_cum_qty(self.__ptr)

    @property
    def leg2_alias(self):
        lib.node().xroad_rollover_leg2_alias_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg2_alias_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg2_alias.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg2_alias.restype = ctypes.POINTER(xtypes.Alias)
            res = lib.node().xroad_rollover_get_leg2_alias(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @leg2_alias.setter
    def leg2_alias(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_rollover_set_leg2_alias.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_rollover_set_leg2_alias(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_rollover_reset_leg2_alias.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg2_alias(self.__ptr)

    @property
    def leg2_side(self):
        lib.node().xroad_rollover_leg2_side_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg2_side_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg2_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg2_side.restype = ctypes.c_int
            return xtypes.Side(lib.node().xroad_rollover_get_leg2_side(self.__ptr))
        else:
            return None

    @leg2_side.setter
    def leg2_side(self, value):
        if not isinstance(value, xtypes.Side) and value is not None:
            raise TypeError("{0} has wrong type. must be Side enum".format(value))
        if value is not None:
            lib.node().xroad_rollover_set_leg2_side.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rollover_set_leg2_side(self.__ptr, value.value)
        else:
            lib.node().xroad_rollover_reset_leg2_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg2_side(self.__ptr)

    @property
    def leg2_state(self):
        lib.node().xroad_rollover_leg2_state_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg2_state_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg2_state.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg2_state.restype = ctypes.c_int
            return lib.node().xroad_rollover_get_leg2_state(self.__ptr)
        else:
            return None

    @leg2_state.setter
    def leg2_state(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_leg2_state.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_rollover_set_leg2_state(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_leg2_state.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg2_state(self.__ptr)

    @property
    def leg2_reason(self):
        lib.node().xroad_rollover_leg2_reason_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg2_reason_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg2_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg2_reason.restype = ctypes.POINTER(xtypes.Text)
            res = lib.node().xroad_rollover_get_leg2_reason(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @leg2_reason.setter
    def leg2_reason(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_rollover_set_leg2_reason.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_rollover_set_leg2_reason(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_rollover_reset_leg2_reason.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg2_reason(self.__ptr)

    @property
    def leg2_price(self):
        lib.node().xroad_rollover_leg2_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg2_price_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg2_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg2_price.restype = ctypes.c_double
            return lib.node().xroad_rollover_get_leg2_price(self.__ptr)
        else:
            return None

    @leg2_price.setter
    def leg2_price(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_leg2_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_rollover_set_leg2_price(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_leg2_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg2_price(self.__ptr)

    @property
    def leg2_qty(self):
        lib.node().xroad_rollover_leg2_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg2_qty_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg2_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg2_qty.restype = ctypes.c_long
            return lib.node().xroad_rollover_get_leg2_qty(self.__ptr)
        else:
            return None

    @leg2_qty.setter
    def leg2_qty(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_leg2_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_rollover_set_leg2_qty(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_leg2_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg2_qty(self.__ptr)

    @property
    def leg2_cum_qty(self):
        lib.node().xroad_rollover_leg2_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_rollover_leg2_cum_qty_is_set(self.__ptr):
            lib.node().xroad_rollover_get_leg2_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_get_leg2_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_rollover_get_leg2_cum_qty(self.__ptr)
        else:
            return None

    @leg2_cum_qty.setter
    def leg2_cum_qty(self, value):
        if value is not None:
            lib.node().xroad_rollover_set_leg2_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_rollover_set_leg2_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_rollover_reset_leg2_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_rollover_reset_leg2_cum_qty(self.__ptr)


class Mmaker(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_mmaker_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_mmaker_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.mmaker

    @property
    def is_valid(self):
        lib.node().xroad_mmaker_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_mmaker_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_mmaker_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_mmaker_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_mmaker_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_mmaker_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_mmaker_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_mmaker_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_mmaker_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Mmaker(lib.node().xroad_mmaker_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_mmaker_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_mmaker_get_id.restype = ctypes.c_long
        return lib.node().xroad_mmaker_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_mmaker_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_mmaker_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_mmaker_copy(self.__ptr, id)
        return Mmaker(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.start_ts
        if v is not None:
            fields["start_ts"] = v
        v = self.instr
        if v is not None:
            fields["instr"] = "({0},{1})".format(v.object_type, v.id)
        v = self.active_side
        if v is not None:
            fields["active_side"] = v.name
        v = self.best_bid
        if v is not None:
            fields["best_bid"] = v
        v = self.last_trade
        if v is not None:
            fields["last_trade"] = v.name
        v = self.total_buy
        if v is not None:
            fields["total_buy"] = v
        v = self.total_sell
        if v is not None:
            fields["total_sell"] = v
        v = self.bids
        if v is not None:
            try:
                fields["bids"] = binascii.b2a_hex(v).decode("utf-8")
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(binascii.b2a_hex(v), self.__class__))
                return ''
        v = self.asks
        if v is not None:
            try:
                fields["asks"] = binascii.b2a_hex(v).decode("utf-8")
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(binascii.b2a_hex(v), self.__class__))
                return ''
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "start_ts":
            self.start_ts = int(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)
        elif field == "active_side":
            self.active_side = xtypes.Side[value] if value is not None else value
        elif field == "best_bid":
            self.best_bid = float(value) if value is not None else value
        elif field == "last_trade":
            self.last_trade = xtypes.Side[value] if value is not None else value
        elif field == "total_buy":
            self.total_buy = int(value) if value is not None else value
        elif field == "total_sell":
            self.total_sell = int(value) if value is not None else value
        elif field == "bids":
            self.bids = binascii.unhexlify(value.replace(" ", "")) if value is not None else value
        elif field == "asks":
            self.asks = binascii.unhexlify(value.replace(" ", "")) if value is not None else value

    @property
    def node_id(self):
        lib.node().xroad_mmaker_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mmaker_node_id_is_set(self.__ptr):
            lib.node().xroad_mmaker_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_mmaker_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_mmaker_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_mmaker_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_mmaker_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_reset_node_id(self.__ptr)

    @property
    def start_ts(self):
        lib.node().xroad_mmaker_start_ts_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mmaker_start_ts_is_set(self.__ptr):
            lib.node().xroad_mmaker_get_start_ts.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_get_start_ts.restype = ctypes.c_ulong
            return lib.node().xroad_mmaker_get_start_ts(self.__ptr)
        else:
            return None

    @start_ts.setter
    def start_ts(self, value):
        if value is not None:
            lib.node().xroad_mmaker_set_start_ts.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_mmaker_set_start_ts(self.__ptr, value)
        else:
            lib.node().xroad_mmaker_reset_start_ts.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_reset_start_ts(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_mmaker_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mmaker_instr_is_set(self.__ptr):
            lib.node().xroad_mmaker_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_mmaker_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_mmaker_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_mmaker_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_mmaker_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_mmaker_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_mmaker_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_reset_instr(self.__ptr)

    @property
    def active_side(self):
        lib.node().xroad_mmaker_active_side_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mmaker_active_side_is_set(self.__ptr):
            lib.node().xroad_mmaker_get_active_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_get_active_side.restype = ctypes.c_int
            return xtypes.Side(lib.node().xroad_mmaker_get_active_side(self.__ptr))
        else:
            return None

    @active_side.setter
    def active_side(self, value):
        if not isinstance(value, xtypes.Side) and value is not None:
            raise TypeError("{0} has wrong type. must be Side enum".format(value))
        if value is not None:
            lib.node().xroad_mmaker_set_active_side.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_mmaker_set_active_side(self.__ptr, value.value)
        else:
            lib.node().xroad_mmaker_reset_active_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_reset_active_side(self.__ptr)

    @property
    def best_bid(self):
        lib.node().xroad_mmaker_best_bid_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mmaker_best_bid_is_set(self.__ptr):
            lib.node().xroad_mmaker_get_best_bid.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_get_best_bid.restype = ctypes.c_double
            return lib.node().xroad_mmaker_get_best_bid(self.__ptr)
        else:
            return None

    @best_bid.setter
    def best_bid(self, value):
        if value is not None:
            lib.node().xroad_mmaker_set_best_bid.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_mmaker_set_best_bid(self.__ptr, value)
        else:
            lib.node().xroad_mmaker_reset_best_bid.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_reset_best_bid(self.__ptr)

    @property
    def last_trade(self):
        lib.node().xroad_mmaker_last_trade_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mmaker_last_trade_is_set(self.__ptr):
            lib.node().xroad_mmaker_get_last_trade.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_get_last_trade.restype = ctypes.c_int
            return xtypes.Side(lib.node().xroad_mmaker_get_last_trade(self.__ptr))
        else:
            return None

    @last_trade.setter
    def last_trade(self, value):
        if not isinstance(value, xtypes.Side) and value is not None:
            raise TypeError("{0} has wrong type. must be Side enum".format(value))
        if value is not None:
            lib.node().xroad_mmaker_set_last_trade.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_mmaker_set_last_trade(self.__ptr, value.value)
        else:
            lib.node().xroad_mmaker_reset_last_trade.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_reset_last_trade(self.__ptr)

    @property
    def total_buy(self):
        lib.node().xroad_mmaker_total_buy_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mmaker_total_buy_is_set(self.__ptr):
            lib.node().xroad_mmaker_get_total_buy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_get_total_buy.restype = ctypes.c_long
            return lib.node().xroad_mmaker_get_total_buy(self.__ptr)
        else:
            return None

    @total_buy.setter
    def total_buy(self, value):
        if value is not None:
            lib.node().xroad_mmaker_set_total_buy.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_mmaker_set_total_buy(self.__ptr, value)
        else:
            lib.node().xroad_mmaker_reset_total_buy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_reset_total_buy(self.__ptr)

    @property
    def total_sell(self):
        lib.node().xroad_mmaker_total_sell_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mmaker_total_sell_is_set(self.__ptr):
            lib.node().xroad_mmaker_get_total_sell.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_get_total_sell.restype = ctypes.c_long
            return lib.node().xroad_mmaker_get_total_sell(self.__ptr)
        else:
            return None

    @total_sell.setter
    def total_sell(self, value):
        if value is not None:
            lib.node().xroad_mmaker_set_total_sell.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_mmaker_set_total_sell(self.__ptr, value)
        else:
            lib.node().xroad_mmaker_reset_total_sell.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_reset_total_sell(self.__ptr)

    @property
    def bids(self):
        lib.node().xroad_mmaker_bids_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mmaker_bids_is_set(self.__ptr):
            lib.node().xroad_mmaker_get_bids.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_get_bids.restype = ctypes.POINTER(xtypes.Levels)
            res = lib.node().xroad_mmaker_get_bids(self.__ptr)
            return bytes(res.contents.data[:res.contents.len])
        else:
            return None

    @bids.setter
    def bids(self, value):
        if value is not None and not isinstance(value, bytes):
            raise TypeError("{0} has wrong type. must be bytes".format(value))
        if value is not None:
            lib.node().xroad_mmaker_set_bids.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]
            lib.node().xroad_mmaker_set_bids(self.__ptr, value, len(value))
        else:
            lib.node().xroad_mmaker_reset_bids.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_reset_bids(self.__ptr)

    @property
    def asks(self):
        lib.node().xroad_mmaker_asks_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mmaker_asks_is_set(self.__ptr):
            lib.node().xroad_mmaker_get_asks.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_get_asks.restype = ctypes.POINTER(xtypes.Levels)
            res = lib.node().xroad_mmaker_get_asks(self.__ptr)
            return bytes(res.contents.data[:res.contents.len])
        else:
            return None

    @asks.setter
    def asks(self, value):
        if value is not None and not isinstance(value, bytes):
            raise TypeError("{0} has wrong type. must be bytes".format(value))
        if value is not None:
            lib.node().xroad_mmaker_set_asks.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]
            lib.node().xroad_mmaker_set_asks(self.__ptr, value, len(value))
        else:
            lib.node().xroad_mmaker_reset_asks.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mmaker_reset_asks(self.__ptr)


class Sniper(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_sniper_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_sniper_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.sniper

    @property
    def is_valid(self):
        lib.node().xroad_sniper_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_sniper_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_sniper_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_sniper_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_sniper_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_sniper_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_sniper_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_sniper_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_sniper_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Sniper(lib.node().xroad_sniper_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_sniper_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_sniper_get_id.restype = ctypes.c_long
        return lib.node().xroad_sniper_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_sniper_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_sniper_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_sniper_copy(self.__ptr, id)
        return Sniper(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        return fields


class TrdCaptLinkPos(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_trd_capt_link_pos_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_trd_capt_link_pos_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.trd_capt_link_pos

    @property
    def is_valid(self):
        lib.node().xroad_trd_capt_link_pos_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_trd_capt_link_pos_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_trd_capt_link_pos_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_trd_capt_link_pos_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_trd_capt_link_pos_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_trd_capt_link_pos_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_trd_capt_link_pos_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_trd_capt_link_pos_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_trd_capt_link_pos_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return TrdCaptLinkPos(lib.node().xroad_trd_capt_link_pos_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_trd_capt_link_pos_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_trd_capt_link_pos_get_id.restype = ctypes.c_long
        return lib.node().xroad_trd_capt_link_pos_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_trd_capt_link_pos_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_trd_capt_link_pos_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_trd_capt_link_pos_copy(self.__ptr, id)
        return TrdCaptLinkPos(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.trd_capt
        if v is not None:
            fields["trd_capt"] = "({0},{1})".format(v.object_type, v.id)
        v = self.pos
        if v is not None:
            fields["pos"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "trd_capt":
            if hasattr(value, "ptr"):
                self.trd_capt = value
            else:
                self.trd_capt = str_to_tuple(value)
        elif field == "pos":
            if hasattr(value, "ptr"):
                self.pos = value
            else:
                self.pos = str_to_tuple(value)

    @property
    def trd_capt(self):
        lib.node().xroad_trd_capt_link_pos_trd_capt_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_link_pos_trd_capt_is_set(self.__ptr):
            lib.node().xroad_trd_capt_link_pos_get_trd_capt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_link_pos_get_trd_capt.restype = ctypes.c_void_p
            obj = lib.node().xroad_trd_capt_link_pos_get_trd_capt(self.__ptr)
            if not obj:
                raise BrokenRefError("reference trd_capt is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @trd_capt.setter
    def trd_capt(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_trd_capt_link_pos_set_trd_capt.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_trd_capt_link_pos_set_trd_capt(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_trd_capt_link_pos_set_trd_capt_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_trd_capt_link_pos_set_trd_capt_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_trd_capt_link_pos_reset_trd_capt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_link_pos_reset_trd_capt(self.__ptr)

    @property
    def pos(self):
        lib.node().xroad_trd_capt_link_pos_pos_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_link_pos_pos_is_set(self.__ptr):
            lib.node().xroad_trd_capt_link_pos_get_pos.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_link_pos_get_pos.restype = ctypes.c_void_p
            obj = lib.node().xroad_trd_capt_link_pos_get_pos(self.__ptr)
            if not obj:
                raise BrokenRefError("reference pos is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @pos.setter
    def pos(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_trd_capt_link_pos_set_pos.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_trd_capt_link_pos_set_pos(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_trd_capt_link_pos_set_pos_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_trd_capt_link_pos_set_pos_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_trd_capt_link_pos_reset_pos.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_link_pos_reset_pos(self.__ptr)


class OrderLog(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_order_log_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_order_log_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.order_log

    @property
    def is_valid(self):
        lib.node().xroad_order_log_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_order_log_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_order_log_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_order_log_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_order_log_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_order_log_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_order_log_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_order_log_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_log_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return OrderLog(lib.node().xroad_order_log_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_order_log_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_order_log_get_id.restype = ctypes.c_long
        return lib.node().xroad_order_log_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_order_log_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_order_log_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_order_log_copy(self.__ptr, id)
        return OrderLog(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.exec_id
        if v is not None:
            fields["exec_id"] = v
        v = self.orderno
        if v is not None:
            fields["orderno"] = v
        v = self.instr
        if v is not None:
            fields["instr"] = "({0},{1})".format(v.object_type, v.id)
        v = self.side
        if v is not None:
            fields["side"] = v.name
        v = self.qty
        if v is not None:
            fields["qty"] = v
        v = self.leaves_qty
        if v is not None:
            fields["leaves_qty"] = v
        v = self.cum_qty
        if v is not None:
            fields["cum_qty"] = v
        v = self.price
        if v is not None:
            fields["price"] = v
        v = self.exec_type
        if v is not None:
            fields["exec_type"] = v.name
        v = self.status
        if v is not None:
            fields["status"] = v.name
        v = self.account
        if v is not None:
            fields["account"] = v
        v = self.client_code
        if v is not None:
            fields["client_code"] = v
        v = self.tran_time
        if v is not None:
            fields["tran_time"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "exec_id":
            self.exec_id = str(value) if value is not None else value
        elif field == "orderno":
            self.orderno = int(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)
        elif field == "side":
            self.side = xtypes.Side[value] if value is not None else value
        elif field == "qty":
            self.qty = int(value) if value is not None else value
        elif field == "leaves_qty":
            self.leaves_qty = int(value) if value is not None else value
        elif field == "cum_qty":
            self.cum_qty = int(value) if value is not None else value
        elif field == "price":
            self.price = float(value) if value is not None else value
        elif field == "exec_type":
            self.exec_type = xtypes.ExecType[value] if value is not None else value
        elif field == "status":
            self.status = xtypes.OrderStatus[value] if value is not None else value
        elif field == "account":
            self.account = str(value) if value is not None else value
        elif field == "client_code":
            self.client_code = str(value) if value is not None else value
        elif field == "tran_time":
            self.tran_time = int(value) if value is not None else value

    @property
    def node_id(self):
        lib.node().xroad_order_log_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_node_id_is_set(self.__ptr):
            lib.node().xroad_order_log_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_order_log_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_order_log_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_order_log_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_order_log_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_node_id(self.__ptr)

    @property
    def exec_id(self):
        lib.node().xroad_order_log_exec_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_exec_id_is_set(self.__ptr):
            lib.node().xroad_order_log_get_exec_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_exec_id.restype = ctypes.POINTER(xtypes.ExecId)
            res = lib.node().xroad_order_log_get_exec_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @exec_id.setter
    def exec_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_log_set_exec_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_log_set_exec_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_log_reset_exec_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_exec_id(self.__ptr)

    @property
    def orderno(self):
        lib.node().xroad_order_log_orderno_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_orderno_is_set(self.__ptr):
            lib.node().xroad_order_log_get_orderno.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_orderno.restype = ctypes.c_ulong
            return lib.node().xroad_order_log_get_orderno(self.__ptr)
        else:
            return None

    @orderno.setter
    def orderno(self, value):
        if value is not None:
            lib.node().xroad_order_log_set_orderno.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            lib.node().xroad_order_log_set_orderno(self.__ptr, value)
        else:
            lib.node().xroad_order_log_reset_orderno.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_orderno(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_order_log_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_instr_is_set(self.__ptr):
            lib.node().xroad_order_log_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_order_log_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_order_log_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_order_log_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_order_log_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_order_log_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_order_log_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_instr(self.__ptr)

    @property
    def side(self):
        lib.node().xroad_order_log_side_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_side_is_set(self.__ptr):
            lib.node().xroad_order_log_get_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_side.restype = ctypes.c_int
            return xtypes.Side(lib.node().xroad_order_log_get_side(self.__ptr))
        else:
            return None

    @side.setter
    def side(self, value):
        if not isinstance(value, xtypes.Side) and value is not None:
            raise TypeError("{0} has wrong type. must be Side enum".format(value))
        if value is not None:
            lib.node().xroad_order_log_set_side.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_log_set_side(self.__ptr, value.value)
        else:
            lib.node().xroad_order_log_reset_side.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_side(self.__ptr)

    @property
    def qty(self):
        lib.node().xroad_order_log_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_qty_is_set(self.__ptr):
            lib.node().xroad_order_log_get_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_qty.restype = ctypes.c_long
            return lib.node().xroad_order_log_get_qty(self.__ptr)
        else:
            return None

    @qty.setter
    def qty(self, value):
        if value is not None:
            lib.node().xroad_order_log_set_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_log_set_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_log_reset_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_qty(self.__ptr)

    @property
    def leaves_qty(self):
        lib.node().xroad_order_log_leaves_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_leaves_qty_is_set(self.__ptr):
            lib.node().xroad_order_log_get_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_leaves_qty.restype = ctypes.c_long
            return lib.node().xroad_order_log_get_leaves_qty(self.__ptr)
        else:
            return None

    @leaves_qty.setter
    def leaves_qty(self, value):
        if value is not None:
            lib.node().xroad_order_log_set_leaves_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_log_set_leaves_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_log_reset_leaves_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_leaves_qty(self.__ptr)

    @property
    def cum_qty(self):
        lib.node().xroad_order_log_cum_qty_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_cum_qty_is_set(self.__ptr):
            lib.node().xroad_order_log_get_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_cum_qty.restype = ctypes.c_long
            return lib.node().xroad_order_log_get_cum_qty(self.__ptr)
        else:
            return None

    @cum_qty.setter
    def cum_qty(self, value):
        if value is not None:
            lib.node().xroad_order_log_set_cum_qty.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_log_set_cum_qty(self.__ptr, value)
        else:
            lib.node().xroad_order_log_reset_cum_qty.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_cum_qty(self.__ptr)

    @property
    def price(self):
        lib.node().xroad_order_log_price_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_price_is_set(self.__ptr):
            lib.node().xroad_order_log_get_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_price.restype = ctypes.c_double
            return lib.node().xroad_order_log_get_price(self.__ptr)
        else:
            return None

    @price.setter
    def price(self, value):
        if value is not None:
            lib.node().xroad_order_log_set_price.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_order_log_set_price(self.__ptr, value)
        else:
            lib.node().xroad_order_log_reset_price.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_price(self.__ptr)

    @property
    def exec_type(self):
        lib.node().xroad_order_log_exec_type_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_exec_type_is_set(self.__ptr):
            lib.node().xroad_order_log_get_exec_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_exec_type.restype = ctypes.c_int
            return xtypes.ExecType(lib.node().xroad_order_log_get_exec_type(self.__ptr))
        else:
            return None

    @exec_type.setter
    def exec_type(self, value):
        if not isinstance(value, xtypes.ExecType) and value is not None:
            raise TypeError("{0} has wrong type. must be ExecType enum".format(value))
        if value is not None:
            lib.node().xroad_order_log_set_exec_type.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_log_set_exec_type(self.__ptr, value.value)
        else:
            lib.node().xroad_order_log_reset_exec_type.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_exec_type(self.__ptr)

    @property
    def status(self):
        lib.node().xroad_order_log_status_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_status_is_set(self.__ptr):
            lib.node().xroad_order_log_get_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_status.restype = ctypes.c_int
            return xtypes.OrderStatus(lib.node().xroad_order_log_get_status(self.__ptr))
        else:
            return None

    @status.setter
    def status(self, value):
        if not isinstance(value, xtypes.OrderStatus) and value is not None:
            raise TypeError("{0} has wrong type. must be OrderStatus enum".format(value))
        if value is not None:
            lib.node().xroad_order_log_set_status.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_order_log_set_status(self.__ptr, value.value)
        else:
            lib.node().xroad_order_log_reset_status.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_status(self.__ptr)

    @property
    def account(self):
        lib.node().xroad_order_log_account_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_account_is_set(self.__ptr):
            lib.node().xroad_order_log_get_account.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_account.restype = ctypes.POINTER(xtypes.Account)
            res = lib.node().xroad_order_log_get_account(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @account.setter
    def account(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_log_set_account.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_log_set_account(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_log_reset_account.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_account(self.__ptr)

    @property
    def client_code(self):
        lib.node().xroad_order_log_client_code_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_client_code_is_set(self.__ptr):
            lib.node().xroad_order_log_get_client_code.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_client_code.restype = ctypes.POINTER(xtypes.ClientCode)
            res = lib.node().xroad_order_log_get_client_code(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @client_code.setter
    def client_code(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_order_log_set_client_code.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_order_log_set_client_code(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_order_log_reset_client_code.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_client_code(self.__ptr)

    @property
    def tran_time(self):
        lib.node().xroad_order_log_tran_time_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_order_log_tran_time_is_set(self.__ptr):
            lib.node().xroad_order_log_get_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_get_tran_time.restype = ctypes.c_long
            return lib.node().xroad_order_log_get_tran_time(self.__ptr)
        else:
            return None

    @tran_time.setter
    def tran_time(self, value):
        if value is not None:
            lib.node().xroad_order_log_set_tran_time.argtypes = [ctypes.c_void_p, ctypes.c_long]
            lib.node().xroad_order_log_set_tran_time(self.__ptr, value)
        else:
            lib.node().xroad_order_log_reset_tran_time.argtypes = [ctypes.c_void_p]
            lib.node().xroad_order_log_reset_tran_time(self.__ptr)


class PosSum(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_pos_sum_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_pos_sum_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.pos_sum

    @property
    def is_valid(self):
        lib.node().xroad_pos_sum_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_pos_sum_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_pos_sum_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_pos_sum_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_pos_sum_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_pos_sum_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_pos_sum_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_pos_sum_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_pos_sum_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return PosSum(lib.node().xroad_pos_sum_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_pos_sum_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_pos_sum_get_id.restype = ctypes.c_long
        return lib.node().xroad_pos_sum_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_pos_sum_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_pos_sum_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_pos_sum_copy(self.__ptr, id)
        return PosSum(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.sender
        if v is not None:
            fields["sender"] = v
        v = self.book
        if v is not None:
            fields["book"] = v
        v = self.desk
        if v is not None:
            fields["desk"] = v
        v = self.realize_pnl
        if v is not None:
            fields["realize_pnl"] = v
        v = self.unrealize_pnl
        if v is not None:
            fields["unrealize_pnl"] = v
        v = self.exch_fee
        if v is not None:
            fields["exch_fee"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "sender":
            self.sender = str(value) if value is not None else value
        elif field == "book":
            self.book = str(value) if value is not None else value
        elif field == "desk":
            self.desk = str(value) if value is not None else value
        elif field == "realize_pnl":
            self.realize_pnl = float(value) if value is not None else value
        elif field == "unrealize_pnl":
            self.unrealize_pnl = float(value) if value is not None else value
        elif field == "exch_fee":
            self.exch_fee = float(value) if value is not None else value

    @property
    def sender(self):
        lib.node().xroad_pos_sum_sender_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_sum_sender_is_set(self.__ptr):
            lib.node().xroad_pos_sum_get_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_get_sender.restype = ctypes.POINTER(xtypes.Sender)
            res = lib.node().xroad_pos_sum_get_sender(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @sender.setter
    def sender(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_pos_sum_set_sender.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_pos_sum_set_sender(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_pos_sum_reset_sender.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_reset_sender(self.__ptr)

    @property
    def book(self):
        lib.node().xroad_pos_sum_book_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_sum_book_is_set(self.__ptr):
            lib.node().xroad_pos_sum_get_book.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_get_book.restype = ctypes.POINTER(xtypes.Desk)
            res = lib.node().xroad_pos_sum_get_book(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @book.setter
    def book(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_pos_sum_set_book.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_pos_sum_set_book(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_pos_sum_reset_book.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_reset_book(self.__ptr)

    @property
    def desk(self):
        lib.node().xroad_pos_sum_desk_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_sum_desk_is_set(self.__ptr):
            lib.node().xroad_pos_sum_get_desk.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_get_desk.restype = ctypes.POINTER(xtypes.Desk)
            res = lib.node().xroad_pos_sum_get_desk(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @desk.setter
    def desk(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_pos_sum_set_desk.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_pos_sum_set_desk(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_pos_sum_reset_desk.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_reset_desk(self.__ptr)

    @property
    def realize_pnl(self):
        lib.node().xroad_pos_sum_realize_pnl_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_sum_realize_pnl_is_set(self.__ptr):
            lib.node().xroad_pos_sum_get_realize_pnl.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_get_realize_pnl.restype = ctypes.c_double
            return lib.node().xroad_pos_sum_get_realize_pnl(self.__ptr)
        else:
            return None

    @realize_pnl.setter
    def realize_pnl(self, value):
        if value is not None:
            lib.node().xroad_pos_sum_set_realize_pnl.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_sum_set_realize_pnl(self.__ptr, value)
        else:
            lib.node().xroad_pos_sum_reset_realize_pnl.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_reset_realize_pnl(self.__ptr)

    @property
    def unrealize_pnl(self):
        lib.node().xroad_pos_sum_unrealize_pnl_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_sum_unrealize_pnl_is_set(self.__ptr):
            lib.node().xroad_pos_sum_get_unrealize_pnl.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_get_unrealize_pnl.restype = ctypes.c_double
            return lib.node().xroad_pos_sum_get_unrealize_pnl(self.__ptr)
        else:
            return None

    @unrealize_pnl.setter
    def unrealize_pnl(self, value):
        if value is not None:
            lib.node().xroad_pos_sum_set_unrealize_pnl.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_sum_set_unrealize_pnl(self.__ptr, value)
        else:
            lib.node().xroad_pos_sum_reset_unrealize_pnl.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_reset_unrealize_pnl(self.__ptr)

    @property
    def exch_fee(self):
        lib.node().xroad_pos_sum_exch_fee_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_pos_sum_exch_fee_is_set(self.__ptr):
            lib.node().xroad_pos_sum_get_exch_fee.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_get_exch_fee.restype = ctypes.c_double
            return lib.node().xroad_pos_sum_get_exch_fee(self.__ptr)
        else:
            return None

    @exch_fee.setter
    def exch_fee(self, value):
        if value is not None:
            lib.node().xroad_pos_sum_set_exch_fee.argtypes = [ctypes.c_void_p, ctypes.c_double]
            lib.node().xroad_pos_sum_set_exch_fee(self.__ptr, value)
        else:
            lib.node().xroad_pos_sum_reset_exch_fee.argtypes = [ctypes.c_void_p]
            lib.node().xroad_pos_sum_reset_exch_fee(self.__ptr)


class Resolve(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_resolve_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_resolve_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.resolve

    @property
    def is_valid(self):
        lib.node().xroad_resolve_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_resolve_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_resolve_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_resolve_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_resolve_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_resolve_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_resolve_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_resolve_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_resolve_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return Resolve(lib.node().xroad_resolve_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_resolve_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_resolve_get_id.restype = ctypes.c_long
        return lib.node().xroad_resolve_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_resolve_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_resolve_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_resolve_copy(self.__ptr, id)
        return Resolve(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.req_id
        if v is not None:
            fields["req_id"] = v
        v = self.alias
        if v is not None:
            fields["alias"] = v
        v = self.from_node
        if v is not None:
            fields["from_node"] = v
        v = self.isin
        if v is not None:
            fields["isin"] = v
        v = self.bb_source
        if v is not None:
            fields["bb_source"] = v
        v = self.bb_code
        if v is not None:
            fields["bb_code"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "req_id":
            self.req_id = str(value) if value is not None else value
        elif field == "alias":
            self.alias = str(value) if value is not None else value
        elif field == "from_node":
            self.from_node = int(value) if value is not None else value
        elif field == "isin":
            self.isin = str(value) if value is not None else value
        elif field == "bb_source":
            self.bb_source = str(value) if value is not None else value
        elif field == "bb_code":
            self.bb_code = str(value) if value is not None else value

    @property
    def req_id(self):
        lib.node().xroad_resolve_req_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_resolve_req_id_is_set(self.__ptr):
            lib.node().xroad_resolve_get_req_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_get_req_id.restype = ctypes.POINTER(xtypes.Uuid)
            res = lib.node().xroad_resolve_get_req_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @req_id.setter
    def req_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_resolve_set_req_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_resolve_set_req_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_resolve_reset_req_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_reset_req_id(self.__ptr)

    @property
    def alias(self):
        lib.node().xroad_resolve_alias_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_resolve_alias_is_set(self.__ptr):
            lib.node().xroad_resolve_get_alias.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_get_alias.restype = ctypes.POINTER(xtypes.Alias)
            res = lib.node().xroad_resolve_get_alias(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @alias.setter
    def alias(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_resolve_set_alias.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_resolve_set_alias(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_resolve_reset_alias.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_reset_alias(self.__ptr)

    @property
    def from_node(self):
        lib.node().xroad_resolve_from_node_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_resolve_from_node_is_set(self.__ptr):
            lib.node().xroad_resolve_get_from_node.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_get_from_node.restype = ctypes.c_ushort
            return lib.node().xroad_resolve_get_from_node(self.__ptr)
        else:
            return None

    @from_node.setter
    def from_node(self, value):
        if value is not None:
            lib.node().xroad_resolve_set_from_node.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_resolve_set_from_node(self.__ptr, value)
        else:
            lib.node().xroad_resolve_reset_from_node.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_reset_from_node(self.__ptr)

    @property
    def isin(self):
        lib.node().xroad_resolve_isin_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_resolve_isin_is_set(self.__ptr):
            lib.node().xroad_resolve_get_isin.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_get_isin.restype = ctypes.POINTER(xtypes.Isin)
            res = lib.node().xroad_resolve_get_isin(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @isin.setter
    def isin(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_resolve_set_isin.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_resolve_set_isin(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_resolve_reset_isin.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_reset_isin(self.__ptr)

    @property
    def bb_source(self):
        lib.node().xroad_resolve_bb_source_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_resolve_bb_source_is_set(self.__ptr):
            lib.node().xroad_resolve_get_bb_source.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_get_bb_source.restype = ctypes.POINTER(xtypes.BbSource)
            res = lib.node().xroad_resolve_get_bb_source(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @bb_source.setter
    def bb_source(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_resolve_set_bb_source.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_resolve_set_bb_source(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_resolve_reset_bb_source.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_reset_bb_source(self.__ptr)

    @property
    def bb_code(self):
        lib.node().xroad_resolve_bb_code_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_resolve_bb_code_is_set(self.__ptr):
            lib.node().xroad_resolve_get_bb_code.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_get_bb_code.restype = ctypes.POINTER(xtypes.BbCode)
            res = lib.node().xroad_resolve_get_bb_code(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @bb_code.setter
    def bb_code(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_resolve_set_bb_code.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_resolve_set_bb_code(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_resolve_reset_bb_code.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_reset_bb_code(self.__ptr)


class ResolveAck(object):

    def __init__(self, ptr, delete_it):
        self.__ptr = ptr
        self.delete_it = delete_it

    def __del__(self):
        if self.delete_it and self.__ptr:
            lib.node().xroad_resolve_ack_destroy.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_ack_destroy(self.__ptr)
            self.__ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_resolve_ack_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_resolve_ack_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.resolve_ack

    @property
    def is_valid(self):
        lib.node().xroad_resolve_ack_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_resolve_ack_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_resolve_ack_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_resolve_ack_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_resolve_ack_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_resolve_ack_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_resolve_ack_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_resolve_ack_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_resolve_ack_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return ResolveAck(lib.node().xroad_resolve_ack_clone(self.__ptr))

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "req_id":
            self.req_id = str(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)

    @property
    def req_id(self):
        lib.node().xroad_resolve_ack_req_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_resolve_ack_req_id_is_set(self.__ptr):
            lib.node().xroad_resolve_ack_get_req_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_ack_get_req_id.restype = ctypes.POINTER(xtypes.Uuid)
            res = lib.node().xroad_resolve_ack_get_req_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @req_id.setter
    def req_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_resolve_ack_set_req_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_resolve_ack_set_req_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_resolve_ack_reset_req_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_ack_reset_req_id(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_resolve_ack_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_resolve_ack_instr_is_set(self.__ptr):
            lib.node().xroad_resolve_ack_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_ack_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_resolve_ack_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_resolve_ack_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_resolve_ack_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_resolve_ack_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_resolve_ack_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_resolve_ack_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_resolve_ack_reset_instr(self.__ptr)


class MdataSubs(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_mdata_subs_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_mdata_subs_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.mdata_subs

    @property
    def is_valid(self):
        lib.node().xroad_mdata_subs_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_mdata_subs_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_mdata_subs_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_mdata_subs_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_mdata_subs_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_mdata_subs_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_mdata_subs_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_mdata_subs_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_mdata_subs_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return MdataSubs(lib.node().xroad_mdata_subs_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_mdata_subs_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_mdata_subs_get_id.restype = ctypes.c_long
        return lib.node().xroad_mdata_subs_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_mdata_subs_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_mdata_subs_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_mdata_subs_copy(self.__ptr, id)
        return MdataSubs(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.node_id
        if v is not None:
            fields["node_id"] = v
        v = self.req_id
        if v is not None:
            fields["req_id"] = v
        v = self.instr
        if v is not None:
            fields["instr"] = "({0},{1})".format(v.object_type, v.id)
        v = self.state
        if v is not None:
            fields["state"] = v.name
        v = self.ref_cnt
        if v is not None:
            fields["ref_cnt"] = v
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "node_id":
            self.node_id = int(value) if value is not None else value
        elif field == "req_id":
            self.req_id = str(value) if value is not None else value
        elif field == "instr":
            if hasattr(value, "ptr"):
                self.instr = value
            else:
                self.instr = str_to_tuple(value)
        elif field == "state":
            self.state = xtypes.MdataSubsState[value] if value is not None else value
        elif field == "ref_cnt":
            self.ref_cnt = int(value) if value is not None else value

    @property
    def node_id(self):
        lib.node().xroad_mdata_subs_node_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mdata_subs_node_id_is_set(self.__ptr):
            lib.node().xroad_mdata_subs_get_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdata_subs_get_node_id.restype = ctypes.c_ushort
            return lib.node().xroad_mdata_subs_get_node_id(self.__ptr)
        else:
            return None

    @node_id.setter
    def node_id(self, value):
        if value is not None:
            lib.node().xroad_mdata_subs_set_node_id.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
            lib.node().xroad_mdata_subs_set_node_id(self.__ptr, value)
        else:
            lib.node().xroad_mdata_subs_reset_node_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdata_subs_reset_node_id(self.__ptr)

    @property
    def req_id(self):
        lib.node().xroad_mdata_subs_req_id_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mdata_subs_req_id_is_set(self.__ptr):
            lib.node().xroad_mdata_subs_get_req_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdata_subs_get_req_id.restype = ctypes.POINTER(xtypes.Uuid)
            res = lib.node().xroad_mdata_subs_get_req_id(self.__ptr)
            res = res.contents.data[:res.contents.len]
            try:
                return res.decode()
            except UnicodeDecodeError:
                logging.debug('incorrect string decode: {} for obj {}'.format(res, self.__class__))
                return ''
        else:
            return None

    @req_id.setter
    def req_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("{0} has wrong type. must be string".format(value))
        if value is not None:
            lib.node().xroad_mdata_subs_set_req_id.argtypes = [ctypes.c_void_p, xtypes.Str]
            lib.node().xroad_mdata_subs_set_req_id(self.__ptr, xtypes.Str(value))
        else:
            lib.node().xroad_mdata_subs_reset_req_id.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdata_subs_reset_req_id(self.__ptr)

    @property
    def instr(self):
        lib.node().xroad_mdata_subs_instr_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mdata_subs_instr_is_set(self.__ptr):
            lib.node().xroad_mdata_subs_get_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdata_subs_get_instr.restype = ctypes.c_void_p
            obj = lib.node().xroad_mdata_subs_get_instr(self.__ptr)
            if not obj:
                raise BrokenRefError("reference instr is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @instr.setter
    def instr(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_mdata_subs_set_instr.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_mdata_subs_set_instr(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_mdata_subs_set_instr_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_mdata_subs_set_instr_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_mdata_subs_reset_instr.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdata_subs_reset_instr(self.__ptr)

    @property
    def state(self):
        lib.node().xroad_mdata_subs_state_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mdata_subs_state_is_set(self.__ptr):
            lib.node().xroad_mdata_subs_get_state.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdata_subs_get_state.restype = ctypes.c_int
            return xtypes.MdataSubsState(lib.node().xroad_mdata_subs_get_state(self.__ptr))
        else:
            return None

    @state.setter
    def state(self, value):
        if not isinstance(value, xtypes.MdataSubsState) and value is not None:
            raise TypeError("{0} has wrong type. must be MdataSubsState enum".format(value))
        if value is not None:
            lib.node().xroad_mdata_subs_set_state.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_mdata_subs_set_state(self.__ptr, value.value)
        else:
            lib.node().xroad_mdata_subs_reset_state.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdata_subs_reset_state(self.__ptr)

    @property
    def ref_cnt(self):
        lib.node().xroad_mdata_subs_ref_cnt_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_mdata_subs_ref_cnt_is_set(self.__ptr):
            lib.node().xroad_mdata_subs_get_ref_cnt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdata_subs_get_ref_cnt.restype = ctypes.c_int
            return lib.node().xroad_mdata_subs_get_ref_cnt(self.__ptr)
        else:
            return None

    @ref_cnt.setter
    def ref_cnt(self, value):
        if value is not None:
            lib.node().xroad_mdata_subs_set_ref_cnt.argtypes = [ctypes.c_void_p, ctypes.c_int]
            lib.node().xroad_mdata_subs_set_ref_cnt(self.__ptr, value)
        else:
            lib.node().xroad_mdata_subs_reset_ref_cnt.argtypes = [ctypes.c_void_p]
            lib.node().xroad_mdata_subs_reset_ref_cnt(self.__ptr)


class TrdCaptMovePos(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        buf = ctypes.create_string_buffer(1024)
        lib.node().xroad_trd_capt_move_pos_print.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]
        sz = lib.node().xroad_trd_capt_move_pos_print(self.__ptr, buf, 1024)
        try:
            return buf.raw[:sz].decode()
        except UnicodeDecodeError:
            logging.debug('incorrect string decode: {} for obj {}'.format(buf.raw[:sz], self.__class__))
            return ''

    def __bool__(self):
        return self.__ptr > 0

    @property
    def ptr(self):
        return self.__ptr

    @property
    def object_type(self):
        return ObjectType.trd_capt_move_pos

    @property
    def is_valid(self):
        lib.node().xroad_trd_capt_move_pos_is_valid.argtypes = [ctypes.c_void_p]
        return lib.node().xroad_trd_capt_move_pos_is_valid(self.__ptr) == 1

    def send(self, node_id):
        lib.node().xroad_trd_capt_move_pos_send.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        res = lib.node().xroad_trd_capt_move_pos_send(self.__ptr, node_id)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} send failed. error = {1}".format(self, xtypes.Errno(res).name))

    def route(self, *args, spec=None):
        lib.node().xroad_trd_capt_move_pos_route.argtypes = [ctypes.c_void_p] + (spec if isinstance(spec, list) else [])
        res = xtypes.Errno.ok
        if len(args):
            res = lib.node().xroad_trd_capt_move_pos_route(self.__ptr, *args)
        else:
            res = lib.node().xroad_trd_capt_move_pos_route(self.__ptr)
        if res != xtypes.Errno.ok:
            raise XroadError("{0!s} route failed. error = {1}".format(self, xtypes.Errno(res).name))

    def clone(self):
        lib.node().xroad_trd_capt_move_pos_clone.argtypes = [ctypes.c_void_p]
        lib.node().xroad_trd_capt_move_pos_clone.restype = ctypes.c_void_p
        if not self.__ptr:
            raise XroadError("Unable to clone NULL object")
        return TrdCaptMovePos(lib.node().xroad_trd_capt_move_pos_clone(self.__ptr))

    @property
    def id(self):
        lib.node().xroad_trd_capt_move_pos_get_id.argtypes = [ctypes.c_void_p]
        lib.node().xroad_trd_capt_move_pos_get_id.restype = ctypes.c_long
        return lib.node().xroad_trd_capt_move_pos_get_id(self.__ptr)

    def copy(self, id):
        lib.node().xroad_trd_capt_move_pos_copy.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        lib.node().xroad_trd_capt_move_pos_copy.restype = ctypes.c_void_p
        new_obj = lib.node().xroad_trd_capt_move_pos_copy(self.__ptr, id)
        return TrdCaptMovePos(new_obj)

    def to_dict(self):
        fields = {"id" : self.id}
        v = self.trd_capt_to
        if v is not None:
            fields["trd_capt_to"] = "({0},{1})".format(v.object_type, v.id)
        v = self.trd_capt_from
        if v is not None:
            fields["trd_capt_from"] = "({0},{1})".format(v.object_type, v.id)
        return fields

    def get_field(self, field):
        if not hasattr(self, field):
            raise XroadError("unknown field {0}".format(field))
        return getattr(self, field)

    def set_field(self, field, value):
        if field == "trd_capt_to":
            if hasattr(value, "ptr"):
                self.trd_capt_to = value
            else:
                self.trd_capt_to = str_to_tuple(value)
        elif field == "trd_capt_from":
            if hasattr(value, "ptr"):
                self.trd_capt_from = value
            else:
                self.trd_capt_from = str_to_tuple(value)

    @property
    def trd_capt_to(self):
        lib.node().xroad_trd_capt_move_pos_trd_capt_to_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_move_pos_trd_capt_to_is_set(self.__ptr):
            lib.node().xroad_trd_capt_move_pos_get_trd_capt_to.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_move_pos_get_trd_capt_to.restype = ctypes.c_void_p
            obj = lib.node().xroad_trd_capt_move_pos_get_trd_capt_to(self.__ptr)
            if not obj:
                raise BrokenRefError("reference trd_capt_to is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @trd_capt_to.setter
    def trd_capt_to(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_trd_capt_move_pos_set_trd_capt_to.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_trd_capt_move_pos_set_trd_capt_to(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_trd_capt_move_pos_set_trd_capt_to_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_trd_capt_move_pos_set_trd_capt_to_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_trd_capt_move_pos_reset_trd_capt_to.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_move_pos_reset_trd_capt_to(self.__ptr)

    @property
    def trd_capt_from(self):
        lib.node().xroad_trd_capt_move_pos_trd_capt_from_is_set.argtypes = [ctypes.c_void_p]
        if lib.node().xroad_trd_capt_move_pos_trd_capt_from_is_set(self.__ptr):
            lib.node().xroad_trd_capt_move_pos_get_trd_capt_from.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_move_pos_get_trd_capt_from.restype = ctypes.c_void_p
            obj = lib.node().xroad_trd_capt_move_pos_get_trd_capt_from(self.__ptr)
            if not obj:
                raise BrokenRefError("reference trd_capt_from is broken in {0} object".format(self))
            return ptr_to_object(obj)
        else:
            return None

    @trd_capt_from.setter
    def trd_capt_from(self, value):
        if value is not None:
            if hasattr(value, "ptr"):
                lib.node().xroad_trd_capt_move_pos_set_trd_capt_from.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                lib.node().xroad_trd_capt_move_pos_set_trd_capt_from(self.__ptr, value.ptr)
            elif isinstance(value, tuple) and len(value) == 2:
                lib.node().xroad_trd_capt_move_pos_set_trd_capt_from_ref.argtypes = [ctypes.c_void_p, xtypes.ObjectRef]
                lib.node().xroad_trd_capt_move_pos_set_trd_capt_from_ref(self.__ptr, xtypes.ObjectRef(value))
            else:
                raise ValueError("wrong value {0}".format(value))
        else:
            lib.node().xroad_trd_capt_move_pos_reset_trd_capt_from.argtypes = [ctypes.c_void_p]
            lib.node().xroad_trd_capt_move_pos_reset_trd_capt_from(self.__ptr)



# vim:et:sts=4:sw=4