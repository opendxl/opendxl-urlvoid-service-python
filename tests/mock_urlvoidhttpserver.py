import socket
import re

try: #Python 3
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer
except ImportError: #Python 2.7
    from SimpleHTTPServer import  SimpleHTTPRequestHandler
    from SocketServer import TCPServer

from threading import Thread

import requests

from dxlbootstrap.util import MessageUtils
from dicttoxml import dicttoxml #pylint: disable=import-error
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

    #pylint: disable=line-too-long
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

        if re.search(SAMPLE_API_KEY, self.path):
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
            response_content = "Test Failure Message - API Key not found"

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

    def __init__(self):
        self.server_name = "mockserver"
        self.mock_server_port = 0
        self.mock_server = None
        self.mock_server_address = ""

    def __enter__(self):
        self.mock_server_address, self.mock_server_port = get_free_port()
        self.mock_server = TCPServer(
            ('localhost', self.mock_server_port),
            MockVtServerRequestHandler
        )

        mock_server_thread = Thread(target=self.mock_server.serve_forever)
        mock_server_thread.setDaemon(True)
        mock_server_thread.start()

        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mock_server.shutdown()
