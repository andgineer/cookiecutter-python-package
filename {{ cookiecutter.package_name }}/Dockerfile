FROM andgineer/python-base

ENV PYTHON_SOURCE=/app
ENV PYTHONPATH="$PYTHON_SOURCE:$PYTHONPATH"

# Local-specific script to set up corporate proxy etc
ARG SSL_CERT_FILE
ENV SSL_CERT_FILE=$SSL_CERT_FILE
ENV REQUESTS_CA_BUNDLE=$SSL_CERT_FILE
#ENV AWS_CA_BUNDLE=$SSL_CERT_FILE
#ENV NODE_EXTRA_CA_CERTS=$SSL_CERT_FILE
#ENV CURL_CA_BUNDLE=$SSL_CERT_FILE
COPY .setup-scripts* /.setup-scripts
RUN /.setup-scripts/debian.sh || true

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY src/ $PYTHON_SOURCE/

WORKDIR $PYTHON_SOURCE

ENTRYPOINT python -m app.{{ cookiecutter.package_name }}
