/**
 * @file   order_aux.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include <node_gen/xroad_objects.h>

#ifdef __cplusplus
extern "C"
{
#endif


#define xroad_order_is_active(order)                                    \
({                                                                      \
   xroad_order_status_t status = xroad_order_base_get_status(order);    \
   xroad_order_status_initial == status ||                              \
   xroad_order_status_active == status ||                               \
   xroad_order_status_awaiting_active == status ||                      \
   xroad_order_status_awaiting_cancel == status ||                      \
   xroad_order_status_awaiting_replace == status;                       \
})

#define xroad_order_is_on_exchange(order)                               \
({                                                                      \
   xroad_order_status_t status = xroad_order_base_get_status(order);    \
   xroad_order_status_active == status ||                               \
   xroad_order_status_awaiting_active == status ||                      \
   xroad_order_status_awaiting_cancel == status ||                      \
   xroad_order_status_awaiting_replace == status;                       \
})

#define xroad_order_is_done(order)                                      \
({                                                                      \
   xroad_order_status_t status = xroad_order_base_get_status(order);    \
   xroad_order_status_filled == status ||                               \
   xroad_order_status_canceled == status ||                             \
   xroad_order_status_rejected == status ||                             \
   xroad_order_status_expired == status ||                              \
   xroad_order_status_removed == status;                                \
})

#define xroad_order_is_pending(order)                                   \
({                                                                      \
   xroad_order_status_t status = xroad_order_base_get_status(order);    \
   xroad_order_status_awaiting_active == status ||                      \
   xroad_order_status_awaiting_cancel == status ||                      \
   xroad_order_status_awaiting_replace == status;                       \
})

#define order_is_active(order)                           \
({                                                       \
   order_state_t state = order_get_state(order);         \
   state == order_state_initial              ||          \
   state == order_state_active               ||          \
   state == order_state_awaiting_active      ||          \
   state == order_state_awaiting_replace     ||          \
   state == order_state_awaiting_destroy     ||          \
   state == order_state_awaiting_cancel;                 \
})

#define order_is_done(order)                             \
({                                                       \
   order_state_t state = order_get_state(order);         \
   state == order_state_destroyed   ||                   \
   state == order_state_canceled    ||                   \
   state == order_state_rejected    ||                   \
   state == order_state_filled      ||                   \
   state == order_state_expired;                         \
})

#define order_is_pending(order)                          \
({                                                       \
   order_state_t state = order_get_state(order);         \
   state == order_state_awaiting_active      ||          \
   state == order_state_awaiting_destroy     ||          \
   state == order_state_awaiting_cancel      ||          \
   state == order_state_awaiting_replace;                \
})

#define order_is_on_exchange(o)                          \
({                                                       \
   order_state_t st = order_get_state(o);                \
   st == order_state_active            ||                \
   st == order_state_awaiting_active   ||                \
   st == order_state_awaiting_cancel   ||                \
   st == order_state_awaiting_destroy  ||                \
   st == order_state_awaiting_replace;                   \
})


#ifdef __cplusplus
}
#endif
