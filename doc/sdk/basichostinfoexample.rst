Basic Host Info Example
=======================

This sample invokes and displays information about a specific website by invoking the URLVoid API service via DXL.

For more information see:
    http://api.urlvoid.com/dashboard/#usage

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The URLVoid API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_host_info.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_host_info.py

The output should appear similar to the following:

    .. code-block:: xml

        Response for URLVoid host info:
        <?xml version="1.0" encoding="UTF-8"?><response>
            <details>
                 <host>027.ru</host>
                 <updated>1499898632</updated>
                 <http_response_code>0</http_response_code>
                 <domain_age>1134018000</domain_age>
                 <google_page_rank>0</google_page_rank>
                 <alexa_rank>0</alexa_rank>
                 <connect_time>0</connect_time>
                 <header_size>0</header_size>
                 <download_size>0</download_size>
                 <speed_download>0</speed_download>
                 <external_url_redirect/>
                 <ip>
                    <addr>185.53.177.31</addr>
                    <hostname/>
                    <asn>61969</asn>
                    <asname>Team Internet AG</asname>
                    <country_code>DE</country_code>
                    <country_name>Germany</country_name>
                    <region_name/>
                    <city_name/>
                    <continent_code>EU</continent_code>
                    <continent_name>Europe</continent_name>
                    <latitude>51.2993</latitude>
                    <longitude>9.491</longitude>
                 </ip>
            </details>
            <detections>
                <engines>
                     <engine>MyWOT</engine>
                     <engine>SCUMWARE</engine>
                     <engine>Avira</engine>
                </engines>
                 <count>3</count>
            </detections>
            <page_load>0.01</page_load>
        </response>

The received results are displayed.

Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

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
                print "Response for URLVoid host info:"
                print xml.toprettyxml(indent='    ', newl='', encoding="UTF-8")
            else:
                print "Error invoking service with topic '{0}': {1} ({2})".format(
                    request_topic, res.error_message, res.error_code)


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "host info" method
of the URLVoid API DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `host`
to report on.

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are formatted and displayed.