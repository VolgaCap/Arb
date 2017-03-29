/**
 * @file   main.c
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#include "process.h"
#include <common/xroad_process.h>

int32_t main(int argc, char *argv[])
{
   xroad_process_iface_t piface =
   {
      .create   = process_create,
      .destroy  = process_destroy,
      .shutdown = process_shutdown,
      .start    = process_start,
      .stop     = process_stop,
      .reconfig = process_reconfig,
      .activate = process_activate,
      .deactivate     = process_deactivate,
      .reset          = process_reset,
      .on_node_object = process_on_node_object,
      .enter_loop     = process_do
   };
   return xroad_process(argc, argv, piface);
}
