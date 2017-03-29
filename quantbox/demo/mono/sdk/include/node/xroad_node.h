/**
 * @file   xroad_node.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include "xroad_registry.h"
#include "xroad_node_types.h"
#include <node_gen/xroad_objects.h>
#include <common/xroad_xml.h>
#include <common/xroad_string.h>
#include <stdint.h>
#include <sys/epoll.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * node main callback
 */
typedef struct
{
   void* ctx;
   /**
    * fired when new object received
    */
   void (*on_object)(void*, xroad_node_id_t, void*);
} xroad_node_callback_t;

/**
 * node epoll callback
 */
typedef struct
{
   void* ctx;
   int32_t fd;
   /**
    * fired when new epoll event received
    */
   void (*on_event)(const struct epoll_event*);
} xroad_node_epoll_callback_t;

/**
 * create new node and registers in registry
 * @param[in] node_name - name of new node. Can be NULL.
 * @param[in] callback - callback method for objects
 * @return XROAD_OK - created, XROAD_ERROR_ALREADY_EXISTS - node already created
 */
xroad_errno_t xroad_node_create(xroad_str_t node_name, xroad_node_callback_t callback);

/**
 * destroy node and free resources
 */
void xroad_node_destroy();

/**
 * reconfigure node
 * @return XROAD_ERROR_OK - reconfiguration complete successfully
 */
xroad_errno_t xroad_node_reconfig();

/**
 * return pointer to configuration
 * @return pointer to configuration
 */
xroad_xml_doc_t* xroad_node_get_cfg();

/**
 * receive and dispatch message from link
 * @param[in] timeout - wait usecs for received message
 * @return XROAD_ERROR_OK - done
 */
xroad_errno_t xroad_node_receive(int32_t timeout);

/**
 * add descriptor to epoll
 * @param[in] events - fd events
 * @param[in] cback  - pointer to epoll callback
 * @return XROAD_ERROR_OK - done
 */
xroad_errno_t xroad_node_add_epoll(uint32_t events, xroad_node_epoll_callback_t* cback);

/**
 * modify events of already added to epoll descriptor
 * @param[in] events - new fd events
 * @param[in] cback  - pointer to epoll callback
 * @return XROAD_ERROR_OK - done
 */
xroad_errno_t xroad_node_mod_epoll(uint32_t events, xroad_node_epoll_callback_t* cback);

/**
 * remove descriptor from epoll
 * @param[in] events - fd events
 * @param[in] cback - callback to remove
 * @return XROAD_ERROR_OK - done
 */
xroad_errno_t xroad_node_del_epoll(uint32_t events, xroad_node_epoll_callback_t* cback);

/**
 * return epoll file descriptor
 */
int32_t xroad_node_get_epoll_fd();

/**
 * create new object
 * @param[in] type - type of object to create
 * @return created object
 */
void* xroad_node_create_object(xroad_object_type_t type);

/**
 * destroy object. Only applicable for objects, which are created in heap
 * @param[in] object - object to destroy
 * @return XROAD_OK - destroyed, else failed
 */
xroad_errno_t xroad_node_destroy_object(void* object);

/**
 * send object directly to node
 * @param[in] obj   - object to send
 * @param[in] id    - id of destination node
 * @return XROAD_ERROR_OK - object was sent
 */
xroad_errno_t xroad_node_send_object(const void* obj, xroad_node_id_t id);

/**
 * route object
 * @param[in] obj   - object to send
 * @return XROAD_ERROR_OK - object was sent
 */
xroad_errno_t xroad_node_route_object(void* obj, ...);

/**
 * route object
 * @param[in] obj   - object to send
 * @param[in] ap    - argument list
 * @return XROAD_ERROR_OK - object was sent
 */
xroad_errno_t xroad_node_route_object_va(void* obj, va_list ap);

/**
 * get function from dll by name
 * @param[in] fname - name of function
 * @return pointer function
 */
void* xroad_node_get_fun(xroad_str_t fname);

/**
 * return object from cache
 * @param[in] type - type of object
 * @param[in] id - id of object
 * @return pointer of object of any
 */
void* xroad_node_get_object(xroad_object_type_t type, xroad_object_id_t id);

/**
 * @return node registry slot
 */
xroad_node_data_t* xroad_node_get_data();

/**
 * reset node statistic
 */
void xroad_node_reset_statistic();

/**
 * get node home dir
 * @return node home dir
 */
const xroad_path_t* xroad_node_get_home_dir();

/**
 * set node flags
 * @param[in] flags - new node flags
 */
void xroad_node_set_flags(uint32_t flags);

/**
 * return node home directory
 * @return home path
 */
const xroad_path_t* xroad_node_get_home_dir();

/**
 * return link descriptor. Can be used in epoll
 * @return link descriptor
 */
int32_t xroad_node_get_link_descriptor();

/**
 * create new cache cursor
 * @param[in] type - type of cursor
 * @return pointer to new cursor
 */
xroad_cursor_t* xroad_node_create_cursor(xroad_object_type_t type);

/**
 * destroy cursor
 * @param[in] cursor - cursor to destroy
 */
void xroad_node_destroy_cursor(xroad_cursor_t* cursor);

/**
 * return next object from cache
 * @param[in] cursor - cache cursor
 * @return object  from cache
 */
void* xroad_node_cursor_get_next(xroad_cursor_t* cursor);

/**
 * return previous object from cache
 * @param[in] cursor - cache cursor
 * @return object  from cache
 */
void* xroad_node_cursor_get_prev(xroad_cursor_t* cursor);

/**
 * return first object from cache
 * @param[in] cursor - cache cursor
 * @return object  from cache
 */
void* xroad_node_cursor_get_first(xroad_cursor_t* cursor);

/**
 * return last object from cache
 * @param[in] cursor - cache cursor
 * @return object  from cache
 */
void* xroad_node_cursor_get_last(xroad_cursor_t* cursor);

/**
 * offset cursor
 * @param[in] cursor - cache cursor
 * @param[in] offset - offset value. Can be negative for offset back
 * @return object from cache, or NULL
 */
void* xroad_node_cursor_offset(xroad_cursor_t* cursor, int64_t offset);

/**
 * shrink object cache to desired size
 * @param[in] type      - type of objects to shrink
 * @param[in] obj_count - count of objects to remain
 */
void xroad_node_shrink_cache(xroad_object_type_t type, size_t obj_count);

/**
 * return count of objects of desired type
 * @param[in] type - type of objects to count
 * @return count of objects
 */
size_t xroad_node_get_object_count(xroad_object_type_t type);

/**
 * return node version
 * @return node version
 */
const xroad_node_version_t* xroad_node_get_version();

/**
 * check if node already created
 * @return 1 - node is initialized, 0 - not yet
 */
int32_t xroad_node_is_initialized();

#ifdef __cplusplus
}
#endif
