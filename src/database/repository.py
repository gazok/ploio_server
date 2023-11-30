from database.connection import Module, Notice
from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from database.connection import get_ploio_db
from model.service.agent_service import packet_data, pod_data


class PloioRepository:
    database = []

    def __init__(self, session: Session = Depends(get_ploio_db)):
        self.session = session

    def create_modules(self, modules_data: dict, db: Session):
        created_modules = []
        try:
            for module_data in modules_data.get("modules", []):
                module = Module(
                    id=module_data.get("GUID", None),
                    name=module_data.get("Name", ""),
                    description=module_data.get("Description", ""),
                    status=module_data.get("status", ""),
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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="모듈 데이터 저장 중 오류 발생",
            )

    def create_notice(self, log_list: dict, db: Session):
        # pod_sample = {
        #     "pods": [
        #         {
        #             "id": "pod-123",
        #             "name": "nginx-7d9f4df5b8-abc12",
        #             "name_space": "default",
        #             "ip": "192.168.1.10",
        #             "danger_degree": "Trace",
        #             "danger_message": "Trace symbol/mark",
        #         },
        #         {
        #             "id": "pod-456",
        #             "name": "redis-6a78bde9c1-xyz34",
        #             "name_space": "app-namespace",
        #             "ip": "172.16.0.8",
        #             "danger_degree": "Trace",
        #             "danger_message": "Trace symbol/mark",
        #         },
        #         {
        #             "id": "pod-789",
        #             "name": "mysql-2e8cfb1a3d-pqr56",
        #             "name_space": "database",
        #             "ip": "1.1.1.1",
        #             "danger_degree": "Trace",
        #             "danger_message": "Trace symbol/mark",
        #         },
        #     ]
        # }
        # packet_sample = {
        #     "data": [
        #         {
        #             "packet_id": "pod-123",
        #             "src_pod": "default:front-end3",
        #             "dst_pod": "default:api-server",
        #             "timestamp": "12341234",
        #             "data_len": 1024,
        #         }
        #     ]
        # }
        created_notices = []
        for log_id, log_entry in log_list.items():
            code = log_entry.get("Code")
            if code in ["Warning", "Fail", "Critical"]:
                for ref in log_entry.get("Refs", []):
                    if ref.get("Source") == "Packet":
                        packet_id = ref.get("Identifier")
                        for packet in packet_data.data:
                            notice = Notice(
                                packet_id=packet_id,
                                src_pod=packet["src_pod"],
                                dst_pod=packet["dst_pod"],
                                timestamp=packet["timestamp"],
                                data_len=packet["data_len"],
                                danger_degree=code,
                                danger_message=log_entry.get("Message", ""),
                            )
                            created_notices.append(notice)
                            db.add(notice)
                        db.commit()

                        for notice in created_notices:
                            db.refresh(notice)

        for log_pod in created_notices:
            for saved_pod in pod_data.pods:
                if log_pod.packet_id == saved_pod["id"]:
                    saved_pod["danger_degree"] = log_pod.danger_degree
                    saved_pod["danger_message"] = log_pod.danger_message

        return created_notices
