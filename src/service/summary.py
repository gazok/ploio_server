import requests

agent_ip = "54.253.191.26"
agent_port = "8080"


class AgentService:
    def __init__(self, agent_ip, agent_port):
        self.agent_url = f"http://{agent_ip}:{agent_port}"

    async def send_http_get_request(self):
        response = requests.get(f"{self.agent_url}")
        return response.content

    def parse_data(self, data):
        # 데이터 파싱 로직 작성
        parsed_data = {}
        # 데이터 파싱 로직 작성
        return parsed_data
