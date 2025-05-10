from fastapi import APIRouter, HTTPException
from app.models.user import UserProfile
from typing import Dict

router = APIRouter(prefix="/users", tags=["users"])

# In-memory "database"
user_db: Dict[str, UserProfile] = {}

@router.post("/", response_model=UserProfile)
async def create_user(profile: UserProfile):
    if profile.name in user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    user_db[profile.name] = profile
    return profile


@router.get("/{user_id}", response_model=UserProfile)
async def get_user(user_id: str):
    user = user_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
