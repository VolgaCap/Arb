##
# @file node.py
# @author Dmitry S. Melnikov, dmitryme@gmail.com
import ctypes
from enum import IntEnum
import xroad.registry as registry
import xroad.objects as objects
import xroad.xtypes as xtypes
import xroad.config as config
import xroad.lib as lib


##
# node status
class NodeStatus(IntEnum):
    active = 1
    offline = 2
    DEAD = 3
    inactive = 4


##
# @class represents cursor which is used to iterate over objects in cache
class NodeCursor(object):

    def __init__(self, obj_type, offset=0):
        self.__ptr = lib.node().xroad_node_create_cursor(obj_type.value)
        if self.__ptr is None:
            raise RuntimeError("unable to create cursor of type '{0}'".format(obj_type.name))
        self.__offset = offset

    def __del__(self):
        if self.__ptr is not None:
            lib.node().xroad_node_destroy_cursor(self.__ptr)
            self.__ptr = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.__del__()

    ##
    # return objects from cache
    # @return object  from cache
    @property
    def objects(self):
        obj = lib.node().xroad_node_cursor_get_first(self.__ptr)
        if self.__offset:
            obj = lib.node().xroad_node_cursor_offset(self.__ptr, self.__offset)
        while obj:
            yield objects.ptr_to_object(obj, False)
            obj = lib.node().xroad_node_cursor_get_next(self.__ptr)

    ##
    # return objects from cache
    # @return object  from cache
    @property
    def objects_with_last_flag(self):
        obj = lib.node().xroad_node_cursor_get_first(self.__ptr)
        if self.__offset:
            obj = lib.node().xroad_node_cursor_offset(self.__ptr, self.__offset)
        while obj:
            tmp = obj
            obj = lib.node().xroad_node_cursor_get_next(self.__ptr)
            yield objects.ptr_to_object(tmp, False), obj is None

    ##
    # return objects from cache in reverse order
    # @return object from cache
    @property
    def robjects(self):
        obj = lib.node().xroad_node_cursor_get_last(self.__ptr)
        if self.__offset:
            obj = lib.node().xroad_node_cursor_offset(-self.__offset)
        while obj:
            yield objects.ptr_to_object(obj, False)
            obj = lib.node().xroad_node_cursor_get_prev(self.__ptr)

on_object_handler = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_void_p)


##
# class represents xroad node. User node classes should be derived from xroad.Node
class Node(object):

    @staticmethod
    def __on_object(obj, node_id, ctx):
        self = ctypes.cast(ctx, ctypes.py_object).value
        self.data.statistic.msg_in_cnt += 1
        self.on_node_object(objects.ptr_to_object(obj), node_id)

    @staticmethod
    def __on_signal(signal_ptr, signal, ctx):
        self = ctypes.cast(ctx, ctypes.py_object).value
        self.on_node_signal(signal)

    class NodeCallbackCTypes(ctypes.Structure):
        _fields_ = [("ctx", ctypes.py_object),
                    ("on_object", on_object_handler)]

    class NodeEpollCallbackCTypes(ctypes.Structure):
        _fields_ = [("ctx", ctypes.py_object),
                    ("fd", ctypes.c_uint32),
                    ("on_event", lib.on_epoll_event_handler)]

    def __init__(self, name, out_of_system=False):
        self.__reg = registry.Registry(out_of_system)
        self.__on_object_fun = on_object_handler(Node.__on_object)
        self.__on_signal_fun = lib.on_signal_handler(Node.__on_signal)
        cback = Node.NodeCallbackCTypes(ctypes.py_object(self), self.__on_object_fun)

        if xtypes.Errno.ok != lib.node().xroad_node_create(xtypes.Str(name), cback):
            raise RuntimeError("node already started")

        self.__ndata = lib.node().xroad_node_get_data()
        self.__timeout = self.config.get_child("node").get_attr_i("wait_timeout_ms")
        cback = lib.SignalCallbackCTypes(ctypes.py_object(self), self.__on_signal_fun)
        self.__signal = lib.common().xroad_signal_create(cback)

    def __del__(self):
        if self.__ndata:
            self.data.status = NodeStatus.DEAD
            lib.common().xroad_signal_destroy(self.__signal)
            lib.node().xroad_node_destroy()
            self.__ndata = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.__del__()

    ##
    # get version
    @staticmethod
    def version():
        ver = lib.node().xroad_node_get_version()
        return ctypes.cast(ver, ctypes.POINTER(registry.NodeVersionCTypes)).contents

    ##
    # catch signal if any
    # @param[in] signal - signal to catch
    def catch_signal(self, signal):
        return lib.common().xroad_signal_catch(self.__signal, signal)

    ##
    # free signal if any
    # @param[in] signal - signal to catch
    def free_signal(self, signal):
        return lib.common().xroad_signal_free(self.__signal, signal)

    ##
    # receive and dispatch message from link
    # @param[in] timeout - wait usecs for received message
    def receive(self):
        lib.node().xroad_node_receive(self.__timeout)

    ##
    # get registry
    # @return registry
    @property
    def registry(self):
        return self.__reg

    ##
    # get node registry slot
    # @return @see NodeData
    @property
    def data(self):
        return registry.NodeData(self.__ndata)

    ##
    # reconfigure node
    def reconfigure(self):
        lib.node().xroad_node_reconfig()
        self.__timeout = self.config.get_child("node").get_attr_i("wait_timeout_ms")

    ##
    # get node Config
    # @return @see Config
    @property
    def config(self):
        return config.Config(lib.common().xroad_xml_get_root(lib.node().xroad_node_get_cfg()))

    ##
    # get variable from environment
    # @return variable value
    def get_variable(self, name):
        cfg = lib.node().xroad_node_get_cfg()
        val = lib.common().xroad_xml_get_variable(cfg, xtypes.Str(name))
        return str(val)

    ##
    # get node home directory
    @property
    def home_dir(self):
        home = lib.node().xroad_node_get_home_dir()
        return home.contents.data[:home.contents.len].decode()

    ##
    # create new object
    # @param[in] type - type of object to create
    def create_object(self, obj_type):
        return objects.create_object(obj_type)

    ##
    # return object from cache
    # @param[in] type    - type of object
    # @param[in] obj_id - id of object
    def get_object(self, obj_type, obj_id):
        obj = lib.node().xroad_node_get_object(obj_type, obj_id)
        if obj:
            return objects.ptr_to_object(obj, False)

    ##
    # create new cache cursor
    # @param[in] type - type of cursor
    # @return @see NodeCursor
    def create_cursor(self, obj_type, offset=0):
        return NodeCursor(obj_type, offset)

    ##
    # shrink cache table
    def shrink_cache(self, obj_type, obj_count):
        lib.node().xroad_node_shrink_cache(obj_type, obj_count)

    # return count of objects of desired type in cache
    def get_object_count(self, obj_type):
        return lib.node().xroad_node_get_object_count(obj_type)

    ##
    # return epoll file descriptor
    @property
    def epoll_fd(self):
        return lib.node().xroad_node_get_epoll_fd()

    ##
    # call when new object arrived
    # should be overrided in child object
    # @param[in] obj - xroad object
    # @param[in] node_id - id of sender node
    def on_node_object(self, obj, node_id):
        pass

    ##
    # call on signal
    # should be overrided in child object
    # @param[in] signal - catched signal
    def on_node_signal(self, signal):
        pass


# vim:et:sts=4:sw=4
