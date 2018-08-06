from dxlurlvoidservice import UrlVoidApiService
from tests.mock_urlvoidhttpserver import MockServerRunner
from tests.test_base import *
from tests.test_service import create_service_configfile
from tests.test_value_constants import *


def configure_service(port):

    create_service_configfile(
        config_file_name=URLVOID_CONFIG_FILENAME
    )

    urlvoid_service = UrlVoidApiService(TEST_FOLDER)

    urlvoid_service.URL_VOID_API_URL_FORMAT = "http://127.0.0.1:" \
          + str(port) \
          + "/api1000/{0}/"

    urlvoid_service.run()

    return urlvoid_service


class TestSamples(BaseClientTest):

    def test_hostinfo_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_host_info.py"

        with MockServerRunner() as mock_server:

            configure_service(mock_server.mock_server_port)

            mock_print = self.run_sample(sample_filename)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_HOST_INFO["page_load"]))
            )


    def test_hostrescan_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_host_rescan.py"

        with MockServerRunner() as mock_server:

            configure_service(mock_server.mock_server_port)

            mock_print = self.run_sample(sample_filename)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_HOST_RESCAN["page_load"]))
            )


    def test_hostscan_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_host_scan.py"

        with MockServerRunner() as mock_server:
            configure_service(mock_server.mock_server_port)

            mock_print = self.run_sample(sample_filename)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_HOST_SCAN["page_load"]))
            )


    def test_statsremained_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_stats_remained.py"

        with MockServerRunner() as mock_server:

            configure_service(mock_server.mock_server_port)

            mock_print = self.run_sample(sample_filename)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_REMAINED_OUTPUT["page_load"]))
            )
