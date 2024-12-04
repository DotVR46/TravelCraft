from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.places import crud as pc
from app.api_v1.routes import crud as rc
from app.core.config import MEDIA_DIR
from app.db.db_helper import db_helper

router = APIRouter(tags=["Media"], prefix="/media")


@router.post("/routes/{route_id}/upload-photo/")
async def upload_route_photo(
    route_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    # Проверяем существование маршрута
    route = await rc.get_route(session, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Загружаем фото через общий обработчик
    target_dir = Path(MEDIA_DIR) / "routes"
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / file.filename
    with file_path.open("wb") as f:
        f.write(await file.read())

    # Обновляем запись маршрута
    route.photo = str(file_path)
    await session.commit()

    return {"detail": "Photo uploaded successfully", "file_url": str(file_path)}


@router.post("/places/{place_id}/upload-photo/")
async def upload_place_photo(
    place_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    # Проверяем существование маршрута
    place = await pc.get_place(session, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # Загружаем фото через общий обработчик
    target_dir = Path(MEDIA_DIR) / "places"
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / file.filename
    with file_path.open("wb") as f:
        f.write(await file.read())

    # Обновляем запись маршрута
    place.photo = str(file_path)
    await session.commit()

    return {"detail": "Photo uploaded successfully", "file_url": str(file_path)}
