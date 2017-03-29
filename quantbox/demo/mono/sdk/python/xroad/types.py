import ctypes
from enum import IntEnum


class Errno(IntEnum):
    ok = 0
    failed = -1
    not_found = -2
    invalid_arg = -3
    too_long = -4
    duplicate_val = -5
    not_connected = -6
    check_failed = -7
    wrong_format = -8
    already_exists = -9
    already_connected = -10
    no_more_resources = -11
    not_impl = -12
    already_done = -13
    wrong_state = -14
    busy = -15,
    unable_to_route = -16


class Str(ctypes.Structure):
    def __init__(self, s=None):
        if not s:
            super().__init__(0, ctypes.c_char_p(0))
        else:
            super().__init__(len(s), ctypes.c_char_p(s.encode()))

    _fields_ = [('len',  ctypes.c_uint),
                ('data', ctypes.c_char_p)]

    def __str__(self):
        if not self.data:
            return ""
        else:
            return self.data[:self.len].decode()

    ##
    # check if string is null
    @property
    def is_null(self):
        return self.len == 0 and self.data == 0


class ObjectRef(ctypes.Structure):
    def __init__(self, t):
        super().__init__(t[0].value, t[1])

    _fields_ = [('type',  ctypes.c_int),
                ('id', ctypes.c_ulong)]

    def __str__(self):
        return "({0},{1})".format(self.type, self.id)


class Path(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 1024)]

    def __str__(self):
        return self.data[:self.len].decode()


class NodeName(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 16)]

    def __str__(self):
        return self.data[:self.len].decode()


class GroupName(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 32)]

    def __str__(self):
        return self.data[:self.len].decode()


class ConfigName(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 16)]

    def __str__(self):
        return self.data[:self.len].decode()


class SystemName(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 32)]

    def __str__(self):
        return self.data[:self.len].decode()


class LinkName(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 64)]

    def __str__(self):
        return self.data[:self.len].decode()


class SenderCompId(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 32)]

    def __str__(self):
        return self.data[:self.len].decode()


class Sender(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 16)]

    def __str__(self):
        return self.data[:self.len].decode()


class ClordId(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 32)]

    def __str__(self):
        return self.data[:self.len].decode()


class ExtRef(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 32)]

    def __str__(self):
        return self.data[:self.len].decode()


class Account(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 16)]

    def __str__(self):
        return self.data[:self.len].decode()


class ClientCode(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 16)]

    def __str__(self):
        return self.data[:self.len].decode()


class Sales(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 16)]

    def __str__(self):
        return self.data[:self.len].decode()


class ExecId(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 32)]

    def __str__(self):
        return self.data[:self.len].decode()


class Text(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 128)]

    def __str__(self):
        return self.data[:self.len].decode()


class AlarmText(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 128)]

    def __str__(self):
        return self.data[:self.len].decode()


class FieldName(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 32)]

    def __str__(self):
        return self.data[:self.len].decode()


class FieldValue(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_ubyte * 128)]

    def __str__(self):
        return self.data[:self.len]


class ShortText(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 64)]

    def __str__(self):
        return self.data[:self.len].decode()


class Name(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 32)]

    def __str__(self):
        return self.data[:self.len].decode()


class Cls(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 20)]

    def __str__(self):
        return self.data[:self.len].decode()


class Alias(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 20)]

    def __str__(self):
        return self.data[:self.len].decode()


class Cfi(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 6)]

    def __str__(self):
        return self.data[:self.len].decode()


class Levels(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_ubyte * 480)]

    def __str__(self):
        return self.data[:self.len]


class UniqId(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 16)]

    def __str__(self):
        return self.data[:self.len].decode()


class Book(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 12)]

    def __str__(self):
        return self.data[:self.len].decode()


class Desk(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 16)]

    def __str__(self):
        return self.data[:self.len].decode()


class Isin(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 12)]

    def __str__(self):
        return self.data[:self.len].decode()


class BbSource(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 16)]

    def __str__(self):
        return self.data[:self.len].decode()


class BbCode(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 32)]

    def __str__(self):
        return self.data[:self.len].decode()


class BbFigi(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 12)]

    def __str__(self):
        return self.data[:self.len].decode()


class Uuid(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 36)]

    def __str__(self):
        return self.data[:self.len].decode()


class Side(IntEnum):
    empty = 48
    buy = 49
    sell = 50


##
# type of order
class OrdType(IntEnum):
    market = 49  # market orer
    limit = 50  # limit order
    stop_limit = 52  # stop-limit order


##
# order flags
class OrderFlags(IntEnum):
    from_mmaker = 1  # order from market maker


class Tif(IntEnum):
    day = 48
    gtc = 49
    ioc = 51
    fok = 52
    gtd = 54


class RejReason(IntEnum):
    other = 1
    too_late = 2
    unknown_instr = 3
    duplicate = 4
    exceed_limit = 5
    exch_closed = 6
    broker_opt = 7
    wrong_account = 8
    already_in_pending = 9
    unknown = 10
    internal_error = 11
    tran_limit = 12
    removed = 13
    guard = 14


class AlarmLevel(IntEnum):
    error = 1
    warning = 2


class OrderFixStatus(IntEnum):
    new = 48
    partially_filled = 49
    filled = 50
    canceled = 52
    pending_cancel = 54
    rejected = 56
    pending_new = 65
    expired = 67
    pending_replace = 69


class OrderStatus(IntEnum):
    initial = 73
    active = 65
    filled = 70
    canceled = 67
    rejected = 82
    expired = 69
    removed = 84
    awaiting_active = 97
    awaiting_cancel = 99
    awaiting_replace = 114


class ExecType(IntEnum):
    new = 48
    canceled = 52
    replace = 53
    pending_cancel = 54
    rejected = 56
    expired = 67
    pending_replace = 69
    trade = 70


class FixSessionStatus(IntEnum):
    up = 85
    down = 68


class RejResponseTo(IntEnum):
    cancel = 49
    replace = 50


class FieldType(IntEnum):
    string = 1
    integer = 2
    double = 3


class OptMmState(IntEnum):
    disabled = 0
    pending = 1
    active = 2
    error = 3
    filled = 4


class ResetHint(IntEnum):
    statistic = 1
    fix_session = 2
    state = 4


class Exchange(IntEnum):
    unknown = 0
    moex = 1
    xroad = 2
    lse = 3
    cme = 4
    nyse = 5
    nasdaq = 6
    nymex = 7
    ice = 8
    eurex = 9
    cboe = 10


class Currency(IntEnum):
    rub = 1
    usd = 2
    eur = 3
    gbp = 4
    gbx = 5
    chf = 6
    jpy = 7
    cad = 8
    hkd = 9
    nok = 10
    pln = 11
    uah = 12
    xxx = 13


class Callput(IntEnum):
    call = 1
    put = 2


class CalcMid(IntEnum):
    by_shift = 1
    by_shift_vol = 2


class MlegReportType(IntEnum):
    single = 49
    leg = 50
    mleg_sec = 51


class SubsResult(IntEnum):
    subscribed = 0
    unsubscribed = 1
    already_subscribed = 2
    instr_not_found = 3
    too_many_subscriptions = 4
    internal_error = 5
    external_error = 6


class NodeState(IntEnum):
    active = 1
    offline = 2
    dead = 3
    inactive = 4
    pending_active = 5
    pending_offline = 6


class MdataSubsState(IntEnum):
    unsubscribed = 1
    subscribed = 2
    awaiting_subs = 3
    awaiting_unsubs = 4


# vim:et:sts=4:sw=4