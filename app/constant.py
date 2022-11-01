from enum import Enum


class ResourceType(str, Enum):
    DATABASE = "database"


class HostType(str, Enum):
    BACKUP = "backup"
    RESTORE = "restore"


class ScheduleJobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
