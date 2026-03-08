from fastapi import APIRouter, HTTPException
from ..schemas import Token, LoginData
from ..auth import verify_password, create_access_token, ADMIN_USERNAME, ADMIN_PASSWORD_HASH

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
def login(data: LoginData):
    if not ADMIN_PASSWORD_HASH:
        raise HTTPException(status_code=503, detail="Admin password not configured")
    if data.username != ADMIN_USERNAME or not verify_password(data.password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return Token(access_token=create_access_token(data.username))
