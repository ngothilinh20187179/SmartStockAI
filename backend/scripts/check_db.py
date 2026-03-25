from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Optional

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.database import engine

def _render_url_masked() -> str:
    try:
        return engine.url.render_as_string(hide_password=True)
    except Exception:
        return str(engine.url)


async def check_connection(query: str = "SELECT 1") -> Optional[object]:
    print("Testing database connection...")
    print(f"DB URL: {_render_url_masked()}")
    print(f"Query: {query}")

    async with engine.connect() as conn:
        result = await conn.execute(text(query))
        return result.scalar()


async def main_async() -> None:
    query = "SELECT 1"
    if len(sys.argv) >= 2 and sys.argv[1].strip():
        query = sys.argv[1].strip()

    try:
        value = await check_connection(query=query)
        print(f"Result: {value}")
        if query.strip().upper() == "SELECT 1" and value != 1:
            print("Connected, but unexpected result.")
            sys.exit(2)
        print("Database connection: OK")
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
