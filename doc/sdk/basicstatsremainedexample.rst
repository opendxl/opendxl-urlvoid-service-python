Basic Stats Remained Example
============================

This sample retrieves and displays the number of queries that remain for the account associated with the
URLVoid API key by invoking the URLVoid API service via DXL.



For more information see:
    http://api.urlvoid.com/dashboard/#usage

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The URLVoid API DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_stats_remained.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_stats_remained.py

The output should appear similar to the following:

    .. code-block:: xml

        Response for URLVoid stats remained:
        <?xml version="1.0" encoding="UTF-8"?><response>
            <queriesRemained>956</queriesRemained>
            <page_load>0.00</page_load>
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

            # Invoke 'stats remained' method
            request_topic = "/opendxl-urlvoid/service/urlvapi/stats/remained"

            req = Request(request_topic)

            res = client.sync_request(req, timeout=60)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                payload = MessageUtils.decode_payload(res)
                xml = xml.dom.minidom.parseString(payload)
                print("Response for URLVoid stats remained:")
                print(xml.toprettyxml(
                    indent='    ', newl='', encoding="UTF-8").decode("UTF-8"))
            else:
                print("Error invoking service with topic '{0}': {1} ({2})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "stats remained" method
of the URLVoid API DXL service.

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are displayed.
