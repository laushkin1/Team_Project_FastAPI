from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException, Form

from sqlalchemy.orm import Session

import cloudinary
import cloudinary.uploader
from typing import List

from src.database.db import get_db
from src.database.models import User
from src.repository import shares as repository_shares
from src.services.auth import auth_service
from src.conf.config import settings
from schemas import PhotoRequest, ShareResponce, PhotoModel


router = APIRouter(prefix="/photo", tags=['my-photo'])


@router.post('/', response_model=ShareResponce, status_code=status.HTTP_201_CREATED)
async def upload_share(description: str = Form(...), file: UploadFile = File(), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    try:
        if not file.content_type.startswith("image"):
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        result = cloudinary.uploader.upload(file.file, folder="photo_base",width=620, height=980, crop="fit")
        
        url = result.get("secure_url")
        
        db_share = await repository_shares.create_share(description, url, db, current_user)
        return db_share
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error uploading photo")


@router.post('/qr', status_code=status.HTTP_201_CREATED)
async def create_qrcode(url: str, name: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    image_qr = await repository_shares.generate_qr_code(url=url, name=name, db=db, current_user=current_user)
    return image_qr


@router.get('/', response_model=List[PhotoModel])
async def read_shares(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    shares = await repository_shares.get_list_shares(db, current_user)   
    return shares


@router.get("/{photo_id}", response_model=PhotoModel)
async def read_share(photo_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_shares.get_share(photo_id, db, current_user)
    return share


@router.put("/{photo_id}", response_model=ShareResponce)
async def update_share(photo_id: int, update_share: PhotoRequest, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_shares.update_share(photo_id, update_share, db, current_user)
    return share


@router.delete("/{photo_id}", response_model=ShareResponce)
async def delete_share(photo_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_shares.delete_share(photo_id, db, current_user)
    return share
