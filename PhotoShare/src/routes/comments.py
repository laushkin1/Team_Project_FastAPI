from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User

from src.repository import comments as repository_comment
from src.services.auth import auth_service
from schemas import CommentRequest, CommentResponce


router = APIRouter(prefix="/comments", tags=['comment'])


@router.post("/", response_model=CommentResponce, status_code=status.HTTP_201_CREATED)
async def create_comment(photo_id: int, comment: CommentRequest, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comment.create_comment(photo_id, comment, db, current_user)  
    return comment


@router.put('/{comment_id}', response_model=CommentResponce)
async def update_comment_id(comment_id: int, new_text: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comment.update_comment(comment_id, new_text, db, current_user)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found.')
    
    return CommentResponce(comment=comment)
