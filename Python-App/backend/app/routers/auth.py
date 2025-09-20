from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import User
from ..schemas import UserCreate, UserRead, LoginIn, TokenOut
from ..auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(data: UserCreate, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.email == data.email)).first():
        raise HTTPException(400, "Email already registered")
    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
        token_balance=5
    )
    session.add(user); session.commit(); session.refresh(user)
    return UserRead(id=user.id, name=user.name, email=user.email, role=user.role, token_balance=user.token_balance)

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email==data.email)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "invalid credentials")
    token = create_access_token({"email": user.email, "role": user.role})
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserRead)
def me(current = Depends(get_current_user)):
    u = current
    return UserRead(id=u.id, name=u.name, email=u.email, role=u.role, token_balance=u.token_balance)