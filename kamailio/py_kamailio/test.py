import requests_oauthlib
import pn_client

from utils import get_logger, log_back_to_kamailio, KAMAILIO_SUCCESS_CODE, KAMAILIO_ERROR_CODE

MODULE_NAME = 'main_kamailio'
logger = get_logger(MODULE_NAME)

class PyKamailio:
    def __init__(self):
        self.pn = pn_client.mod_init()

        self.pn_clean_contact = self.pn.handler_clean_contact
        self.pn_register_pn_token = self.pn.handler_register_pn_token
        self.pn_trigger_pn = self.pn.handler_trigger_pn
        self.pn_delete_token = self.pn.handler_delete_token

    def child_init(self, rank):
        """
        Executed by app_python module when a new worker process (child)
        is initialized by Kamailio.
        """
        return 1

def mod_init():
    """
    Executed by app_python module when it is initialized by Kamailio.
    """
    return PyKamailio()
