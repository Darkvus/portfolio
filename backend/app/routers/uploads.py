import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import PostImage
from ..auth import get_current_admin

router = APIRouter(tags=["uploads"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"}
MAX_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/uploads/image")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported image type")

    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 10 MB)")

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "png"
    filename = f"{uuid.uuid4().hex}.{ext}"

    img = PostImage(filename=filename, data=data, content_type=file.content_type)
    db.add(img)
    db.commit()

    return JSONResponse({"url": f"/uploads/{filename}"})


@router.get("/uploads/{filename}")
def serve_image(filename: str, db: Session = Depends(get_db)):
    img = db.query(PostImage).filter(PostImage.filename == filename).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return Response(content=img.data, media_type=img.content_type)
