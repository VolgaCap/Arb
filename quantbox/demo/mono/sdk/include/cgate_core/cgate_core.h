/**
 * @file   cgate_core.h
 * @author Dmitry S. Melnikov, dmitryme@quantbox.ru
 */

#pragma once

#include <common/xroad_xml.h>
#include <node_gen/xroad_objects.h>
#include <mdata/engine/mdata_proto.h>
#include <order/order.h>

typedef struct cgate_core_s cgate_core_t;
typedef struct cgate_book_s cgate_book_t;

typedef struct
{
   void* ctx;
   void (*on_connected)(cgate_core_t*, void* ctx);
   void (*on_disconnected)(cgate_core_t*, void* ctx);
   void (*on_quote)(cgate_core_t*, const mdata_quote_t*, void* ctx);
   void (*on_book)(cgate_core_t*, const mdata_book_20_t*, void* ctx);
   void (*on_trade)(cgate_core_t*, const mdata_trade_t*, void* ctx);
} cgate_core_callback_t;

cgate_core_t* cgate_core_create(xroad_xml_tag_t cfg, cgate_core_callback_t cback);

void cgate_core_destroy(cgate_core_t* core);

xroad_errno_t cgate_core_start(cgate_core_t* core);

void cgate_core_stop(cgate_core_t* core);

void cgate_core_receive(cgate_core_t* core, uint64_t timeout);

void cgate_core_enqueue(cgate_core_t* core, cgate_book_t* book);

void cgate_core_flush(cgate_core_t* core);

xroad_errno_t cgate_core_subscribe(cgate_core_t* core, xroad_instr_t* instr, mdata_subscription_mask_t mask);

order_t* cgate_core_create_order(
      cgate_core_t*    core,
      xroad_str_t      name,
      order_callback_t callback,
      xroad_instr_t*   instr,
      xroad_str_t      account,
      xroad_str_t      client_code,
      xroad_str_t      broker_code,
      xroad_side_t     side,
      xroad_qty_t      qty,
      xroad_price_t    price,
      xroad_str_t      ext_ref,
      void*            ctx,
      xroad_str_t*     err);
