import logging
from datetime import datetime

import boto3
import botocore

from syncbyte import db
from syncbyte.db import get_session
from syncbyte.constant import BackupJobStatus

logger = logging.getLogger(__name__)


def complete_backup(job_id):
    session = get_session()

    j = session.query(db.BackupJob).filter(db.BackupJob.id == job_id).first()
    s = session.query(db.S3).filter(db.S3.id == j.storage_id).first()

    s3 = boto3.resource(
        "s3", 
        endpoint_url=s.endpoint,
        aws_access_key_id=s.access_key,
        aws_secret_access_key=s.secret_key,
    )

    object_name = f"{j.dataset_name}.sql.gz"

    is_exists_object = False
    try:
        s3.Object(s.bucket_name, object_name).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            is_exists_object = False
        else:
            raise Exception("Error occurred while fetching a file from S3. Try Again.")
    else:
        is_exists_object = True


    if is_exists_object is True:
        object = s3.Object(s.bucket_name, object_name)
        size = object.content_length

        session.query(db.BackupJob).filter(db.BackupJob.id == job_id).update(
            {"size": size, "is_valid": True, "status": BackupJobStatus.Successed, "end_time": datetime.now()}
        )

    else:
        session.query(db.BackupJob).filter(db.BackupJob.id == job_id).update(
            {"size": 0, "is_valid": False, "status": BackupJobStatus.Failed, "end_time": datetime.now()}
        )
    
    session.commit()

    logger.info(f"backup job {job_id} completed")
