from backend.core.config import config
from backend.models import load_models
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker, declarative_base
import subprocess

Base = declarative_base()

_engine = {}
_SessionLocal = None


def get_engine(db=config.SQL_DB_NAME):
    global _engine
    if db not in _engine:
        _engine[db] = create_engine(config.SQL_DB_URL + db)
    return _engine[db]


def get_session_local() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )()
    return _SessionLocal


def get_sql_db():
    return Base


def reset_database():
    engine = get_engine("postgres")

    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")

        conn.execute(text(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{config.SQL_DB_NAME}'
              AND pid <> pg_backend_pid();
            """))

        conn.execute(text(f'DROP DATABASE IF EXISTS "{config.SQL_DB_NAME}"'))

        conn.execute(text(f'CREATE DATABASE "{config.SQL_DB_NAME}"'))

    subprocess.run(["alembic", "upgrade", "head"], check=True)


def truncate_tables():
    load_models()

    engine = get_engine()
    metadata = Base.metadata

    tables = []

    for table in metadata.sorted_tables:
        model_should_truncate = True

        for mapper in Base.registry.mappers:
            model = mapper.class_

            if getattr(model, "__tablename__", None) == table.name:
                model_should_truncate = getattr(model, "__truncate__", True)
                break

        if model_should_truncate:
            tables.append(table)

    if not tables:
        return

    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")

        tables_sql = ", ".join(
            f'"{table.schema}"."{table.name}"' if table.schema else f'"{table.name}"'
            for table in tables
        )

        conn.execute(text(f"TRUNCATE TABLE {tables_sql} " f"RESTART IDENTITY CASCADE"))
