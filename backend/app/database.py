import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

TURSO_URL   = os.getenv("TURSO_DATABASE_URL")
TURSO_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

if TURSO_URL and TURSO_TOKEN:
    # Production: Turso (libSQL) — drop-in SQLite replacement
    import libsql_experimental as libsql

    def _creator():
        conn = libsql.connect("local.db", sync_url=TURSO_URL, auth_token=TURSO_TOKEN)
        conn.sync()
        # SQLAlchemy's pysqlite dialect requires create_function for REGEXP support
        if not hasattr(conn, "create_function"):
            conn.create_function = lambda *args, **kwargs: None
        return conn

    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        creator=_creator,
        connect_args={"check_same_thread": False},
    )
else:
    # Local dev: plain SQLite
    _url = os.getenv("DATABASE_URL", "sqlite:///./portfolio.db")
    engine = create_engine(_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
