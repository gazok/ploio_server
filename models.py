# # models.py

# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Item(Base):
#     __tablename__ = 'test'  # 데이터베이스 테이블 이름
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#         }
