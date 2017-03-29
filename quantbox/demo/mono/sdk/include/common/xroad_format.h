/**
 * @file   xroad_format.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include "xroad_common_types.h"
#include <stdint.h>
#include <stdarg.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * printf like formatter
 * @param[in] buf - buffer with formatted output
 * @param[in] len - maximum buffer length
 * @param[in] fmt - format string. Placeholders format %[pad_sym][length]<type>, where
 *                  pad_sym - padding symbol for numbers
 *                  length - precision for floats, field length for numbers and chars.
 *                  Available types
 *                   - d - argument is int32_t
 *                   - D - argument is int64_t
 *                   - u - argument is uint32_t
 *                   - U - argument is uint64_t
 *                   - c - argument is char
 *                   - s(zs) - argument is C-string
 *                   - S(zS) - argument is fixed length string created by xroad_str_decl
 *                   - P(zP) - argument is xroad_str_t
 *                   - f - argument is double
 *                   - X - argument is byte array
 * NOTE: xroad_format doesn't support %O, %R formatter as xroad_logger does, because I dont want to make
 * common lib dependent from objects library
 * @return number of written chars even if there is no enought space in buf to write, if result < 0, error
 *         happened
 */
int32_t xroad_format(char* buf, uint32_t len, const char* fmt, ...);

/**
 * the same as xroad_format, but accept va_list instead of ...
 */
int32_t xroad_vformat(char* buf, uint32_t len, const char* fmt, va_list ap);

#ifdef __cplusplus
}
#endif
