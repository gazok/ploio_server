from database.connection import Module, Notice
from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from database.connection import get_ploio_db
from model.service.agent_service import packet_data, pod_data


class PloioRepository:
    database = []

    def __init__(self, session: Session = Depends(get_ploio_db)):
        self.session = session

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
        #     "packets": [
        #         {
        #             "packet_id": "pkt-1",
        #             "src_pod": "default:pod-1",
        #             "dst_pod": "default:pod-22",
        #             "timestamp": "2023-12-04 12:34:56",
        #             "data_len": 1024,
        #         },
        #         {
        #             "packet_id": "pkt-2",
        #             "src_pod": "default:pod-2",
        #             "dst_pod": "default:api-server2",
        #             "timestamp": "2023-12-03 00:00:12",
        #             "data_len": 512,
        #         },
        #     ]
        # }
        created_notices = []

        for log_id, log_entry in log_list.items():
            code = log_entry.get("Code", "Trace")

            if code in ["Warning", "Fail", "Critical"]:
                self.process_notices_with_log(
                    log_entry, packet_data, created_notices, db
                )

        db.commit()
        self.refresh_notices(created_notices, db)

        for log_pod in created_notices:
            for saved_pod in pod_data.pods:
                if log_pod.packet_id == saved_pod["id"]:
                    saved_pod["danger_degree"] = log_pod.danger_degree
                    saved_pod["danger_message"] = log_pod.danger_message

        return created_notices

    def process_notices_with_log(self, log_entry, packet_data, created_notices, db):
        for ref in self.get_packet_refs(log_entry):
            malicious_packet_id = self.get_packet_identifier(ref)

            packet_info = self.find_packet_info(packet_data, malicious_packet_id)
            if packet_info:
                notice = self.create_notice_from_packet(ref, packet_info, log_entry)
                self.save_notice_to_database(notice, created_notices, db)

    def get_packet_refs(self, log_entry):
        return log_entry.get("Refs", [])

    def get_packet_identifier(self, ref):
        return ref.get("Identifier", "None")

    def find_packet_info(self, packet_data, malicious_packet_id):
        for packet in packet_data.packets:
            if packet["packet_id"] == malicious_packet_id:
                return packet

    def create_notice_from_packet(self, ref, packet_info, log_entry):
        return Notice(
            packet_id=ref.get("Identifier", "None"),
            src_pod=packet_info["src_pod"],
            dst_pod=packet_info["dst_pod"],
            timestamp=packet_info["timestamp"],
            data_len=packet_info["data_len"],
            danger_degree=log_entry.get("Code", "Trace"),
            danger_message=log_entry.get("Message", "Trace symbol/mark"),
        )

    def save_notice_to_database(self, notice, created_notices, db):
        created_notices.append(notice)
        db.add(notice)

    def refresh_notices(self, created_notices, db):
        for notice in created_notices:
            db.refresh(notice)
