from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/ploio_db"
engine = create_engine(DATABASE_URL)
PLOIO_SESSION = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Module(Base):
    __tablename__ = "modules"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    status = Column(String(50))


class Notice(Base):
    __tablename__ = "notices"

    packet_id = Column(String(50), primary_key=True, index=True)
    src_pod = Column(String(255))
    dst_pod = Column(String(255))
    timestamp = Column(String(255))
    data_len = Column(Integer)
    danger_degree = Column(String(255))
    danger_message = Column(String(255))


Base.metadata.create_all(bind=engine)


def get_ploio_db():
    session = PLOIO_SESSION()
    try:
        yield session
    finally:
        session.close()
