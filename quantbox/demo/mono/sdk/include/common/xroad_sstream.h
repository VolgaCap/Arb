/**
 * @file   xroad_sstream.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include <common/xroad_common_types.h>
#include <common/xroad_string.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct xroad_sstream_s xroad_sstream_t;

/**
 * create new string stream
 * @param[in] buf_size - initial stream buffer size
 * return stream instance
 */
xroad_sstream_t* xroad_sstream_create(uint32_t buf_size);

/**
 * clear stream buffer
 * @param[in] s - stream to clear
 */
void xroad_sstream_clear(xroad_sstream_t* s);

/**
 * destroy stream
 * @param[in] s - stream to destroy. If NULL, nothing happened
 */
void xroad_sstream_destroy(xroad_sstream_t* s);

/**
 * return stream content
 * @param[in] s - stream
 * @return stream content as xroad_string_t
 */
xroad_str_t xroad_sstream_gets(xroad_sstream_t* s);

/**
 * append formatted text to stream
 * @param[in] s - stream
 * @param[in] fmt - format
 * @return count of appended chars
 */
uint32_t xroad_sstream_format(xroad_sstream_t* s, const char* fmt, ...);

/**
 * drop N last appended chars
 * @param[in] s - stream
 * @param[in] cnt - number of chars to drop
 * @return number of dropped chars
 */
uint32_t xroad_sstream_unformat(xroad_sstream_t* s, uint32_t cnt);

#ifdef __cplusplus
}
#endif
