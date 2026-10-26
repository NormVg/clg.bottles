"""HTTP endpoints for folders, items, uploads, and search."""

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from pydantic import BaseModel

from ...utils.db import get_connection
from .service import BookmarkService

router = APIRouter(prefix="/api")


class FolderInput(BaseModel):
    path: str


class FolderUpdate(BaseModel):
    name: str


class ItemInput(BaseModel):
    type: str
    title: str | None = None
    url: str | None = None
    note: str | None = None
    path: str | None = None


class ItemUpdate(BaseModel):
    title: str | None = None
    url: str | None = None
    note: str | None = None


def get_service():
    connection = get_connection()
    try:
        yield BookmarkService(connection)
    finally:
        connection.close()


@router.get("/fs")
def list_directory(path: str = "/", service: BookmarkService = Depends(get_service)):
    try:
        return service.list_directory(path)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/folders")
def list_folders(service: BookmarkService = Depends(get_service)):
    return service.list_folders()


@router.post("/folders", status_code=201)
def create_folder(input: FolderInput, service: BookmarkService = Depends(get_service)):
    try:
        return service.create_folder(input.path)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/folders/{folder_id}")
def rename_folder(
    folder_id: int, input: FolderUpdate, service: BookmarkService = Depends(get_service)
):
    try:
        return service.rename_folder(folder_id, input.name)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/folders/{folder_id}", status_code=204)
def delete_folder(folder_id: int, service: BookmarkService = Depends(get_service)):
    try:
        service.delete_folder(folder_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/items", status_code=201)
def create_item(input: ItemInput, service: BookmarkService = Depends(get_service)):
    try:
        return service.create_item(input.type, input.title, input.url, input.note, input.path)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/items/{item_id}")
def update_item(
    item_id: int, input: ItemUpdate, service: BookmarkService = Depends(get_service)
):
    try:
        return service.update_item(item_id, input.title, input.url, input.note)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, service: BookmarkService = Depends(get_service)):
    try:
        service.delete_item(item_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/media", status_code=201)
def upload_media(
    file: UploadFile = File(...),
    path: str = Form("/"),
    title: str = Form(""),
    service: BookmarkService = Depends(get_service),
):
    data = file.file.read()
    try:
        return service.upload_media(
            file.filename or "file", file.content_type or "", data, path, title
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/media/{media_id}")
def get_media(media_id: int, service: BookmarkService = Depends(get_service)):
    try:
        return service.get_media(media_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/media/{media_id}/raw")
def get_media_raw(media_id: int, service: BookmarkService = Depends(get_service)):
    try:
        row = service.get_media_row(media_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    return Response(content=bytes(row["data"]), media_type=row["mime_type"])


@router.get("/media/{media_id}/download")
def download_media(media_id: int, service: BookmarkService = Depends(get_service)):
    try:
        row = service.get_media_row(media_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    return Response(
        content=bytes(row["data"]),
        media_type=row["mime_type"],
        headers={"Content-Disposition": f'attachment; filename="{row["filename"]}"'},
    )


@router.get("/search")
def search(q: str, service: BookmarkService = Depends(get_service)):
    if not q.strip():
        return {"folders": [], "items": []}
    return service.search(q.strip())
