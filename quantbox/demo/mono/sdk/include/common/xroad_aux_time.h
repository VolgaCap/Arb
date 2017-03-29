/**
 * @file   xroad_aux_time.h
 * @author Danil Krivopustov
 */

#pragma once

#include "xroad_common_fwd.h"
#include <stdint.h>
#include <time.h>
#include <sys/time.h>

#ifdef __cplusplus
extern "C"
{
#endif
/**
 * return current day of year
 */
#define xroad_day_of_year()      \
({                               \
   struct timeval tv;            \
   gettimeofday(&tv, NULL);      \
   struct tm tm = {};            \
   localtime_r(&tv.tv_sec, &tm); \
   tm.tm_yday;                   \
})

/**
 * @return now timestamp in microseconds
 */
uint64_t xroad_now();

/**
 * @param[in] now - timestamp in seconds, if NULL current timestamp will be given
 * @return EPOCH seconds to the begin of the current day
 */
int32_t xroad_start_of_day(time_t now);

#ifdef __cplusplus
}
#endif
