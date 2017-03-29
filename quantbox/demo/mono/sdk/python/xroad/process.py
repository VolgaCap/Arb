##
# @file process.py

import sys
import signal
import logging
from xroad.node import Node
import xroad.objects as objects
import xroad.registry as registry


##
# class represents process in xroad. User Process classes should be derived from xroad.Process
class Process(Node):

    ##
    # @ctor
    # @param[in] name - name of the process
    def __init__(self, name, out_of_system=False):
        Node.__init__(self, name, out_of_system)
        self.__state = True
        self.catch_signal(signal.SIGTERM)
        self.catch_signal(signal.SIGINT)
        self.catch_signal(signal.SIGHUP)
        if name and not out_of_system:
            obj = self.create_object(objects.ObjectType.start)
            try:
                obj.send(self.data.id)
            except Exception as ex:
                logging.error(str(ex))

    ##
    # called on signal
    # @param[in] signal - catched signal
    def on_node_signal(self, sig):
        if sig in [signal.SIGTERM, signal.SIGINT]:
            self.__state = False
            self.shutdown()
        elif sig == signal.SIGHUP:
            Node.reconfigure(self)
            self.reconfig()

    ##
    # called when new object arrived
    # @param[in] obj - xroad object
    # @param[in] node_id - id of sender node
    def on_node_object(self, obj, node_id):
        logging.info("received object {0} from {1}".format(obj, node_id))
        if obj.object_type == objects.ObjectType.start:
            if self.data.status != registry.NodeStatus.active:
                self.start()
        elif obj.object_type == objects.ObjectType.stop:
            if self.data.status != registry.NodeStatus.offline:
                self.stop()
        elif obj.object_type == objects.ObjectType.activate:
            if self.data.status != registry.NodeStatus.active:
                self.activate()
        elif obj.object_type == objects.ObjectType.deactivate:
            if self.data.status == registry.NodeStatus.active:
                self.deactivate()
        elif obj.object_type == objects.ObjectType.reset:
            self.data.statistic.reset()
            self.reset(obj.hint)
        elif obj.object_type == objects.ObjectType.reconfig:
            Node.reconfigure(self)
            self.reconfig()
        else:
            self.on_object(obj, node_id)

    ##
    # main loop
    def do(self):
        while self.__state:
            try:
                self.receive()
            except RuntimeError:
                logging.error("Unexpected error:{0}".format(sys.exc_info()))

    ##
    # called when applcation should start
    # should be overrided in child object
    def start(self):
        pass

    ##
    # called when applcation should stop
    # should be overrided in child object
    def stop(self):
        pass

    ##
    # called when applcation should go to shutdown
    # should be overrided in child object
    def shutdown(self):
        pass

    ##
    # called when applcation should be activated
    # should be overrided in child object
    def activate(self):
        pass

    ##
    # called when applcation should be deactivated
    # should be overrided in child object
    def deactivate(self):
        pass

    ##
    # called when reset signal received
    # should be overrided in child object
    def reset(self, hint):
        pass

    ##
    # called when applcation should be reconfigured
    # should be overrided in child object
    def reconfig(self):
        pass

    ##
    # call when new object arrived and should be processed by child class
    # should be overrided in child object
    # @param[in] obj - xroad object
    # @param[in] node_id - id of sender node
    def on_object(self, obj, node_id):
        pass

# vim:et:sts=4:sw=4
