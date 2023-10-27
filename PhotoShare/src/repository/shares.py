from sqlalchemy.orm import Session
from sqlalchemy import and_

from fastapi import HTTPException

from sqlalchemy.orm import Session
from typing import Type

from src.database.models import User, Share, Tag, Comment
from schemas import PhotoRequest, PhotoModel, CommentResponce, TagRequest
import qrcode as qr
import cloudinary.uploader
from src.repository.tags import extract_tags
from src.conf.config import settings
from io import BytesIO


async def create_share(description: str, url: str, db: Session, current_user: User) -> Share:
    tags = extract_tags(description)  # список тегів
    created_tags = []

    if tags:
        for tag_name in tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
            created_tags.append(tag)

    db_share = Share(url=url, description=description, user=current_user) #, tags=created_tags
    db.add(db_share)
    for tag in created_tags:
        db_share.tags.append(tag)
    db.commit()
    db.refresh(db_share)
    return db_share


async def get_list_shares(db: Session, current_user: User) -> list[Type[Share]]:
    shares = db.query(Share).filter(Share.user_id == current_user.id).all()

    share_models = []
    for share in shares:
        comments = db.query(Comment).filter(Comment.shares.contains(share)).all()
        comment_responses = [CommentResponce(comment=comment.description) for comment in comments]
        tags = db.query(Tag).filter(Tag.shares.contains(share)).all()
        tags_responce = [TagRequest(name=tag.name) for tag in tags]

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



async def get_share(photo_id: int, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == photo_id, Share.user_id == current_user.id)).first()

    if share is None:
        raise HTTPException(status_code=404, detail='Share not found')
    
    comments = db.query(Comment).filter(Comment.shares.contains(share)).all()
    comment_responses = [CommentResponce(comment=comment.description) for comment in comments]
    tags = db.query(Tag).filter(Tag.shares.contains(share)).all()
    tags_responce = [TagRequest(name=tag.name) for tag in tags]

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
    


async def update_share(photo_id: int, updated_share: PhotoRequest, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == photo_id, Share.user_id == current_user.id)).first()

    if share is None:
        raise HTTPException(status_code=404, detail='Share not found')
    
    for attr, value in updated_share.model_dump().items():
        setattr(share, attr, value)

    db.commit()
    db.refresh(share)
    return share


async def delete_share(photo_id: int, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == photo_id, Share.user_id == current_user.id)).first()

    if share is None:
        raise HTTPException(status_code=404, detail='Share not found') 

    db.delete(share)
    db.commit()
    return share 


async def generate_qr_code(url: str, name: str, db: Session, current_user: User):
    share = db.query(Share).filter(and_(Share.url == url, Share.user_id == current_user.id)).first()
    if share.image_qr:
        return share.image_qr

    
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    if share is None:
        raise HTTPException(status_code=404, detail='Share not found')

    combined_data = f"{name}\n{url}"

    image_qr = qr.QRCode(
        error_correction=qr.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    image_qr.add_data(combined_data)
    image_qr.make(fit=True)

    img = image_qr.make_image(fill_color="black", back_color="white")
    img_byte_io = BytesIO()
    img.save(img_byte_io)
    img_bytes = img_byte_io.getvalue()

    cloudinary_response = cloudinary.uploader.upload(img_bytes, folder="qr_codes")
    image_url = cloudinary_response.get("secure_url")

    share.image_qr = image_url

    db.commit()
    db.refresh(share)

    return image_url
