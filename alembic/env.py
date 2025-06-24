import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

#Add app to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

#Load .env variables
from dotenv import load_dotenv
load_dotenv()

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Set DB URL from .env
db_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://actinia:actinia@localhost:5432/actinia")
config.set_main_option("sqlalchemy.url", db_url)

# Import your models and metadata
from app.database import Base
from app import models  # ensures models are registered

target_metadata = Base.metadata

# Ignore PostGIS tables that should not be touched
def include_object(object, name, type_, reflected, compare_to):
    excluded_tables = {
        "addrfeat", "featnames", "zcta5", "direction_lookup", "bg",
        "county_lookup", "state_lookup", "place_lookup", "zip_lookup_base"
    }
    if type_ == "table" and name in excluded_tables:
        return False
    return True


# Migration offline mode
def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )
    with context.begin_transaction():
        context.run_migrations()

# Migration online mode
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )
        with context.begin_transaction():
            context.run_migrations()

# Run migrations depending on mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

