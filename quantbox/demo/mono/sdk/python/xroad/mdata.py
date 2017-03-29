##
# @file mdata.py
# @author Danil Krivopustov, krivopustovda@gmail.com

import ctypes
from enum import IntEnum

import xroad.xtypes as xtypes
from xroad import mdata_ctypes
from xroad import lib
import logging


##
# describes side of updated quote
class SideType(IntEnum):
    Ask = 1,
    Bid = 2


class ProtoType(IntEnum):
    heartbeat = 0,
    resolve = 1,
    subscribe = 2,
    symbol = 3,
    book = 4,
    trade = 5,
    subscribeRes = 6,
    feedState = 7,
    quote = 8,
    common_info = 9


class StateType(IntEnum):
    ok = 0
    connectionFailed = 1
    unavailable = 2


##
# describes type of data which interests client
class SubscriptionType(IntEnum):
    book = 1,
    trade = 2,
    quote = 4,
    common = 8,
    snapshot = 16,  # receive snapshot
    updates = 32   # receive regular updates


##
# describes type of data which was updated in CommonInfo
class CommonInfoType(IntEnum):
    OI = 1,
    Min = 2,
    Max = 4,
    Open = 8,
    High = 16,
    Low = 32,
    Last = 64,
    Volume = 128


##
# Book level class
class BookLevel(object):

    def __init__(self, level=None):
        if level is None:
            self.__level = ctypes.pointer(mdata_ctypes.BookLevelCTypes())
        else:
            self.__level = level

    ##
    # gets qty of level
    @property
    def qty(self):
        return self.__level.contents.qty

    ##
    # sets qty of level
    @qty.setter
    def qty(self, value):
        self.__level.contents.qty = value

    ##
    # get price of level
    @property
    def price(self):
        return self.__level.contents.price

    ##
    # sets price of level
    @price.setter
    def price(self, value):
        self.__level.contents.price = value


##
# Book class
class Book(object):

    def __init__(self, instr, book=None):
        self.__instr = instr
        if book is None:
            self.__book = ctypes.pointer(mdata_ctypes.Book_20CTypes())
            self.__book.contents.instr_id = instr.id
        else:
            self.__book = book

    ##
    # gets exchange ts
    @property
    def exch_ts(self):
        return self.__book.contents.exch_ts

    ##
    # sets exchange ts
    @exch_ts.setter
    def exch_ts(self, value):
        self.__book.contents.exch_ts = value

    ##
    # gets local ts
    @property
    def ts(self):
        return self.__book.contents.ts

    ##
    # sets local ts
    @ts.setter
    def ts(self, value):
        self.__book.contents.ts = value

    ##
    # gets instrument
    @property
    def instr(self):
        return self.__instr

    ##
    # gets bids level by index
    # @param[in] index - index of level
    def get_bid(self, index):
        if 0 <= index < 20:
            return BookLevel(ctypes.pointer(self.__book.contents.bids[index]))
        raise IndexError('bid index {0} out of bounds'.format(index))

    ##
    # sets bids level by index
    # @param[in] index - index of level
    def set_bid(self, index, price, qty):
        if 0 <= index < 20:
            self.__book.contents.bids[index].price = price
            self.__book.contents.bids[index].qty = qty
        else:
            raise IndexError('bid index {0} out of bounds'.format(index))

    ##
    # gets asks level by index
    # @param[in] index - index of level
    def get_ask(self, index):
        if 0 <= index < 20:
            return BookLevel(ctypes.pointer(self.__book.contents.asks[index]))
        raise IndexError('ask index {0} out of bounds'.format(index))

    ##
    # sets asks level by index
    # @param[in] index - index of level
    def set_ask(self, index, price, qty):
        if 0 <= index < 20:
            self.__book.contents.asks[index].price = price
            self.__book.contents.asks[index].qty = qty
        else:
            raise IndexError('ask index {0} out of bounds'.format(index))

    ##
    # sends data to consumers
    def send(self, mdata):
        mdata.send(ProtoType.book, self.__book)


##
# CommonInfo class
class CommonInfo(object):

    def __init__(self, instr, info=None):
        self.__instr = instr
        if info is None:
            self.__info = ctypes.pointer(mdata_ctypes.CommonInfoCTypes())
            self.__info.contents.instr_id = instr.id
        else:
            self.__info = info

    ##
    # gets local ts
    @property
    def ts(self):
        return self.__info.contents.ts

    ##
    # sets local ts
    @ts.setter
    def ts(self, value):
        self.__info.contents.ts = value

    ##
    # gets exch ts
    @property
    def exch_ts(self):
        return self.__info.contents.exch_ts

    ##
    # sets exch ts
    @exch_ts.setter
    def exch_ts(self, value):
        self.__info.contents.exch_ts = value

    ##
    # gets instrument
    @property
    def instr(self):
        return self.__instr

    ##
    # gets flags
    @property
    def flag(self):
        return self.__info.contents.flag

    ##
    # sets flags
    @flag.setter
    def flag(self, value):
        self.__info.contents.flag = value

    ##
    # gets open interest
    @property
    def oi(self):
        return self.__info.contents.oi

    ##
    # sets open interest
    @oi.setter
    def oi(self, value):
        self.__info.contents.oi = value

    ##
    # gets open
    @property
    def open(self):
        return self.__info.contents.open

    ##
    # sets open
    @open.setter
    def open(self, value):
        self.__info.contents.open = value

    ##
    # gets last
    @property
    def last(self):
        return self.__info.contents.last

    ##
    # sets last
    @last.setter
    def last(self, value):
        self.__info.contents.last = value

    ##
    # gets high
    @property
    def high(self):
        return self.__info.contents.high

    ##
    # sets high
    @high.setter
    def high(self, value):
        self.__info.contents.high = value

    ##
    # gets low
    @property
    def low(self):
        return self.__info.contents.low

    ##
    # sets low
    @low.setter
    def low(self, value):
        self.__info.contents.low = value

    ##
    # gets close
    @property
    def close(self):
        return self.__info.contents.close

    ##
    # sets close
    @close.setter
    def close(self, value):
        self.__info.contents.close = value

    ##
    # gets volume
    @property
    def volume(self):
        return self.__info.contents.volume

    ##
    # sets volume
    @volume.setter
    def volume(self, value):
        self.__info.contents.volume = value

    ##
    # gets min
    @property
    def min(self):
        return self.__info.contents.min

    ##
    # sets min
    @min.setter
    def min(self, value):
        self.__info.contents.min = value

    ##
    # gets max
    @property
    def max(self):
        return self.__info.contents.max

    ##
    # sets max
    @max.setter
    def max(self, value):
        self.__info.contents.max = value

    ##
    # sends data to consumers
    def send(self, mdata):
        mdata.send(ProtoType.common_info, self.__info)


##
# Trade class
class Trade(object):

    def __init__(self, instr, trade=None):
        self.__instr = instr
        if trade is None:
            self.__trade = ctypes.pointer(mdata_ctypes.TradeCTypes())
            self.__trade.contents.instr_id = instr.id
        else:
            self.__trade = trade

    ##
    # gets exchange ts
    @property
    def exch_ts(self):
        return self.__trade.contents.exch_ts

    ##
    # sets exchange ts
    @exch_ts.setter
    def exch_ts(self, value):
        self.__trade.contents.exch_ts = value

    ##
    # gets local ts
    @property
    def ts(self):
        return self.__trade.contents.ts

    ##
    # sets local ts
    @ts.setter
    def ts(self, value):
        self.__trade.contents.ts = value

    ##
    # gets instrument
    @property
    def instr(self):
        return self.__instr

    ##
    # gets quantity
    @property
    def qty(self):
        return self.__trade.contents.qty

    ##
    # sets quantity
    @qty.setter
    def qty(self, value):
        self.__trade.contents.qty = value

    ##
    # gets price
    @property
    def price(self):
        return self.__trade.contents.price

    ##
    # sets price
    @price.setter
    def price(self, value):
        self.__trade.contents.price = value

    ##
    # gets side of trade
    @property
    def side(self):
        return xtypes.Side(self.__trade.contents.side)

    ##
    # sets side of trade
    @side.setter
    def side(self, value):
        self.__trade.contents.side = int(value)

    ##
    # sends data to consumers
    def send(self, mdata):
        mdata.send(ProtoType.trade, self.__trade)


##
# Quote class
class Quote(object):

    def __init__(self, instr, quote=None):
        self.__instr = instr
        if quote is None:
            self.__quote = ctypes.pointer(mdata_ctypes.QuoteCTypes())
            self.__quote.contents.instr_id = instr.id
        else:
            self.__quote = quote

    ##
    # gets exchange ts
    @property
    def exch_ts(self):
        return self.__quote.contents.exch_ts

    ##
    # sets exchange ts
    @exch_ts.setter
    def exch_ts(self, value):
        self.__quote.contents.exch_ts = value

    ##
    # gets local ts
    @property
    def ts(self):
        return self.__quote.contents.ts

    ##
    # sets local ts
    @ts.setter
    def ts(self, value):
        self.__quote.contents.ts = value

    ##
    # gets instrument
    @property
    def instr(self):
        return self.__instr

    ##
    # gets best bid level
    @property
    def bid(self):
        return BookLevel(ctypes.pointer(self.__quote.contents.bid))

    ##
    # sets best bid level
    @bid.setter
    def bid(self, value):
        self.__quote.contents.bid.price = value.price
        self.__quote.contents.bid.qty = value.qty

    ##
    # gets best ask level
    @property
    def ask(self):
        return BookLevel(ctypes.pointer(self.__quote.contents.ask))

    ##
    # sets best ask level
    @ask.setter
    def ask(self, value):
        self.__quote.contents.ask.price = value.price
        self.__quote.contents.ask.qty = value.qty

    ##
    # gets flag side
    @property
    def flag(self):
        return self.__quote.contents.flag

    ##
    # sets flag side
    @flag.setter
    def flag(self, value):
        self.__quote.contents.flag = value

    ##
    # sends data to consumers
    def send(self, mdata):
        mdata.send(ProtoType.quote, self.__quote)


##
# Market data engine wrapper
class MarketData(object):

    @staticmethod
    def __on_symbol(symbol, ctx):
        pass

    @staticmethod
    def __on_mdata(md_type, mdata, ctx):
        self = ctypes.cast(ctx, ctypes.py_object).value
        if md_type == ProtoType.heartbeat:
            self.on_mdata_heartbeat()
        elif md_type == ProtoType.book:
            book = ctypes.cast(mdata, ctypes.POINTER(mdata_ctypes.Book_20CTypes))
            instr = self.__instrdb.get_by_id(book.contents.instr_id)
            self.on_mdata_book(Book(instr, book))
        elif md_type == ProtoType.trade:
            trade = ctypes.cast(mdata, ctypes.POINTER(mdata_ctypes.TradeCTypes))
            instr = self.__instrdb.get_by_id(trade.contents.instr_id)
            self.on_mdata_trade(Trade(instr, trade))
        elif md_type == ProtoType.quote:
            quote = ctypes.cast(mdata, ctypes.POINTER(mdata_ctypes.QuoteCTypes))
            instr = self.__instrdb.get_by_id(quote.contents.instr_id)
            self.on_mdata_quote(Quote(instr, quote))
        elif md_type == ProtoType.common_info:
            info = ctypes.cast(mdata, ctypes.POINTER(mdata_ctypes.CommonInfoCTypes))
            instr = self.__instrdb.get_by_id(info.contents.instr_id)
            self.on_mdata_common_info(CommonInfo(instr, info))

    @staticmethod
    def __on_resolve(subs, ctx):
        pass

    @staticmethod
    def __on_subscribe(subs, ctx):
        self = ctypes.cast(ctx, ctypes.py_object).value
        if subs.contents.instr_id != 0:
            instr = self.__instrdb.get_by_id(result.contents.instr_id)
            self.on_mdata_subscribe(instr, result.contents.mask)
        else:
            self.on_mdata_subscribe(None, result.contents.mask)

    @staticmethod
    def __on_subscribe_result(result, ctx):
        self = ctypes.cast(ctx, ctypes.py_object).value
        if result.contents.instr_id != 0:
            instr = self.__instrdb.get_by_id(result.contents.instr_id)
            self.on_mdata_subscribe_result(instr, result.contents.mask, result.contents.error_num)
        else:
            self.on_mdata_subscribe_result(None, result.contents.mask, result.contents.error_num)

    @staticmethod
    def __on_feed_state(state, ctx):
        # self = ctypes.cast(ctx, ctypes.py_object).value
        pass

    @staticmethod
    def __on_connected(ctx):
        self = ctypes.cast(ctx, ctypes.py_object).value
        self.on_mdata_connected()

    @staticmethod
    def __on_disconnected(ctx):
        self = ctypes.cast(ctx, ctypes.py_object).value
        self.on_mdata_disconnected()

    __on_symbol_fun = None
    __on_mdata_fun = None
    __on_resolve_fun = None
    __on_subscribe_fun = None
    __on_subscribe_result_fun = None
    __on_feed_state_fun = None
    __on_connected_fun = None
    __on_disconnected_fun = None

    __instrdb = None
    __data = None

    def __init__(self, config, instrdb):
        self.__instrdb = instrdb
        self.__on_symbol_fun = mdata_ctypes.on_mdata_symbol_type(self.__on_symbol)
        self.__on_mdata_fun = mdata_ctypes.on_mdata_mdata_type(self.__on_mdata)
        self.__on_resolve_fun = mdata_ctypes.on_mdata_resolve_type(self.__on_resolve)
        self.__on_subscribe_fun = mdata_ctypes.on_mdata_subscribe_type(self.__on_subscribe)
        self.__on_subscribe_result_fun = mdata_ctypes.on_mdata_subscribe_result_type(self.__on_subscribe_result)
        self.__on_feed_state_fun = mdata_ctypes.on_mdata_feed_state_type(self.__on_feed_state)
        self.__on_connected_fun = mdata_ctypes.on_mdata_connected_type(self.__on_connected)
        self.__on_disconnected_fun = mdata_ctypes.on_mdata_disconnected_type(self.__on_disconnected)
        srv_cb = mdata_ctypes.ServerCallbackCTypes(
            ctypes.py_object(self), self.__on_resolve_fun, self.__on_subscribe_fun,
            self.__on_connected_fun, self.__on_disconnected_fun)
        client_cb = mdata_ctypes.ClientCallbackCTypes(
            ctypes.py_object(self), self.__on_symbol_fun, self.__on_subscribe_result_fun,
            self.__on_feed_state_fun, self.__on_connected_fun, self.__on_disconnected_fun)
        self.__engine = lib.mdata_engine().mdata_engine_create(config.ptr, srv_cb, client_cb)

    def __del__(self):
        if self.__engine:
            lib.mdata_engine().mdata_engine_destroy(self.__engine)

    ##
    # initializes connect to source of market data
    def start(self):
        if not lib.mdata_engine().mdata_engine_start(self.__engine) == 0:
            raise RuntimeError("unable to start market data channel")

    ##
    # stops processing of market data
    def stop(self):
        lib.mdata_engine().mdata_engine_stop(self.__engine)

    ##
    # subscribes to the market data of specific instrument
    # @param [in] alias - alias of instr
    # @param [in] mask - subscription mask @see SubscriptionType
    def subscribe(self, alias, mask):
        cback = mdata_ctypes.ChannelCallbackCTypes(ctypes.py_object(self), self.__on_mdata_fun)
        if alias is not None:
            instr = self.__instrdb.get_by_alias(alias)
            if not instr:
                raise RuntimeError("instrument not found by alias {0}".format(alias))
        else:
            instr = None

        res = lib.mdata_engine().mdata_engine_subscribe(
            self.__engine, None if instr is None else instr.ptr, mask, cback)

        if not res == 0:
            raise RuntimeError("mdata_channel is unable to subscribe "
                               "to instrument with alias {0}. error = {1}".format(alias, res))

    def send(self, mdtype, data):
        """
        sends data to stream
        :param mdtype - type of mdata @see class ProtoType
        :param data -

        """
        if self.__engine:
            lib.mdata_engine().mdata_engine_send(self.__engine, mdtype, data)

    def on_mdata_resolve(self, alias):
        """
        Callback on resolve instr
        :param alias:
        :return:
        """

    def on_mdata_subscribe(self, instr, mask):
        """
        Callback on subscribe instr
        :param instr:
        :param mask:
        :return:
        """

    def on_mdata_subscribe_result(self, instr, mask, error_num):
        """
        Callback on subscribe instr
        :param instr:
        :param mask:
        :param error_num:
        :return:
        """

    def on_mdata_book(self, quote):
        """
        :param quote:
        :return:
        """

    def on_mdata_trade(self, trade):
        """

        :param trade:
        :return:
        """

    def on_mdata_quote(self, book):
        """

        :param book:
        :return:
        """

    def on_mdata_common_info(self, info):
        """

        :param info:
        :return:
        """

    def on_mdata_heartbeat(self):
        """

        :return:
        """
        logging.info("hbt")

    def on_mdata_connected(self):
        """

        :return:
        """

    def on_mdata_disconnected(self):
        """

        :return:
        """
