import requests
from typing import Dict, List

class TessieAPIManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tessie.com"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def get_vehicles(self) -> List[Dict]:
        response = self.session.get(f"{self.base_url}/vehicles?only_active=false")
        return response.json()["results"]