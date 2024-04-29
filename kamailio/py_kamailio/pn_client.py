import json
import datetime
from requests import post, delete
import sys
from utils import get_logger, KAMAILIO_SUCCESS_CODE


PN_TYPE = 'pn-type'
PN_TOK = 'pn-tok'
PN_UUID='+sip.instance="<urn:uuid:'

PN_TYPE_APPLE = 'ios'
PN_TYPE_FB = 'android'

SIP_INSTANCE_STR = '>;+sip.instance='

NO_PN_LOG_MSG = "No PN detected"


logger = get_logger('pn_client')

class PnClient:
    def __init__(self, parser, rest_handler):
        logger.info("PnClient.__init__() called, id: {}".format(id(self)))
        self.start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.parser = parser
        self.rest_handler = rest_handler

    def child_init(self, rank):
        logger.debug("PnClient.child_init() called with rank {}, id {}, time {}".format(rank, id(self), self.start_date))
        return 0

    # CLEAN CONTACT HEADER
    def handler_clean_contact(self, msg, args):
        try:
            self.clean_contact(msg, args)

        except Exception as e:
            logger.exception(e)

            if msg:
                err_msg = '[ERROR] handler_clean_contact: {}'.format(e)
                self.log_back_to_kamailio(msg, err_msg)

        return KAMAILIO_SUCCESS_CODE


    def clean_contact(self, msg, args):
        logger.debug("clean_contact START (PnClient id: {})".format(id(self)))

        contact_header = msg.getHeader('contact')
        contact_clean = self.parser.clean_contact(contact_header)
        logger.info('Contact after clean: {}'.format(contact_clean))

        msg.call_function('append_hf', 'Contact: {}\n'.format(contact_clean))
        self.log_back_to_kamailio(msg, 'Contact after clean: {}'.format(contact_clean))

    # REGISTER PN TOKEN
    def handler_register_pn_token(self, msg, args):
        try:
            self.register_pn_token(msg, args)

        except Exception as e:
            logger.exception(e)
            if msg:
                err_msg = 'ERROR in register_pn_token: {}'.format(e)
                self.log_back_to_kamailio(msg, err_msg)

        return KAMAILIO_SUCCESS_CODE

    def register_pn_token(self, msg, args):
        logger.info("register_pn  START (PnClient started at: {})".format(self.start_date))

        username = self.parser.fetch_username(msg.getHeader('from'))
        auth_user = args
        contact_header = msg.getHeader('contact')
        pn_type = self.parser.check_pn_type(contact_header)

        if not pn_type:
            self.log_back_to_kamailio(msg, NO_PN_LOG_MSG)
            logger.info("register_pn: no PN info detected for {}".format(username))
            return

        token_parsed_info = self.parser.fetch_token_from_contact(contact_header)

        pn_data = self.rest_handler.build_register_pn_content(username, auth_user, token_parsed_info['pn-tok'], pn_type, token_parsed_info['pn-uuid'])
        response = self.rest_handler.register_pn(pn_data)

        pn_info_log_msg = 'pn-type: {}, token[:10]: {}, uuid[:10]: {}'.format(token_parsed_info[PN_TYPE], token_parsed_info[PN_TOK][:10], token_parsed_info['pn-uuid'][:10])
        log_msg = 'register_pn: [{}, {}, {}] responses: {}'.format(username, auth_user, pn_info_log_msg, response if response else 'n/a')

        logger.info(log_msg)
        self.log_back_to_kamailio(msg, log_msg)

    # TRIGGER PN
    def handler_trigger_pn(self, msg, args):
        try:
            # do some stuff
            self.trigger_pn(msg, args)

        except Exception as e:
            logger.exception(e)
            if msg:
                err_msg = 'ERROR in register_pn_token: {}'.format(e)
                self.log_back_to_kamailio(msg, err_msg)

        return KAMAILIO_SUCCESS_CODE

    def trigger_pn(self, msg, args):
        logger.info("trigger_pn  START (PnClient started at: {})".format(self.start_date))

        to_number = args
        call_id = args


        pn_data = self.rest_handler.build_trigger_pn_content(to_number, call_id)
        response = self.rest_handler.trigger_pn(pn_data)

        log_msg = 'trigger_pn: [{}, {}] responses: {}'.format(to_number, call_id, response if response else 'n/a')

        logger.info(log_msg)
        self.log_back_to_kamailio(msg, log_msg)

    # DELETE PN TOKEN
    def handler_delete_token(self, msg, args):
        try:
            self.delete_token(msg, args)
        except Exception as e:
            logger.exception(e)
            if msg:
                err_msg = 'ERROR in delete_token: {}'.format(e)
                self.log_back_to_kamailio(msg, err_msg)

        return KAMAILIO_SUCCESS_CODE

    def delete_token(self, msg, args):
        logger.info("delete_token  START (PnClient started at: {})".format(self.start_date))

        auth_user = args

        pn_data = self.rest_handler.build_delete_token_content(auth_user)
        response = self.rest_handler.delete_token(pn_data)

        log_msg = 'delete_token: [{}] responses: {}'.format(auth_user, response if response else 'n/a')

        logger.info(log_msg)
        self.log_back_to_kamailio(msg, log_msg)

    def log_back_to_kamailio(self, logger_obj, msg_to_log):
        full_log_msg = '[PN.py] {} \n'.format(msg_to_log)
        if logger_obj:
            logger_obj.call_function('xlog', '$var(debug_level)', full_log_msg)

class PnHeaderParser:
    def check_pn_type(self, contact_header):
        if 'pn-type=apple' in contact_header or 'pn-provider=apns' in contact_header:
            return PN_TYPE_APPLE
        elif 'pn-type=firebase' in contact_header or 'pn-provider=fcm' in contact_header:
            return PN_TYPE_FB
        else:
            return None

    def fetch_username(self, from_header):
        start='<sip:'
        end = '@'
        from_header_front_cut = from_header.split(start)[1]
        from_header_final = from_header_front_cut.split(end)[0]
        return from_header_final

    def clean_contact(self, contact_h):
        pn_type = self.check_pn_type(contact_h)
        if not pn_type:
            return contact_h

        contact_parts = contact_h.split(SIP_INSTANCE_STR)

        part_to_clean = contact_parts[0]
        elems = part_to_clean.split(';')
        user_part = elems[0]
        transport_part = elems[-1]

        #clean_contact_header = '{};{}{}{}'.format(user_part, transport_part, SIP_INSTANCE_STR, constant_part)
        clean_contact_header = '{0};{1}>'.format(user_part, transport_part)

        return clean_contact_header

    def fetch_token_from_contact(self, contact_header):
        result_dict = dict()
        result_dict[PN_TYPE] = self.check_pn_type(contact_header)

        header_contact_params = contact_header[1:-1].split(';')

        for param in header_contact_params:
            if param.startswith(PN_TOK):
                # FB and Apple v1
                result_dict[PN_TOK] = param[len(PN_TOK) + 1:]
            elif param.startswith(PN_UUID):
                result_dict['pn-uuid'] = param[len(PN_UUID) :-1].replace('>', '')
            elif param.startswith('pn-prid='):
                if ':voip' in param:
                    splited_token = param[8:].split('&')
                    for token in splited_token:
                        if ':voip' in token:
                            result_dict[PN_TOK] = token.replace(':voip', '')
                else:
                    # FB v2
                    result_dict[PN_TOK] = param[8:]

        if PN_TOK not in result_dict:
            raise Exception("Unable to fetch token from header: {}".format(contact_header))

        return result_dict

class PnRestHandler:
    def __init__(self, http_handler, pn_register_addresses, pn_trigger_addresses):
        self.http_handler = http_handler
        self.pn_register_addresses = pn_register_addresses
        self.pn_trigger_addresses = pn_trigger_addresses

        register_endpoint_format = 'https://{}/api/v1/push-devices/'
        trigger_endpoint_format = 'https://{}/api/v1/push-devices/send/'

        self.register_urls = []
        for pn_register_addr in self.pn_register_addresses:
            self.register_urls.append(register_endpoint_format.format(pn_register_addr))

        self.trigger_urls = []
        for pn_trigger_addr in self.pn_trigger_addresses:
            self.trigger_urls.append(trigger_endpoint_format.format(pn_trigger_addr))



    def build_register_pn_content(self, username, auth_user, token, pn_type, uuid):
        pn_data = {
            "phoneNumber": username,
            "deviceToken": token,
            "system": pn_type,
            "uuid": uuid,
            "deviceName" : auth_user
        }
        return pn_data

    def build_trigger_pn_content(self, to_number, call_id):
        pn_data = {
            "toNumber": to_number,
            "callId": call_id
        }
        return pn_data

    def build_delete_token_content(self, auth_user):
        pn_data = {
            "device_name" : auth_user
        }
        return pn_data

    def register_pn(self, pn_data):
        # We want to trigger ALL endpoints with same data
        responses = dict()
        for url in self.register_urls:
            try:
                response = self.http_handler.send_http_post(url, pn_data, timeout=5)
                responses[url] = response
            except Exception as e:
                responses[url] = 'EXCEPTION: {0}'.format(e)
        return responses

    def trigger_pn(self, pn_data):

        # We want to stop after first successful response
        for url in self.trigger_urls:
            response = None
            try:
                response = self.http_handler.send_http_post(url, pn_data, timeout=3)
                if 200 <= response.status_code <=299:
                    logger.info("PN Trigger to {} SUCCESS response code {}".format(url, response.status_code))
                    return response
                else:
                    logger.info("PN Trigger to {} failed with code {}".format(url, response.status_code))
            except Exception as e:
                if response:
                    logger.info("EXCEPTION: PN Trigger to {} failed with code {}".format(url, response.status_code))
                else:
                    logger.info('EXCEPTION: {0}'.format(e))

        ### If we are here, means that none of PNS enspoints worked.
        # raise Exception("None of PNS Endpoints worked.")

    def delete_token(self, pn_data):
        # We want to trigger ALL endpoints with same data
        responses = dict()
        for url in self.register_urls:
            try:
                response = self.http_handler.send_http_delete(url, pn_data, timeout=5)
                responses[url] = response
            except Exception as e:
                responses[url] = 'EXCEPTION: {0}'.format(e)
        return responses

class HttpHandler:
    def send_http_post(self, url, json_content, timeout=None):
        response = post(
                    url,
                    data = json.dumps(json_content),
                    headers={ 'Accept': 'application/json', 'Content-Type': 'application/json' },
                    verify=False,
                    timeout=timeout
                )

        return response

    def send_http_delete(self, url, json_content, timeout=None):
        response = delete(
                    url,
                    data = json.dumps(json_content),
                    headers={ 'Accept': 'application/json', 'Content-Type': 'application/json' },
                    verify=False,
                    timeout=timeout
                )

        return response

def mod_init():
    logger.debug("mod_init() called, returning PnClient, dir {}".format(dir()))

    parser = PnHeaderParser()
    rest_handler = PnRestHandler(
        HttpHandler(),
        ['localhost'],
        ['localhost'],
    )
    return PnClient(parser, rest_handler)

def trigger_pn_standalone(to_number, call_id):
    logger.debug("trigger_pn_standalone")

    rest_handler = PnRestHandler(
        HttpHandler(),
        ['localhost'],
        ['localhost'],
    )
    pn_trigger_data = rest_handler.build_trigger_pn_content(to_number, call_id)
    return rest_handler.trigger_pn(pn_trigger_data)

if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 3:
        logger.info("This is PN Trigger script called with args: {}, {}".format(args[1], args[2]))
        to_number = args[1]
        call_id = args[2]
        result = trigger_pn_standalone(to_number, call_id)
        logger.info("Result is: {}".format(result if result else 'n/a'))
    else:
        logger.error("This script should be executed with 2 args: to_number and call_id. Got {}".format(args))
