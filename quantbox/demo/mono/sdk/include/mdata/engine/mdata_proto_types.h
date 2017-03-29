#pragma once
/**
 * @file   mdata_proto_types.h
 * @author Danil Krivopustov krivopustovda@gmail.com
 */

#include <common/xroad_common_types.h>
#include <common/xroad_string.h>
#include <node_gen/xroad_objects_types.h>
#pragma pack(push, 4)

typedef enum
{
   mdata_proto_type_heartbeat     = 0,
   mdata_proto_type_resolve       = 1,
   mdata_proto_type_subscribe     = 2,
   mdata_proto_type_symbol        = 3,
   mdata_proto_type_book          = 4,
   mdata_proto_type_trade         = 5,
   mdata_proto_type_subscribe_res = 6,
   mdata_proto_type_feed_state    = 7,
   mdata_proto_type_quote         = 8,
   mdata_proto_type_common_info   = 9
} mdata_proto_type_t;

typedef enum
{
   mdata_feed_state_ok           = 0,
   mdata_feed_connection_failed  = 1,
   mdata_feed_unavailable        = 2
} mdata_feed_state_type_t;

typedef enum
{
   mdata_ask_t =  1,
   mdata_bid_t =  2
} mdata_side_t;

typedef enum
{
   mdata_subscription_book       = 1,
   mdata_subscription_trade      = 2,
   mdata_subscription_quote      = 4,
   mdata_subscription_common     = 8,
   mdata_subscription_snapshot   = 16,
   mdata_subscription_updates    = 32
} mdata_subscription_type_t;

typedef struct mdata_book_level_s
{
   xroad_price_t price;
   xroad_qty_t   qty;
} mdata_book_level_t;

typedef uint32_t mdata_subscription_mask_t;

typedef struct mdata_subscribe_s
{
   xroad_object_id_t          instr_id;
   mdata_subscription_mask_t  mask;
} mdata_subscribe_t;

typedef struct mdata_resolve_s
{
   char alias[xroad_str_fixed_size((xroad_alias_t*)0) + 1];
} mdata_resolve_t;

typedef struct mdata_book_20_s
{
   xroad_object_id_t    instr_id;
   mdata_book_level_t   asks[20];
   mdata_book_level_t   bids[20];
   xroad_timestamp_t    exch_ts;
   xroad_timestamp_t    ts;
   //xroad_timestamp_t    rcv_ts;
} mdata_book_20_t;

typedef struct mdata_quote_s
{
   xroad_object_id_t    instr_id;
   mdata_book_level_t   ask;
   mdata_book_level_t   bid;
   xroad_timestamp_t    exch_ts;
   xroad_timestamp_t    ts;
   uint32_t             flag;
   //xroad_timestamp_t    rcv_ts;
} mdata_quote_t;

typedef struct mdata_symbol_s
{
   xroad_object_id_t instr_id;
   char              alias[xroad_str_fixed_size((xroad_alias_t*)0) + 1];
} mdata_symbol_t;

typedef struct mdata_trade_s
{
   xroad_object_id_t instr_id;
   xroad_price_t     price;
   xroad_qty_t       qty;
   xroad_side_t      side;
   xroad_timestamp_t exch_ts;
   xroad_timestamp_t ts;
   //xroad_timestamp_t rcv_ts;
} mdata_trade_t;

typedef struct mdata_subscribe_result_s
{
   xroad_object_id_t          instr_id;
   xroad_errno_t              error_num;
   mdata_subscription_mask_t  mask;
} mdata_subscribe_result_t;

typedef struct mdata_feed_state_s
{
   mdata_subscription_mask_t mask;
   mdata_feed_state_type_t   state;
   xroad_object_id_t         instr_id;
} mdata_feed_state_t;

typedef enum
{
   mdata_oi_t  =  1,
   mdata_min_t =  2,
   mdata_max_t =  4,
   mdata_open_t = 8,
   mdata_high_t = 16,
   mdata_low_t  = 32,
   mdata_last_t = 64,
   mdata_volume_t = 128
} mdata_stat_flag_t;

typedef struct mdata_common_info_s
{
   xroad_object_id_t instr_id;
   int32_t           flag;
   xroad_price_t     oi;
   xroad_price_t     min;
   xroad_price_t     max;
   xroad_price_t     open;
   xroad_price_t     close;
   xroad_price_t     high;
   xroad_price_t     low;
   xroad_price_t     last;
   xroad_price_t     volume;
   xroad_timestamp_t ts;
   xroad_timestamp_t exch_ts;
} mdata_common_info_t;

#pragma pack(pop)
