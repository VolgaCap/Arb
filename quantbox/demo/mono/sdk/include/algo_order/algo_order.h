/**
 * @file   algo_order.h
 * @author Danil Krivopustov
 */

#pragma once

#include <common/xroad_string.h>
#include <node_gen/xroad_objects.h>
#include <mdata/engine/mdata_engine.h>

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct algo_order_s algo_order_t;

/**
 * order state
 */
typedef enum
{
   algo_order_state_initial           = 0, ///< order is in initial state
   algo_order_state_active            = 1, ///< order is in active state
   algo_order_state_middle            = 2, ///< order is in midle state
   algo_order_state_liquidate         = 3, ///< order is in liquidation state
   algo_order_state_completed         = 4, ///< order is in completed state
   algo_order_state_awaiting_cancel   = 5, ///< order is in awaiting cancel state
   algo_order_state_canceled          = 6, ///< order is in canceled state
   algo_order_state_awaiting_replace  = 7, ///< order is in awaiting replace state
} algo_order_state_t;

/**
 * order callback
 */
typedef struct
{
   /**
    * fired then order is activated on exchange
    */
   void (*on_accepted)(void*, xroad_order_t*);
   /**
    * fired when trade received
    */
   void (*on_trade)(void*, xroad_order_t*, xroad_trade_t*);
   /**
    * fired then order is canceled
    */
   void (*on_canceled)(void*, xroad_order_t*);
   /**
    * fired then order is unexpected canceled
    */
   void (*on_unexpected_canceled)(void*, xroad_order_t*);
   /**
    * fired then order is expired
    */
   void (*on_removed)(void*, xroad_order_t*);
   /**
    * fired then order is expired
    */
   void (*on_expired)(void*, xroad_order_t*);
   /**
    * fired then order is replaced
    */
   void (*on_replaced)(void*, xroad_order_t*, xroad_replaced_t*);
   /**
    * fired then order is rejected
    */
   void (*on_rejected)(void*, xroad_order_t*, xroad_rejected_t*);
   /**
    * fired then order cancel is rejected
    */
   void (*on_cancel_rejected)(void*, xroad_order_t*, xroad_cancel_rejected_t* cr);
   /**
    * fired then order replace is rejected
    */
   void (*on_replace_rejected)(void*, xroad_order_t*);

} algo_order_callback_t;

/**
 * create new order
 * @param[in] mdata          - order name. Must be unique
 * @param[in] callback       - order callback
 * @param[in] parent         - parent xroad order
 * @param[in] ctx            - order context
 * @param[in] deep_of_book   - book depth (in levels)
 * @param[in] level_interval - interval between levels (in price levels)
 * @return pointer to order, in case of error - NULL (see errno)
 */
algo_order_t* algo_order_create(
      mdata_engine_t*       mdata,
      algo_order_callback_t callback,
      xroad_order_t*        parent,
      void*                 ctx,
      int64_t               deep_of_book,
      int64_t               level_interval);

//void algo_order_start(algo_order_t* o);
/**
 * destroy order
 * @param[in] o     - order to destory
 * @param[in] force - force order destruction (don't wait for exchange ack, if any)
 * @return XROAD_OK - destroy operation applied, else failed
 */
void algo_order_destroy(algo_order_t* o);

/**
 * cancel order. order will be cancelled
 * @param[in] o - order to cancel
 * @return XROAD_OK - cancel operation applied, else failed
 */
xroad_errno_t algo_order_cancel(algo_order_t* o);

/**
 * replace order
 * @param[in] o      - order to replace
 * @param[in] qty    - order new qty
 * @param[in] price  - order new price
 * @param[in] mask   - replace mask (see algo_order_replace_mask_t)
 * @return XROAD_OK  - replace operation applied, else failed
 */
xroad_errno_t algo_order_send(algo_order_t* o, xroad_qty_t qty, xroad_qty_t display_qty, int64_t mid_shift, int64_t liq_shift, int64_t agression_level);

/**
 * process node events
 * @param[in] obj  - object to process
 * @param[in] from - object source
 */
void algo_order_on_node_object(algo_order_t* order, void* obj);

/**
 * gets context for algo order
 * @param[in] o - algo order
 */
void* algo_order_get_ctx(algo_order_t* order);

/**
 * gets order qty
 * @param[in] o - algo order
 */
xroad_qty_t algo_order_get_qty(algo_order_t*);

/**
 * gets order state
 * @param[in] o - algo order
 */
algo_order_state_t algo_order_get_state(algo_order_t*);

/**
 * sets order state
 * @param[in] o - algo order
 * @param[in] s - algo order state
 */
void algo_order_set_state(algo_order_t* o, algo_order_state_t s);

/**
 * gets order statistice
 * @param[in] o - algo order
 */
xroad_str_t algo_order_stat(algo_order_t* o);

/**
 * gets order parent
 * @param[in] o - algo order
 */
xroad_order_t* algo_order_get_parent(algo_order_t* order);

/**
 * check order limit
 * TODO consider move it to callback
 * @param[in] o - algo order
 */
int32_t algo_order_exceed_limit(algo_order_t*, xroad_price_t);

#ifdef __cplusplus
}
#endif
