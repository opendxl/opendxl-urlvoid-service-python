import socket
import re
import time

try: #Python 3
    from http.server import HTTPServer, SimpleHTTPRequestHandler
except ImportError: #Python 2.7
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler

from threading import Thread

import requests

from dxlbootstrap.util import MessageUtils
from dicttoxml import dicttoxml
from dxlurlvoidservice import UrlVoidApiService
from dxlurlvoidservice.requesthandlers import UrlVoidApiCallback
from tests.test_value_constants import *

TEST_FOLDER = str(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"))
MOCK_EPOHTTPSERVER_CERTNAME = TEST_FOLDER + "/client.crt"
MOCK_EPOHTTPSERVER_KEYNAME = TEST_FOLDER + "/client.key"


def get_free_port():
    stream_socket = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    stream_socket.bind(('localhost', 0))
    address, port = stream_socket.getsockname()
    stream_socket.close()

    return address, port


class MockVtServerRequestHandler(SimpleHTTPRequestHandler):

    HEALTH_CHECK_PATH = "/healthcheck"

    BASE_PATTERN = "/api1000/" + SAMPLE_API_KEY + "/{0}"

    HOST_PATTERN = BASE_PATTERN.format(
        "{0}/{1}".format(
            UrlVoidApiCallback.PARAM_HOST,
            SAMPLE_HOST
        )
    )

    HOST_INFO_PATTERN = re.compile(HOST_PATTERN)

    HOST_RESCAN_PATTERN = re.compile("{0}/{1}".format(HOST_PATTERN, "rescan"))

    HOST_SCAN_PATTERN = re.compile("{0}/{1}".format(HOST_PATTERN, "scan"))

    STATS_REMAINED_PATTERN = re.compile(
        BASE_PATTERN.format(
            UrlVoidApiService.CMD_STATS_REMAINED
        )
    )

    HTTP_ERROR_PATTERN = re.compile(HTTP_ERROR_SERVER_PATH)

    def do_GET(self):

        response_code = requests.codes.ok #pylint: disable=no-member

        if self.path == self.HEALTH_CHECK_PATH:
            response_content = "".encode()
        elif re.search(SAMPLE_API_KEY, self.path):
            if re.search(self.HOST_RESCAN_PATTERN, self.path):
                response_content = self.host_rescan_cmd()

            elif re.search(self.HOST_SCAN_PATTERN, self.path):
                response_content = self.host_scan_cmd()

            elif re.search(self.HOST_INFO_PATTERN, self.path):
                response_content = self.host_info_cmd()

            elif re.search(self.STATS_REMAINED_PATTERN, self.path):
                response_content = self.stats_remained_cmd()

            elif re.search(self.HTTP_ERROR_PATTERN, self.path):
                response_code = requests.codes.internal_server_error #pylint: disable=no-member
                response_content = "500 - Internal Server Error"

            else:
                response_content = self.unknown_call(self.path)
        else:
            response_content = "Test Failure Message - API Key not found".encode()

        self.send_response(response_code, response_content)

        self.send_header('Content-Type', 'text/plain; charset=utf-8', )
        self.end_headers()

        self.wfile.write(response_content)


    @staticmethod
    def host_info_cmd():
        return dicttoxml(SAMPLE_HOST_INFO, custom_root=XML_ROOT_RESPONSE, attr_type=False)


    @staticmethod
    def host_rescan_cmd():
        return dicttoxml(SAMPLE_HOST_RESCAN, custom_root=XML_ROOT_RESPONSE, attr_type=False)


    @staticmethod
    def host_scan_cmd():
        return dicttoxml(SAMPLE_HOST_SCAN, custom_root=XML_ROOT_RESPONSE, attr_type=False)


    @staticmethod
    def stats_remained_cmd():
        return dicttoxml(SAMPLE_REMAINED_OUTPUT, custom_root=XML_ROOT_RESPONSE, attr_type=False)


    @staticmethod
    def unknown_call(path):
        return MessageUtils.dict_to_json(
            {
                "unit_test_error_unknown_host": path
            },
            pretty_print=False
        )


class MockServerRunner(object):

    SERVER_HOST = "localhost"
    SERVING_TIMEOUT = 60

    def __init__(self):
        self.mock_server_port = 0
        self.mock_server = None
        self.mock_server_address = ""
        self.mock_server_thread = None

    def __enter__(self):
        self.mock_server_address, self.mock_server_port = get_free_port()
        self.mock_server = HTTPServer(
            (self.SERVER_HOST, self.mock_server_port),
            MockVtServerRequestHandler
        )

        self.mock_server_thread = Thread(target=self.mock_server.serve_forever)
        self.mock_server_thread.setDaemon(True)
        self.mock_server_thread.start()

        serving_wait_end = time.time() + self.SERVING_TIMEOUT
        serving = False
        while not serving and time.time() < serving_wait_end:
            if requests.get("http://{}:{}{}".format(
                    self.SERVER_HOST,
                    self.mock_server_port,
                    MockVtServerRequestHandler.HEALTH_CHECK_PATH)).status_code == 200:
                serving = True

        if not serving:
            raise Exception(
                "Timed out waiting for mock server to start serving requests")

        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mock_server.shutdown()
        self.mock_server_thread.join()
        self.mock_server.server_close()
