import logging
import logging.handlers

KAMAILIO_SUCCESS_CODE = 1
KAMAILIO_ERROR_CODE = -1

SIP_AUTH_SUCCESS_CODE = 200
SIP_AUTH_ERROR_CODE = 403

MAX_LOG_SIZE_BYTES = 10000000
LOG_FILE_BACKUP_COUNT = 10

# Must return:
# >0 for sucess
# 0 to stop further processing (like exit() in kamailio.cfg)
# <0 for error

def get_logger(module_name, debug_level = logging.DEBUG):
    logger = logging.getLogger(module_name)
    logger.setLevel(debug_level)
    fh = logging.handlers.RotatingFileHandler(
        f'/var/log/{module_name}.log',
        mode='a',
        maxBytes=MAX_LOG_SIZE_BYTES,
        backupCount=LOG_FILE_BACKUP_COUNT
    )
    fh.setLevel(debug_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def log_back_to_kamailio(logger_obj, msg_to_log):
    try:
        full_log_msg = f'[py_kamailio] {msg_to_log}\n'
        if logger_obj:
            logger_obj.call_function('xlog', '$var(debug_level)', full_log_msg)
    except Exception as e:
        print(f"ERROR while logging back to Kamailio. You should never see this message: {e}")
