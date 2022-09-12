import logging
from time import sleep

from celery import Celery

from syncbyte.config import CeleryConfig
from syncbyte.backup.remote import remote_backup
from syncbyte.backup.local import complete_backup

logger = logging.getLogger(__name__)


app = Celery("syncbyte")
app.config_from_object(CeleryConfig)


@app.task(bind=True)
def test_async(self, job_id):
    logger.info(f"receive celery task, task_name: {self.name}, task_id: {self.request.id}")

    for i in range(0, 10):
        sleep(1)
        logger.info(f"waiting task {self.request.id} {i}s")

    logger.info(f"task completed{self.request.id}")

    return job_id


@app.task
def remote_backup_async(dataset_name, db_options, st_options):
    remote_backup(dataset_name, db_options, st_options)


@app.task
def complete_backup_async(_, job_id):
    complete_backup(job_id)
