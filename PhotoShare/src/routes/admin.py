from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.database.models import User

from src.repository import admin as repository_admin
from src.services.auth import auth_service
from schemas import  ShareResponce, PhotoRequest, CommentResponce, PhotoModel, GetRole, AdminPhotosModel


router = APIRouter(prefix="/photos", tags=['admin-moder'])


@router.get('/', response_model=List[AdminPhotosModel])
async def read_photos(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    shares = await repository_admin.get_list_users_photos(db, current_user)
    return shares


@router.get("/{photo_id}", response_model=PhotoModel)
async def read_photo(photo_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.get_user_photo(photo_id, db, current_user)
    return share


@router.put("/{photo_id}", response_model=ShareResponce)
async def update_photo(photo_id: int, updated_photo: PhotoRequest, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.update_photo(photo_id, updated_photo, db, current_user)
    return share


@router.delete("/{photo_id}", response_model=ShareResponce)
async def delete_photo(photo_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.delete_photo(photo_id, db, current_user)
    return share


@router.put("/user/{user_id}", response_model=GetRole)
async def transfer_role(user_id: int, role: GetRole, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.get_role(user_id, role, db, current_user)
    return share 


@router.put('/{comment_id}', response_model=CommentResponce)
async def update_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_admin.update_comment(comment_id, db, current_user)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')
    return comment


@router.delete('/{comment_id}', response_model=CommentResponce)
async def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_admin.delete_comment(comment_id, db, current_user)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found.")
    return comment
