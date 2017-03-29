##
# @file instrdb.py
# @author Dmitry S. Melnikov, dmitryme@gmail.com

import xroad.objects as objects
import xroad.lib as lib
from xroad.xtypes import Str


##
# instrument database class
class InstrDB(object):

    def __init__(self):
        self.__instrdb = lib.idb().instrdb_create()
        if self.__instrdb == 0:
            raise RuntimeError('instrdb creation failed')

    def __del__(self):
        if self.__instrdb:
            lib.idb().instrdb_destroy(self.__instrdb)

    ##
    # gets instrument by its alias
    # @param[in] alias - instrument alias
    # @return @see Instrument
    def get_by_alias(self, alias):
        i = lib.idb().instrdb_get_by_alias(self.__instrdb, Str(alias))
        if i:
            return objects.Instr(i)
        return None

    ##
    # gets instrument by its name and class
    # @param[in] name  - instrument name
    # @param[in] cls   - instrument class
    # @return @see Instrument
    def get_by_name(self, name, cls):
        i = lib.idb().instrdb_get_by_name(self.__instrdb, Str(name), Str(cls))
        if i:
            return objects.Instr(i)
        return None

    ##
    # gets instrument by its instr id
    # @param[in] id - instrument id
    # @return @see Instrument
    def get_by_id(self, instr_id):
        i = lib.idb().instrdb_get_by_id(self.__instrdb, instr_id)
        if i:
            return objects.Instr(i)
        return None

    ##
    # create instrument
    # @param[in] alias      - instrument alias
    # @param[in] name       - instrument name
    # @param[in] long_name  - instrument long name
    # @param[in] cls        - instrument class
    # @return @see Instrument
    def add(self, alias, name, long_name, cls):
        i = lib.idb().instrdb_add(
            self.__instrdb, Str(alias), Str(name), Str(long_name), Str(cls))
        if i:
            return objects.Instr(i)
        return None

# vim:et:sts=4:sw=4
