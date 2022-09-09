docker build \
    --no-cache \
    -t syncbyte-py:latest \
    --build-arg=APP_HOME=/syncbyte_project/syncbyte \
    --build-arg=DATA_PATH=/var/run/syncbyte \
    --build-arg=LOGGER_PATH=/var/log/syncbyte \
    --build-arg=PYPI_INDEX_URL=http://10.168.1.202:8080/simple/ \
    --build-arg=PYPI_TRUSTED_HOST=10.168.1.202 \
    -f docker/Dockerfile .
