from fastapi import APIRouter,Depends

router = APIRouter()

from sqlalchemy.orm import Session

from database.repository import PloioRepository
from database.connection import get_ploio_db
repository = PloioRepository()


# 로컬 디비 테스트 api (임시)

@router.get("/dbtest")
def db_test_handler(db: Session = Depends(get_ploio_db)):
    from database.orm import test  # test 모델을 가져옵니다.

    # 데이터베이스에서 모든 test 데이터를 가져옵니다.
    todos = db.query(test).all()

    repository = PloioRepository()

    todos = repository.get_test_data()
    # 가져온 데이터를 JSON 형식으로 반환합니다.
    return todos
