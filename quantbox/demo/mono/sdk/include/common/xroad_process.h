/**
 * @file   xroad_process.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include <node/xroad_node.h>
#include <node/xroad_node_types.h>
#include <node_gen/xroad_objects.h>
#include <logger/xroad_logger.h>
#include <common/xroad_signal.h>

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct process_s process_t;

/**
 * process interface
 */
typedef struct xroad_process_iface_s
{
   /**
    * fired at process creation
    * @param[in] - argv
    * @param[in] - argc
    * @return process instance
    */
   process_t* (*create)(int32_t, char*[]);
   /*
    * fired at process destruction
    * @param [] - process instance to destroy
    */
   void (*destroy)(process_t*);
   /**
    * fired at process start
    * @param[in] - process instance to start
    */
   void (*start)(process_t*);
   /**
    * fired at process stop
    * @param[in] - process instalce to stop
    */
   void (*stop)(process_t*);
   /**
    * fired at process activation
    * @param[in] - process instance to activate
    */
   void (*activate)(process_t*);
   /**
    * fired at process deactivation
    * @param[in] - process instalce to deactivate
    */
   void (*deactivate)(process_t*);
   /**
    * fired at process shutdown
    * @param[in] - process instance to shutdown
    */
   void (*shutdown)(process_t*);
   /**
    * fired at new object received
    * @param[in] - process instance
    * @param[in] - received object
    * @param[in] - source node id
    */
   void (*on_node_object)(process_t*, void*, xroad_node_id_t);
   /**
    * fired at process reconfiguration
    * @param[in] - process to reconfigure
    * @return XROAD_OK - process reconfigured, else - failed
    */
   xroad_errno_t (*reconfig)(process_t*);
   /**
    * fired at date changed. optional
    * @param[in] - process instance
    */
   void (*date_changed)(process_t*);
   /**
    * fired at reset received. optional
    * @param[in] - process instance
    * @param[in] - reset hint
    */
   void (*reset)(process_t*, xroad_int32_t hint);
   /**
    * fired when some node exited. optional
    * @param[in] - process instance
    * @param[in] - node id
    * @param[in] - 1 - crashed, 0 - exited
    */
   void (*exited)(process_t*, xroad_node_id_t, xroad_is_crashed_t);
   /**
    * fired each time process enter into loop
    * @param[in] - process instance
    * @return   0 - process leaves loop successfully
    *          <0 - process leaves loop with error
    *          >0 - continue to work
    */
   int32_t (*enter_loop)(process_t*);
} xroad_process_iface_t;

typedef struct xroad_process_s xroad_process_t;

/**
 * creates process and enter main loop
 * @param[in] argc - argument count
 * @param[in] argv - arguments array
 * @param[in] piface - process interface
 * @return EXIT_FAILURE, EXIT_SUCCESS
 */
int32_t xroad_process(int32_t argc, char* argv[], xroad_process_iface_t piface);

#ifdef __cplusplus
}
#endif
