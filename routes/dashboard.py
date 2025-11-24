from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/api/v1", tags=["dashboard"])
security = HTTPBearer()

# Simple token validation (we’ll add full JWT verify later if you want)
@router.get("/dashboard")
async def get_dashboard(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # For now just return role-based message
    return {"message": "Welcome to your dashboard!", "hint": "Full JWT verify coming soon"}