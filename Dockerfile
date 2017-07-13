# Base image from Python 2.7 (alpine)
FROM python:2.7-alpine

# Install required packages
RUN pip install "requests"
RUN pip install "dxlbootstrap"
RUN pip install "dxlclient"

# Copy application files
COPY . /tmp/build
WORKDIR /tmp/build

# Clean application
RUN python ./clean.py

# Build application
RUN python ./setup.py bdist_wheel

# Install application
RUN pip install dist/*.whl

# Cleanup build
RUN rm -rf /tmp/build

################### INSTALLATION END #######################
#
# Run the service.
#
# NOTE: The configuration files for the service must be
#       mapped to the path: /opt/dxlurlvoidservice-config
#
# For example, specify a "-v" argument to the run command
# to mount a directory on the host as a data volume:
#
#   -v /host/dir/to/config:/opt/dxlurlvoidservice-config
#
CMD ["python", "-m", "dxlurlvoidservice", "/opt/dxlurlvoidservice-config"]
