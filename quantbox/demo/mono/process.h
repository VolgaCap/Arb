/**
 * @file   process.h
 * @author Dmitry S. Melnikov, dmitryme@quantbox.ru
 */

#pragma once

#include <common/xroad_common_types.h>
#include <node_gen/xroad_objects.h>

#ifdef __cplusplus
extern "C"
{
#endif

struct epoll_event;

typedef struct process_s process_t;

/**
 * create new process
 * @param[in] argc - argument count
 * @param[in] argv - argument array
 * @return new process instance
 */
process_t* process_create(int32_t argc, char* argv[]);

/**
 * destroy process
 * @param[in] process - process to destroy
 */
void process_destroy(process_t* process);

/**
 * reconfigure process
 * @param process    - process to reconfigure
 * @return XROAD_OK  - reconfigured
 */
xroad_errno_t process_reconfig(process_t* process);

/**
 * start process
 * @param[in] process - process to start
 */
void process_start(process_t* process);

/**
 * stop process
 * @param[in] process  - process to stop
 */
void process_stop(process_t* process);

/**
 * shutdown process
 * @param[in] process  - process to shutdown
 */
void process_shutdown(process_t* process);

/**
 * activate process
 * @param[in] process - process to activate
 */
void process_activate(process_t* process);

/**
 * deactivate process
 * @param[in] process - process to deactivate
 */
void process_deactivate(process_t* process);

/**
 * process reset event
 * @param[in] process - process to reset
 * @param[in] hint    - reset hint
 */
void process_reset(process_t* process, xroad_int32_t hint);

/**
 * process object arrived
 * @param[in] process  - pointer to process
 * @param[in] obj      - pointer to xroad_object
 * @param[in] from     - id of node obj from
 */
void process_on_node_object(process_t* process, void* obj, xroad_node_id_t from);

/**
 * go into waiting loop
 * @param[in] process - pointer to process
 */
int32_t process_do(process_t* process);

#ifdef __cplusplus
}
#endif
