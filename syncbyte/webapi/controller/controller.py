import logging
from datetime import datetime

from sqlalchemy.orm import Session

from syncbyte import db
from syncbyte.backup.api import start_backup

logger = logging.getLogger(__name__)


def gen_dataset_name(resource_name):
    now = datetime.strftime(datetime.now(),'%Y%m%d%H%M%S')

    return f"{resource_name}-{now}"


class ResourceController:
    def __init__(self, session: Session):
        self.session = session

    def create_resource(self, name, db_type, db_version, host, port, user, password, dbname, args=None):
        r = db.Resource(
            name=name,
            db_type=db_type,
            db_version=db_version,
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
            args=args
        )

        self.session.add(r)
        self.session.commit()

        return r.id

    def get_resource_all(self):
        resources = self.session.query(db.Resource).all()
        self.session.commit()

        return [{"resource_id": r.id, "name": r.name} for r in resources]


class StorageController:
    def __init__(self, session: Session):
        self.session = session

    def add_storage(self, endpoint, access_key, secret_key, bucket_name, type):
        s = db.S3(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            bucket_name=bucket_name,
            type=type,
        )

        self.session.add(s)
        self.session.commit()

        return s.id

    def get_storages_all(self):
        storages = self.session.query(db.S3).all()
        self.session.commit()

        return [{"storage_id": s.id, "bucket_name": s.bucket_name} for s in storages]


class BackupController:
    def __init__(self, session):
        self.session = session
    
    def backup(self, resource_id, storage_id):
        task_id = start_backup(resource_id, storage_id)

        return task_id
