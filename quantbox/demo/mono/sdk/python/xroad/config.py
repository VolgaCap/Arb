##
# @file config.py
# @author Dmitry S. Melnikov, dmitryme@gmail.com

import xroad.xtypes as xtypes
import xroad.lib as lib


##
# the main class to process xml config files
class Config(object):

    def __init__(self, ptr):
        self.__ptr = ptr

    ##
    # return raw pointer
    @property
    def ptr(self):
        return self.__ptr

    ##
    # check if child exists
    def has_child(self, path):
        return bool(lib.common().xroad_xml_has_tag(self.__ptr, xtypes.Str(path)))

    ##
    # check if attribute exists
    def has_attr(self, attr):
        return bool(lib.common().xroad_xml_has_attr(self.__ptr, xtypes.Str(attr)))

    ##
    # gets child config by its path
    # @param[in] path - path to config elements
    def get_child(self, path):
        tag = lib.common().xroad_xml_get_tag(self.__ptr, xtypes.Str(path))
        if tag == 0:
            return None
        return Config(tag)

    ##
    # iterate via children tag
    @property
    def children(self):
        tag = lib.common().xroad_xml_get_first(self.__ptr, xtypes.Str(''))
        while tag:
            _next = Config(tag)
            yield _next
            tag = lib.common().xroad_xml_get_next(_next.__ptr, xtypes.Str(''))

    ##
    # gets quantity of children of the xml tag parent
    @property
    def children_count(self):
        return lib.common().xroad_xml_get_children_count(self.__ptr)

    ##
    # gets name of the xml tag
    @property
    def name(self):
        res = lib.common().xroad_xml_get_name(self.__ptr)
        return str(res)

    ##
    # gets text of the xml tag
    @property
    def text(self):
        res = lib.common().xroad_xml_get_text(self.__ptr)
        return str(res)

    ##
    # gets content of tag's attribute as a string by its name
    def get_attr_s(self, name):
        res = lib.common().xroad_xml_get_attr_s(self.__ptr, xtypes.Str(name))
        if res.is_null:
            return None
        return str(res)

    ##
    # gets content of tag's attribute as an integer by its name
    def get_attr_i(self, name):
        return lib.common().xroad_xml_get_attr_i(self.__ptr, xtypes.Str(name))

    ##
    # gets content of tag's attribute as a double by its name
    def get_attr_d(self, name):
        return lib.common().xroad_xml_get_attr_d(self.__ptr, xtypes.Str(name))

    ##
    # gets content of tag's attribute as a boolean by its name
    def get_attr_b(self, name):
        return lib.common().xroad_xml_get_attr_b(self.__ptr, xtypes.Str(name)) == 1


# vim:et:sts=4:sw=4
