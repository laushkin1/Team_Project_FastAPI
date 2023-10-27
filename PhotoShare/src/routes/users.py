from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from schemas import UserDb

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.patch("/avatar", response_model=UserDb)
async def update_avatar_user(file: UploadFile, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    r = cloudinary.uploader.upload(
        file.file,
        public_id=f"NotesApp/{current_user.username}",
        width=500,
        height=500,
        crop="limit",
        format="jpg",
    )

    
    src_url = cloudinary.CloudinaryImage(f"NotesApp/{current_user.username}").build_url(width=500, height=500, crop="limit", format="jpg")

    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
