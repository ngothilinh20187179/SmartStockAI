from logging.config import fileConfig
import os
import sys
from os.path import abspath, dirname, join
from typing import Optional
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from sqlmodel import SQLModel

_backend_root = dirname(dirname(abspath(__file__)))
_repo_root = dirname(_backend_root)
sys.path.insert(0, _backend_root)
for _env_path in (join(_backend_root, ".env"), join(_repo_root, ".env")):
    load_dotenv(_env_path)

from app.models import (
    User, 
    Supplier, 
    Product, 
    Category, 
    Unit, 
    ProductUnitConversion, 
    Invoice, 
    InvoiceItem, 
    StockLog
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


def _sync_database_url() -> Optional[str]:
    """Build sync URL for Alembic (psycopg). Prefer DATABASE_URL from .env."""
    raw = os.getenv("DATABASE_URL")
    if raw:
        url = (
            raw.replace("postgresql+asyncpg", "postgresql+psycopg", 1)
            .replace("postgres+asyncpg", "postgresql+psycopg", 1)
        )
        # Same hostname issue when DATABASE_URL still points at the Compose service name.
        if "@db:" in url:
            url = url.replace("@db:", "@localhost:", 1)
        elif "@db/" in url:
            url = url.replace("@db/", "@localhost/", 1)
        return url
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    name = os.getenv("DB_NAME")
    if user is None or password is None or not name:
        return None
    port = os.getenv("DB_PORT", "5432")
    host = os.getenv("DB_HOST", "localhost")
    # Docker Compose service name; on the host machine use localhost instead.
    if host.strip() == "db":
        host = "localhost"
    pw = quote_plus(password)
    return f"postgresql+psycopg://{user}:{pw}@{host}:{port}/{name}"


def _effective_sqlalchemy_url() -> str:
    url = _sync_database_url()
    if url:
        return url
    ini_url = config.get_main_option("sqlalchemy.url")
    if not ini_url:
        raise RuntimeError(
            "No database URL configured. Set DATABASE_URL (recommended) or "
            "configure sqlalchemy.url in alembic.ini."
        )
    return ini_url


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = _effective_sqlalchemy_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    ini_section = config.get_section(config.config_ini_section, {})
    url = _sync_database_url()
    if url:
        ini_section = dict(ini_section)
        ini_section["sqlalchemy.url"] = url

    connectable = engine_from_config(
        ini_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
