from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=True)
    
class Module(Base):
    __tablename__ = "modules"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
