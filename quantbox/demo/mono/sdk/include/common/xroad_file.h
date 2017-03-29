/**
 * @file   xroad_file.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include "xroad_string.h"

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct xroad_file_s xroad_file_t;

/**
 * read file callback
 */
typedef struct
{
   void* ctx;     ///< read context
   void (*on_read)(xroad_file_t*, off_t, void*, size_t, void*); ///< read is done
   void (*on_read_error)(xroad_file_t*, int32_t, void*);        ///< read error rised
   void (*on_canceled)(xroad_file_t*, void*);                   ///< read canceled
} xroad_file_rcallback_t;

/**
 * write file callback
 */
typedef struct
{
   void* ctx;                                             ///< write context
   void (*on_write)(xroad_file_t*, off_t, size_t, void*); ///< write is done
   void (*on_write_error)(xroad_file_t*, int32_t, void*); ///< write error
   void (*on_canceled)(xroad_file_t*, void*);             ///< write canceled
} xroad_file_wcallback_t;

/**
 * create file
 * @param[in] name - file name (path)
 * @param[in] signal - real time signal from SIGRTMIN to SIGRTMAX, which will be sent after operation completion
 * @param[in] flags - open flags (man 2 open for details)
 * @param[in] mode - open mode (man 2 open for details)
 * @return file instance, NULL - in case of error
 */
xroad_file_t* xroad_file_create(xroad_str_t name, int32_t signal, int32_t flags, mode_t mode);

/**
 * file destroy
 * @param[in] file - file to destroy
 * @return XROAD_OK - destroyed, XROAD_ERROR_BUSY - not destroyed, not all tasks are completed
 */
xroad_errno_t xroad_file_destroy(xroad_file_t* file);

/**
 * cancel all async tasks
 * @param[in] file - file instance
 * @return 0 - all canceled, 1 - some tasks are still alive
 */
int32_t xroad_file_cancel(xroad_file_t* file);

/**
 * return count of active tasks
 * @param[in] file - file instance
 * @return count of active tasks
 */
uint32_t xroad_file_get_req_cnt(xroad_file_t* file);

/**
 * read file chunk
 * @param[in] file - file instance to read
 * @param[in] offset - file read offset
 * @param[in] buf - preallocated buffer to store read data
 * @param[in] len - buffer length
 * @param[in] callback - read callback
 */
xroad_errno_t xroad_file_read(xroad_file_t* f, off_t offset, void* buf, size_t len, xroad_file_rcallback_t callback);

/**
 * write file chunk
 * @param[in] file     - file instance to read
 * @param[in] offset   - file write offset
 * @param[in] buf      - data to write
 * @param[in] len      - data length
 * @param[in] callback - write callback
 */
xroad_errno_t xroad_file_write(xroad_file_t* f, off_t offset, void* buf, size_t len, xroad_file_wcallback_t callback);

#ifdef __cplusplus
}
#endif
