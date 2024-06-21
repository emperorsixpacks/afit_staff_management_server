from sqlmodel import create_engine
from sqlmodel.orm.session import Session

from management_server.server.settings import DBSettings


database = DBSettings()
engine = create_engine(
    url=database.database_url,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)


def get_session():
    with Session(engine) as session:
        try:
            return session
        finally:
            session.close()
