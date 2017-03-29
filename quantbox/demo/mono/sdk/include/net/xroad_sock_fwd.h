#pragma once
/**
 * @file   xroad_sock_fwd.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * socket type
 */
typedef enum
{
   xroad_sock_type_tcp = 1,   ///< TCP socket
   xroad_sock_type_udp = 2,   ///< UDP socket
   xroad_sock_type_uds = 3,   ///< Unix domain socket
   xroad_sock_type_shm = 4    ///< shared memory socket
} xroad_sock_type_t;

///< socket id type
typedef int32_t xroad_sockid_t;

typedef struct xroad_net_buf_s xroad_net_buf_t;

typedef struct xroad_sock_s xroad_sock_t;

typedef struct xroad_sock_addr_s xroad_sock_addr_t;

typedef struct xroad_sock_vtbl_s xroad_sock_vtbl_t;

#ifdef __cplusplus
}
#endif
