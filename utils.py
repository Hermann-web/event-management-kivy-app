import traceback
from config.config import logging 


def parse_mongo_obj_to_json_serializable(list_obj):
    list_obj = list(list_obj)
    for c in list_obj:
        c['_id'] = str(c['_id'])
    return list_obj

def log_exception(err, action):
    detail_ = f"--> action: {action}\n err: {err}"
    error_message = "EXCEPTION:\n" + detail_
    exception_details = traceback.format_exc()
    logging.error(f"An exception occurred: {error_message}")
    logging.error(f"Exception details:\n{exception_details}")

def catch_exceptions(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logging.debug(f"function call: {func_name}")
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logging.info(f"function details: name={func_name} args={args} kwargs={kwargs}")
            log_exception(err=e, action=f"wrapping {func_name} exceptions (RETURNING NONE): \nmodule:{func.__module__} \nannotations:{func.__annotations__} \ndocstring:{func.__doc__}")
            result = None
        return result
    return wrapper
