#pragma once

/**
 * @file   xroad_map.h
 * @author Danil Krivopustov, krivopustovda@gmail.com
 */

#include <stdlib.h>
#include "xroad_common_fwd.h"
#include "xroad_common_types.h"


#ifdef __cplusplus
extern "C"
{
#endif

/**
 * equal function type
 */
typedef int32_t (*xroad_map_cmp_func_t)(const void*, uint32_t,  const void*, uint32_t);

/**
 * map entry free function
 */
typedef void (*xroad_map_free_func_t)(void*);

/**
 * result of xroad_map_insert call
 */
typedef struct
{
   xroad_map_entry_t* entry;    ///< inserted or existing entry
   xroad_errno_t      result;   ///< result of insertion
} xroad_map_result_t;

/**
 * create new map
 * @param[in] cmp    - comparer function to compare keys
 * @param[in] dtor   - free function to destroy value
 * @return pointer to new map, NULL - error
 */
xroad_map_t* xroad_map_create(xroad_map_cmp_func_t cmp, xroad_map_free_func_t dtor);

/**
 * delete map and free all resources
 * @param[in] map      - map to delete. If hash is NULL, nothing happened
 */
void xroad_map_destroy(xroad_map_t* map);

/**
 * delete all entries from map
 * @param[in] map      - map with deleted entry
 */
void xroad_map_clear(xroad_map_t* map);

/**
 * insert new entry into table map
 * @param[in] map        - instance of map
 * @param[in] key        - pointer to key data
 * @param[in] key_size   - size of key data
 * @param[in] value      - pointer to data
 * @param[in] value_size - size of data
 * @return result of insertion. entry - result of insertion or existing entry,
 *     errno - XROAD_OK - inserted, XROAD_ERROR_ALREADY_EXISTS - entry with the same key already exists
 */
xroad_map_result_t xroad_map_insert(xroad_map_t* map, const void* key, uint32_t key_size, const void* value, uint32_t value_size);

/**
 * find entry in map
 * @param[in] map        - instance of map
 * @param[in] key       - key to find
 * @param[in] key_size  - size of key
 * @return entry or NULL if not found
 */
xroad_map_entry_t* xroad_map_find(xroad_map_t* map, const void* key, uint32_t size);

xroad_map_entry_t* xroad_map_lower_bound(xroad_map_t* map, const void* key, uint32_t size);
xroad_map_entry_t* xroad_map_upper_bound(xroad_map_t* map, const void* key, uint32_t size);

/**
 * delete entry and free all allocated resources
 * @param[in] map        - instance of map
 * @param[in] key        - key to find
 * @param[in] key_size   - size of key
 * @return XROAD_OK if entry was deleted otherwise XROAD_ERROR_NOT_FOUNDy
 */
xroad_errno_t xroad_map_entry_delete(xroad_map_t* map, const void* key, uint32_t size);

/**
 * deletes max key entry
 * @param[in] map        - instance of map
 */
void xroad_map_delete_max(xroad_map_t* map);

/**
 * deletes minkey entry
 * @param[in] map        - instance of map
 */
void xroad_map_delete_min(xroad_map_t* map);

/**
 * return max entry from map
 * @param[in] map - map with enries
 */
xroad_map_entry_t* xroad_map_get_max(xroad_map_t* map);

/**
 * return min entry from map
 * @param[in] map - map with enries
 */
xroad_map_entry_t* xroad_map_get_min(xroad_map_t* map);

/**
 * gets next map entry
 * @param[in] e - map entry
 * @return xroad_map_entry_t if exists otherwise NULL
 */
xroad_map_entry_t* xroad_map_entry_get_next(xroad_map_entry_t* e);

/**
 * gets previous map entry
 * @param[in] e - map entry
 * @return xroad_map_entry_t if exists otherwise NULL
 */
xroad_map_entry_t* xroad_map_entry_get_prev(xroad_map_entry_t* e);

/**
 * return entry value size
 * @param[in] entry - entry to explore
 * @return entry size
 */
uint32_t xroad_map_entry_get_value_size(const xroad_map_entry_t* entry);

/**
 * return entry value
 * @param[in] entry - entry to explore
 * @return entry value
 */
void* xroad_map_entry_get_value(xroad_map_entry_t* entry);

/**
 * set entry value
 * @param[in] entry - entry to set
 * @param[in] value - new value to set
 * @param[in] value_size - size of new value
 * @param[in] free_func - func for destroying previous value, if NULL - no destroy performed
 * @return entry. The addess may be changed, so use return value instead of param one
 */
xroad_map_entry_t* xroad_map_entry_set_value(xroad_map_entry_t* entry, const void* value, uint32_t value_size, xroad_map_free_func_t dtor);

/**
 * return entry key size
 * @param[in] entry - entry to explore
 * @return entry size
 */
uint32_t xroad_map_entry_get_key_size(const xroad_map_entry_t* entry);

/**
 * return entry key
 * @param[in] entry - entry to explore
 * @return entry value
 */
void* xroad_map_entry_get_key(xroad_map_entry_t* entry);
/**
 * return number of entries in map
 * @param[in] map - map table
 * @return number of entries in map
 */
int32_t xroad_map_get_size(xroad_map_t* map);

/**
 * convert map structure to sorted list
 * @param[in] map - map to convert
 * @return new list structure
 */
xroad_list_t* xroad_map_to_list(xroad_map_t* map);

#ifdef __cplusplus
}
#endif
