/**
 * @file   xroad_string.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include "xroad_aux.h"
#include "xroad_format.h"
#include <string.h>
#include <stdio.h>
#include <stdarg.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * pointer to const string buffer
 */
struct xroad_str_s
{
   uint32_t    len;  ///< length of string
   const char* data; ///< string data
};

/**
 * fixed length string
 */
struct xroad_str_fixed_s
{
   uint32_t len; ///< string length
   char data[0]; ///< string data
};

/**
 * concatenate two strings
 * @param[in, out] str1 - destination string
 * @param[in]      str2 - source c-string
 */
#define xroad_str_concat(str1, str2)                                             \
({                                                                               \
   xroad_str_t tmp_1234599 = (str1);                                             \
   xroad_str_t tmp_5432199 = (str2);                                             \
   char* data_1234 = (char*)malloc(tmp_1234599.len + tmp_5432199.len);           \
   memcpy(data_1234, tmp_1234599.data, tmp_1234599.len);                         \
   memcpy(data_1234 + tmp_1234599.len, tmp_5432199.data, tmp_5432199.len);       \
   (xroad_str_t){tmp_1234599.len + tmp_5432199.len, data_1234};                  \
})

/**
 * convert string to c-string
 * @param[in] str - string to convert
 * @return c-string, must NOT be deallocated to free call
 */
#define xroad_str_to_cstr(str)                          \
({                                                      \
   xroad_str_t _tmp_9023 = (str);                       \
   char* res = (char*)alloca(_tmp_9023.len + 1);        \
   res[_tmp_9023.len] = '\0';                           \
   (char*)memcpy(res, _tmp_9023.data, _tmp_9023.len);   \
})

/**
 * compare two strings
 * @return the same as for strsmp
 */
#define xroad_str_cmp(a, b)                                             \
({                                                                      \
   xroad_str_t tmp_1234599 = (a);                                       \
   xroad_str_t tmp_5432199 = (b);                                       \
   tmp_1234599.len == tmp_5432199.len ?                                 \
      strncmp(tmp_1234599.data, tmp_5432199.data, tmp_1234599.len) :    \
      (tmp_1234599.len < tmp_5432199.len ? -1 : 1);                     \
})

/**
 * null string
 */
#define xroad_str_null (xroad_str_t){0, NULL}

/**
 * check if string is null
 */
#define xroad_str_is_null(str)      \
({                                  \
   xroad_str_t a = (str);           \
   (a.len == 0 && a.data == NULL);  \
})

/**
 * convert string literal(!) to xroad_str_t
 */
#define xroad_str(str) (xroad_str_t){sizeof(str) - 1, str}

/**
 * convert char array to xroad_str_t
 */ 
#define xroad_str_from_arr(arr) (xroad_str_t){strnlen(arr, sizeof(arr)), arr}

/**
 * convert string to xroad_str_t
 */
#define xroad_str_from_cstr(str)                                            \
   ({                                                                       \
      char* _s_11_ = (char*)(str);                                          \
      (xroad_str_t){_s_11_ == NULL ? 0 : (uint32_t)strlen(_s_11_), _s_11_}; \
   })

/**
 * create xroad_str_t from str and its length
 */
#define xroad_str_len(str, len)                          \
   ({                                                    \
      char* _s_11_ = (char*)(str);                       \
      (xroad_str_t){_s_11_ == NULL ? 0 : (len), _s_11_}; \
   })

/**
 * frees string data
 */
#define xroad_str_free(str)                     \
({                                              \
   xroad_str_t* ptr = (xroad_str_t*)&(str);     \
   free((void*)ptr->data);                      \
   ptr->data = NULL;                            \
   ptr->len = 0;                                \
})

/**
 * duplicates string
 */
#define xroad_str_dup(str)                                           \
({                                                                   \
   xroad_str_t a = (str);                                            \
   (xroad_str_t){a.len, a.data == NULL ? NULL : strdup(a.data)};     \
})

/**
 * allocate new string
 */
#define xroad_str_alloc(str)                                               \
({                                                                         \
   const char* tmp = (str);                                                \
   (xroad_str_t){(uint32_t)strlen(tmp), tmp == NULL ? NULL : strdup(tmp)}; \
})

/**
 * returns fixed string size
 */
#define xroad_str_fixed_size(str) sizeof((str)->data)

/**
 * converts fixed length string ptr to xroad_str_t
 */
#define xroad_str_from_fixed(str)                                             \
({                                                                            \
   __typeof__ (str) ptr_6584 = (str);                                         \
   ptr_6584 ? xroad_str_len(ptr_6584->data, ptr_6584->len) : xroad_str_null;  \
})

/**
 * creates fixed length string and related methods
 * for string data + 1 byte for zero end char
 * @param[in] name - name of type
 * @param[in] sz - maximum string length.
 */
#define xroad_str_decl(name, sz)                                                          \
typedef struct { uint32_t len; char data[sz]; } name ## _t;

/**
 * set fixed length string with data
 * @param[in] str - pointer to fixed length string to set
 * @param[in] val - pointer to xroad_str_t with value to set
 * @return new length of fixed string
 */
#define xroad_str_fixed_set(str, val)                                                     \
({                                                                                        \
   __typeof__ (str) _str_123 = (str);                                                     \
   xroad_str_t _val_123 = (val);                                                          \
   _str_123->len = xroad_min(xroad_str_fixed_size(_str_123), _val_123.len);               \
   if (!xroad_str_is_null(_val_123))                                                      \
   {                                                                                      \
      memcpy(_str_123->data, _val_123.data, _str_123->len);                               \
   }                                                                                      \
   _str_123->len;                                                                         \
})

/**
 * set fixed length string using format
 * @param[in] str - pointer to fixed length string to set
 * @param[in] fmt - format (see xroad_format.h for format details)
 * @param[in] ap  - list of parameters
 * @return length of str after applying format
 */
#define xroad_str_fixed_vformat(str, fmt, ap)                                             \
({                                                                                        \
   __typeof__ (str) _str_123 = (str);                                                     \
   int32_t res = xroad_vformat(_str_123->data, xroad_str_fixed_size(_str_123), fmt, ap);  \
   if (res > 0)                                                                           \
   {                                                                                      \
      _str_123->len = xroad_min((uint32_t)res, xroad_str_fixed_size(_str_123));           \
   }                                                                                      \
   res;                                                                                   \
})

/**
 * set fixed length string using format. The same as xroad_str_fixed_vformat
 * @param[in] str - pointer to fixed length string to set
 * @param[in] fmt - format (see xroad_format.h for format details)
 * @return length of str after applying format
 */
#define xroad_str_fixed_format(str, fmt, ...)                                                      \
({                                                                                                 \
   __typeof__ (str) _str_123 = (str);                                                              \
   int32_t res = xroad_format(_str_123->data, xroad_str_fixed_size(_str_123), fmt, __VA_ARGS__);   \
   if (res > 0)                                                                                    \
   {                                                                                               \
      _str_123->len = xroad_min((uint32_t)res, xroad_str_fixed_size(_str_123));                    \
   }                                                                                               \
   res;                                                                                            \
})

/**
 * concatenate two fixed length strings
 * @param[in] lhs - pointer to fixed length string
 * @param[in] rhs - xroad_str_t
 * @return new fixed length str size
 */
#define xroad_str_fixed_concat(lhs, rhs)                                                        \
({                                                                                              \
   __typeof__ (lhs) _lhs = (lhs);                                                               \
   xroad_str_t _rhs = (rhs);                                                                    \
   uint32_t cat_len_123 = xroad_min((xroad_str_fixed_size(_lhs) - _lhs->len), _rhs.len);        \
   memcpy(_lhs->data + _lhs->len, _rhs.data, cat_len_123);                                      \
   _lhs->len += cat_len_123;                                                                    \
   cat_len_123;                                                                                 \
})

/**
 * convert fixed length string to c-string. c-string is allocated on stack
 * @param[in] str - pointer to fixed length string
 * @return c-string
 */
#define xroad_str_fixed_to_cstr(str)                                     \
({                                                                       \
   __typeof__ (str) tmp_1234599 = (str);                                 \
   char* res = NULL;                                                     \
   if (tmp_1234599)                                                      \
   {                                                                     \
      char* tmp_991 = (char*)alloca(tmp_1234599->len + 1);               \
      tmp_991[tmp_1234599->len] = 0;                                     \
      res = (char*)memcpy(tmp_991, tmp_1234599->data, tmp_1234599->len); \
   }                                                                     \
   res;                                                                  \
})

#ifdef __cplusplus
}
#endif
