#pragma once
/**
 * @file   mdata_proto.h
 * @author Danil Krivopustov krivopustovda@gmail.com
 */

#include <net/xroad_sock_fwd.h>
#include <node/xroad_node_types.h>
#include <node_gen/xroad_objects.h>

#include "mdata_proto_types.h"
#include "mdata_book.h"

#ifdef __cplusplus
extern "C"
{
#endif

#define BOOK_INITIAL_SIZE 10000
/**
 * callback structure for market data
 */
typedef struct
{
   void* ctx;
   /**
    * fired, when new market data arrived
    */
   void (*on_mdata)(mdata_proto_type_t, void*, void*);
   /**
    * fired, when resolved symbol has been arrived
    */
   void (*on_symbol)(mdata_symbol_t*, void*);
   /**
    * fired, when resolve request has been received
    */
   void (*on_resolve)(mdata_resolve_t*, void*);
   /**
    * fired, when subscribe request has been received
    */
   void (*on_subscribe)(mdata_subscribe_t*, void*);
   /**
    * fired, when subscibe result has been arrived
    */
   void (*on_subscribe_result)(mdata_subscribe_result_t*, void*);
   /**
    * fired, when  feed state as been changed
    */
   void (*on_feed_state)(mdata_feed_state_t*, void*);
   /**
    * fired, when heartbeat received
    */
   void (*on_heartbeat)(void*);
} mdata_proto_callback_t;

typedef struct
{
   void* ctx;
   /**
    * fired, when market data arrived
    * @param[in] - type of mdata
    * @param[in] - pointer to mdata
    * @param[in] - context
    */
   void (*on_mdata)(mdata_proto_type_t, void*, void*);
} mdata_channel_callback_t;

/**
 * updates book with new data, sorts levels
 * @param[in] book  - pointer to book
 * @param[in] price - the price
 * @param[in] qty   - the quantity
 * @param[in] side  - side[buy=1, sell=2]
 * @return 1 - if best bid or best aks have changed, otherwise 0
 */
int32_t mdata_book_20_update(mdata_book_20_t* book, xroad_price_t price, xroad_qty_t qty, xroad_side_t side);

/**
 * prints book in log with debug log levels
 * @param[in] book - pointer to book
 */
void mdata_book_20_print(mdata_book_20_t* book);

/**
 * removes all book entries
 * @param[in] pointer to book
 */
void mdata_book_20_clear(mdata_book_20_t* book);

/**
 * parses buffer and calls apropriate callback
 * @param[in] buf - pointer to net buffer
 * @param[in] cb  - pointer to the mdata callback
 * @return count of processed bytes
 */
size_t mdata_proto_parse(const xroad_net_buf_t* buf, mdata_proto_callback_t* cb, uint64_t* seq_num, uint64_t* cnt);

/**
 * clears quote value
 */
void mdata_quote_clear(mdata_quote_t* q);

/**
 * converts mdata_book_20_t to mdata_quote_t
 * @param[out] book - quote pointer to mdata_quote_t
 * @param[in]  book - pointer to mdata_book_20_t
 */
void mdata_quote_update(mdata_quote_t* quote, mdata_book_20_t* book);

/**
 * gets size of mdata type
 * @param[in] type - type of mdata
 * @return size of mdata
 */
size_t mdata_type_get_size(mdata_proto_type_t type);

#ifdef __cplusplus
}
#endif
