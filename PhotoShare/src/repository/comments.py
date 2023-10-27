from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from fastapi import HTTPException

from src.database.models import User, Comment, Share
from schemas import CommentRequest, CommentResponce


async def create_comment(photo_id: int, comment: CommentRequest, db: Session, current_user: User) -> Comment:
    if comment == '':
        raise HTTPException(status_code=204, detail='You comment is empty.')
    
    
    new_comment = Comment(description=comment.comment, user=current_user)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    db_share = db.query(Share).filter(Share.id == photo_id).first()
    
    if db_share is None:
        raise HTTPException(status_code=404, detail='Share not found')
    
    db_share.comments.append(new_comment)
    
    db.commit()
    return CommentResponce(comment=new_comment.description, share_id=photo_id)


async def update_comment(comment_id: int, new_text: str ,db: Session, current_user: User) -> Comment:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail='You are not allowed to edit this comment.')
    
    comment.description = new_text
    db.commit()
    db.refresh(comment)
    return comment.description