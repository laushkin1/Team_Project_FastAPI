from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.database.models import User

from src.repository import public as repository_public
from src.services.auth import auth_service
from schemas import PhotoModel


router = APIRouter(prefix="/photos", tags=['recomendations'])


@router.get('/', response_model=List[PhotoModel])
async def read_shares(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    shares = await repository_public.get_list_users_photos(db, current_user)
    return shares


@router.get("/{photo_id}", response_model=PhotoModel)
async def read_share(photo_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_public.get_user_photo(photo_id, db, current_user)
    return share