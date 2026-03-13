from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ProfileConfig
from ..schemas import ProfileOut, ProfileUpdate
from ..auth import get_current_admin

router = APIRouter(prefix="/profile", tags=["profile"])

DEFAULTS = {
    "open_to_work": "true",
    "location":     "Cádiz, Spain",
    "available_from": "",
}


def _get(db: Session) -> dict:
    rows = {r.key: r.value for r in db.query(ProfileConfig).all()}
    merged = {**DEFAULTS, **rows}
    return {
        "open_to_work":   merged["open_to_work"].lower() == "true",
        "location":       merged["location"],
        "available_from": merged["available_from"] or None,
    }


def _set(db: Session, key: str, value: str) -> None:
    row = db.query(ProfileConfig).filter(ProfileConfig.key == key).first()
    if row:
        row.value = value
    else:
        db.add(ProfileConfig(key=key, value=value))


@router.get("/", response_model=ProfileOut)
def get_profile(db: Session = Depends(get_db)):
    return _get(db)


@router.put("/", response_model=ProfileOut)
def update_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    if data.open_to_work is not None:
        _set(db, "open_to_work", str(data.open_to_work).lower())
    if data.location is not None:
        _set(db, "location", data.location)
    if data.available_from is not None:
        _set(db, "available_from", data.available_from)
    db.commit()
    return _get(db)
