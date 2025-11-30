from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, UUID, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, mapped_column
from uuid import uuid4

db = SQLAlchemy()

class User(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4, unique=True)
    username= Column(String(length=40), nullable=False, unique=True)
    password= Column(String(length=150), nullable=False)
    email= Column(String(length=120), nullable=False, unique=False)
    first_name= Column(String(length=50), nullable=False) 
    last_name= Column(String(length=50), nullable=True) 
    is_activated= Column(Boolean, nullable=False, default=True)
    created_at= Column(DateTime, nullable=False, default=lambda x: datetime.now(timezone.utc))

    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete",
    )

class Post(db.Model):
    id= Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4, unique=True)
    title= Column(String(length=120), nullable=False)
    content= Column(String, nullable=False)
    likes= Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=lambda x: datetime.now(timezone.utc))
    is_published = Column(Boolean, nullable=False, default=False)
    published_on = Column(DateTime, nullable=True)

    author_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
        nullable=False
    )

    author = relationship(
        "User",
        back_populates="posts",
    )


