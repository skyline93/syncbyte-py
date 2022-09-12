from enum import Enum


class DBType(str, Enum):
    PostgreSQL = "postgresql"


class StorageType(str, Enum):
    MinIO = "minio"


class BackupJobStatus(str, Enum):
    Running = "running"
    Successed = "successed"
    Failed = "failed"
