from fastapi import FastAPI
import asyncio
import json
import requests
import struct

from collections import deque

app = FastAPI()

# 나중에 노드 순회해야함.
# 워커노드 1
agent_ip = "3.24.213.237"
agent_port = "65001"

traffic_path = "/traffic"
pod_path = "/pod"
log_path = "/log"

parsed_data = deque(maxlen=100)
packet_data = deque(maxlen=100)
pod_data = deque(maxlen=100)
log_data = deque(maxlen=100)

malicious_pod = deque(maxlen=100)


async def fetching_process():
    # 반복적으로 req를 보내고, reply를 파싱해서 공유변수 parsed_data에 저장
    while True:
        agent_service = AgentService(agent_ip, agent_port)

        # agent_service.get_bit_stream()
        packet_data.append(agent_service.get_packet_data())
        pod_data.append(agent_service.get_pod_data())
        log_data.append(agent_service.get_log_data())

        # 텀 두기
        await asyncio.sleep(2)


class AgentService:
    # agent에 접근할 때 쓰일 서비스 클래스
    def __init__(self):
        pass

    def get_packet_data():
        agent_url = f"http://{agent_ip}{traffic_path}:{agent_port}"
        response = requests.get(f"{agent_url}")
        for packet_id, packet_info in response.json().items():
            if "Raw" in packet_info:
                del packet_info["Raw"]
        return response.json()

    def get_pod_data():
        agent_url = f"http://{agent_ip}{pod_path}:{agent_port}"
        response = requests.get(f"{agent_url}")
        return response.content

    def get_log_data():
        agent_url = f"http://{agent_ip}{log_path}:{agent_port}"
        response = requests.get(f"{agent_url}")
        malicious_packet = deque
        malicious_packet.extend(
            log["Refs"][0]["Identifier"]
            for log_id, log in response.items()
            if log.get("Code", 0) >= 2
        )
        for packet in malicious_packet:
            packet_id = packet["packet-id"]

            # 예시 JSON 데이터에서 해당 패킷의 정보 가져오기
            if packet_id in packet_data:
                packet_info = packet_data[packet_id]

                # packet-id에 해당하는 패킷의 Source와 Destination 가져오기
                malicious_pod.append(packet_info["Source"])
                malicious_pod.append(packet_info["Destination"])

        return response.content

    # 아래부터는 비트 스트림 받아오는 구 버전 api들

    # fetching process에서 쓰는 멤버함수.
    def get_bit_stream(self, agent_ip: str, agent_port: str) -> bytes:
        agent_url = f"http://{agent_ip}:{agent_port}"
        response = requests.get(f"{agent_url}")
        data = AgentService.parse_data(response.content)
        parsed_data.append(data)

    # req로 받아온 reply data를 파싱하는 로직
    def parse_data(self, bitstream):
        log_data = {"data": []}
        signature, version, count_of_log = struct.unpack(">4s4si", bitstream[:12])

        # add header info into temp buffer
        log_data["signature"] = signature.decode("utf-8")
        log_data["version"] = int.from_bytes(version, byteorder="little")
        log_data["count_of_log"] = count_of_log

        offset = 12  # header size

        # insert logs into temp buffer by the count
        for i in range(count_of_log):
            data = {}
            # parse agent data
            (
                unix_epoch,
                l2_protocol,
                l3_protocol,
                l7_protocol,
                sip,
                dip,
                sport,
                dport,
                size,
            ) = struct.unpack(">qHBB16s16sHHi", bitstream[offset : offset + 52])

            # assign data after Ipv4 / Ipv6 check
            data["src_ip"] = self.check_ip(l2_protocol, sip)
            data["src_port"] = sport

            # assign data after Ipv4 / Ipv6 check
            data["dst_ip"] = self.check_ip(l2_protocol, dip)
            data["dst_port"] = dport
            data["data_len"] = size

            data["protocol"] = self.check_protocol(l3_protocol)
            data["timestamp"] = unix_epoch

            # add into temp buffer
            log_data["data"].append(data)

            offset += 52  # 다음 로그 항목으로 이동
        # insert temp buffer into log buffer
        with open("tmp/parsed_data.json", "w") as json_file:
            json.dump(log_data, json_file, indent=4)

        return log_data

    def check_protocol(self, protocol):
        # check protocol type
        if protocol == 6:
            protocol_type = "TCP"
        elif protocol == 17:
            protocol_type = "UDP"
        return protocol_type

    def check_ip(self, ip_type, ip_hex):
        # Ipv4
        if ip_type == 1:
            bytes_list = [ip_hex[i : i + 4] for i in range(0, len(ip_hex), 4)]
            ip_address = ".".join([str(byte) for byte in bytes_list[0]])
            return ip_address
        # 그외
        # else:
