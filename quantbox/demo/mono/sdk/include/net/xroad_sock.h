#pragma once
/**
 * @file   xroad_sock.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#include "xroad_sock_fwd.h"
#include <common/xroad_string.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C"
{
#endif

#define XROAD_SOCK_OPT_SO_NODELAY      1
#define XROAD_SOCK_OPT_SO_REUSE_ADDR   2
#define XROAD_SOCK_OPT_SO_KEEP_ALIVE   3
#define XROAD_SOCK_OPT_BUF_SIZE        4
#define XROAD_SOCK_OPT_BUF_MAX_SIZE    5
#define XROAD_SOCK_OPT_MAX_CLNT_CONN   6
#define XROAD_SOCK_OPT_SO_LINGER       7
#define XROAD_SOCK_OPT_SO_REUSE_PORT   8

/**
 * socket callbacks
 */
typedef struct
{
   void* ctx; ///< stored context. It passed to each callback method
   /**
    * optional. fired, when connection has been established
    */
   void (*on_connected)(xroad_sockid_t, void*);
   /**
    * optional. fired, when connection closed
    */
   void (*on_disconnected)(xroad_sockid_t, void*);
   /**
    * mandatory. fired, when new data received
    * return count of processed bytes
    */
   size_t (*on_data)(xroad_sockid_t, const xroad_net_buf_t*, void*);
   /**
    * optional. fired, when socket is ready to send data
    */
   void (*on_ready_to_send)(xroad_sockid_t, void*);
} xroad_sock_callback_t;

/**
 * create new socket
 * @param[in] addr - address of socket (see xroad_addr.h for details)
 * @param[in] cback - socket callback
 * @return id of created socket (> 0). < 0 - error happened
 */
xroad_sockid_t xroad_sock_create(xroad_str_t addr, xroad_sock_callback_t* cback);

/**
 * destroy socket and free its resources
 * @param[in] sockid - id of socket to destroy
 * @return XROAD_OK - destroyed, < 0 - error happened
 */
xroad_errno_t xroad_sock_destroy(xroad_sockid_t sockid);

/**
 * return type of socket
 * @param[in] sockid - socket id
 * @return see xroad_sock_type_t enum for possible values. if return value < 0, socket is unknown
 */
xroad_sock_type_t xroad_sock_get_type(xroad_sockid_t sockid);

/**
 * replace socket callback with new one
 * @param[in] sockid - socket id
 * @param[in] cback  - new socket callback
 * @return XROAD_OK - callback replaced, < 0 - error happened
 */
xroad_errno_t xroad_sock_set_callback(xroad_sockid_t sockid, xroad_sock_callback_t* cback);

/**
 * connect socket
 * @param[in] sockid - socket id
 * @return XROAD_OK - connected, < 0 - failed
 */
xroad_errno_t xroad_sock_connect(xroad_sockid_t sockid);

/**
 * disconnect socket
 * @param[in] sockid - socket id
 * @return XROAD_OK - disconnected, < 0 - failed
 */
xroad_errno_t xroad_sock_disconnect(xroad_sockid_t sockid);

/**
 * bind socket
 * @param[in] sockid - socket id
 * @return XROAD_OK - socket has been bound, < 0 - failed
 */
xroad_errno_t xroad_sock_bind(xroad_sockid_t sockid);

/**
 * unbind socket
 * @param[in] sockid - socket id
 * @return XROAD_OK - socket has been bound, < 0 - failed
 */
xroad_errno_t xroad_sock_unbind(xroad_sockid_t sockid);

/**
 * send data to socket
 * @param[in] sockid - socket id
 * @param[in] buf - data to send
 * @return number of sent bytes, < 0 - send failed (see xroad_errno_t for details)
 */
ssize_t xroad_sock_send(xroad_sockid_t sockid, const xroad_net_buf_t* buf);

/**
 * set socket option
 * @param[in] sockid - socket id
 * @param[in] optid  - option id (see XROAD_SOCK_OPT_*)
 * @param[in] opt    - option value
 * @return XROAD_OK  - option has been set, <0 - failed
 */
xroad_errno_t xroad_sock_set_opt(xroad_sockid_t sockid, int32_t optid, void* opt);

#ifdef __cplusplus
}
#endif
