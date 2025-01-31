import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(url_connection):
    global __factory

    if __factory:
        return

    if not url_connection or not url_connection.strip():
        raise Exception("Database file not found")

    print(f"Connection to {url_connection}")

    conn_str = f'sqlite:///{url_connection.strip()}?check_same_thread=False'

    engine = sa.create_engine(conn_str, echo=False, pool_timeout=60, pool_size=2000, max_overflow=4000)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
