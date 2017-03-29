#pragma once

/**
 * @file   xroad_heap.h
 * @author Danil Krivopustov, krivopustovda@gmail.com
 */

#include "xroad_common_fwd.h"
#include "xroad_common_types.h"
#include <stdint.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * heap entry free function
 */
typedef void (*xroad_heap_free_func_t)(void*);

/**
 * heap entry compare function
 */
typedef int32_t (*xroad_heap_cmp_func_t)(void*, void*);

/**
 * create new heap container
 * @param[in] entry_size - the size of entry
 * @param[in] capacity - the initial capacity of heap
 * @return heap object
 */
xroad_heap_t* xroad_heap_create(size_t entry_size, size_t capacity, xroad_heap_cmp_func_t cmp);

/**
 * destroy heap container
 * @param[in] heap    - container to destroy. If NULL, nothing happened
 * @param[in] free_func - function for free heap entries data, NULL - no free performed
 * */
void xroad_heap_destroy(xroad_heap_t* heap, xroad_heap_free_func_t free_func);

/**
 * return heap size
 * @param[in] heap - pointer to heap container
 */
size_t xroad_heap_get_size(const xroad_heap_t* heap);

/**
 * insert value into heap
 * @param[in] heap - pointer to heap container
 * @param[in] val    - pointer to inserted value
 * return 1 - if root has been changed
 */
int32_t xroad_heap_insert(xroad_heap_t* heap, void* val);

/**
 * delete root entry from heap
 * @param[in] heap    - pointer to heap container
 * @param[in] free_func - function for free heap entries data, NULL - no free performed
 */
void xroad_heap_pop(xroad_heap_t* heap, xroad_heap_free_func_t free_func);

/**
 * remove all position from heap
 * @param[in] heap    - pointer to heap container
 * @param[in] free_func - function for free heap entries data, NULL - no free performed
 * */
void xroad_heap_clear(xroad_heap_t* heap, xroad_heap_free_func_t free_func);

/**
 * get first elem from container
 * @param[in] heap    - pointer to heap container
 * @return heap entry
 * */
void* xroad_heap_get_root(xroad_heap_t* heap);

#ifdef __cplusplus
}
#endif
