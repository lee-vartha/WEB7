from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from passlib.hash import bcrypt
from sqlmodel import Session, select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings
from .models import User
from .database import get_session

# setting up an HTTP bearer authentication, which will expect a JWT token in the Authorization header of any incoming requests
security = HTTPBearer()

# hashes a plain text password using the bcrypt library which makes sure that any passwords stored are hashed and not seen as plain passwords (for best security)
def hash_password(pw: str) -> str:
    return bcrypt.hash(pw)

# checks if a plain-text password matches a previously hashed password - returns true if they match
def verify_password(pw: str, hashed: str) -> bool:
    return bcrypt.verify(pw, hashed)

# generates a JWT access token, copies the proivded user data, adds expiration time and encodes the token using secret key and HS256 algorihm
def create_access_token(sub: dict) -> str:
    to_encode = sub.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")

# User is a dependency function which extracts the JWT token from the request, decodes it and retrieves the users email from the payload
# queries the database for a user with that email - if the token is wrong or user isnt found then it raises an error
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

# checks if the current users role matches the required role - if it doesnt, then it raises an HTTP 403 error, which will restrict access to particular endpoints based on user roles
def require_role(user: User, role: str):
    if user.role != role:
        raise HTTPException(status_code=403, detail=f"{role.title()} only")