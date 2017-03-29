#pragma once
/**
 * @file   xroad_rwlock.h
 * @author Danil Krivopustov danilk@quantbox.ru
 */

#include <stdint.h>

typedef struct xroad_rwlock_s xroad_rwlock_t;

/*
 * @brief agressively acuires write lock
 * @param[in] l - rwlock
 */
void xroad_rwlock_lock(xroad_rwlock_t* l);

/*
 * @brief releases write lock
 * @param[in] l - rwlock
 */
void xroad_rwlock_unlock(xroad_rwlock_t* l);

/*
 * @brief tries to aquire read lock
 * @param[in] l - rwlock
 * @return true if success
 */
int32_t xroad_rwlock_try_shared_lock(xroad_rwlock_t* l);

/*
 * @brief aquires read lock, waits if there is writer
 * @param[in] l - rwlock
 */
void xroad_rwlock_shared_lock(xroad_rwlock_t* l);

/*
 * @brief releases read lock
 * @param[in] l - rwlock
 */
void xroad_rwlock_shared_unlock(xroad_rwlock_t* l);

/*
 *
 *
 */
int32_t xroad_rwlock_number_wlock(xroad_rwlock_t* l);

int32_t xroad_rwlock_number_rlock(xroad_rwlock_t* l);
