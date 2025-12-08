import os
from alembic import context
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine

load_dotenv()

from core.database import BASE
from contact.models import Contact 
from auth.models import User
from vacancy.models import VacancyApplication
from therapy.models import Therapy

target_metadata = BASE.metadata 

DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: int = os.getenv("DB_PORT")
DB_USER: str = os.getenv("DB_USER")
DB_NAME: str = os.getenv("DB_NAME")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Logging setup
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode(): run_migrations_offline()
else: run_migrations_online()

# alembic revision --autogenerate -m "initial tables"
# alembic upgrade head