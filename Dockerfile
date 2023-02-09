FROM python:3.11

# Set environment variables needed here
ENV VIRTUAL_ENV=".venv"
ENV PATH=$PATH:$VIRTUAL_ENV/bin
ENV GUID=1001
ENV UUID=1002
ENV UM_MCC_DIR="/service/um_mcc"

RUN apt-get -yq update \
    && apt-get -yq upgrade \
    && apt-get install -yq nginx supervisor

RUN groupadd -g $GUID api-service \
    && useradd --no-log-init -d "/service/um_mcc" -s /bin/bash -u $UUID -g $GUID api-service

WORKDIR /service/um_mcc
COPY --chown=$UIID:$GUID . /service/um_mcc
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisord.conf

RUN python -m venv $VIRTUAL_ENV \
    && $VIRTUAL_ENV/bin/python -m pip install --upgrade pip \
    && $VIRTUAL_ENV/bin/pip install setuptools build \
    && $VIRTUAL_ENV/bin/python -m build --wheel -o ./ \
    && $VIRTUAL_ENV/bin/pip install ./*.whl

EXPOSE 8000
ENTRYPOINT ["/usr/bin/supervisord", "-c", "/service/um_mcc/supervisord.conf"]
