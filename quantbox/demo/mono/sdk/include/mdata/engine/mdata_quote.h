#pragma once
/**
 * @file   mdata_quote.h
 * @author Danil Krivopustov danilk@quantbox.ru
 */

#include <node_gen/xroad_objects.h>
#include "mdata_proto_types.h"

/* *
 * stores mdata_quote to mdstat to file cache
 * @param mdata_quote_t [in] - quote to store
 * */
void mdata_quote_set_last(mdata_quote_t q);

/**
 * gets mdata_quote_t from cache
 * @param i[in] - instrument for which quote should be return
 * @return last mdata_quote for instrument
 */
mdata_quote_t mdata_quote_get_last(xroad_instr_t* i);
