##
# @file registry.py
# @author Dmitry S. Melnikov, dmitryme@gmail.com

import ctypes
from enum import IntEnum
import xroad.xtypes as xtypes
import xroad.lib as lib
from datetime import datetime

XROAD_REGISTRY_NODE_COUNT_MAX = 1024


##
# Node status
class NodeStatus(IntEnum):
    active = 1
    offline = 2
    DEAD = 3
    inactive = 4


##
# Node flags
class NodeFlags(IntEnum):
    stand_alone = 0x1
    hidden = 0x2


class GitHash(ctypes.Structure):
    _fields_ = [('len', ctypes.c_uint),
                ('data', ctypes.c_char * 7)]

    def __str__(self):
        return self.data[:self.len].decode()


##
# class represents th node statistics
class NodeStatistic(object):

    class NodeStatisticCtypes(ctypes.Structure):
        _fields_ = [('error_cnt', ctypes.c_uint),
                    ('warn_cnt', ctypes.c_uint),
                    ('msg_in_cnt', ctypes.c_ulong),
                    ('msg_out_cnt', ctypes.c_ulong),
                    ('start_ts',  ctypes.c_ulong),
                    ('curr_ts',  ctypes.c_ulong)]

    def __init__(self, data):
        self.data = ctypes.cast(data, ctypes.POINTER(NodeStatistic.NodeStatisticCtypes))

    ##
    # reset statistics information
    def reset(self):
        lib.node().xroad_node_reset_statistic()

    ##
    # get errors total number
    @property
    def error_cnt(self):
        return self.data.contents.error_cnt

    ##
    # set errors counter
    @error_cnt.setter
    def error_cnt(self, cnt):
        self.data.contents.error_cnt = cnt

    ##
    # get warnings total number
    @property
    def warn_cnt(self):
        return self.data.contents.warn_cnt

    ##
    # set warnings counter
    @warn_cnt.setter
    def warn_cnt(self, cnt):
        self.data.contents.warn_cnt = cnt

    ##
    # get number of incoming messages
    @property
    def msg_in_cnt(self):
        return self.data.contents.msg_in_cnt

    ##
    # set number of incoming messages
    @msg_in_cnt.setter
    def msg_in_cnt(self, val):
        self.data.contents.msg_in_cnt = val

    ##
    # get counter of outgoing messages
    @property
    def msg_out_cnt(self):
        return self.data.contents.msg_out_cnt

    ##
    # increment counter of outgoing messages
    @msg_out_cnt.setter
    def msg_out_cnt(self, val):
        self.data.contents.msg_out_cnt = val

    ##
    # get start datetime
    @property
    def start_dt(self):
        return datetime.fromtimestamp(self.data.contents.start_ts)

    ##
    # get current datetime
    @property
    def curr_dt(self):
        return datetime.fromtimestamp(self.data.contents.curr_ts)


##
# node version
class NodeVersionCTypes(ctypes.Structure):
    _fields_ = [('major_ver', ctypes.c_ushort),
                ('minor_ver', ctypes.c_ushort),
                ('git_hash', GitHash),
                ('is_debug', ctypes.c_ubyte),
                ('git_uncommited', ctypes.c_ubyte)]


class NodeNotFound(RuntimeError):
    def __init__(self, txt):
        RuntimeError.__init__(self, txt)


##
# class contains data information of node
class NodeData(object):

    class NodeDataCtypes(ctypes.Structure):
        _fields_ = [('id', ctypes.c_short),
                    ('name', xtypes.NodeName),
                    ('group', xtypes.GroupName),
                    ('pid', ctypes.c_int),
                    ('statistic', NodeStatistic.NodeStatisticCtypes),
                    ('status', ctypes.c_int),
                    ('flags', ctypes.c_uint),
                    ('link', xtypes.LinkName),
                    ('version', NodeVersionCTypes),
                    ('config', xtypes.ConfigName)]

    def __init__(self, data):
        self.data = ctypes.cast(data, ctypes.POINTER(NodeData.NodeDataCtypes))
        if not self.id:
            raise NodeNotFound("node not found")

    def __str__(self):
        return self.name

    ##
    # get node unique id
    @property
    def id(self):
        return self.data.contents.id

    ##
    # get pid of node process
    @property
    def pid(self):
        return self.data.contents.pid

    ##
    # get node name
    @property
    def name(self):
        return self.data.contents.name.data[:self.data.contents.name.len].decode()

    ##
    # get node group
    @property
    def group(self):
        return self.data.contents.group.data[:self.data.contents.group.len].decode()

    ##
    # get statistics
    # @return @see NodeStatistic
    @property
    def statistic(self):
        return NodeStatistic(ctypes.pointer(self.data.contents.statistic))

    ##
    # get node status
    # @return @see NodeStatus
    @property
    def status(self):
        return NodeStatus(self.data.contents.status)

    ##
    # set node status
    # @param[in] status - @see NodeStatus
    @status.setter
    def status(self, node_status):
        self.data.contents.status = node_status

    ##
    # get node flags
    # @return see NodeFlags
    @property
    def flags(self):
        flags = []
        if self.data.contents.flags & NodeFlags.stand_alone:
            flags.append(NodeFlags.stand_alone)
        if self.data.contents.flags & NodeFlags.stand_alone:
            flags.append(NodeFlags.hidden)
        return flags

    ##
    # set node flags
    # @param[in] flags - @see NodeFlags
    @flags.setter
    def flags(self, flags):
        self.data.contents.flags = 0
        for f in flags:
            self.data.contents.flags |= f.value

    ##
    # get version
    @property
    def version(self):
        ver = ""
        if self.data.contents.version.git_hash:
            ver = "{0}.{1}.{2}".format(self.data.contents.version.major_ver, self.data.contents.version.minor_ver,
                                       self.data.contents.version.git_hash)
        else:
            ver = "{0}.{1}".format(self.data.contents.version.major_ver, self.data.contents.version.minor_ver)

        if self.data.contents.version.git_uncommited:
            ver += "*"
        if self.data.contents.version.is_debug:
            ver = "[" + ver + "]"
        return ver
        # else:
        #     return "-"

    ##
    # get config
    @property
    def config(self):
        return self.data.contents.config.data[:self.data.contents.config.len].decode()


##
# Registry class. Main nodes registration place
class Registry(object):

    class RegistryCtypes(ctypes.Structure):
        _fields_ = [('major_ver', ctypes.c_ushort),
                    ('lock', ctypes.c_int),
                    ('out_of_system', ctypes.c_int),
                    ('system_name', xtypes.SystemName),
                    ('root_dir', xtypes.Path),
                    ('home_dir', xtypes.Path),
                    ('entries', NodeData.NodeDataCtypes * XROAD_REGISTRY_NODE_COUNT_MAX)]

    def __init__(self, out_of_system=False):
        res = lib.node().xroad_registry_init(1 if out_of_system is True else 0)
        if res == xtypes.Errno.failed:
            raise RuntimeError("unable to init registry")

    @property
    def system_name(self):
        reg = ctypes.cast(lib.node().xroad_registry_get(), ctypes.POINTER(Registry.RegistryCtypes))
        return reg.contents.system_name.data[:reg.contents.system_name.len].decode()

    ##
    # find NodeData by node name
    # @param[in] node_name - node name
    # @return NodeData or None
    def get_by_name(self, node_name):
        ndata = lib.node().xroad_registry_get_by_name(xtypes.Str(node_name))
        try:
            if not ndata:
                raise NodeNotFound("node not found")
            return NodeData(ndata)
        except NodeNotFound:
            raise NodeNotFound("node not found by {0} name".format(node_name))

    ##
    # find NodeData by node id
    # @param[in] id - node id
    # return NodeData or None
    def get_by_id(self, id):
        ndata = lib.node().xroad_registry_get_by_id(id)
        try:
            if not ndata:
                raise NodeNotFound("node not found")
            return NodeData(ndata)
        except NodeNotFound:
            raise NodeNotFound("node not found by {0} id".format(id))

    ##
    # find NodeData by pid
    # @param[in] node_pid - process pid
    # @return NodeData or None
    def get_by_pid(self, node_pid):
        ndata = lib.node().xroad_registry_get_by_id(node_pid)
        try:
            if not ndata:
                raise NodeNotFound("node not found")
            return NodeData(ndata)
        except NodeNotFound:
            raise NodeNotFound("node not found by {0} pid".format(node_pid))

    ##
    # iterate via nodes
    # @return NodeData or None
    @property
    def nodes(self):
        reg = ctypes.cast(lib.node().xroad_registry_get(), ctypes.POINTER(Registry.RegistryCtypes))
        i = 0
        while i < XROAD_REGISTRY_NODE_COUNT_MAX:
            ndata = reg.contents.entries[i]
            if not ndata.id:
                i += 1
                continue
            else:
                yield NodeData(ctypes.pointer(ndata))
                i += 1


# vim:et:sts=4:sw=4
