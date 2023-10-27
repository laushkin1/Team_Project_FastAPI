from sqlalchemy.orm import Session
from sqlalchemy import and_

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Type

from src.database.models import User, Share, Comment, Tag
from schemas import PhotoRequest, CommentResponce, PhotoModel, TagRequest, GetRole, AdminComment, AdminPhotosModel



async def get_list_users_photos(db: Session, current_user: User) -> list[Type[Share]]:
    shares = db.query(Share).all()

    if not shares:
        raise HTTPException(status_code=404, detail="Shares not found")
    
    if current_user.role != 'admin' and current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    
    share_models = []
    for share in shares:
        comments = db.query(Comment).filter(Comment.shares.contains(share)).all()
        comment_responses = [AdminComment(id=comment.id, comment=comment.description, share_id=share.id) for comment in comments]
        tags = db.query(Tag).filter(Tag.shares.contains(share)).all()
        tags_responce = [TagRequest(id=tag.id, name=tag.name) for tag in tags]

        share_model = AdminPhotosModel(
            id=share.id,
            url=share.url,
            image_qr=share.image_qr,
            description=share.description,
            comments=comment_responses,
            tags=tags_responce,
            created_at=share.created_at,
            updated_at=share.updated_at
        )
        
        share_models.append(share_model)
    return share_models


async def get_user_photo(photo_id: str, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(Share.id == photo_id).first() #, Share.user_id != current_user.id

    if not share:
        raise HTTPException(status_code=404, detail="Share not found.")
    
    if current_user.role != 'admin' and current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    
    comments = db.query(Comment).filter(Comment.shares.contains(share)).all()
    comment_responses = [CommentResponce(id=comment.id, comment=comment.description, share_id=share.id) for comment in comments]
    tags = db.query(Tag).filter(Tag.shares.contains(share)).all()
    tags_responce = [TagRequest(id=tag.id, name=tag.name) for tag in tags]

    share_model = PhotoModel(
        id=share.id,
        url=share.url,
        image_qr=share.image_qr,
        description=share.description,
        comments=comment_responses,
        tags=tags_responce,
        created_at=share.created_at,
        updated_at=share.updated_at
    )
    
    return share_model


async def update_photo(photo_id: int, updated_photo: PhotoRequest, db: Session, current_user: User) -> Type[Share]:
    photo = db.query(Share).filter(and_(Share.id == photo_id, Share.user_id == current_user.id)).first()

    if not photo:
        raise HTTPException(status_code=404, detail='Share not found.')
    
    if current_user.role != 'admin' and current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power.")
    
    for attr, value in updated_photo.model_dump().items():
        setattr(photo, attr, value)

    db.commit()
    db.refresh(photo)
    return photo


async def delete_photo(photo_id: int, db: Session, current_user: User) -> Type[Share]:
    photo = db.query(Share).filter(Share.id == photo_id).first() # , Share.user_id == current_user.id

    if not photo:
        raise HTTPException(status_code=404, detail='Share not found')

    if current_user.role != 'admin' and current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power.") 

    db.delete(photo)
    db.commit()
    return photo


async def get_role(user_id: int, role: GetRole, db: Session, current_user: User) -> Type[User]:
    user = db.query(User).filter(User.id == user_id).first() #, user_id != current_user)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found.')
    
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="You don't have such power.")
    
    if role.role != 'moder' and role.role != 'user':
        raise HTTPException(status_code=404, detail="Role must be a user or moder.")
    
    role_data = role.dict()
    
    # Оновлюємо користувача на основі role_data
    user.role = role_data.get('role', user.role)
    db.commit()
    db.refresh(user)
    return user



async def update_comment(comment_id: str, db: Session, current_user: User) -> Type[Comment]:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id != current_user.id))
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")
    
    if current_user.role != 'admin' or current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    return comment


async def delete_comment(comment_id: str, db: Session, current_user: User) -> Type[Comment]:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, User.id != current_user.id))

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")

    if current_user.role != 'admin' or current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    return comment
