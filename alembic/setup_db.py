import subprocess

from sqlalchemy import create_engine, text


DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "llm"

ADMIN_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
)


def create_database_if_not_exists():
    engine = create_engine(ADMIN_DATABASE_URL)

    with engine.connect() as connection:
        connection = connection.execution_options(isolation_level="AUTOCOMMIT")

        result = connection.execute(
            text(
                "SELECT 1 FROM pg_database WHERE datname = :db_name"
            ),
            {"db_name": DB_NAME},
        )

        exists = result.scalar()

        if not exists:
            connection.execute(text(f'CREATE DATABASE "{DB_NAME}"'))
            print(f"Database '{DB_NAME}' created")
        else:
            print(f"Database '{DB_NAME}' already exists")



def run_migrations():
    print("Running alembic migrations...")

    subprocess.run(
        ["alembic", "upgrade", "head"],
        check=True,
    )

    print("Migrations completed")


if __name__ == "__main__":
    create_database_if_not_exists()
    run_migrations()