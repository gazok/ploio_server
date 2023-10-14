from typing import List

from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.connection import get_ploio_db
from database.orm import test


class PloioRepository:
    def __init__(self, session: Session = Depends(get_ploio_db)):
        self.session = session

    def get_test_data(self) -> List[test]:
        return list(self.session.scalars(select(test)))