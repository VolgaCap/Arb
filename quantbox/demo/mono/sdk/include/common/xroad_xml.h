/**
 * @file   xroad_xml.h
 * @author Danil Krivopustov, krivopustovda@gmail.com
 */

#pragma once

#include "xroad_common_fwd.h"
#include "xroad_string.h"
#include <stdint.h>
#include <libxml/parser.h>

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * parse xml file and validates it according scheme
 * @param[in] xml - path to the xml file
 * @param[in] xsd - optional path to the xsd scheme
 * @param[in] env - document with enviroment variabes. Can be NULL
 * @return pointer to new xml document, NULL - error
 */
xroad_xml_doc_t* xroad_xml_read_file(xroad_str_t xml, xroad_str_t xsd, xroad_xml_doc_t* env);

/**
 * parse xml string and validates it according scheme
 * @param[in] xml_data - xml string
 * @param[in] xsd - optional path to the xsd scheme
 * @param[in] env - document with environment variabes. Can be NULL
 * @return pointer to new xml document, NULL - error
 */
xroad_xml_doc_t* xroad_xml_read_memory(xroad_str_t xml_data, xroad_str_t xsd, xroad_xml_doc_t* env);

/**
 * destroy document and frees memory
 * @param[in] doc - pointer to the xml document. It NULL, nothing happened
 */
void xroad_xml_destroy(xroad_xml_doc_t* doc);

/**
 * get environment variable by name
 * @param[in] doc - xml document
 * @param[in] var - environment variable
 * @return variable value, xroad_str_null if no variable found
 */
xroad_str_t xroad_xml_get_variable(xroad_xml_doc_t* doc, xroad_str_t var);

/**
 * get the root tag of the xml document
 * @param[in] doc - pointer to the xml document
 * @return pointer to the xml tag, NULL - error
 */
xroad_xml_tag_t xroad_xml_get_root(xroad_xml_doc_t* doc);

/**
 * check if xml tag exists
 * @param[in] tag - pointer to the xml document
 * @param[in] path - path to the tag
 * @return 1 - exists, 0 - no such tag
 */
int32_t xroad_xml_has_tag(xroad_xml_tag_t tag, xroad_str_t path);

/**
 * get the tag of the xml document by its path
 * @param[in] tag - pointer to the xml document
 * @param[in] path - path to the tag
 * @return pointer to the xml tag, NULL - error
 */
xroad_xml_tag_t xroad_xml_get_tag(xroad_xml_tag_t tag, xroad_str_t path);

/**
 * get name of the xml tag
 * @param[in] tag - pointer to the xml tag
 * @return pointer to string, NULL - error
 */
xroad_str_t xroad_xml_get_name(xroad_xml_tag_t tag);

/**
 * get text of the xml tag
 * @param[in] tag - pointer to the xml tag
 * @return pointer to string, NULL - error
 */
xroad_str_t xroad_xml_get_text(xroad_xml_tag_t tag);

/**
 * get quantity of children of the xml tag parent
 * @param[in] tag - pointer to the xml tag
 * @return quantity of children
 */
uint32_t xroad_xml_get_children_count(xroad_xml_tag_t tag);

/**
 * get quantity of children of the xml tag parent
 * @param[in] tag - pointer to the xml tag
 * @param[in] path - path to the tag
 * @return quantity of children
 */
uint32_t xroad_xml_get_children_by_tag_count(xroad_xml_tag_t tag, xroad_str_t path);

/**
 * get first child of the xml tag parent
 * @param[in] tag - pointer to the xml tag
 * @param[in] child_name - name of first child tag
 * @return pointer to the xml tag, NULL - childfree node
 */
xroad_xml_tag_t xroad_xml_get_first(xroad_xml_tag_t tag, xroad_str_t child_name);

/**
 * find child of the xml tag parent
 * @param[in] tag - pointer to the xml tag
 * @param[in] child_name - name of next child tag
 * @return pointer to the xml tag, NULL - error
 */
xroad_xml_tag_t xroad_xml_get_next(xroad_xml_tag_t tag, xroad_str_t child_name);

/**
 * check if tag has attribute
 * @param[in] tag - pointer to the xml tag
 * @param[in] attribute - attribute name
 * @return 1 - exists, 0 - absent
 */
int32_t xroad_xml_has_attr(xroad_xml_tag_t tag, xroad_str_t attribute);

/**
 * get content as string of tag's attribute by its name
 * @param[in] tag - pointer to the xml tag
 * @param[in] attribute - attribute name
 * @return pointer to string, NULL - error
 */
xroad_str_t xroad_xml_get_attr_s(xroad_xml_tag_t tag, xroad_str_t attribute);

/**
 * get content as int32_t of tag's attribute by its name
 * @param[in] tag - pointer to the xml tag
 * @param[in] attribute - attribute name
 * @return integer value
 */
int32_t xroad_xml_get_attr_i(xroad_xml_tag_t tag, xroad_str_t attribute);

/**
 * get content as double of tag's attribute by its name
 * @param[in] tag - pointer to the xml tag
 * @param[in] attribute - attribute name
 * @return double value
 */
double xroad_xml_get_attr_d(xroad_xml_tag_t tag, xroad_str_t attribute);

/**
 * get content as bool of tag's attribute by its name
 * @param[in] tag - pointer to the xml tag
 * @param[in] attribute - attribute name
 * @return pointer to string, NULL - error
 */
int32_t xroad_xml_get_attr_b(xroad_xml_tag_t tag, xroad_str_t attribute);

#ifdef __cplusplus
}
#endif
