from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Subscriber(Base):
    __tablename__ = "subscribers"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String(254), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)


class Post(Base):
    __tablename__ = "posts"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(200), nullable=False)
    slug       = Column(String(200), unique=True, nullable=False, index=True)
    content    = Column(Text, nullable=False)
    excerpt    = Column(String(500), nullable=True)
    tags         = Column(String(500), nullable=True)
    cover_image  = Column(String(500), nullable=True)
    published    = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    images = relationship("PostImage", back_populates="post", cascade="all, delete-orphan",
                          foreign_keys="PostImage.post_id")


class PostImage(Base):
    __tablename__ = "post_images"

    id           = Column(Integer, primary_key=True, index=True)
    filename     = Column(String(200), unique=True, nullable=False, index=True)
    data         = Column(LargeBinary, nullable=False)
    content_type = Column(String(100), nullable=False)
    post_id      = Column(Integer, ForeignKey("posts.id", ondelete="SET NULL"), nullable=True)
    created_at   = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    post = relationship("Post", back_populates="images", foreign_keys=[post_id])
