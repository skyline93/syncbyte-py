import logging
from time import sleep

from app import db
from app.db import get_session
from app.backup.api import start_backup

logger = logging.getLogger(__name__)


def schedule():
    while True:
        try:
            session = get_session()
            items = session.query(db.Resource).all()
            st = session.query(db.S3).first()
            session.commit()

            for i in items:
                task_id = start_backup(i.id, st.id)
                logger.info(f"start backup, task_id: {task_id}")
        except Exception as e:
            logger.error(f"schedule start backup failed, err: {str(e)}")

        wait_time = 60 * 60
        sleep_time = 5
        for i in range(1, int(wait_time / sleep_time)):
            sleep(sleep_time)
            logger.info(f"waiting next backup {i * sleep_time}/{int(wait_time / sleep_time)}s")
