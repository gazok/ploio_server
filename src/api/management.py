from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_ploio_db
from database.connection import Module
from model.service.operation_service import Operation_service
from model.domain.module import ModuleItem, ModuleList

router = APIRouter()

operation_service = Operation_service()


@router.get("/management")
def get_module_data(db: Session = Depends(get_ploio_db)):
    module_list = db.query(Module).all()
    module_data = ModuleList(modules=[])
    for module in module_list:
        module_data.modules.append(
            ModuleItem(
                GUID="guidguid-guidguid-guid-guid",  # Replace with actual GUID
                Name=module.name,
                Description=module.description,
                Status=module.status,
            )
        )

    return module_data


@router.post("/management")
def update_module_status(request: dict, db: Session = Depends(get_ploio_db)):
    id = request["id"]
    try:
        module = db.query(Module).filter(Module.id == id).first()

        if module:
            module.status = "inactive" if module.status == "active" else "active"
            db.commit()

            db.refresh(module)

            return {"GUID": module.id, "status": module.status}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Module not found"
            )

    except Exception as e:
        print("모듈 상태 업데이트 중 오류:", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="모듈 상태 업데이트 중 오류 발생",
        )
