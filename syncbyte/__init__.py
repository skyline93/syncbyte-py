import os
import logging

from syncbyte.webapi import app as web_app
from syncbyte.config import settings

logging.basicConfig(
    filename=os.path.join(settings.LOGGER_PATH, "app.log"),
    level=logging.INFO, 
    format="[%(asctime)s] %(levelname)s [:%(lineno)d]: %(message)s"
)
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
