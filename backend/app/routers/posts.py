import re
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Post, PostImage
from ..schemas import PostCreate, PostUpdate, PostOut, PostAdminOut
from ..auth import get_current_admin

router = APIRouter(prefix="/posts", tags=["posts"])


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def link_images(content: str, post_id: int, db: Session) -> None:
    """Find /uploads/{filename} references in markdown and set their post_id."""
    filenames = re.findall(r"/uploads/([^\s\)\"']+)", content)
    if filenames:
        db.query(PostImage).filter(
            PostImage.filename.in_(filenames),
            PostImage.post_id.is_(None),
        ).update({"post_id": post_id}, synchronize_session=False)


def resolve_content(post: Post, lang: str) -> Post:
    """Return a post-like object with content resolved for the requested language."""
    if lang == "es" and post.content_es:
        post.content = post.content_es
    return post


# ── Public endpoints ──────────────────────────────────────────────────────────

@router.get("/", response_model=List[PostOut])
def list_posts(
    lang: str = Query("en", pattern="^(en|es)$"),
    db: Session = Depends(get_db),
):
    posts = (
        db.query(Post)
        .filter(Post.published == True)
        .order_by(Post.created_at.desc())
        .all()
    )
    for post in posts:
        resolve_content(post, lang)
    return posts


# ── Admin endpoints ───────────────────────────────────────────────────────────

@router.get("/all", response_model=List[PostAdminOut])
def list_all_posts(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    return db.query(Post).order_by(Post.created_at.desc()).all()


@router.get("/{slug}", response_model=PostOut)
def get_post(
    slug: str,
    lang: str = Query("en", pattern="^(en|es)$"),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.slug == slug, Post.published == True).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    resolve_content(post, lang)
    return post


@router.post("/", response_model=PostAdminOut, status_code=201)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    slug = data.slug or slugify(data.title)
    if db.query(Post).filter(Post.slug == slug).first():
        raise HTTPException(status_code=409, detail="Slug already exists")
    post = Post(
        title=data.title,
        slug=slug,
        content=data.content,
        content_es=data.content_es or None,
        excerpt=data.excerpt,
        tags=data.tags,
        cover_image=data.cover_image,
        published=data.published,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    link_images(post.content, post.id, db)
    if post.content_es:
        link_images(post.content_es, post.id, db)
    db.commit()
    return post


@router.put("/{post_id}", response_model=PostAdminOut)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(post, key, val)
    post.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(post)
    if post.content:
        link_images(post.content, post.id, db)
    if post.content_es:
        link_images(post.content_es, post.id, db)
    db.commit()
    return post


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
