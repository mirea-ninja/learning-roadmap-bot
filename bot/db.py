import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from bot import config

logger = logging.getLogger(__name__)

engine = create_engine(config.DATABASE_URI, isolation_level="AUTOCOMMIT")
base = declarative_base()
base.metadata.bind = engine
base.metadata.create_all(engine)


@contextmanager
def db_session():
    session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
    try:
        yield session
    except:
        logger.error("An error has occured in runtime SQL query.")
        session.rollback()
        raise
    finally:
        session.close()
