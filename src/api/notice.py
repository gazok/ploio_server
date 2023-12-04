from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_ploio_db, Notice

router = APIRouter()


@router.get("/notice")
def get_notice_data(db: Session = Depends(get_ploio_db)):
    return db.query(Notice).all()

@router.get("/notice-analysis")
def get_notice_analysis(db: Session = Depends(get_ploio_db)):
    notices = db.query(Notice).all()

    result = {}

    for notice in notices:
        timestamp = notice.timestamp
        danger_degree = notice.danger_degree

        if timestamp not in result:
            result[timestamp] = {"Warning": 0, "Fail": 0, "Critical": 0}

        if danger_degree == "Warning":
            result[timestamp]["Warning"] += 1
        if danger_degree == "Fail":
            result[timestamp]["Fail"] += 1
        if danger_degree == "Critical":
            result[timestamp]["Critical"] += 1

    return result