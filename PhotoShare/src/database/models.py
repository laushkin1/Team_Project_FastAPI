from sqlalchemy import Column, Integer, String, func, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship


Base = declarative_base()

comments_shares = Table('comments_shares', Base.metadata,
    Column('comment_id', Integer, ForeignKey('comments.id')),
    Column('share_id', Integer, ForeignKey('shares.id'))
)


shares_tags = Table(
    'shares_tags',
    Base.metadata,
    Column('share_id', Integer, ForeignKey('shares.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15), unique=True)
    shares = relationship('Share', secondary=shares_tags, back_populates='tags')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    user_id = Column('users_id', ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', backref='comments')
    shares = relationship('Share', secondary=comments_shares, back_populates='comments')

class Share(Base):
    __tablename__ = 'shares'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, nullable=False)
    image_qr = Column(String, index=True, nullable=True)
    description = Column(String, index=True, nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), server_default=None)
    user_id = Column('users_id', ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', backref='shares')
    comments = relationship('Comment', secondary=comments_shares, back_populates='shares')
    tags = relationship('Tag', secondary=shares_tags, back_populates='shares')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)
    role = Column(String, index=True, default='user')
    confirmed = Column(Boolean, default=False)
    