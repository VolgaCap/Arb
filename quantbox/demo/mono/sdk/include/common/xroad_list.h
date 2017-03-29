/**
 * @file   xroad_list.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include "xroad_common_fwd.h"
#include "xroad_common_types.h"
#include <stdint.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * list entry free function
 */
typedef void (*xroad_list_free_func_t)(void*, uint32_t);

/**
 * list entries compare function
 */
typedef int32_t (*xroad_list_cmp_func_t)(const void*, const void*);

/**
 * create new list container
 * @return list object
 */
xroad_list_t* xroad_list_create();

/**
 * clear list container
 * @param[in] list      - list to clear
 * @param[in] free_func - function for free list entries data, NULL - no free performed
 * */
void xroad_list_clear(xroad_list_t* list, xroad_list_free_func_t free_func);

/**
 * destroy list container
 * @param[in] list      - container to destroy. If NULL, nothing happened
 * @param[in] free_func - function for free list entries data, NULL - no free performed
 * */
void xroad_list_destroy(xroad_list_t* list, xroad_list_free_func_t free_func);

/**
 * return list size
 * @param[in] list - pointer to list container
 */
uint32_t xroad_list_get_size(xroad_list_t* list);

/**
 * insert value at the end of list
 * @param[in] list - pointer to list container
 * @param[in] val - pointer to inserted value
 * @param[in] size - size of inserted value
 * @return pointer to created entry
 */
#define xroad_list_push_back(list, val, size) \
   xroad_list_insert(list, xroad_list_get_last(list), val, size)

/**
 * insert value at the top of list
 * @param[in] list - pointer to list container
 * @param[in] val - pointer to inserted value
 * @param[in] size - size of inserted value
 * @return pointer to created entry
 */
#define xroad_list_push_front(list, val, size) \
   xroad_list_insert(list, NULL, val, size)

/**
 * insert value into list at specified position
 * @param[in] list - pointer to list container
 * @param[in] entry - new value will be inserted right after this entry
 * @param[in] val - pointer to inserted value
 * @param[in] size - size of inserted value
 * @return pointer to created entry
 */
xroad_list_entry_t* xroad_list_insert(xroad_list_t* list, xroad_list_entry_t* entry, void* val, uint32_t size);

/**
 * delete entry from list
 * @param[in] list      - pointer to list container
 * @param[in] entry     - entry to delete
 * @param[in] free_func - function for free list entries data, NULL - no free performed
 * @return next entry
 */
xroad_list_entry_t* xroad_list_delete(xroad_list_t* list, xroad_list_entry_t* entry, xroad_list_free_func_t free_func);

/**
 * return first entry of list
 * @param[in] list - pointer to list container
 * @return first entry
 */
xroad_list_entry_t* xroad_list_get_first(xroad_list_t* list);

/**
 * return last entry of list
 * @param[in] list - pointer to list container
 * @return last entry
 */
xroad_list_entry_t* xroad_list_get_last(xroad_list_t* list);

/**
 * return next entry of list
 * @param[in] entry - previous entry
 * @return next entry
 */
xroad_list_entry_t* xroad_list_get_next(xroad_list_entry_t* entry);

/**
 * return previous entry of list
 * @param[in] entry - next entry
 * @return previous entry
 */
xroad_list_entry_t* xroad_list_get_prev(xroad_list_entry_t* entry);

/**
 * return entry value
 * @param[in] entry - entry with required value
 * @return entry value
 */
void* xroad_list_entry_get_value(xroad_list_entry_t* entry);

/**
 * return entry data size
 * @param[in] entry - entry with required value
 * @return entry value
 */
uint32_t xroad_list_entry_get_size(xroad_list_entry_t* entry);

/**
 * return first found entry
 * @param[in] list - pointer to list container
 * @param[in] val  - searching value
 * @param[in] cb   - pointer to comparer callback
 * @return entry value if found otherwise NULL
 */
xroad_list_entry_t* xroad_list_find(xroad_list_t* list, void* val, xroad_list_cmp_func_t cb);

#ifdef __cplusplus
}
#endif
