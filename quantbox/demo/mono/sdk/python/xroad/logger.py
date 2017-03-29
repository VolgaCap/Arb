import sys
import ctypes
import syslog
import logging
import traceback
from enum import IntEnum
from xroad import lib
from xroad.xtypes import Str


class LogLevel(IntEnum):
    """
    Log level xroad
    """
    error = 1
    warn = 2
    info = 4
    debug = 8
    trace = 16


class DisableLogger():

    def __enter__(self):
        logging.disable(logging.CRITICAL)

    def __exit__(self, a, b, c):
        logging.disable(logging.NOTSET)


class XroadLogger(logging.Handler):

    def __init__(self):
        super(XroadLogger, self).__init__(logging.DEBUG)
        self.cache = []

    def levelno_to_log_level(self, levelno):
        if logging.ERROR == levelno:
            return LogLevel.error
        elif logging.CRITICAL == levelno:
            return LogLevel.error
        elif logging.WARN == levelno:
            return LogLevel.warn
        elif logging.INFO == levelno:
            return LogLevel.info
        return LogLevel.debug

    def write_xroad_log(self, record):
        msg = self.format(record)
        name = Str("main") if record.name == "root" else Str(record.name)
        logger = lib.logger().xroad_logger_get(name)
        lib.logger().xroad_logx(logger,
                                self.levelno_to_log_level(record.levelno), Str("%s"), ctypes.c_char_p(msg.encode()))

    def emit(self, record):
        try:
            if lib.node().xroad_node_is_initialized():
                if self.cache:
                    for rec in self.cache:
                        self.write_xroad_log(rec)
                    self.cache = []
                self.write_xroad_log(record)
            else:
                if record.levelno == logging.ERROR:
                    msg = self.format(record)
                    syslog.syslog(syslog.LOG_ERR, msg)
                    if self.cache:
                        for rec in self.cache:
                            syslog.syslog(syslog.LOG_ERR, self.format(rec))
        except TypeError:
            record.args = []
            self.emit(record=record)
        except Exception:
            self.handleError(record)


def log_exception(except_type, msg, trace):
    # trace exception
    logging.error("{}:    {}".format(except_type, msg))
    for s in traceback.extract_tb(trace):
        data = "File {0}, line {1}, in {2}".format(s[0], s[1], s[2])
        logging.error(data)
        if s[3] is not None:
            data = "     {0}".format(s[3])
            logging.error(data)


def init():
    logging.raiseExceptions = False
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    xlogger = XroadLogger()
    root.addHandler(xlogger)

    add_handler = False
    for arg in sys.argv:
        if '--stdout' in arg:
            add_handler = True

    if add_handler:
        # xroad_logger.propagate = True
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        xlogger.addHandler(sh)
    else:
        xlogger.propagate = False

# vim:et:sts=4:sw=4
