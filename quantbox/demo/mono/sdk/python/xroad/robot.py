from xroad.process import Process
from xroad.node import NodeStatus
from xroad.order import OrderPool
from xroad.mdata import MarketData
from xroad.instrdb import InstrDB
from xroad.ui import Ui, FieldWrapper
import xroad.objects as objects
import traceback
import logging


class Robot(Process, InstrDB, MarketData, OrderPool, Ui):

    def __init__(self, name):
        self.__working = True
        self.__timeout = -1
        Process.__init__(self, name)
        config = self.config
        InstrDB.__init__(self)
        Ui.__init__(self, config.get_child("ui"))
        MarketData.__init__(self, config.get_child("mdata_engine"), self)
        OrderPool.__init__(self, self)

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace):
        self.data.status = NodeStatus.DEAD
        if trace:
            val = traceback.format_tb(trace)
            logging.error(''.join(val))
        return True

    def on_object(self, obj, node_id):
        if obj.object_type == objects.ObjectType.field:
            self.on_node_field(FieldWrapper(obj), node_id)
        else:
            OrderPool.process_node_object(self, obj, node_id)

    def run(self):
        MarketData.start(self)
        self.data.status = NodeStatus.inactive
        self.do()
        MarketData.stop(self)

    def on_field(self, fld, node_id):
        pass

# vim:et:sts=4:sw=4
