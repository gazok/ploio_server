from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/ploio_db"

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_ploio_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
