/**
 * @file   xroad_aux.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include "xroad_common_fwd.h"
#include "xroad_aux_time.h"
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

#define xroad_likely(x) __builtin_expect(!!(x), 1)
#define xroad_unlikely(x) __builtin_expect(!!(x), 0)

#define xroad_cpu_pause() asm volatile("pause\n": : :"memory")
#define xroad_fence() asm volatile("mfence": : :"memory")

/**
 * find min among a and b
 */
#define xroad_min(a, b)          \
   ({ __typeof__ (a) _a = (a);   \
    __typeof__ (b) _b = (b);     \
    _a < _b ? _a : _b; })

/**
 * find max among a and b
 */
#define xroad_max(a, b)          \
   ({ __typeof__ (a) _a = (a);   \
    __typeof__ (b) _b = (b);     \
    _a > _b ? _a : _b; })

/**
 * compare two doubles
 * @return 0 - equal, <0 - less, >0 - greater
 */
#define xroad_dbl_cmp(lhs, rhs)                       \
({                                                    \
   __typeof__(lhs) lhs1977_ = (lhs);                  \
   __typeof__(rhs) rhs1977_ = (rhs);                  \
   (fabs(lhs1977_ - rhs1977_) < XROAD_EPSILON) ? 0 :  \
   (lhs1977_ < rhs1977_ ? -1 : 1);  \
})

/**
 * calculate hash
 * @param[in] data - data to hash
 * @param[in] len  - data length
 * @return hash value
 */
uint32_t xroad_murmur_hash2(const uint8_t *data, uint32_t len);

/**
 * convert error code into string representation
 * @param[in] err - error to convert
 * @return error string representation
 */
xroad_str_t xroad_strerror(int32_t err);

#ifdef __cplusplus
}
#endif
