from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from pkg.rds import Base, ModelBase


class Resource(ModelBase, Base):
    __tablename__ = "resource"

    name = Column(String(60), unique=True)
    resource_type = Column(String(20))

    databases = relationship("Database", backref="resource")
    backup_policies = relationship("BackupPolicy", backref="resource")


class Database(ModelBase, Base):
    __tablename__ = "database"

    db_type = Column(String(60))
    version = Column(String(60))
    server = Column(String(60))
    port = Column(Integer)
    user = Column(String(60))
    password = Column(String(60))
    db_name = Column(String(60))

    resource_id = Column(Integer, ForeignKey("resource.id"), nullable=False)


class BackupPolicy(ModelBase, Base):
    __tablename__ = "backup_policy"

    retention = Column(Integer)
    is_compress = Column(Boolean)
    status = Column(String(60))

    resource_id = Column(Integer, ForeignKey("resource.id"), nullable=False)
    backup_schedules = relationship("BackupSchedule", backref="backup_policy")


class BackupSchedule(ModelBase, Base):
    __tablename__ = "backup_schedule"

    schedule_type = Column(String(20))
    cron = Column(String(60))
    frequency = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_active = Column(Boolean, default=True)

    policy_id = Column(Integer, ForeignKey("backup_policy.id"), nullable=False)


class DataStorage(ModelBase, Base):
    __tablename__ = "data_storage"

    storage_type = Column(String(20))


class S3(ModelBase, Base):
    __tablename__ = "s3"

    end_point = Column(String(60))
    access_key = Column(String(200))
    secret_key = Column(String(200))
    bucket = Column(String(120))

    data_storage_id = Column(Integer)


class Local(ModelBase, Base):
    __tablename__ = "local"

    mount_point = Column(String(500))

    data_storage_id = Column(Integer)


class BackupSet(ModelBase, Base):
    __tablename__ = "backup_set"

    is_compress = Column(Boolean)
    is_valid = Column(Boolean)
    size = Column(Integer)
    backup_time = Column(DateTime)

    resource_id = Column(Integer)


class Host(ModelBase, Base):
    __tablename__ = "host"

    ip = Column(String(100))
    hostname = Column(String(100))
    host_type = Column(String(20))


class ScheduledJob(ModelBase, Base):
    __tablename__ = "scheduled_job"

    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String(20))
    args = Column(String(1000))

    resource_id = Column(Integer)
    backup_set_id = Column(Integer)
    backup_policy_id = Column(Integer)
