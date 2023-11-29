from database.connection import Module
from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from database.connection import get_ploio_db


class PloioRepository:
    database = []
    def __init__(self, session: Session = Depends(get_ploio_db)):
        self.session = session

    def create_modules(self, modules_data: dict, db: Session):
        created_modules = []
        try:
            for module_data in modules_data.get('modules', []):
                module = Module(
                    id=module_data.get('GUID', None),
                    name=module_data.get('Name', ''),
                    description=module_data.get('Description', ''),
                    status=module_data.get('status', '')
                )
                created_modules.append(module)
                db.add(module)
            
            db.commit()

            for module in created_modules:
                db.refresh(module)
        
            return created_modules
        except Exception as e:
            print("모듈 데이터 저장 중 오류:", e)
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="모듈 데이터 저장 중 오류 발생")
