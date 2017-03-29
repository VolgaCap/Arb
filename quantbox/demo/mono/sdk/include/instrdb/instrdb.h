/**
 * @file   instr.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include <common/xroad_common_fwd.h>
#include <common/xroad_common_types.h>
#include <node_gen/xroad_objects.h>
#include <common/xroad_string.h>

#ifdef __cplusplus
extern "C"
{
#endif

#define instrdb_make_name(name, cls)                                                      \
({                                                                                        \
   xroad_str_t name1977 = (name);                                                         \
   xroad_str_t cls1977 = (cls);                                                           \
   size_t buf_len = name1977.len + cls1977.len + (xroad_str_is_null(cls1977) ? 0 : 1);    \
   char* buf = alloca(buf_len);                                                           \
   if (xroad_str_is_null(cls1977))                                                        \
   {                                                                                      \
      buf_len = xroad_format(buf, buf_len, "%P", name1977);                               \
   }                                                                                      \
   else                                                                                   \
   {                                                                                      \
      buf_len = xroad_format(buf, buf_len, "%P.%P", name1977, cls1977);                   \
   }                                                                                      \
   xroad_str_len(buf, buf_len);                                                           \
})

/**
 * instrument object - a cache for xroad_instrdb_t objects
 */
typedef struct instrdb_s instrdb_t;

/**
 * create new instr object, according to configuration
 * @return pointer to created instrdb_t object. NULL - error happens
 */
instrdb_t* instrdb_create(xroad_xml_tag_t cfg);

/**
 * reconfigure, rebuild cache
 * @param[in] idb   - lib to reload
 * @param[in] cfg   - configuration
 * @return XROAD_OK - reloaded, else failed
 */
xroad_errno_t instrdb_reconfig(instrdb_t* idb, xroad_xml_tag_t cfg);

/**
 * destroy instr object
 * @param[in] idb - object to destroy. If NULL, nothing happened
 */
void instrdb_destroy(instrdb_t* idb);

/**
 * search instrument by alias
 * @param[in] idb   - cache with instruments
 * @param[in] alias - alias for search
 * @return pointer to instr, NULL - not found
 */
xroad_instr_t* instrdb_get_by_alias(instrdb_t* idb, xroad_str_t alias);

/**
 * search instrument by name
 * @param[in] idb  - cache with instrs
 * @param[in] name - name for search
 * @param[in] cls  - class for search
 * @return pointer to instr, NULL - not found
 */
xroad_instr_t* instrdb_get_by_name(instrdb_t* idb, xroad_str_t name, xroad_str_t cls);

/**
 * search instrument by long name
 * @param[in] idb   - cache with instrs
 * @param[in] lname - long name for search
 * @return pointer to instr, NULL - not found
 */
xroad_instr_t* instrdb_get_by_long_name(instrdb_t* idb, xroad_str_t lname);

/**
 * search instrument by name
 * @param[in] idb  - cache with instrs
 * @param[in] id - id of instrument
 * @return pointer to instr, NULL - not found
 */
xroad_instr_t* instrdb_get_by_id(instrdb_t* idb, xroad_object_id_t id);

/**
 * search instrument by exchange id
 * @param[in] idb  - cache with instrs
 * @param[in] id - exchange id of instrument
 * @return pointer to instr, NULL - not found
 */
xroad_instr_t* instrdb_get_by_exch_id(instrdb_t* idb, xroad_object_id_t id);

/**
 * create new instrument or return existing
 * @param[in] idb   - cache with instrs
 * @param[in] alias - instrument alias
 * @param[in] name  - instrument name (exchange name)
 * @param[in] long_name - instrument long name (exchange name)
 * @param[in] cls   - instrument class, if any
 */
xroad_instr_t* instrdb_add(instrdb_t* idb, xroad_str_t alias, xroad_str_t name, xroad_str_t long_name, xroad_str_t cls);

#ifdef __cplusplus
}
#endif
