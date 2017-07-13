Running Service
===============

Once the URLVoid DXL Service has been installed and the configuration files are populated it can be started by
executing the following command line:

    .. parsed-literal::

        python -m dxlurlvoidservice <configuration-directory>

    The ``<configuration-directory>`` argument must point to a directory containing the configuration files
    required for the URLVoid DXL Service (see :doc:`configuration`).

For example:

    .. parsed-literal::

        python -m dxlurlvoidservice config

Output
------

The output from starting the service should appear similar to the following:

    .. parsed-literal::

        Running application ...
        On 'run' callback.
        On 'load configuration' callback.
        Incoming message configuration: queueSize=1000, threadCount=10
        Message callback configuration: queueSize=1000, threadCount=10
        Attempting to connect to DXL fabric ...
        Connected to DXL fabric.
        Registering service: urlvoidservice
        Registering request callback: host/info
        Registering request callback: host/rescan
        Registering request callback: host/scan
        Registering request callback: stats/remained
        On 'DXL connect' callback.