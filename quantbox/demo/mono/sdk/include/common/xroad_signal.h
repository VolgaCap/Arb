/**
 * @file   xroad_signal.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include <stdint.h>
#include "xroad_common_types.h"

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct xroad_signal_s xroad_signal_t;

/**
 * signal callback
 */
typedef struct xroad_signal_callback_s
{
   void* ctx; ///< context, which will be passed in on_signal callback
   /**
    * called on signal received
    * @param[in] - signal instance
    * @param[in] - signal number
    * @param[in] - context
    */
   void (*on_signal)(xroad_signal_t*, int32_t, void*);
} xroad_signal_callback_t;

/**
 * create new signal handler
 * @param[in] cb - signal callback
 * @return created signal, NULL - error happened
 */
xroad_signal_t* xroad_signal_create(xroad_signal_callback_t cb);

/**
 * catch signal
 * @param[in] s - signal handler instance
 * @param[in] signal - signal number to catch
 * @return XROAD_OK - catched, else failed
 */
xroad_errno_t xroad_signal_catch(xroad_signal_t* s, int32_t signal);

/**
 * free signal
 * @param[in] s - signal handler instance
 * @param[in] signal - signal number to free
 * @return XROAD_OK - freed, else failed
 */
xroad_errno_t xroad_signal_free(xroad_signal_t* s, int32_t signal);

/**
 * destroy signal handler
 * @param[in] s - signal handler to destroy
 */
void xroad_signal_destroy(xroad_signal_t* s);

#ifdef __cplusplus
}
#endif
