from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import xml.dom.minidom

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlclient.message import Message, Request
from dxlbootstrap.util import MessageUtils

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    logger.info("Connected to DXL fabric.")

    # Invoke 'host info' method
    request_topic = "/opendxl-urlvoid/service/urlvapi/host/info"

    req = Request(request_topic)
    MessageUtils.dict_to_json_payload(req, {"host": "027.ru"})

    res = client.sync_request(req, timeout=60)
    if res.message_type != Message.MESSAGE_TYPE_ERROR:
        payload = MessageUtils.decode_payload(res)
        xml = xml.dom.minidom.parseString(payload)
        print("Response for URLVoid host info:")
        print(xml.toprettyxml(
            indent='    ', newl='', encoding="UTF-8").decode("UTF-8"))
    else:
        print("Error invoking service with topic '{0}': {1} ({2})".format(
            request_topic, res.error_message, res.error_code))
