##
# @file ui.py
# @author Dmitry S. Melnikov, dmitryme@gmail.com

import struct
from xroad.common import *
from xroad.order_ctypes import *
import xroad.objects as objects
import xroad.xtypes as xtypes
import xroad.lib as lib


class FieldWrapper(object):

    def __init__(self, field):
        self.__fld = field

    @property
    def name(self):
        return self.__fld.name

    @property
    def field(self):
        return self.__fld

    @property
    def value(self):
        value = self.__fld.value
        if value is None:
            return None
        if self.__fld.type == xtypes.FieldType.string:
            return value.decode("utf-8")
        elif self.__fld.type == xtypes.FieldType.double:
            if len(value) == 4:
                return struct.unpack("f", value)[0]
            else:
                return struct.unpack("d", value)[0]
        else:
            if len(value) == 1:
                return struct.unpack("c", value)[0]
            elif len(value) == 2:
                return struct.unpack("h", value)[0]
            elif len(value) == 4:
                return struct.unpack("i", value)[0]
            else:
                return struct.unpack("l", value)[0]

    @value.setter
    def value(self, v):
        if isinstance(v, int):
            self.__fld.value = struct.pack("L", v)
        elif isinstance(v, float):
            self.__fld.value = struct.pack("d", v)
        elif isinstance(v, str):
            self.__fld.value = str.encode(v)
        else:
            raise RuntimeError("value {0} has wrong type".format(v))


class Ui(object):

    def __init__(self, cfg):
        self.ui = lib.ui().ui_create(cfg.ptr)
        if not self.ui:
            raise RuntimeError("unable to create ui")

    def get_field(self, name, node_id=0):
        fld = lib.ui().ui_get_field(self.ui, node_id, xtypes.Str(name))
        if not fld:
            raise RuntimeError("field {0} not found".format(name))
        return FieldWrapper(objects.Field(fld))

# vim:et:sts=4:sw=4
