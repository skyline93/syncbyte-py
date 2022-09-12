from datetime import datetime

from syncbyte import db
from syncbyte.db import get_session
from syncbyte.constant import BackupJobStatus
from syncbyte.celery import remote_backup_async, complete_backup_async


def gen_dataset_name(resource_name):
    now = datetime.strftime(datetime.now(),'%Y%m%d%H%M%S')

    return f"{resource_name}-{now}"


def start_backup(resource_id, storage_id):
    session = get_session()

    res = session.query(db.Resource).filter(db.Resource.id == resource_id).first()
    session.commit()

    if res is None:
        raise Exception("resource not found")

    st = session.query(db.S3).filter(db.S3.id == storage_id).first()
    session.commit()

    if st is None:
        raise Exception("storage not found")

    dataset_name = gen_dataset_name(res.name)

    b = db.BackupJob(
        resource_id=resource_id,
        storage_id=storage_id,
        start_time=datetime.now(),
        status=BackupJobStatus.Running,
        dataset_name=dataset_name,
    )

    session.add(b)
    session.commit()

    db_options = {
        "name": res.name,
        "db_type": res.db_type,
        "host": res.host,
        "port": res.port,
        "user": res.user,
        "password": res.password,
        "dbname": res.dbname,
        "db_version": res.db_version,
    }

    st_options = {
        "endpoint": st.endpoint,
        "access_key": st.access_key,
        "secret_key": st.secret_key,
        "bucket": st.bucket_name,
    }

    task = remote_backup_async.apply_async((dataset_name, db_options, st_options), link=complete_backup_async.s(b.id))

    return task.id