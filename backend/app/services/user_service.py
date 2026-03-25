from __future__ import annotations

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.user import UserRead
from app.models.users import User


async def list_users_service(session: AsyncSession) -> list[UserRead]:
    """
    Service layer: query DB and map ORM models -> API schemas.
    """
    result = await session.exec(select(User))
    users = result.all()

    return [
        UserRead(
            id=str(u.id),
            user_name=u.user_name,
            role=getattr(u.role, "value", str(u.role)),
            email=u.email,
            status=getattr(u.status, "value", str(u.status)),
        )
        for u in users
    ]

