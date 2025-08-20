import logging
from typing import List, Dict, Any


__all__ = []

def safe_get_list(buckets: List[Dict], mapping: Dict[str, list], log_prefix="parse_data_fields",soft_errors = True) -> List[Dict[str, Any]]:
    final_list = []
    if buckets:
        for count, bucket in enumerate(buckets):
            entry = {}
            
            current = bucket
            for key,f_path in mapping.items():
                rem_path = f_path.copy()
                for path in f_path:
                    if not isinstance(current, dict):
                        if not soft_errors:  
                            logging.error(f"[{log_prefix}] At index {count}, expected dict but got {type(current)} at key '{key}'", extra={"data": str(current)})
                            current = None
                        break
                    if path not in current:
                        if not soft_errors:
                            logging.error(f"[{log_prefix}] At index {count}, missing key '{key}'", extra={"data": str(current)})
                            current = None
                        break
                    
                    if isinstance(current[path], list):
                        rem_path.pop(0)
                        intermediate = safe_get_list(current[path],rem_path[0],log_prefix="parse_nested_data_fields")
                        
                        current = {}
                        for dict_ind in intermediate:
                            for dict_key,dict_value in dict_ind.items():
                                if dict_key not in current:
                                    current[dict_key] = [dict_value]
                                else:
                                    current[dict_key].extend([dict_value])

                        current = str(current)
                        break

                    else:
                        current = current[path]
                        rem_path.pop(0)

                entry[key] = current
                
                current = bucket
            final_list.append(entry)
    else:
        return []
    return final_list