/**
 * @file   process.c
 * @author Dmitry S. Melnikov, dmitryme@quantbox.ru
 */

#include "process.h"
#include "cgate_core/cgate_core.h"
#include <logger/xroad_logger.h>
#include <node/xroad_node.h>
#include <common/xroad_string.h>
#include <instrdb/instrdb.h>
#include <ui/lib/ui.h>
#include <mdata/engine/mdata_proto_types.h>
#include <order/order_aux.h>

#define change_pstate(p, new_state)                                                        \
{                                                                                          \
   xroad_log_debug("process state changed: %P->%P",                                        \
         process_state_to_str(p->state), process_state_to_str(process_state_##new_state)); \
   p->state = process_state_##new_state;                                                   \
}

typedef enum
{
   process_state_awaiting_start     = 0,
   process_state_started            = 1,
   process_state_awaiting_stop      = 2,
   process_state_stopped            = 3,
   process_state_awaiting_inactive  = 4,
   process_state_inactive           = 5,
   process_state_awaiting_shutdown  = 6,
   process_state_shutdown_ready     = 7
} process_state_t;

struct process_s
{
   uint32_t             wait_timeout;
   process_state_t      state;
   ui_t*                ui;
   instrdb_t*           idb;
   cgate_core_t*        cgate_core;
   order_t*             order;
   xroad_instr_t*       quote_instr;
   xroad_instr_t*       order_instr;
   xroad_account_t      account;
   xroad_account_t      broker_code;
   xroad_client_code_t  client_code;
   xroad_qty_t          size;
   xroad_price_t        price;
   xroad_side_t         side;
   xroad_int32_t        price_offset;
   xroad_price_t        denominator;
   xroad_price_t        last_prc;
   xroad_str_t          prefix;
};

//--------------------------------------------------------------------------------------------------------------------//
xroad_str_t process_state_to_str(process_state_t st)
{
   switch(st)
   {
      case process_state_awaiting_start:     return xroad_str("awaiting_start");
      case process_state_started:            return xroad_str("started");
      case process_state_awaiting_stop:      return xroad_str("awaiting_stop");
      case process_state_stopped:            return xroad_str("stopped");
      case process_state_awaiting_inactive:  return xroad_str("awaiting_inactive");
      case process_state_inactive:           return xroad_str("inactive");
      case process_state_awaiting_shutdown:  return xroad_str("awaiting_shutdown");
      case process_state_shutdown_ready:     return xroad_str("shutdown_ready");
      default:                               return xroad_str("unknown");
   }
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_order_activated(order_t* order)
{
   xroad_log_debug("order %P activated", order_get_name(order));
   order_cancel(order);
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_order_canceled(order_t* order)
{
   xroad_log_debug("order %P canceled", order_get_name(order));
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_order_rejected(order_t* order, xroad_rej_reason_t reason, xroad_str_t text)
{
   xroad_log_error("order %P rejected. error = %P", order_get_name(order), text);
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_order_destroyed(order_t* order)
{
   xroad_log_debug("order %P destroyed", order_get_name(order));
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_core_connected(cgate_core_t* core, void* ctx)
{
   process_t* process = (process_t*)ctx;
   xroad_node_get_data()->status = xroad_node_status_inactive;
   xroad_log_info("cgate core connected");
   if (process->order)
   {
      order_destroy(process->order, 1);
   }
   process->order = cgate_core_create_order(
         process->cgate_core,
         xroad_str("order1"),
         (order_callback_t){
            .on_activated = on_order_activated,
            .on_rejected = on_order_rejected,
            .on_canceled = on_order_canceled,
            .on_destroyed = on_order_destroyed},
         process->order_instr,
         xroad_str_from_fixed(&process->account),
         xroad_str_from_fixed(&process->broker_code),
         xroad_str_from_fixed(&process->client_code),
         process->side,
         process->size,
         0,
         xroad_str_null,
         process,
         NULL);
   if (!process->order)
   {
      xroad_log_error("unable to create order");
   }
   else
   {
      change_pstate(process, started);
   }
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_core_disconnected(cgate_core_t* core, void* ctx)
{
   process_t* process = (process_t*)ctx;
   if (process->state == process_state_awaiting_inactive)
   {
      change_pstate(process, inactive);
      xroad_node_get_data()->status = xroad_node_status_inactive;
   }
   else
   {
      change_pstate(process, stopped);
      xroad_node_get_data()->status = xroad_node_status_offline;
   }
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_quote_updated(const mdata_quote_t* quote, void* ctx)
{
   if (xroad_node_get_data()->status != xroad_node_status_active)
   {
      return;
   }
   process_t* p = (process_t*)ctx;
   xroad_log_info("quote changed. bid = %D@%f, ask = %D@%f",
         quote->bid.qty, quote->bid.price, quote->ask.qty, quote->ask.price);
   int32_t fire = 0;
   const mdata_book_level_t* level =  p->side == xroad_side_buy ? &quote->bid : &quote->ask;
   fire = level->qty > 0 && fabs(remainder(level->price, p->denominator)) <= XROAD_EPSILON;
   xroad_log_debug("FIRE = %d, denom = %f, price = %f, qty = %D", fire, p->denominator, level->price, level->qty);
   if (!xroad_dbl_cmp(p->last_prc, level->price))
   {
       xroad_log_debug("price %f is the same as previous one. skipped", level->price);
       fire = 0;
   }
   if (!xroad_dbl_cmp(p->price, 0.0))
   {
      xroad_log_debug("not order price");
      return;
   }
   if (fire)
   {
      if (order_is_done(p->order) || order_get_state(p->order) == order_state_initial)
      {
         p->last_prc = level->price;
         xroad_ext_ref_t ext_ref;
         ext_ref.len = xroad_format(ext_ref.data, xroad_str_fixed_size(&ext_ref),
               "%P_%fX%D", p->prefix, level->price, level->qty);
         xroad_log_debug("ext_ref = %S", &ext_ref);
         xroad_price_t price = p->price + ((p->side == xroad_side_buy) ? -p->price_offset : p->price_offset);
         order_replace(p->order, 0, price, xroad_str_from_fixed(&ext_ref), order_replace_ext_ref | order_replace_price);
         order_send(p->order);
      }
   }
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_order_updated(const mdata_quote_t* quote, void* ctx)
{
   process_t* process = (process_t*)ctx;
   if (process->side == xroad_side_buy)
   {
      if (quote->bid.qty > 0)
      {
         process->price = quote->bid.price;
      }
   }
   else
   {
      if (quote->ask.qty > 0)
      {
         process->price = quote->ask.price;
      }
   }
   xroad_log_info("order new base price is %f", process->price);
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_trade_updated(const mdata_trade_t* trade, void* ctx)
{
   if (xroad_node_get_data()->status != xroad_node_status_active)
   {
      return;
   }
   process_t* p = (process_t*)ctx;
   xroad_log_info("trade received %D@%f", trade->qty, trade->price);
   int32_t fire = 0;
   fire = trade->qty > 0 && fabs(remainder(trade->price, p->denominator)) <= XROAD_EPSILON;
   xroad_log_debug("FIRE = %d, denom = %f, price = %f, qty = %D", fire, p->denominator, trade->price, trade->qty);
   if (!xroad_dbl_cmp(p->last_prc, trade->price))
   {
       xroad_log_debug("price %f is the same as previous one. skipped", trade->price);
       fire = 0;
   }
   if (!xroad_dbl_cmp(p->price, 0.0))
   {
      xroad_log_debug("not order price");
      return;
   }
   if (fire)
   {
      if (order_is_done(p->order) || order_get_state(p->order) == order_state_initial)
      {
         p->last_prc = trade->price;
         xroad_ext_ref_t ext_ref;
         ext_ref.len = xroad_format(ext_ref.data, xroad_str_fixed_size(&ext_ref),
               "%P_%fX%D", p->prefix, trade->price, trade->qty);
         xroad_log_debug("ext_ref = %S", &ext_ref);
         xroad_price_t price = p->price + ((p->side == xroad_side_buy) ? -p->price_offset : p->price_offset);
         order_replace(p->order, 0, price, xroad_str_from_fixed(&ext_ref), order_replace_ext_ref | order_replace_price);
         order_send(p->order);
      }
   }
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_trade_order_updated(const mdata_trade_t* trade, void* ctx)
{
   process_t* process = (process_t*)ctx;
   if (trade->qty > 0)
   {
      process->price = trade->price;
   }
   xroad_log_info("order new base price is %f", process->price);
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_quote(cgate_core_t* core, const mdata_quote_t* quote, void* ctx)
{
   process_t* process = (process_t*)ctx;
   if (quote->instr_id == xroad_instr_get_id(process->quote_instr))
   {
      on_quote_updated(quote, ctx);
   }
   if (quote->instr_id == xroad_instr_get_id(process->order_instr))
   {
      on_order_updated(quote, ctx);
   }
}

//--------------------------------------------------------------------------------------------------------------------//
static void on_trade(cgate_core_t* core, const mdata_trade_t* trade, void* ctx)
{
   process_t* process = (process_t*)ctx;
   if (trade->instr_id == xroad_instr_get_id(process->quote_instr))
   {
      on_trade_updated(trade, ctx);
   }
   if (trade->instr_id == xroad_instr_get_id(process->order_instr))
   {
      on_trade_order_updated(trade, ctx);
   }
}

//--------------------------------------------------------------------------------------------------------------------//
static xroad_errno_t reconfig(process_t* process)
{
   xroad_xml_doc_t* doc = xroad_node_get_cfg();
   xroad_xml_tag_t root = xroad_xml_get_root(doc);
   xroad_xml_tag_t tag = xroad_xml_get_tag(root, xroad_str("node"));
   process->wait_timeout = xroad_xml_get_attr_i(tag, xroad_str("wait_timeout_ms"));
   xroad_str_t alias = ui_get_str(process->ui, 0, xroad_str("quote_instr"));
   xroad_instr_t* i = instrdb_get_by_alias(process->idb, alias);
   if (!i)
   {
      xroad_log_warn("quote_instr %P is not set or found", alias);
   }
   else
   {
      xroad_log_info("quote_instr %S has been found by id %d", xroad_instr_get_alias(i), xroad_instr_get_id(i));
   }
   if (i != process->quote_instr)
   {
      cgate_core_subscribe(process->cgate_core, i, mdata_subscription_trade);
      process->quote_instr = i;
   }
   alias = ui_get_str(process->ui, 0, xroad_str("order_instr"));
   i = instrdb_get_by_alias(process->idb, alias);
   if (!i)
   {
      xroad_log_warn("order_instr %P is not set or found", alias);
   }
   else
   {
      xroad_log_info("order_instr %S has been found by id %d", xroad_instr_get_alias(i), xroad_instr_get_id(i));
   }
   if (i != process->order_instr)
   {
      cgate_core_subscribe(process->cgate_core, i, mdata_subscription_quote);
      process->order_instr = i;
   }
   return XROAD_OK;
}

//--------------------------------------------------------------------------------------------------------------------//
process_t* process_create(int32_t argc, char* argv[])
{
   process_t* process = calloc(1, sizeof(process_t));
   process->state = process_state_stopped;
   xroad_xml_doc_t* doc = xroad_node_get_cfg();
   xroad_xml_tag_t root = xroad_xml_get_root(doc);
   process->ui = ui_create(xroad_xml_get_tag(root, xroad_str("ui")));
   if (!process->ui)
   {
      goto error;
   }
   xroad_str_t tmp = ui_get_str(process->ui, 0, xroad_str("account"));
   xroad_str_fixed_set(&process->account, tmp);
   tmp = ui_get_str(process->ui, 0, xroad_str("broker_code"));
   xroad_str_fixed_set(&process->broker_code, tmp);
   process->size = ui_get_int32(process->ui, 0, xroad_str("order_size"));
   process->side = xroad_side_from_str(ui_get_str(process->ui, 0, xroad_str("order_side")));
   process->price_offset = ui_get_int32(process->ui, 0, xroad_str("order_price_offset"));
   process->denominator = ui_get_double(process->ui, 0, xroad_str("quote_price_denominator"));
   process->prefix = ui_get_str(process->ui, 0, xroad_str("prefix"));
   process->idb = instrdb_create(xroad_xml_get_tag(root, xroad_str("node")));
   if (!process->idb)
   {
      goto error;
   }
   process->cgate_core = cgate_core_create(
         xroad_xml_get_tag(root, xroad_str("cgate_engine")),
         (cgate_core_callback_t){process, on_core_connected, on_core_disconnected, NULL, NULL, on_trade});
   if (!process->cgate_core)
   {
      goto error;
   }
   if (XROAD_OK != reconfig(process))
   {
      goto error;
   }
   return process;
error:
   if (process)
   {
      process_destroy(process);
   }
   return NULL;
}
//--------------------------------------------------------------------------------------------------------------------//
void process_destroy(process_t* process)
{
   ui_destroy(process->ui);
   instrdb_destroy(process->idb);
   free(process);
}

//--------------------------------------------------------------------------------------------------------------------//
xroad_errno_t process_reconfig(process_t* process)
{
   return reconfig(process);
}

//--------------------------------------------------------------------------------------------------------------------//
void process_start(process_t* process)
{
   switch(process->state)
   {
      case process_state_stopped:
      {
         cgate_core_start(process->cgate_core);
         change_pstate(process, awaiting_start);
         break;
      }
      default:
      {
         break;
      }
   }
}

//--------------------------------------------------------------------------------------------------------------------//
void process_stop(process_t* process)
{
   switch(process->state)
   {
      case process_state_awaiting_start:
      case process_state_started:
      {
         change_pstate(process, awaiting_stop);
         cgate_core_stop(process->cgate_core);
         break;
      }
      case process_state_awaiting_stop:
      case process_state_stopped:
      case process_state_awaiting_shutdown:
      case process_state_shutdown_ready:
      {
         break;
      }
      case process_state_inactive:
      {
         change_pstate(process, stopped);
         xroad_node_get_data()->status = xroad_node_status_offline;
         break;
      }
      case process_state_awaiting_inactive:
      {
         change_pstate(process, awaiting_stop);
      }
   }
}

//--------------------------------------------------------------------------------------------------------------------//
void process_shutdown(process_t* process)
{
   process_stop(process);
   switch(process->state)
   {
      case process_state_stopped:
      {
         change_pstate(process, shutdown_ready);
         break;
      }
      case process_state_awaiting_stop:
      {
         change_pstate(process, awaiting_shutdown);
         break;
      }
      default:
      {
         break;
      }
   }
}

//--------------------------------------------------------------------------------------------------------------------//
void process_activate(process_t* process)
{
   xroad_node_get_data()->status = xroad_node_status_active;
}

//--------------------------------------------------------------------------------------------------------------------//
void process_deactivate(process_t* process)
{
   xroad_node_get_data()->status = xroad_node_status_inactive;
}

//--------------------------------------------------------------------------------------------------------------------//
void process_reset(process_t* process, xroad_int32_t hint)
{
   if (hint & xroad_reset_hint_statistic)
   {
      xroad_node_reset_statistic();
   }
}

//--------------------------------------------------------------------------------------------------------------------//
void process_on_node_object(process_t* process, void* obj, const xroad_node_id_t from)
{
   xroad_log_debug("%O received from %u node", obj, from);
   switch(xroad_object_get_type(obj))
   {
      case xroad_object_type_field:
      {
         reconfig(process);
         break;
      }
      default:
      {
         break;
      }
   }
}

//--------------------------------------------------------------------------------------------------------------------//
int32_t process_do(process_t* process)
{
   if (process->state <= process_state_started)
   {
      cgate_core_receive(process->cgate_core, process->wait_timeout);
      xroad_node_receive(0);
   }
   else
   {
      xroad_node_receive(process->wait_timeout);
   }
   if (process->state == process_state_shutdown_ready)
   {
      return 0;
   }
   return 1;
}
