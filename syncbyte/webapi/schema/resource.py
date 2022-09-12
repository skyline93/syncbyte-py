from typing import Optional, List

from pydantic import BaseModel, Field

from syncbyte.constant import DBType


class CreateResourceRequest(BaseModel):
    name: str = Field(..., description="资源名称")
    db_type: DBType = Field(..., description="数据库类型")
    db_version: str = Field(..., description="数据库版本")
    host: str = Field(..., description="数据库IP")
    port: int = Field(..., description="端口")
    user: str = Field(..., description="用户")
    password: str = Field(..., description="密码")
    dbname: str = Field(..., description="数据库名称")
    args: str = Field(None, description="连接扩展参数")


class _CreateResourceResponseItem(BaseModel):
    resource_id: int = Field(..., description="资源ID")


class CreateResourceResponse(BaseModel):
    error: str = Field(..., description="错误信息")
    result: Optional[_CreateResourceResponseItem] = Field(..., description="响应结果")


class BackupResourceRequest(BaseModel):
    resource_id: int = Field(..., description="资源ID")
    storage_id: int = Field(..., description="存储ID")


class BackupResourceResponse(BaseModel):
    error: str = Field(..., description="错误信息")
    result: str = Field(..., description="结果")


class _GetResourceResponseItem(BaseModel):
    resource_id: int = Field(..., description="资源ID")
    name: str = Field(..., description="资源名称")


class GetResourceResponse(BaseModel):
    error: str = Field(..., description="错误信息")
    result: List[_GetResourceResponseItem] = Field(..., description="响应结果")
