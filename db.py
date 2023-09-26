from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HOST = 'localhost'  # MySQL 호스트
PORT = '3306'  # MySQL 포트
DBNAME = 'ploio_db'  # 데이터베이스 이름
USER = 'root'  # MySQL 사용자 이름
PASSWORD = 'root'  # MySQL 비밀번호

DB_URL = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

class EngineConn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle=500)

    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def get_connection(self):
        conn = self.engine.connect()
        return conn
