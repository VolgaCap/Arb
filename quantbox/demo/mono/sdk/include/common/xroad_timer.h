#pragma once
/**
 * @file   xroad_timer.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 * @author Danil Krivopustov krivopustovda@gmail.com
 */

#include <stdbool.h>
#include "xroad_common_types.h"
#include "xroad_common_fwd.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * callback structure for timer
 */
typedef struct
{
   void* ctx;                    ///< callback context
   void (*on_timer)(void* ctx);  ///< called, when time expired
} xroad_timer_callback_t;

/**
 * create new timer instance
 * @param[in] cb - callback function
 * @return pointer to new instance, NULL - error
 */
xroad_timer_t* xroad_timer_create(xroad_timer_callback_t cb);

/**
 * once fires timer in interval time
 * @param[in] tm       - pointer to the timer instance
 * @param[in] interval - timer interval in microseconds
 * @return XROAD_OK if success otherwise XROAD_FAILED
 */
xroad_errno_t xroad_timer_start(xroad_timer_t* tm, uint64_t interval);

/**
 * fires timer after start interval and repeat in repeat interval
 * @param[in] tm     - pointer to the timer instance
 * @param[in] start  - timer interval in microseconds when it starts first time
 * @param[in] repeat - timer repeat interval in microseconds
 * @return XROAD_OK if success otherwise XROAD_FAILED
 */
xroad_errno_t xroad_timer_start_repeat(xroad_timer_t* tm, uint64_t start, uint64_t repeat);

/**
 * repeatedly fires timer in interval time
 * @param[in] tm       - pointer to the timer instance
 * @param[in] interval - timer interval in microseconds
 * @return XROAD_OK if success otherwise XROAD_FAILED
 */
xroad_errno_t xroad_timer_repeat(xroad_timer_t* tm, uint64_t interval);

/**
 * stop timer
 * @param[in] tm - pointer to the timer instance
 */
void xroad_timer_stop(xroad_timer_t* tm);

/**
 * destroy timer instance
 * @param[in] tm - pointer to the timer instance. If NULL, nothing happened
 */
void xroad_timer_destroy(xroad_timer_t* tm);

/**
 * returns true if timer is armed
 * @param[in] tm - pointer to the timer instance
 * */
bool xroad_timer_is_armed(xroad_timer_t* tm);

#ifdef __cplusplus
}
#endif
