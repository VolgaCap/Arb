/**
 * @file   order.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include <common/xroad_string.h>
#include <node_gen/xroad_objects.h>

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct order_s order_t;

#define ORDER_OPT_MAX_CANCEL_ATTEMPTS 1
#define ORDER_OPT_CANCEL_TIMEOUT_MS   2

/**
 * order state
 */
typedef enum
{
   order_state_initial           = 0, ///< order is in initial state
   order_state_active            = 1, ///< order is in active state
   order_state_destroyed         = 2, ///< order is in destroyed state
   order_state_canceled          = 3, ///< order is in canceled state
   order_state_rejected          = 4, ///< order is in rejected state
   order_state_filled            = 5, ///< order is in filled state
   order_state_expired           = 6, ///< order is in expired state
   order_state_awaiting_active   = 7, ///< order is in awaiting active state
   order_state_awaiting_destroy  = 8, ///< order is in awaiting destroyed state
   order_state_awaiting_cancel   = 9, ///< order is in awaiting cancel state
   order_state_awaiting_replace  = 10 ///< order is in awaiting replace state
} order_state_t;

/**
 * replace mask
 */
typedef enum
{
   order_replace_qty     = 1, ///< replace qty
   order_replace_price   = 2, ///< replace price
   order_replace_ext_ref = 4  ///< replace ext_ref
} order_replace_mask_t;

/**
 * convert order state to string representation
 * @param[in] state - order state
 * @return string representation
 */
xroad_str_t order_state_to_str(order_state_t state);

/**
 * order callback
 */
typedef struct
{
   /**
    * fired then order is activated on exchange
    */
   void (*on_activated)(order_t*);
   /**
    * fired before order is sent to exchange
    */
   void (*on_before_send)(order_t*);
   /**
    * fired when trade received
    */
   void (*on_trade)(order_t*, xroad_qty_t, xroad_price_t);
   /**
    * fired then order is canceled
    */
   void (*on_canceled)(order_t*);
   /**
    * fired then order is unexpected canceled
    */
   void (*on_unexpected_canceled)(order_t*);
   /**
    * fired then order is expired
    */
   void (*on_expired)(order_t*);
   /**
    * fired then order is going to be destroyed
    */
   void (*on_destroyed)(order_t*);
   /**
    * fired then order is replaced
    */
   void (*on_replaced)(order_t*);
   /**
    * fired then order is rejected
    */
   void (*on_rejected)(order_t*, xroad_rej_reason_t, xroad_str_t);
   /**
    * fired then order cancel is rejected
    */
   void (*on_cancel_rejected)(order_t*, xroad_rej_reason_t, xroad_str_t);
   /**
    * fired then order replace is rejected
    */
   void (*on_replace_rejected)(order_t*, xroad_rej_reason_t, xroad_str_t);
} order_callback_t;

/**
 * create new order
 * @param[in] name         - order name. Must be unique
 * @param[in] callback     - order callback
 * @param[in] instr        - instrument
 * @param[in] account      - order account
 * @param[in] client_code  - order client_code
 * @param[in] side         - order side
 * @param[in] qty          - order qty
 * @param[in] price        - order price
 * @param[in] ext_ref      - reference info, which will be sent with order
 * @param[in] ctx          - order ctx
 * @param[out] err         - error description is any
 * @return pointer to order, in case of error - NULL (see errno)
 */
order_t* order_create(
      xroad_str_t      name,
      order_callback_t callback,
      xroad_instr_t*   instr,
      xroad_str_t      account,
      xroad_str_t      client_code,
      xroad_side_t     side,
      xroad_qty_t      qty,
      xroad_price_t    price,
      xroad_str_t      ext_ref,
      void*            ctx,
      xroad_str_t*     err);

/**
 * set order option
 * @param[in] o      - order to set
 * @param[in] optid  - option id to set
 * @param[in] opt    - option value
 */

xroad_errno_t order_set_opt(order_t* o, int32_t optid, void* opt);

/**
 * destroy order
 * @param[in] o     - order to destory
 * @param[in] force - force order destruction (don't wait for exchange ack, if any)
 * @return XROAD_OK - destroy operation applied, else failed
 */
xroad_errno_t order_destroy(order_t* o, int32_t force);

/**
 * send order. order will be send to exchange
 * @param[in] o - order to send
 * @return XROAD_OK - send operation applied, else failed
 */
xroad_errno_t order_send(order_t* o);

/**
 * cancel order. order will be cancelled
 * @param[in] o - order to cancel
 * @return XROAD_OK - cancel operation applied, else failed
 */
xroad_errno_t order_cancel(order_t* o);

/**
 * replace order
 * @param[in] o       - order to replace
 * @param[in] qty     - order new qty
 * @param[in] price   - order new price
 * @param[in] ext_ref - reference info, which will be sent with order
 * @param[in] mask    - replace mask (see order_replace_mask_t)
 * @return XROAD_OK   - replace operation applied, else failed
 */
xroad_errno_t order_replace(
      order_t* o,
      xroad_qty_t qty,
      xroad_price_t price,
      xroad_str_t ext_ref,
      int32_t mask);

/**
 * reset order statistic
 * @param[in] o - order to reset
 */
void order_reset(order_t* o);

/**
 * process node events
 * @param[in] obj  - object to process
 * @param[in] from - object source
 */
void order_on_node_object(void* obj, xroad_node_id_t from);

/**
 * get order name
 * @param[in] o - order
 * @return order name
 */
xroad_str_t order_get_name(const order_t* o);

/**
 * get order instrument
 * @param[in] o - order
 * @return order instrument
 */
const xroad_instr_t* order_get_instr(const order_t* o);

/**
 * get order side
 * @param[in] o - order
 * @return order side
 */
xroad_side_t order_get_side(const order_t* o);

/**
 * get order qty
 * @param[in] o - order
 * @return order qty
 */
xroad_qty_t order_get_qty(const order_t* o);

/**
 * get order leaves qty
 * @param[in] o - order
 * @return order qty
 */
xroad_qty_t order_get_leaves_qty(const order_t* o);

/**
 * get order price
 * @param[in] o - order
 * @return order price
 */
xroad_price_t order_get_price(const order_t* o);

/**
 * get order context
 * @param[in] o - order
 * @return order context
 */
void* order_get_ctx(order_t* o);

/**
 * get order state
 * @param[in] o - order
 * @return order state
 */
order_state_t order_get_state(order_t* o);

/**
 * get order total qty
 * @param[in] o - order
 * @return order total qty
 */
uint64_t order_get_total_qty(order_t* o);

/**
 * get order avg price
 * @param[in] o - order
 * @return order avg price
 */
xroad_price_t order_get_avg_price(order_t* o);

/**
 * print order
 * @param[in] o - order to print
 * @return order strint representation
 */
xroad_str_t order_print(order_t* o);

/**
 * return xroad_order_t* pointer, if any
 * @param[in] o - pointer to order
 * return xroad_order_t* pointer if any
 */
xroad_order_t* order_get_xorder(order_t* o);

#ifdef __cplusplus
}
#endif
