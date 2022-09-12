from typing import Optional, List

from pydantic import BaseModel, Field

from syncbyte.constant import StorageType


class AddObjectStorageRequest(BaseModel):
    endpoint: str = Field(..., description="存储节点地址")
    access_key: str = Field(..., description="access key")
    secret_key: str = Field(..., description="secret key")
    bucket_name: str = Field(..., description="存储桶名")
    type: StorageType = Field(..., description="存储类型")


class _AddObjectStorageResponseItem(BaseModel):
    storage_id: int = Field(..., description="存储ID")


class AddObjectStorageResponse(BaseModel):
    error: str = Field(..., description="错误信息")
    result: Optional[_AddObjectStorageResponseItem] = Field(..., description="响应结果")


class _GetStorageResponseItem(BaseModel):
    storage_id: int = Field(..., description="存储ID")
    bucket_name: str = Field(..., description="存储桶名")


class GetStorageResponse(BaseModel):
    error: str = Field(..., description="错误信息")
    result: List[_GetStorageResponseItem] = Field(..., description="响应结果")
