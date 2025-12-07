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



