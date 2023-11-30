from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_ploio_db, Notice

router = APIRouter()


@router.get("/notice")
def get_notice_data(db: Session = Depends(get_ploio_db)):
    return db.query(Notice).all()
