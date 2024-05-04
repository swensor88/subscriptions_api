from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

from app.backend.config import config


# create session factory to generate new database sessions
SessionFactory = sessionmaker(
    bind=create_engine(config.database.dsn, pool_size=10, pool_timeout=5, pool_pre_ping=True, connect_args={'options': '-c lock_timeout=5 -c statement_timeout=5'}),
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def create_session() -> Iterator[Session]:
    """Create new database session.

    Yields:
        Database session.
    """

    session = SessionFactory()

    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@contextmanager
def open_session() -> Iterator[Session]:
    """Create new database session with context manager.

    Yields:
        Database session.
    """

    return create_session()