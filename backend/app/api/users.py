from fastapi import APIRouter, Depends

from app.schemas.user import UserRead
from app.services.user_service import list_users_service
from app.core.database import get_session

router = APIRouter()

@router.get("/api/users", response_model=list[UserRead])
async def list_users(session=Depends(get_session)) -> list[UserRead]:
    return await list_users_service(session)

