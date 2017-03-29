/**
 * @file   xroad_logger.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include <common/xroad_string.h>
#include <common/xroad_xml.h>
#include <stdio.h>

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct xroad_logger_s xroad_logger_t;

/**
 * log level
 */
typedef enum
{
   xroad_log_level_error = 0x1,
   xroad_log_level_warn  = 0x2,
   xroad_log_level_info  = 0x4,
   xroad_log_level_debug = 0x8,
   xroad_log_level_trace = 0x10
} xroad_log_level_t;

/**
 * create logger.
 * NOTE: Alarming is disable by default. call xroad_logger_enable_alarm to enable it
 * @return XROAD_OK - created, else failed
 */
xroad_errno_t xroad_logger_create();

/**
 * configure logger
 * @param[in] cfg - logger configuration
 */
void xroad_logger_configure(xroad_xml_tag_t cfg);

/**
 * create new log file
 * @return XROAD_OK - rotated, else failed
 */
xroad_errno_t xroad_logger_rotate();

/**
 * disable alarm sending
 */
void xroad_logger_disable_alarm();

/**
 * enable alarm senging
 */
void xroad_logger_enable_alarm();

/*
 * return logger
 * @param[in] name - logger name. If no such logger found, return "main"
 * @return logger - logger instance
 */
xroad_logger_t* xroad_logger_get(xroad_str_t name);

/**
 * get current log level
 * @param[in] logger - logger to set. if NULL, main logger alarm is set
 */
xroad_log_level_t xroad_logger_get_level(xroad_logger_t* logger);

//--------------------------------------------------------------------------------------------------------------------//
// info logging
//--------------------------------------------------------------------------------------------------------------------//
/**
 * log record as info
 */
#define xroad_logx_info(logger, fmt, ...) xroad_logx(logger, xroad_log_level_info, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record as info
 */
#define xroad_vlogx_info(logger, fmt, ap) xroad_vlogx(logger, xroad_log_level_info, xroad_str(fmt), ap)

/**
 * log record as info using main logger
 */
#define xroad_log_info(fmt, ...) xroad_logx(NULL, xroad_log_level_info, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record as info using main logger
 */
#define xroad_vlog_info(fmt, ap) xroad_vlogx(NULL, xroad_log_level_info, xroad_str(fmt), ap)

//--------------------------------------------------------------------------------------------------------------------//
// error logging
//--------------------------------------------------------------------------------------------------------------------//
/**
 * log record as error
 */
#define xroad_logx_error(logger, fmt, ...) xroad_logx(logger, xroad_log_level_error, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record as error
 */
#define xroad_vlogx_error(logger, fmt, ap) xroad_vlogx(logger, xroad_log_level_error, xroad_str(fmt), ap)

/**
 * log record as error using main logger
 */
#define xroad_log_error(fmt, ...) xroad_logx(NULL, xroad_log_level_error, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record as error using main logger
 */
#define xroad_vlog_error(fmt, ap) xroad_vlogx(NULL, xroad_log_level_error, xroad_str(fmt), ap)

//--------------------------------------------------------------------------------------------------------------------//
// warning logging
//--------------------------------------------------------------------------------------------------------------------//
/**
 * log record as warn
 */
#define xroad_logx_warn(logger, fmt, ...) xroad_logx(logger, xroad_log_level_warn, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record as warn
 */
#define xroad_vlogx_warn(logger, fmt, ap) xroad_vlogx(logger, xroad_log_level_warn, xroad_str(fmt), ap)

/**
 * log record as warn using main logger
 */
#define xroad_log_warn(fmt, ...) xroad_logx(NULL, xroad_log_level_warn, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record as warn using main logger
 */
#define xroad_vlog_warn(fmt, ap) xroad_vlogx(NULL, xroad_log_level_warn, xroad_str(fmt), ap)

//--------------------------------------------------------------------------------------------------------------------//
// debug logging
//--------------------------------------------------------------------------------------------------------------------//
/**
 * log record as debug
 */
#define xroad_logx_debug(logger, fmt, ...) xroad_logx(logger, xroad_log_level_debug, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record as debug
 */
#define xroad_vlogx_debug(logger, fmt, ap) xroad_vlogx(logger, xroad_log_level_debug, xroad_str(fmt), ap)

/**
 * log record as debug using main logger
 */
#define xroad_log_debug(fmt, ...) xroad_logx(NULL, xroad_log_level_debug, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record as debug using main logger
 */
#define xroad_vlog_debug(fmt, ap) xroad_vlogx(NULL, xroad_log_level_debug, xroad_str(fmt), ap)


//--------------------------------------------------------------------------------------------------------------------//
// trace logging
//--------------------------------------------------------------------------------------------------------------------//
/**
 * log record as trace
 */
#define xroad_logx_trace(logger, fmt, ...) xroad_logx(logger, xroad_log_level_trace, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record as trace
 */
#define xroad_vlogx_trace(logger, fmt, ap) xroad_vlogx(logger, xroad_log_level_trace, xroad_str(fmt), ap)

/**
 * log record as trace using main logger
 */
#define xroad_log_trace(fmt, ...) xroad_logx(NULL, xroad_log_level_trace, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record as trace using main logger
 */
#define xroad_vlog_trace(fmt, ap) xroad_vlogx(NULL, xroad_log_level_trace, xroad_str(fmt), ap)

/**
 * log with setting level in variable.
 * @param[in] logger - logger
 * @param[in] llevel - log level
 * @param[in] fmt - log pettern
 */
void xroad_logx(
      xroad_logger_t* logger,
      xroad_log_level_t llevel,
      xroad_str_t fmt,
      ...);

/**
 * log with setting level in variable.
 * @param[in] logger - logger
 * @param[in] llevel - log level
 * @param[in] fmt - log pettern
 * @param[in] ap - argument list
 */
void xroad_vlogx(
      xroad_logger_t* logger,
      xroad_log_level_t llevel,
      xroad_str_t fmt,
      va_list ap);

/**
 * log record using main logger
 */
#define xroad_log(llevel, fmt, ...) xroad_logx(NULL, llevel, xroad_str(fmt), ##__VA_ARGS__)

/**
 * log record using main logger
 */
#define xroad_vlog(llevel, fmt, ap) xroad_vlogx(NULL, llevel, xroad_str(fmt), ap)


#ifdef __cplusplus
}
#endif
