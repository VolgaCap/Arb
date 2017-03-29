/**
 * @file   xroad_hash.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include "xroad_common_fwd.h"
#include "xroad_common_types.h"
#include <stdlib.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * hash function type
 */
typedef uint32_t (*xroad_hash_func_t)(const uint8_t*, uint32_t);

/**
 * equal function type
 */
typedef int32_t (*xroad_hash_equal_func_t)(const void*, uint32_t, const void*, uint32_t);

/**
 * hash entry free function
 */
typedef void (*xroad_hash_free_func_t)(void*, uint32_t);

/**
 * result of xroad_hash_insert call
 */
typedef struct
{
   xroad_hash_entry_t* entry;    ///< inserted or existing entry
   xroad_errno_t       result;   ///< result of insertion
} xroad_hash_ins_res_t;

/**
 * create new hash table
 * @param[in] initial_size - initial size of hash table
 * @param[in] hash_func    - hash function, if NULL - default function is used
 * @param[in] equal_func   - equality function, used for entry search. if NULL - default function is used
 * @return pointer to new hash table, NULL - error
 */
xroad_hash_t* xroad_hash_create(uint32_t initial_size, xroad_hash_func_t hash_func, xroad_hash_equal_func_t equal_func);

/**
 * delete hash table and free all resources
 * @param[in] hash      - hash table to delete. If hash is NULL, nothing happened
 * @param[in] free_func - func for destroying data, if NULL - no destroy performed
 */
void xroad_hash_destroy(xroad_hash_t* hash, xroad_hash_free_func_t free_func);

/**
 * insert new entry into table
 * @param[in] hash       - instance of hash table
 * @param[in] key        - pointer to key data
 * @param[in] key_size   - size of key data
 * @param[in] value      - pointer to data
 * @param[in] value_size - size of data
 * @return result of insertion. entry - result of insertion or existing entry,
 *     errno - XROAD_OK - inserted, XROAD_ERROR_ALREADY_EXISTS - entry with the same key already exists
 */
xroad_hash_ins_res_t xroad_hash_insert(
      xroad_hash_t* hash, const void* key, uint32_t key_size, const void* value, uint32_t value_size);

/**
 * find entry in hash table
 * @param[in] hash      - instance of hash table
 * @param[in] key       - key to find
 * @param[in] key_size  - size of key
 * @return entry or NULL if not found
 */
xroad_hash_entry_t* xroad_hash_find(xroad_hash_t* hash, const void* key, uint32_t key_size);

/**
 * delete all entries from hash table
 * @param[in] hash      - hash with deleted entry
 * @param[in] free_func - func for destroying data, if NULL - no destroy performed
 */
void xroad_hash_clear(xroad_hash_t* hash, xroad_hash_free_func_t free_func);

/**
 * return entry value size
 * @param[in] entry - entry to explore
 * @return entry size
 */
uint32_t xroad_hash_entry_get_value_size(const xroad_hash_entry_t* entry);

/**
 * return entry value
 * @param[in] entry - entry to explore
 * @return entry value
 */
void* xroad_hash_entry_get_value(xroad_hash_entry_t* entry);

/**
 * set entry value
 * @param[in] entry - entry to set
 * @param[in] value - new value to set
 * @param[in] value_size - size of new value
 * @param[in] free_func - func for destroying previous value, if NULL - no destroy performed
 * @return entry. The addess may be changed, so use return value instead of param one
 */
xroad_hash_entry_t* xroad_hash_entry_set_value(
      xroad_hash_entry_t* entry, const void* value, uint32_t value_size, xroad_hash_free_func_t free_func);

/**
 * return entry key size
 * @param[in] entry - entry to explore
 * @return entry size
 */
uint32_t xroad_hash_entry_get_key_size(const xroad_hash_entry_t* entry);

/**
 * return entry key
 * @param[in] entry - entry to explore
 * @return entry value
 */
void* xroad_hash_entry_get_key(xroad_hash_entry_t* entry);

/**
 * delete entry and free all allocated resources
 * @param[in] entry     - entry to delete
 * @param[in] free_func - func for destroying data, if NULL - no destroy performed
 * @return next entry, if any
 */
xroad_hash_entry_t* xroad_hash_entry_delete(xroad_hash_entry_t* entry, xroad_hash_free_func_t free_func);

/**
 * return first entry from hash
 * @param[in] hash - hash with enries
 */
xroad_hash_entry_t* xroad_hash_get_first(xroad_hash_t* hash);

/**
 * return next entry from hash
 * @param[in] entry  - first entry, NULL - no more entries
 */
xroad_hash_entry_t* xroad_hash_get_next(xroad_hash_entry_t* entry);

/**
 * delete entry from hash table
 * @param[in] hash      - hash table
 * @param[in] key       - key to delete
 * @param[in] key_size  - size of key
 * @param[in] free_func - func for destroying data, if NULL - no destroy performed
 * @return XROAD_OK - found&deleted, XROAD_ERROR_NOT_FOUND - entry with key not found
 */
xroad_errno_t xroad_hash_delete(xroad_hash_t* hash, const void* key, uint32_t key_size, xroad_hash_free_func_t free_func);

/**
 * return number of entries in hash
 * @param[in] hash - hash table
 * @return number of entries in hash
 */
uint32_t xroad_hash_get_size(xroad_hash_t* hash);

/**
 * convert hash structure to list
 * @param[in] hash - hash to convert
 * @return new list structure
 */
xroad_list_t* xroad_hash_to_list(xroad_hash_t* hash);

#ifdef __cplusplus
}
#endif
