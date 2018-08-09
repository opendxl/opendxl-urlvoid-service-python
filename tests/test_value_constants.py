import os

TEST_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))
URLVOID_CONFIG_FILENAME = TEST_FOLDER + "/dxlurlvoidservice.config"

SAMPLE_API_KEY = '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
HTTP_ERROR_SERVER_PATH = "/test/http/error"

SAMPLE_HOST = '027.ru'

XML_ROOT_RESPONSE = 'response'

SAMPLE_HOST_INFO = {
    "details": {
        "host": SAMPLE_HOST,
        "updated": 1525450716,
        "http_response_code": 0,
        "domain_age": 1134018000,
        "google_page_rank": 0,
        "alexa_rank": 0,
        "connect_time": 0,
        "header_size": 0,
        "download_size": 0,
        "speed_download": 0,
        "external_url_redirect": None,
        "ip" : {
            "addr": "185.53.177.31",
            "hostname": None,
            "asn": 61969,
            "asname": "Team Internet AG",
            "country_code": "DE",
            "region_name": None,
            "city_name": None,
            "continent_code": "EU",
            "continent_name": "Europe",
            "latitude": 51.2993,
            "longitude": 9.491
        }
    },
    "detections": {
        "engines": [
            "MyWOT",
            "SCUMWARE",
            "Avira"
        ],
        "count": 3,
    },
    "page_load": 1.11
}

SAMPLE_HOST_RESCAN = {
    "details": SAMPLE_HOST_INFO["details"],
    "detections": SAMPLE_HOST_INFO["detections"],
    "action_result": "OK",
    "page_load": 2.22
}

SAMPLE_HOST_SCAN = {
    "details": SAMPLE_HOST_INFO["details"],
    "detections": SAMPLE_HOST_INFO["detections"],
    "action_result": "OK",
    "page_load": 3.33
}

SAMPLE_REMAINED_OUTPUT = {
    "queriesRemained": 997,
    "page_load": 4.44
}
