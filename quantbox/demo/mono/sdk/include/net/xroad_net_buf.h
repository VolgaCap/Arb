#pragma once
/**
 * @file   xroad_net_buf.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */


#include "xroad_sock_fwd.h"
#include <common/xroad_common_types.h>
#include <stdint.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * memory buffer for sending/receiving data
 */
struct xroad_net_buf_s
{
   char*  begin;      ///< buffer begin
   char*  data_begin; ///< data begin
   char*  data_end;   ///< data end
   char*  end;        ///< buffer end
   size_t max_size;   ///< maximum buffer size
};

/**
 * alocate new buffer
 * @param[in] buf       - buffer for witch data will be allocated
 * @param[in] size      - initial size of data to allocate
 * @param[in] max_size  - set maximum allocated data size
 * @return XROAD_OK     - created,
 *         XROAD_FAILED - error
 */
xroad_errno_t xroad_net_buf_create(xroad_net_buf_t* buf, size_t size, size_t max_size);

/**
 * try to increase buffer size_t
 * @param[in] buf          - buffer to increase
 * @param[in] size         - increase space size
 * @return XROAD_ERROR_OK  - increased,
 *         XROAD_ERROR_NO_MORE_SPACE - buffer space is a maximum
 */
xroad_errno_t xroad_net_buf_increase(xroad_net_buf_t* buf, size_t size);

/**
 * free buffer
 * @param[in] buf - buffer to destroy
 */
void xroad_net_buf_destroy(xroad_net_buf_t* buf);

/**
 * frees unused space in buffer
 * @param[in] buf - buffer to free space
 */
void xroad_net_buf_free_space(xroad_net_buf_t* buf);

/**
 * reset buffer to initial state. No decreasing space is made.
 * @param[in] buf - buf to reset
 */
static inline void xroad_net_buf_reset(xroad_net_buf_t* buf)
{
   buf->data_begin = buf->data_end = buf->begin;
}

/**
 * return buffer data size
 * @param[in] buf - buf with data
 * @return size of data stored in buf
 */
static inline size_t xroad_net_buf_get_data_size(const xroad_net_buf_t* buf)
{
   return buf->data_end - buf->data_begin;
}

/**
 * return total(allocated) buffer size
 * @param[in] buf - buf with data
 * @return size of total buffer size
 */
static inline size_t xroad_net_buf_get_total_size(const xroad_net_buf_t* buf)
{
   return buf->end - buf->begin;
}

/**
 * return buffer free allocated space
 * @param[in] buf - buf with data
 * @return size of free buffer space
 */
static inline size_t xroad_net_buf_get_free_size(const xroad_net_buf_t* buf)
{
   return buf->end - buf->data_end;
}

#ifdef __cplusplus
}
#endif
