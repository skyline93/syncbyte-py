FROM syncbyte:python-3.8.13-bullseye

ARG USER_ID=2000
ARG USER_NAME=admin
ARG GROUP_ID=2000
ARG GROUP_NAME=admin

ARG APP_HOME=/project_home/app_home
ARG LOGGER_PATH=/var/log/app
ARG DATA_PATH=/var/run/app

ARG PYPI_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
ARG PYPI_TRUSTED_HOST=mirrors.aliyun.com

WORKDIR ${APP_HOME}
COPY . ${APP_HOME}

RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install -i ${PYPI_INDEX_URL} --trusted-host ${PYPI_TRUSTED_HOST} --upgrade pip \
    && /opt/venv/bin/pip install -i ${PYPI_INDEX_URL} --trusted-host ${PYPI_TRUSTED_HOST} -r requirements.txt \
    && mkdir -p ${DATA_PATH} \
    && mkdir -p ${LOGGER_PATH} \
    && chown -R ${USER_NAME}:${GROUP_NAME} ${APP_HOME} \
    && chown -R ${USER_NAME}:${GROUP_NAME} /opt/venv \
    && chown -R ${USER_NAME}:${GROUP_NAME} ${LOGGER_PATH} \
    && chown -R ${USER_NAME}:${GROUP_NAME} ${DATA_PATH}

USER ${USER_NAME}
VOLUME [ ${APP_HOME},${DATA_PATH},${LOGGER_PATH} ]

CMD [ "/opt/venv/bin/python3", "main.py", "run"]
