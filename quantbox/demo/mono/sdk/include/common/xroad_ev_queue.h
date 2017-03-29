#pragma once
/**
 * @file   xroad_ev_queue.h
 * @author Danil Krivopustov, krivopustovda@gmail.com
 */

#include <stdint.h>
#include "xroad_common_fwd.h"
#include "xroad_common_types.h"

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct
{
   void* ctx; // pointer to contex
   void (*on_event)(void* ctx); // pointer to function
} xroad_ev_callback_t;

/**
 * create new event queue
 * @return event queue object
 */
xroad_ev_queue_t* xroad_ev_queue_create();

/**
 * arm timer for nearest event if ones exists
 * @param[in] q - event queue instance
 */
void xroad_ev_queue_start(xroad_ev_queue_t* q);

/**
 * disarm timer
 * @param[in] q - event queue instance
 */
void xroad_ev_queue_stop(xroad_ev_queue_t* q);

/**
 * disarm timer and clear events heap
 * @param[in] q - event queue instance
 */
void xroad_ev_queue_clear(xroad_ev_queue_t* q);

/**
 * destroy event queue instance
 * @param[in] q - event queue instance
 */
void xroad_ev_queue_destroy(xroad_ev_queue_t* q);

/**
 * add new events to event queue and arm timer if event has nearest time to be fired
 * @param[in] q - event queue instance
 * @param[in] cb - event callback
 * @param[in] tm_usec - event time in usec
 */
void xroad_ev_queue_add_ev(xroad_ev_queue_t* q, xroad_ev_callback_t cb, uint64_t tm_usec);

#ifdef __cplusplus
}
#endif
