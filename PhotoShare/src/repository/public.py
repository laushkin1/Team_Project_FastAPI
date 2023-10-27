from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from fastapi import HTTPException

from typing import Type


from src.database.models import User, Share, Comment, Tag
from schemas import ShareResponce, CommentResponce, TagRequest, PhotoModel
from typing import List


async def get_list_users_photos(db: Session, current_user: User) -> List[ShareResponce]:
    shares = db.query(Share).filter(Share.user_id != current_user.id).all()

    share_models = []
    for share in shares:
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
        
        share_models.append(share_model)
    return share_models


async def get_user_photo(share_id: str, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id != current_user.id)).first()
    if share is None:
        raise HTTPException(status_code=404, detail='Share not found')
    
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
    return share


