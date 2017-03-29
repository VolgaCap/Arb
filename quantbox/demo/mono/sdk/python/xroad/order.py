##
# @file order.py
# @author Dmitry S. Melnikov, dmitryme@gmail.com

import ctypes
from enum import IntEnum
from xroad.order_ctypes import *
from xroad.xtypes import Str, Errno, RejReason
import xroad.objects as xobj
import xroad.lib as lib


class State(IntEnum):
    initial = 0,
    active = 1,
    destroyed = 2,
    canceled = 3,
    rejected = 4,
    filled = 5,
    expired = 6,
    awaiting_active = 7,
    awaiting_destroy = 8,
    awaiting_cancel = 9,
    awaiting_replace = 10


class ReplaceMask(IntEnum):
    qty = 1
    price = 2


class OrderOption(IntEnum):
    max_cancel_attempts = 1
    cancel_timeout_ms = 2


class Order(object):

    def __init__(self, pool, name, cback, instr, acc, client_code, side, qty, price, ext_ref):
        err = Str()
        self.__order = lib.order().order_create(
            Str(name), cback, instr.ptr, Str(acc), Str(client_code),
            side, qty, price, Str(ext_ref), ctypes.py_object(pool), ctypes.pointer(err))
        if not self.__order:
            raise RuntimeError("unable to create order. reason = {0}".format(err))

    ##
    # set order option
    def set_option(self, opt, val):
        if opt == OrderOption.max_cancel_attempts:
            val_ = ctypes.c_uint32(val)
            lib.order().order_set_opt(self.__order, opt.value, ctypes.pointer(val_))
        elif opt == OrderOption.cancel_timeout_ms:
            val_ = ctypes.c_uint32(val)
            lib.order().order_set_opt(self.__order, opt.value, ctypes.pointer(val_))

    ##
    # convert order to string
    def __str__(self):
        return str(lib.order().order_print(self.__order))

    ##
    # checks if order is active
    @property
    def is_active(self):
        return (self.state == State.active or
                self.state == State.awaiting_active or
                self.state == State.awaiting_replace or
                self.state == State.awaiting_cancel or
                self.state == State.awaiting_destroy)

    ##
    # delete order
    # @param[in] order - order to delete
    def destroy(self, force=False):
        lib.order().order_destroy(self.__order, 1 if force else 0)

    ##
    # send order to exchange
    def send(self):
        res = lib.order().order_send(self.__order)
        if res != Errno.ok:
            raise RuntimeError("unable to send order")

    ##
    # cancel order on exchange
    def cancel(self):
        if self.is_active:
            res = lib.order().order_cancel(self.__order)
            if res != Errno.ok:
                raise RuntimeError("unable to send order {0}. error = {1}".format(self.state. Errno(res).name))

    ##
    # replace order
    # @param[in] qty - new order qty
    # @param[in] price - new order price
    # @param[in] ext_ref - order ext_ref
    def replace(self, qty=None, price=None, ext_ref=None):
        mask = 0
        if qty is not None:
            mask |= ReplaceMask.qty
        else:
            qty = 0
        if price is not None:
            mask |= ReplaceMask.price
        else:
            price = 0
        if ext_ref is not None:
            mask |= ReplaceMask.ext_ref
        if mask:
            res = lib.order().order_replace(self.__order, qty, price, Str(ext_ref), mask)
        if res != Errno.ok:
            raise RuntimeError("unable to replace order. error = {0}".format(Errno(res).name))

    ##
    # get order name
    @property
    def name(self):
        return str(lib.order().order_get_name(self.__order))

    ##
    # get order state
    @property
    def state(self):
        return State(lib.order().order_get_state(self.__order))

    ##
    # get order instrument
    @property
    def instr(self):
        return xobj.Instr(lib.order().xroad_order_get_instr(self.__order))

    ##
    # get order quantity
    @property
    def qty(self):
        return lib.order().order_get_qty(self.__order)

    ##
    # get order leaves quantity
    @property
    def leaves_qty(self):
        return lib.order().order_get_leaves_qty(self.__order)

    ##
    # get order price
    @property
    def price(self):
        return lib.order().order_get_price(self.__order)

    ##
    # get order total_qty
    @property
    def total_qty(self):
        return lib.order().order_get_total_qty(self.__order)

    ##
    # get order average price
    @property
    def avg_price(self):
        return lib.order().order_get_avg_price(self.__order)

    ##
    # get xroad_order
    @property
    def xorder(self):
        return xobj.Order(lib.order().order_get_xorder(self.__order))


class OrderPool(object):

    @staticmethod
    def get_order_from_ctx(obj):
        name = lib.order().order_get_name(obj)
        ctx = lib.order().order_get_ctx(obj)
        self = ctypes.cast(ctx, ctypes.py_object).value
        return (self.get_order(str(name)), self)

    @staticmethod
    def __on_activate(obj):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_order_activate(order)

    @staticmethod
    def __on_before_send(obj):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_before_send(order)

    @staticmethod
    def __on_trade(obj, qty, price):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_order_trade(order, qty, price)

    @staticmethod
    def __on_canceled(obj):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_order_canceled(order)

    @staticmethod
    def __on_unexpected_canceled(obj):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_order_unexpected_canceled(order)

    @staticmethod
    def __on_expired(obj):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_order_expired(order)

    @staticmethod
    def __on_destroyed(obj):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_order_destroyed(order)
        del self.__orders[order.name]

    @staticmethod
    def __on_replaced(obj):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_order_replaced(order)

    @staticmethod
    def __on_rejected(obj, err_code, err_txt):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_order_rejected(order, RejReason(err_code), str(err_txt))

    @staticmethod
    def __on_cancel_rejected(obj, err_code, err_txt):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_order_cancel_rejected(order, RejReason(err_code), str(err_txt))

    @staticmethod
    def __on_replace_rejected(obj, err_code, err_txt):
        order, self = OrderPool.get_order_from_ctx(obj)
        self.on_order_replace_rejected(order, RejReason(err_code), str(err_txt))

    ##
    # create order pool
    # @param[in] instrdb - instrdb instance
    def __init__(self, instrdb):
        self.__orders = dict()
        self.__instrdb = instrdb
        self.__on_activate_fun = on_activate(OrderPool.__on_activate)
        self.__on_before_send_fun = on_before_send(OrderPool.__on_before_send)
        self.__on_trade_fun = on_trade(OrderPool.__on_trade)
        self.__on_canceled_fun = on_canceled(OrderPool.__on_canceled)
        self.__on_unexpected_canceled_fun = on_unexpected_canceled(OrderPool.__on_unexpected_canceled)
        self.__on_expired_fun = on_expired(OrderPool.__on_expired)
        self.__on_destroyed_fun = on_destroyed(OrderPool.__on_destroyed)
        self.__on_replaced_fun = on_replaced(OrderPool.__on_replaced)
        self.__on_rejected_fun = on_rejected(OrderPool.__on_rejected)
        self.__on_cancel_rejected_fun = on_cancel_rejected(OrderPool.__on_cancel_rejected)
        self.__on_replace_rejected_fun = on_replace_rejected(OrderPool.__on_replace_rejected)
        self.__cback = OrderCallbackCTypes(
            self.__on_activate_fun,
            self.__on_before_send_fun,
            self.__on_trade_fun,
            self.__on_canceled_fun,
            self.__on_unexpected_canceled_fun,
            self.__on_expired_fun,
            self.__on_destroyed_fun,
            self.__on_replaced_fun,
            self.__on_rejected_fun,
            self.__on_cancel_rejected_fun,
            self.__on_replace_rejected_fun)

    ##
    # create new order
    # @param[in] name         - name of order. must be unique
    # @param[in] alias        - instrument alias
    # @param[in] acc          - account
    # @param[in] client_code  - client_code if any
    # @param[in] side         - order side. see xtypes.Side for details
    # @param[in] qty          - order quantity
    # @param[in] price        - order price
    # @param[in] ext_ref      - order external reference data
    # @return order instance
    def create_order(self, name, alias, acc, side, qty, price, client_code=None, ext_ref=None):
        instr = self.__instrdb.get_by_alias(alias)
        if not instr:
            raise RuntimeError("instrument not found by alias '{0}'".format(alias))
        order = Order(self, name, self.__cback, instr, acc, client_code, side, qty, price, ext_ref)
        self.__orders[name] = order
        return order

    ##
    # process node incoming objects
    # @param[in] obj - object to process
    # @param[in] node_id - id of source node
    def process_node_object(self, obj, node_id):
        lib.order().order_on_node_object(obj.ptr, node_id)

    ##
    # get order by name
    # @param[in] name - order name
    def get_order(self, name):
        if name not in self.__orders:
            return None
        else:
            return self.__orders[name]

    ##
    # send all orders
    def send(self):
        for k, o in self.__orders.items():
            o.send()

    ##
    # cancel all orders
    def cancel(self):
        for k, o in self.__orders.items():
            o.cancel()

    ##
    # destroy all orders
    def destroy(self, force=False):
        for k, o in list(self.__orders.items()):
            o.destroy(force)

    def on_before_send(self, order):
        pass

    def on_order_activate(self, order):
        pass

    def on_order_trade(self, order, qty, price):
        pass

    def on_order_canceled(self, order):
        pass

    def on_order_unexpected_canceled(self, order):
        pass

    def on_order_expired(self, order):
        pass

    def on_order_destroyed(self, order):
        pass

    def on_order_replaced(self, order):
        pass

    def on_order_rejected(self, order, err_core, err_txt):
        pass

    def on_order_cancel_rejected(self, order, err_code, err_txt):
        pass

    def on_order_replace_rejected(self, order, err_code, err_txt):
        pass

# vim:et:sts=4:sw=4
