/**
 * @file   ui.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#include <common/xroad_xml.h>
#include <node_gen/xroad_objects.h>

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct ui_s ui_t;

/**
 * create library instance
 * @param[in] cfg - configuration
 * @return ui instance, NULL - in case of error
 */
ui_t* ui_create(xroad_xml_tag_t cfg);

/**
 * destroys library instance
 * @param[in] ui - library instance to destroy. If NULL, nothing happened
 */
void ui_destroy(ui_t* ui);

/**
 * gets field
 * @param[in] ui   - library instance
 * @param[in] id   - node id. if 0 current node id is used
 * @param[in] name - field name to find
 * @return pointer to field if any, NULL - field not found
 */
xroad_field_t* ui_get_field(ui_t* ui, xroad_node_id_t id, xroad_str_t name);

/**
 * gets field value as 32-bit integer
 * @param[in] ui   - library instance
 * @param[in] id   - node id. if 0 current node id is used
 * @param[in] name - field name
 * @return field value as integer
 */
int32_t ui_get_int32(ui_t* ui, xroad_node_id_t id, xroad_str_t name);

/**
 * gets field value as 64-bit integer
 * @param[in] ui   - library instance
 * @param[in] id   - node id. if 0 current node id is used
 * @param[in] name - field name
 * @return field value as integer
 */
int64_t ui_get_int64(ui_t* ui, xroad_node_id_t id, xroad_str_t name);

/**
 * gets field value as double
 * @param[in] ui   - library instance
 * @param[in] id   - node id. if 0 current node id is used
 * @param[in] name - field name
 * @return field value as double
 */
double ui_get_double(ui_t* ui, xroad_node_id_t id, xroad_str_t name);

/**
 * gets field value as string
 * @param[in] ui   - library instance
 * @param[in] id   - node id. if 0 current node id is used
 * @param[in] name - field name
 * @return field value as string
 */
xroad_str_t ui_get_str(ui_t* ui, xroad_node_id_t id, xroad_str_t name);

#ifdef __cplusplus
}
#endif
