docker build \
    --no-cache \
    -t syncbyte:python-3.8.13-bullseye \
    --build-arg=APP_HOME=/syncbyte_project/syncbyte \
    --build-arg=DATA_PATH=/var/run/syncbyte \
    --build-arg=LOGGER_PATH=/var/log/syncbyte \
    -f docker/Dockerfile.base .
