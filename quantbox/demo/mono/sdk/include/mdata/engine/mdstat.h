#pragma once
/**
 * @file   mdata_quote.h
 * @author Danil Krivopustov danilk@quantbox.ru
 */

#include <stdbool.h>
#include <node_gen/xroad_objects.h>
#include "mdata_proto_types.h"

#ifdef __cplusplus
extern "C"
{
#endif
/* *
 * stores mdata_quote to mdstat to file cache
 * @param mdata_quote_t [in] - quote to store
 * */
void mdstat_set_last_quote(mdata_quote_t q);

/**
 * gets mdata_quote_t from cache
 * @param i[in] - instrument for which quote should be return
 * @return last mdata_quote for instrument
 */
mdata_quote_t mdstat_get_last_quote(xroad_object_id_t id);

/* *
 * checks if we have last quote
 * @param i[in] - instrument for which quote should be return
 * */
bool mdstat_has_last_quote(xroad_object_id_t id);

/* *
 * stores mdata_trade to mdstat to file cache
 * @param mdata_trade_t [in] - trade to store
 * */
void mdstat_set_last_trade(mdata_trade_t t);

/**
 * gets mdata_trade_t from cache
 * @param i[in] - instrument for which trade should be return
 * @return last mdata_trade for instrument
 */
mdata_trade_t mdstat_get_last_trade(xroad_object_id_t id);

/* *
 * checks if we have last trade
 * @param i[in] - instrument for which trade should be return
 * */
bool mdstat_has_last_trade(xroad_object_id_t id);
#ifdef __cplusplus
}
#endif
