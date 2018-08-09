import sys
from configparser import ConfigParser
from dxlbootstrap.util import MessageUtils
from dxlclient import Request
from dicttoxml import dicttoxml #pylint: disable=import-error
from dxlurlvoidservice import UrlVoidApiService
from dxlurlvoidservice.requesthandlers import UrlVoidApiCallback

from tests.test_base import BaseClientTest
from tests.test_value_constants import *
from tests.mock_urlvoidhttpserver import MockServerRunner

sys.path.append(
    os.path.dirname(os.path.abspath(__file__)) + "/../.."
)

def create_service_configfile(config_file_name):
    config = ConfigParser()

    config['General'] = {'apiKey': SAMPLE_API_KEY}

    with open(config_file_name, 'w') as config_file:
        config.write(config_file)


class TestConfiguration(BaseClientTest):

    def test_loadconfig(self):

        create_service_configfile(
            config_file_name=URLVOID_CONFIG_FILENAME,
        )

        urlvoid_service = UrlVoidApiService(TEST_FOLDER)
        urlvoid_service._load_configuration()

        self.assertEqual(urlvoid_service.api_key, SAMPLE_API_KEY)

        os.remove(URLVOID_CONFIG_FILENAME)


    def test_registerservices(self):
        with MockServerRunner():
            with self.create_client(max_retries=0) as dxl_client:
                dxl_client.connect()

                urlvoid_service = UrlVoidApiService(TEST_FOLDER)
                urlvoid_service._dxl_client = dxl_client

                create_service_configfile(
                    config_file_name=URLVOID_CONFIG_FILENAME
                )

                urlvoid_service._load_configuration()
                urlvoid_service.on_register_services()

                self.assertTrue(len(urlvoid_service._services) == 1)

                expected_topics = (
                    UrlVoidApiService.REQ_TOPIC_HOST_INFO,
                    UrlVoidApiService.REQ_TOPIC_HOST_RESCAN,
                    UrlVoidApiService.REQ_TOPIC_HOST_SCAN,
                    UrlVoidApiService.REQ_TOPIC_STATS_REMAINED
                )

                self.assertEqual(
                    sorted(expected_topics),
                    sorted(urlvoid_service._services[0].topics)
                )


class TestVtRequestCallback(BaseClientTest):

    def test_validate_params(self):
        test_params = ["test", "required", "parameters"]
        urlvoid_callback = UrlVoidApiCallback(None, required_params=test_params)

        test_req_dict = {
            "test": True,
            "required": True,
            "parameters": True
        }

        # Expected to raise an exception if there is a mismatch, so no need to assert
        urlvoid_callback._validate(test_req_dict)

        test_req_dict = {
            "test": True,
            "parameters": True
        }

        self.assertRaisesRegex(
            Exception,
            r"Required parameter not specified: ",
            urlvoid_callback._validate,
            test_req_dict,
        )

        test_req_dict = {
            "test": True,
            "required": True,
            "parameters": True,
            "false": True
        }

        # Expected to raise an exception if there is a mismatch, so no need to assert
        urlvoid_callback._validate(test_req_dict)

        test_req_dict = {
            "test": True,
            "required": True,
            "false": True
        }

        self.assertRaisesRegex(
            Exception,
            r"Required parameter not specified: ",
            urlvoid_callback._validate,
            test_req_dict,
        )

    def test_callback_hostinfo(self):
        with MockServerRunner() as server_runner:
            with self.create_client(max_retries=0) as dxl_client:
                dxl_client.connect()

                urlvoid_service = UrlVoidApiService(TEST_FOLDER)
                urlvoid_service._dxl_client = dxl_client

                urlvoid_service.URL_VOID_API_URL_FORMAT = "http://127.0.0.1:" \
                                              + str(server_runner.mock_server_port) \
                                              + "/api1000/{0}/"

                urlvoid_service._load_configuration()
                urlvoid_service.on_register_services()

                request_topic = UrlVoidApiService.REQ_TOPIC_HOST_INFO
                req = Request(request_topic)
                MessageUtils.dict_to_json_payload(
                    req,
                    {
                        UrlVoidApiCallback.PARAM_HOST: SAMPLE_HOST
                    }
                )

                res = dxl_client.sync_request(req, timeout=30)

                self.assertEqual(
                    dicttoxml(
                        SAMPLE_HOST_INFO,
                        custom_root=XML_ROOT_RESPONSE,
                        attr_type=False
                    ),
                    res.payload
                )


    def test_callback_hostrescan(self):
        with MockServerRunner() as server_runner:
            with self.create_client(max_retries=0) as dxl_client:
                dxl_client.connect()

                urlvoid_service = UrlVoidApiService(TEST_FOLDER)
                urlvoid_service._dxl_client = dxl_client

                urlvoid_service.URL_VOID_API_URL_FORMAT = "http://127.0.0.1:" \
                                              + str(server_runner.mock_server_port) \
                                              + "/api1000/{0}/"

                urlvoid_service._load_configuration()
                urlvoid_service.on_register_services()

                request_topic = UrlVoidApiService.REQ_TOPIC_HOST_RESCAN
                req = Request(request_topic)
                MessageUtils.dict_to_json_payload(
                    req,
                    {
                        UrlVoidApiCallback.PARAM_HOST: SAMPLE_HOST
                    }
                )

                res = dxl_client.sync_request(req, timeout=30)

                self.assertEqual(
                    dicttoxml(
                        SAMPLE_HOST_RESCAN,
                        custom_root=XML_ROOT_RESPONSE,
                        attr_type=False
                    ),
                    res.payload
                )

    def test_callback_hostscan(self):
        with MockServerRunner() as server_runner:
            with self.create_client(max_retries=0) as dxl_client:
                dxl_client.connect()

                urlvoid_service = UrlVoidApiService(TEST_FOLDER)
                urlvoid_service._dxl_client = dxl_client

                urlvoid_service.URL_VOID_API_URL_FORMAT = "http://127.0.0.1:" \
                                              + str(server_runner.mock_server_port) \
                                              + "/api1000/{0}/"

                urlvoid_service._load_configuration()
                urlvoid_service.on_register_services()

                request_topic = UrlVoidApiService.REQ_TOPIC_HOST_SCAN
                req = Request(request_topic)
                MessageUtils.dict_to_json_payload(
                    req,
                    {
                        UrlVoidApiCallback.PARAM_HOST: SAMPLE_HOST
                    }
                )

                res = dxl_client.sync_request(req, timeout=30)

                self.assertEqual(
                    dicttoxml(
                        SAMPLE_HOST_SCAN,
                        custom_root=XML_ROOT_RESPONSE,
                        attr_type=False
                    ),
                    res.payload
                )

    def test_callback_statsremained(self):
        with MockServerRunner() as server_runner:
            with self.create_client(max_retries=0) as dxl_client:
                dxl_client.connect()

                urlvoid_service = UrlVoidApiService(TEST_FOLDER)
                urlvoid_service._dxl_client = dxl_client

                urlvoid_service.URL_VOID_API_URL_FORMAT = "http://127.0.0.1:" \
                                              + str(server_runner.mock_server_port) \
                                              + "/api1000/{0}/"

                urlvoid_service._load_configuration()
                urlvoid_service.on_register_services()

                request_topic = UrlVoidApiService.REQ_TOPIC_STATS_REMAINED
                req = Request(request_topic)
                MessageUtils.dict_to_json_payload(
                    req,
                    {
                        UrlVoidApiCallback.PARAM_HOST: SAMPLE_HOST
                    }
                )

                res = dxl_client.sync_request(req, timeout=30)

                self.assertEqual(
                    dicttoxml(
                        SAMPLE_REMAINED_OUTPUT,
                        custom_root=XML_ROOT_RESPONSE,
                        attr_type=False
                    ),
                    res.payload
                )
