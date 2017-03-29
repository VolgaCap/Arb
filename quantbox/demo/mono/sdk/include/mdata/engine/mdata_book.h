#pragma once
/**
 * @file   mdata_book.h
 * @author Danil Krivopustov krivopustovda@gmail.com
 */

#include <node_gen/xroad_objects.h>
#include <stdbool.h>

#include "mdata_proto_types.h"

typedef struct mdata_book_s mdata_book_t;

typedef enum
{
   book_order_add    = 1,
   book_order_update = 2,
   book_order_delete = 3,
   book_add          = 4,
   book_update       = 5,
   book_delete       = 6
} mdata_book_action_t;


#ifdef __cplusplus
extern "C"
{
#endif
/**
 * creates book with dynamic qty of levels
 * @param[in] instr - book instrument
 * returns pointer to book
 */
mdata_book_t* mdata_book_create(xroad_instr_t* instr);

/**
 * destroys book
 * @param[in] book - pointer to book
 */
void mdata_book_destroy(mdata_book_t* book);

/**
 * removes all book entries
 * @param[in] book - pointer to book
 */
void mdata_book_clear(mdata_book_t* book);

/**
 * updates book with new data, sorts levels
 * @param[in] book  - pointer to book
 * @param[in] action  - update action
 * @param[in] price - the price
 * @param[in] qty   - the quantity
 * @param[in] side  - side[buy=1, sell=2]
 * @return 1 - if best bid or best aks have changed, otherwise 0
 */
int32_t mdata_book_update(mdata_book_t* book, mdata_book_action_t action, xroad_price_t price, xroad_qty_t qty, xroad_side_t side, xroad_timestamp_t ts);

/**
 * updates book with new data, sorts levels
 * @param[in] book  - pointer to book
 * @param[in] action  - update action
 * @param[in] order_id  - id of order
 * @param[in] price - the price
 * @param[in] qty   - the quantity
 * @param[in] side  - side[buy=1, sell=2]
 * @return 1 - if best bid or best aks have changed, otherwise 0
 */
int32_t mdata_book_order_update(mdata_book_t* book, mdata_book_action_t action, int64_t order_id, xroad_price_t price, xroad_qty_t qty, xroad_side_t side, xroad_timestamp_t ts);

/**
 * gets instrument of the book
 * @param[in] book - pointer to book
 * @return instument of the book
 */
xroad_instr_t*  mdata_book_get_instr(mdata_book_t* book);

/**
 * returns true if best bid >= best ask
 * @param[in] book - pointer to book
 */
bool mdata_book_is_crossed(mdata_book_t* book);

/**
 * returns true if book is empty
 * @param[in] book - pointer to book
 */
bool mdata_book_is_empty(mdata_book_t* book);

/**
 * map entry free function
 */
typedef void (*book_level_func_t)(int32_t, xroad_side_t, xroad_price_t, xroad_qty_t, void*);

/**
 * returns true if best bid >= best ask
 * @param[in] book - pointer to book
 */
void mdata_book_get_levels(mdata_book_t* book, xroad_side_t side, int32_t num, book_level_func_t cback, void* ctx);

/**
 * prints book in log with debug log levels
 * @param[in] book - pointer to book
 */
void mdata_book_print(mdata_book_t* book);

/**
 * converts mdata_book_t to mdata_quote_t
 * @param[out] book - quote pointer to mdata_quote_t
 * @param[in] book  - pointer to mdata_book_t
 */
void mdata_quote_update_book(mdata_quote_t* quote, mdata_book_t* book);

/**
 * converts @see mdata_book_t to @see mdata_book_20_t
 * @param[out] book  - pointer to mdata_book_20_t
 * @param[in] book   - pointer to mdata_book_t
 */
void mdata_book_20_update_book(mdata_book_20_t* book_20, mdata_book_t* book);

#ifdef __cplusplus
}
#endif
