from sqlalchemy.orm import Session
from models.user import User
from utils.security import verify_password, get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, full_name: str, password: str, role: str):
    # Basic role validation
    allowed_roles = ["superadmin", "schooladmin", "teacher", "student"]
    if role not in allowed_roles:
        raise ValueError("Invalid role")
        
    hashed_password = get_password_hash(password)
    new_user = User(
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user