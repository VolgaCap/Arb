#pragma once
/**
 * @file   mdata_engine.h
 * @author Danil Krivopustov krivopustovda@gmail.com
 */
#include "mdata_proto.h"

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct mdata_channel_s mdata_channel_t;

typedef struct
{
   void* ctx;
   /**
    * fired, when resolve request has been received
    */
   void (*on_resolve)(mdata_resolve_t*, void*);
   /**
    * fired, when subscribe request has been received
    */
   void (*on_subscribe)(mdata_subscribe_t*, void*);
   /**
    * fired, when client has established connection
    */
   void (*on_connected)(void*);
   /**
    * fired, when client has closed connection
    */
   void (*on_disconnected)(void*);
} mdata_server_callback_t;

typedef struct
{
   void* ctx;
   /**
    * fired, when resolved symbol has been arrived
    */
   void (*on_symbol)(mdata_symbol_t*, void*);
   /**
    * fired, when subscibe result has been arrived
    */
   void (*on_subscribe_result)(mdata_subscribe_result_t*, void*);
   /**
    * fired, when  feed state as been changed
    */
   void (*on_feed_state)(mdata_feed_state_t*, void*);
   /**
    * fired, when connection has been established
    */
   void (*on_connected)(void*);
   /**
    * fired, when connection has been closed
    */
   void (*on_disconnected)(void*);
} mdata_client_callback_t;

typedef struct mdata_engine_s mdata_engine_t;

/**
 * create new mdata client-server instance
 * @param[in] cfg - mdata_engine config
 * @param[in] scb - server callback function
 * @param[in] ccb - client callback function
 * @return pointer to new instance, NULL - error
 */
mdata_engine_t* mdata_engine_create(xroad_xml_tag_t cfg, mdata_server_callback_t scb, mdata_client_callback_t ccb);

/**
 * create new mdata client instance
 * @param[in] cfg - mdata_engine config
 * @param[in] cb - callback function
 * @return pointer to new instance, NULL - error
 */
mdata_engine_t* mdata_engine_client_create(xroad_xml_tag_t cfg, mdata_client_callback_t cb);

/**
 * create new mdata server instance
 * @param[in] cfg - mdata_engine config for connecting to mdata provider
 * @param[in] cb - callback function
 * @return pointer to new instance, NULL - error
 */
mdata_engine_t* mdata_engine_server_create(xroad_xml_tag_t cfg, mdata_server_callback_t cb);

/**
 * connects mdata consumer to the producer
 * @param[in] mdata - pointer to the mdata instance
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
xroad_errno_t mdata_engine_start(mdata_engine_t* mdata);

/**
 * disconnects mdata consumer from the producer
 * @param[in] mdata - pointer to the mdata instance
 */
void mdata_engine_stop(mdata_engine_t* mdata);

/**
 * destroys mdata consumer
 * @param[in] mdata - pointer to the mdata instance. If NULL, nothing happened
 */
void mdata_engine_destroy(mdata_engine_t* mdata);

/**
 * prepares to publish data in connection
 * @param[in] mdata - pointer to the mdata instance
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
xroad_errno_t mdata_engine_put(mdata_engine_t* mdata, mdata_proto_type_t type, void* val, size_t size);

/**
 * publish data in connection
 * @param[in] mdata - pointer to the mdata instance
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
xroad_errno_t mdata_engine_flush(mdata_engine_t* mdata);
/**
 * publish data in connection
 * @param[in] mdata - pointer to the mdata instance
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
xroad_errno_t mdata_engine_send(mdata_engine_t* mdata, mdata_proto_type_t type, void* val);

/**
 * sends resolve request for symbol by its alias
 * @param[in] mdata - pointer to the mdata instance
 * @param[in] alias - alias of the instrument
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
xroad_errno_t mdata_engine_resolve(mdata_engine_t* mdata, xroad_alias_t alias);

/**
 * subscribes consumer to market data of particular instrument
 * @param[in] mdata     - pointer to the mdata instance
 * @param[in] instr     - instrument to subscribe
 * @param[in] mask      - subscription mask, see mdata_subscription_type_t
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
xroad_errno_t mdata_engine_subscribe(mdata_engine_t* mdata, xroad_instr_t* instr, mdata_subscription_mask_t mask, mdata_channel_callback_t cb);

/**
 * gets subscription mask
 * @param[in] mdata - pointer to the mdata instance
 * @param[in] instr - instrument to subscribe
 * @param[in] mask  - subscription mask, see mdata_subscription_type_t
 * @param[in] client - callback to the client
 * @return XROAD_OK if succesed otherwise XROAD_FAILED
 */
mdata_subscription_mask_t mdata_engine_get_mask(mdata_engine_t* mdata, xroad_instr_t* instr, mdata_channel_callback_t cb);

/*
 * gets last mdata_book_20_t value for instrument
 * @param[in] c - pointer to the mdata_engine_t instance
 * @param[in] i - id of instrument
 * @return pointer to the mdata_book_20_t or NULL in case no value exists
 */
mdata_book_20_t* mdata_engine_get_book(mdata_engine_t* c, xroad_object_id_t s);

/*
 * gets last mdata_quote_t value for instrument
 * @param[in] c - pointer to the mdata_engine_t instance
 * @param[in] i - id of instument
 * @return pointer to the mdata_quote_t or NULL in case no value exists
 */
mdata_quote_t* mdata_engine_get_quote(mdata_engine_t* c, xroad_object_id_t s);

/*
 * gets last mdata_trade_t value for instrument
 * @param[in] c - pointer to the mdata_engine_t instance
 * @param[in] i - id of instrument
 * @return pointer to the mdata_trade_t or NULL in case no value exists
 */
mdata_trade_t* mdata_engine_get_trade(mdata_engine_t* c, xroad_object_id_t s);

#ifdef __cplusplus
}
#endif
