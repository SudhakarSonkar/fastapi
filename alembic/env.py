from logging.config import fileConfig
from urllib.parse import quote
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.models import Base
from app.config import settings

# Alembic Config object
config = context.config

# URL-encode the password (this ensures special characters like % are handled properly)
encoded_password = quote(settings.database_password)

# Build the SQLAlchemy URL string with the encoded password
sqlalchemy_url = f'postgresql+psycopg2://{settings.database_username}:{encoded_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Ensure no interpolation occurs by directly setting the URL without using the .ini
config.set_main_option("sqlalchemy.url", sqlalchemy_url)

# Set up logging if needed
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate support
target_metadata = Base.metadata

# Migration functions
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=sqlalchemy_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Decide which mode to run
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
