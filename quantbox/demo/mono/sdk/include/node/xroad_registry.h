/**
 * @file   xroad_registry.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include "xroad_node_fwd.h"
#include "xroad_node_types.h"
#include <common/xroad_common_types.h>
#include <common/xroad_string.h>
#include <stdint.h>
#include <signal.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * main node id
 */
#define XROAD_INIT_NODE_ID 1

/**
 * maximum nodes in registry
 */
#define XROAD_NODE_COUNT_MAX 1024

xroad_str_decl(xroad_git_hash, 7)

/**
 * node status
 */
typedef enum
{
   xroad_node_status_active   = 1, ///< node is active and works
   xroad_node_status_offline  = 2, ///< node started, but is not active
   xroad_node_status_dead     = 3, ///< node is DEAD, process stopped
   xroad_node_status_inactive = 4  ///< node is working, but inactive
} xroad_node_status_t;

/**
 * node flags
 */
typedef enum
{
   xroad_node_flag_stand_alone   = 0x1, ///< node is a standalone, i.e. not controlled by init process
   xroad_node_flag_hidden        = 0x2  ///< node is hidden, i.e. not shown by view or WebUI
} xroad_node_flag_t;

/**
 * node statistic
 */
struct xroad_node_statistic_s
{
   uint32_t error_cnt;   ///< count of errors
   uint32_t warn_cnt;    ///< count of warnings
   uint64_t msg_in_cnt;  ///< count of incoming messages
   uint64_t msg_out_cnt; ///< count of outgoing messages
   time_t   start_ts;    ///< node start timestamp
   time_t   curr_ts;     ///< node current timestamp
};

/**
 * node version
 */
typedef struct
{
   uint16_t          major_ver;      ///< major version
   uint16_t          minor_ver;      ///< minor version
   xroad_git_hash_t  git_hash;       ///< git_hash
   uint8_t           is_debug;       ///< debug build
   uint8_t           git_uncommited; ///< code has uncommited changes
} xroad_node_version_t;

/**
 * node info in registry
 */
typedef struct
{
   xroad_node_id_t        id;        ///< index of node in registry
   xroad_node_name_t      name;      ///< name of node
   xroad_group_name_t     group;     ///< group of node
   pid_t                  pid;       ///< pid of process
   xroad_node_statistic_t statistic; ///< node statistic
   xroad_node_status_t    status;    ///< node status
   uint32_t               flags;     ///< node flags (see xroad_node_flag_t)
   xroad_link_name_t      link;      ///< link name
   xroad_node_version_t   version;   ///< version
   xroad_config_name_t    config;    ///< node default config file name
} xroad_node_data_t;

/**
 * registry
 */
typedef struct
{
   uint16_t            major_ver;     ///< major version
   int32_t             lock;          ///< locks call xroad_registry_init
   int32_t             out_of_system; ///< registry created of of system (not shared)
   xroad_system_name_t system_name;   ///< given from XROAD_SYSTEM
   xroad_path_t        root_dir;      ///< given from XROAD_ROOT_DIR
   xroad_path_t        home_dir;      ///< given from XROAD_ROOT_DIR/data
   xroad_node_data_t   entries[XROAD_NODE_COUNT_MAX]; ///< array of nodes in registry
} xroad_registry_t;

/**
 * init registry
 * @param[in] out_of_system - 1 - process is not a part of system. it only has an access to cache
 * @return XROAD_OK - registry has been initialized
 */
xroad_errno_t xroad_registry_init(int32_t out_of_system);

/**
 * return pointer to created registry
 * @return pointer to registry
 */
xroad_registry_t* xroad_registry_get();

/**
 * find node by name
 * @param[in] name - name of node to find
 * @return pointer to node data in registry, NULL - no such node
 */
xroad_node_data_t* xroad_registry_get_by_name(xroad_str_t name);

/**
 * find node by id
 * @param[in] id - id of node
 * @return pointer to node data in registry, NULL - no such node
 */
xroad_node_data_t* xroad_registry_get_by_id(xroad_node_id_t id);

/**
 * find node by pid
 * @param[in] pid - pid of node
 * @return pointer to node data in registry, NULL - no such node
 */
xroad_node_data_t* xroad_registry_get_by_pid(pid_t pid);

#ifdef __cplusplus
}
#endif
