#pragma once
/**
 * @file   xroad_vector.h
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
 * hash entry free function
 */
typedef void (*xroad_vector_free_func_t)(void*);

/**
 * create new vector container
 * @param[in] entry_size - the size of entry
 * @param[in] capacity - the initial capacity of vector
 * @return vector object
 */
xroad_vector_t* xroad_vector_create(size_t entry_size, size_t capacity);

/**
 * destroy vector container
 * @param[in] vector    - container to destroy. If NULL, nothing happened
 * @param[in] free_func - function for free vector entries data, NULL - no free performed
 * */
void xroad_vector_destroy(xroad_vector_t* vector, xroad_vector_free_func_t free_func);

/**
 * return vector size
 * @param[in] vector - pointer to vector container
 */
int32_t xroad_vector_get_size(const xroad_vector_t* vector);

/**
 * return vector capacity
 * @param[in] vector - pointer to vector container
 */
int32_t xroad_vector_get_capacity(const xroad_vector_t* vector);

/**
 * insert value at the end of vector
 * @param[in] vector - pointer to vector container
 * @param[in] val - pointer to inserted value
 */
#define xroad_vector_push_back(vector, val) \
   xroad_vector_insert(vector, xroad_vector_get_size(vector), val)

/**
 * insert value at the top of vector
 * @param[in] vector - pointer to vector container
 * @param[in] val - pointer to inserted value
 */
#define xroad_vector_push_front(vector, val) \
   xroad_vector_insert(vector, 0, val)

/**
 * insert value into vector at specified position
 * @param[in] vector - pointer to vector container
 * @param[in] pos    - insert position
 * @param[in] val    - pointer to inserted value
 */
void xroad_vector_insert(xroad_vector_t* vector, size_t pos, void* val);

/**
 * delete entry from vector
 * @param[in] vector    - pointer to vector container
 * @param[in] pos       - position in the container where entry should be deleted
 * @param[in] free_func - function for free vector entries data, NULL - no free performed
 */
void xroad_vector_delete_at(xroad_vector_t* vector, size_t pos, xroad_vector_free_func_t free_func);

/**
 * return entry of vector
 * @param[in] vector - pointer to vector container
 * @param[in] pos - position in the vector container
 * @return vector entry
 */
void* xroad_vector_get_at(xroad_vector_t* vector, size_t pos);

/**
 * return last entry of vector
 * @param[in] vector - pointer to vector container
 * @return last entry
 */
#define xroad_vector_get_last(vector) \
   xroad_vector_get_at(vector, xroad_vector_get_size(vector) - 1)

/**
 * return first entry of vector
 * @param[in] vector - pointer to vector container
 * @return first entry
 */
#define xroad_vector_get_first(vector) \
   xroad_vector_get_at(vector, 0)

/**
 * vector entries compare function
 */
typedef int32_t (*xroad_cmp_func_t)(const void*, const void*);

/**
 * return first found entry
 * @param[in] vector - pointer to vector container
 * @param[in] val    - searching value
 * @param[in] cb     - pointer to comparer callback
 * @return - finded position otherwise -1
 */
int32_t xroad_vector_find(xroad_vector_t* vector, void* val, xroad_cmp_func_t cb);

/**
 * sort vector elements
 * @param[in] vector - vector to sort
 * @param[in] cb     - comparer function
 */
void xroad_vector_sort(xroad_vector_t* vector, xroad_cmp_func_t cb);

/**
 * removes all position from vector
 * @param[in] vector    - pointer to vector container
 * @param[in] free_func - function for free vector entries data, NULL - no free performed
 * */
void xroad_vector_clear(xroad_vector_t* vector, xroad_vector_free_func_t free_func);

#ifdef __cplusplus
}
#endif
