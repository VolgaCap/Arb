/**
 * @file   xroad_common_types.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include <stdint.h>
#include <stdlib.h>
#include <math.h>

typedef int32_t         xroad_errno_t;

#define XROAD_OK             0
#define XROAD_FAILED        -1

#define XROAD_ERROR_NOT_FOUND          -2
#define XROAD_ERROR_INVALID_ARG        -3
#define XROAD_ERROR_TOO_LONG           -4
#define XROAD_ERROR_DUPLICATE_VAL      -5
#define XROAD_ERROR_NOT_CONNECTED      -6
#define XROAD_ERROR_CHECK_FAILED       -7
#define XROAD_ERROR_WRONG_FORMAT       -8
#define XROAD_ERROR_ALREADY_EXISTS     -9
#define XROAD_ERROR_ALREADY_CONNECTED -10
#define XROAD_ERROR_NO_MORE_RESOURCES -11
#define XROAD_ERROR_NOT_IMPL          -12
#define XROAD_ERROR_ALREADY_DONE      -13
#define XROAD_ERROR_WRONG_STATE       -14
#define XROAD_ERROR_BUSY              -15
#define XROAD_ERROR_UNABLE_TO_ROUTE   -16

#define XROAD_EPSILON 0.00000001
#define XROAD_SECONDS_IN_DAY 86400

/**
 * xroad boolean
 */
typedef enum
{
   xroad_bool_true = 1,
   xroad_bool_false = 0
} xroad_bool_t;
