from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/ploio_db"
engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Module(Base):
    __tablename__ = "modules"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))

Base.metadata.create_all(bind=engine)

def get_ploio_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
