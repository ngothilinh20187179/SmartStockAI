from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import async_session_maker
from app.models import User
from app.models.enums import UserRole, UserStatus


SEED_PASSWORD = "changeme123"
SEED_USERS: list[dict] = [
    {"user_name": "Demo Manager", "role": UserRole.manager, "email": "manager@demo.smartstock"},
    {"user_name": "Demo Staff", "role": UserRole.staff, "email": "staff@demo.smartstock"},
]

def _hash_password(password: str) -> str:
    """
    Try bcrypt first (matches historical config), but fallback to pbkdf2_sha256
    if the container's bcrypt dependency is incompatible.
    """
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    except Exception as e:
        print(f"bcrypt hashing failed; fallback to pbkdf2_sha256: {e}")
        return pbkdf2_sha256.hash(password)

async def seed_users(*, force: bool) -> None:
    password_hash = _hash_password(SEED_PASSWORD)

    print("Seeding users (idempotent)...")
    async with async_session_maker() as session:
        for u in SEED_USERS:
            stmt = select(User).where(User.email == u["email"])
            result = await session.execute(stmt)
            existing: User | None = result.scalar_one_or_none()

            if existing is None:
                session.add(
                    User(
                        user_name=u["user_name"],
                        hash_password=password_hash,
                        role=u["role"],
                        email=u["email"],
                        status=UserStatus.active,
                    )
                )
                print(f"  - added {u['email']}")
            elif force:
                existing.user_name = u["user_name"]
                existing.hash_password = password_hash
                existing.role = u["role"]
                existing.status = UserStatus.active
                session.add(existing)
                print(f"  - updated {u['email']} (force)")
            else:
                print(f"  - exists {u['email']} (skip)")

        await session.commit()


async def main_async() -> None:
    parser = argparse.ArgumentParser(description="Seed demo data.")
    parser.add_argument("--force", action="store_true", help="Update seeded users (password/name).")
    args = parser.parse_args()

    try:
        await seed_users(force=args.force)
        print("Seed completed.")
    except SQLAlchemyError as e:
        print("Seed failed (SQLAlchemyError):", e)
        raise


def main() -> None:
    asyncio.run(main_async())

if __name__ == "__main__":
    main()