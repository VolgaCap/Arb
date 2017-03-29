#pragma once
/**
 * @file   mdata_channel.h
 * @author Danil Krivopustov krivopustovda@gmail.com
 */

#include "mdata_engine.h"
#include <common/xroad_xml.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * create new mdata server instance
 * @param[in] cfg - mdata_channel config for connecting to mdata publisher
 * @param[in] cb - callback function
 * @return pointer to new instance, NULL - error
 */
mdata_channel_t* mdata_channel_server_create(xroad_xml_tag_t cfg, mdata_server_callback_t cb);

/**
 * create new mdata client instance
 * @param[in] cfg - mdata_channel config for connecting to mdata publisher
 * @param[in] cb - callback function
 * @return pointer to new instance, NULL - error
 */
mdata_channel_t* mdata_channel_client_create(xroad_xml_tag_t cfg, mdata_client_callback_t cb);

/**
 * connects mdata consumer to the producer
 * @param[in] mdata - pointer to the mdata instance
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
xroad_errno_t mdata_channel_start(mdata_channel_t* mdata);

/**
 * disconnects mdata consumer from the producer
 * @param[in] mdata - pointer to the mdata instance
 */
void mdata_channel_stop(mdata_channel_t* mdata);

/**
 * destroys mdata consumer
 * @param[in] mdata - pointer to the mdata instance
 */
void mdata_channel_destroy(mdata_channel_t* mdata);

/**
 * puts data to network buffer
 * @param[in] mdata - pointer to the mdata instance
 * @param[in] type - type of mdata
 * @param[in] val - pointer to data
 * @param[in] size - size of data
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
void mdata_channel_put(mdata_channel_t* mdata, mdata_proto_type_t type, void* val, size_t size);

/**
 * flushes not sendet data
 * @param[in] mdata - pointer to the mdata instance
 */
xroad_errno_t mdata_channel_flush(mdata_channel_t* mdata);

/**
 * subscribes consumer to market data of particular inst
 * @param[in] mdata - pointer to the mdata instance
 * @param[in] instr - instrument id to subscribe
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
xroad_errno_t mdata_channel_send(mdata_channel_t* mdata, mdata_proto_type_t type, void* val, size_t size);

/**
 * subscribes consumer to market data of particular instrument
 * @param[in] mdata - pointer to the mdata instance
 * @param[in] instr - instrument to subscribe
 * @param[in] mask  - subscription mask, see mdata_subscription_type_t
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
xroad_errno_t mdata_channel_subscribe(mdata_channel_t* mdata, xroad_instr_t* instr, mdata_subscription_mask_t mask, mdata_channel_callback_t cb);

/*
 * gets last mdata_book_20_t value for instrument
 * @param[in] c - pointer to the mdata_channel_t instance
 * @param[in] i - id of instrument
 * @return pointer to the mdata_book_20_t or NULL in case no value exists
 */
mdata_book_20_t* mdata_channel_get_book(mdata_channel_t* c, xroad_object_id_t s);

/*
 * gets last mdata_quote_t value for instrument
 * @param[in] c - pointer to the mdata_channel_t instance
 * @param[in] i - id of instument
 * @return pointer to the mdata_quote_t or NULL in case no value exists
 */
mdata_quote_t* mdata_channel_get_quote(mdata_channel_t* c, xroad_object_id_t s);

/*
 * gets last mdata_trade_t value for instrument
 * @param[in] c - pointer to the mdata_channel_t instance
 * @param[in] i - id of instrument
 * @return pointer to the mdata_trade_t or NULL in case no value exists
 */
mdata_trade_t* mdata_channel_get_trade(mdata_channel_t* c, xroad_object_id_t s);

/**
 * gets subscription mask
 * @param[in] mdata - pointer to the mdata instance
 * @param[in] instr - instrument to subscribe
 * @param[in] mask  - subscription mask, see mdata_subscription_type_t
 * @param[in] client - callback to the client
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
mdata_subscription_mask_t mdata_channel_get_mask(mdata_channel_t* mdata, xroad_instr_t* instr, mdata_channel_callback_t cb);

#ifdef __cplusplus
}
#endif
