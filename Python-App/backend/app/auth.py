from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from passlib.hash import bcrypt
from sqlmodel import Session, select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings
from .models import User
from .database import get_session

security = HTTPBearer()

def hash_password(pw: str) -> str:
    return bcrypt.hash(pw)

def verify_password(pw: str, hashed: str) -> bool:
    return bcrypt.verify(pw, hashed)

def create_access_token(sub: dict) -> str:
    to_encode = sub.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")

def get_current_user(
        creds: HTTPAuthorizationCredentials = Depends(security),
        session: Session = Depends(get_session)
) -> User:
    token = creds.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        email = payload.get("email")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(user: User, role: str):
    if user.role != role:
        raise HTTPException(status_code=403, detail=f"{role.title()} only")