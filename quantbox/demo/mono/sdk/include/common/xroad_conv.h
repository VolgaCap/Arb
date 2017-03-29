/**
 * @file   xroad_conv.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include "xroad_string.h"
#include <stdint.h>
#include <node_gen/xroad_objects_types.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * return number of digits. E.g. 10221 -> 5
 * @param[in] val - numeric value
 * @return number of digits
 */
uint32_t xroad_conv_numdigits(int64_t val);

/**
 * return number of digits after dot. E.g. 1.234 -> 3, 1 -> 0
 * @param[in] val - float value
 * @return number of digits
 */
uint32_t xroad_conv_precision(xroad_double_t val);

/**
 * pow10 calculation
 */
int64_t xroad_conv_lpow10(int32_t n);

/**
 * convert int64 value into string
 * @param[in] val     - converted value
 * @param[out] buf    - bufer with converted value
 * @param[in] buf_len - length of bufer
 * @param[in] padSym  - padding symbol
 * @return how many characters written (can be written). If this value greater than buf_len, value converted
 * incompletely
 */
uint32_t xroad_conv_i64toa(int64_t val, char* buf, uint32_t buf_len, char padSym);

/**
 * convert uint64 value into string
 * @param[in] val     - converted value
 * @param[out] buf    - bufer with converted value
 * @param[in] buf_len - length of bufer
 * @param[in] padSym  - padding symbol
 * @return how many characters written (can be written). If this value greater than buf_len, value converted
 * incompletely
 */
uint32_t xroad_conv_u64toa(uint64_t val, char* buf, uint32_t buf_len, char padSym);

/**
 * convert double to string
 * @param[in] val     - converted value
 * @param[in] prec    - value precision
 * @param[out] buf    - bufer with converted value
 * @param[in] buf_len - length of bufer
 * @return how many characters written (can be written). If this value greater than buf_len, value converted
 * incompletely
 */
uint32_t xroad_conv_dtoa(double val, uint32_t prec, char* buf, uint32_t buf_len);

/**
 * convert string to 32-bit unsigned number
 * @param[in] str     - string value to convert
 * @param[out] cnt    - how many characters processed
 * @return converted value
 */
uint32_t xroad_conv_atou32(xroad_str_t str, int32_t* cnt);

/**
 * convert string to 32-bit number
 * @param[in] str     - string value to convert
 * @param[out] cnt    - how many characters processed
 * @return converted value
 */
int32_t xroad_conv_atoi32(xroad_str_t str, int32_t* cnt);

/**
 * convert string to 64-bit unsigned number
 * @param[in] str     - string value to convert
 * @param[out] cnt    - how many characters processed
 * @return converted value
 */
uint64_t xroad_conv_atou64(xroad_str_t str, int32_t* cnt);

/**
 * convert string to 64-bit number
 * @param[in] str     - string value to convert
 * @param[out] cnt    - how many characters processed
 * @return converted value
 */
int64_t xroad_conv_atoi64(xroad_str_t str, int32_t* cnt);

/**
 * convert string to double
 * @param[in] str     - string value to convert
 * @param[out] cnt    - how many characters processed
 * @return converted value
 */
double xroad_conv_atod(xroad_str_t str, int32_t* cnt);

#ifdef __cplusplus
}
#endif
