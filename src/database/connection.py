from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import os
from fastapi import Depends, HTTPException

# DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/ploio_db"
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
PLOIO_SESSION = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Module(Base):
    __tablename__ = "modules"

    guid = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    status = Column(String(50))


class Notice(Base):
    __tablename__ = "notices"

    packet_id = Column(String(50), primary_key=True, index=True)
    src_pod = Column(String(255))
    dst_pod = Column(String(255))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
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

def insert_default_modules(db: Session = Depends(get_ploio_db)):
    try:
        module1 = Module(
            guid="a41bf61a-aa05-40b5-b8a1-252a9884e768",
            name="ssh",
            description="Module that detects that ssh connection attempts per second increase by a certain level.",
            status="inactive"
        )
        module2 = Module(
            guid="c9478e3c-0c5b-4eac-815a-c5682263574f",
            name="log4j",
            description="log4j4j4j4j4j4j",
            status="inactive"
        )

        db.add_all([module1, module2])
        db.commit()
        db.refresh(module1)
        db.refresh(module2)
        return {"message": "Default modules inserted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()