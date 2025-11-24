from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from crud.user import authenticate_user, get_user_by_email, create_user
from utils.security import create_access_token
from schemas.user import UserCreate, Token, UserLogin
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "full_name": user.full_name
    }

# ... existing imports and login route ...

@router.post("/signup")
async def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # For now allow anyone to signup as anything (we'll lock superadmin later)
    user = create_user(
        db=db,
        email=user_create.email,
        full_name=user_create.full_name,
        password=user_create.password,
        role=user_create.role
    )
    
    return {"message": f"{user.role.capitalize()} created successfully!", "email": user.email}