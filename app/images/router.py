import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import resize_photo

router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


@router.post("/services")
async def add_service_image(name: int, file: UploadFile):
    path = f"app/static/services/{name}.webp"
    with open(path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    resize_photo.delay(path)
