from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import schema
from . import controller
from .depends import get_db

router = APIRouter()


@router.post(
    "/resource",
    response_model=schema.CreateResourceResponse,
    name="create resource",
)
def create_resource(
    body: schema.CreateResourceRequest,
    session: Session = Depends(get_db)
):
    c = controller.ResourceController(session)
    resource_id = c.create_resource(
        body.name,
        body.db_type,
        body.db_version,
        body.host,
        body.port,
        body.user,
        body.password,
        body.dbname,
        args=body.args,
    )

    return {"error": "", "result": {"resource_id": resource_id}}


@router.get(
    "/resource",
    response_model=schema.GetResourceResponse,
    name="get resource all",
)
def get_resources(session: Session = Depends(get_db)):
    c = controller.ResourceController(session)
    items = c.get_resource_all()

    return {"error": "", "result": items}


@router.post(
    "/storage",
    response_model=schema.AddObjectStorageResponse,
    name="add storage",
)
def add_storage(
    body: schema.AddObjectStorageRequest,
    session: Session = Depends(get_db)
):
    c = controller.StorageController(session)
    storage_id = c.add_storage(
        body.endpoint,
        body.access_key,
        body.secret_key,
        body.bucket_name,
        body.type,
    )
    return {"error": "", "result": {"storage_id": storage_id}}


@router.get(
    "/storage",
    response_model=schema.GetStorageResponse,
    name="get storages all",
)
def get_storages(session: Session = Depends(get_db)):
    c = controller.StorageController(session)
    items = c.get_storages_all()

    return {"error": "", "result": items}


@router.post(
    "/backup",
    response_model=schema.BackupResourceResponse,
    name="backup resource",
)
def backup(
    body: schema.BackupResourceRequest,
    session: Session = Depends(get_db)
):
    c = controller.BackupController(session)
    result = c.backup(body.resource_id, body.storage_id)

    return {"error": "", "result": result}
