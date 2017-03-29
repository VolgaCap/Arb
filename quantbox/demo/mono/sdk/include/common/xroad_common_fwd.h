/**
 * @file   xroad_common_fwd.h
 * @author Dmitry S. Melnikov, dmitryme@gmail.com
 */

#pragma once

#ifdef __cplusplus
extern "C"
{
#endif

///@{ see common/xroad_hash.h for details
typedef struct xroad_hash_s xroad_hash_t;
typedef struct xroad_hash_entry_s xroad_hash_entry_t;
///@}

///@{ see common/xroad_list.h for deaails
typedef struct xroad_list_s xroad_list_t;
typedef struct xroad_list_entry_s xroad_list_entry_t;
///@}

///@{ see common/xroad_xml.h for deatails
typedef struct _xmlNode* xroad_xml_tag_t;
typedef struct xroad_xml_doc_s xroad_xml_doc_t;
///@}

///@{ see common/xroad_vector.h for details
typedef struct xroad_vector_s xroad_vector_t;
///@}

///@{ see common/xroad_string.h for details
typedef struct xroad_str_s xroad_str_t;
typedef struct xroad_str_fixed_s xroad_str_fixed_t;
///@}

///@{ see common/xroad_heap.h for details
typedef struct xroad_heap_s xroad_heap_t;
///@}

///@{ see common/xroad_ev_queue.h for details
typedef struct xroad_ev_queue_s xroad_ev_queue_t;
///@}

///@{ see common/xroad_map.h for details
typedef struct xroad_map_s xroad_map_t;
typedef struct xroad_map_entry_s xroad_map_entry_t;
///@}

///@{ see common/xroad_timer.h for details
typedef struct timer_s xroad_timer_t;
///@}

#ifdef __cplusplus
}
#endif
