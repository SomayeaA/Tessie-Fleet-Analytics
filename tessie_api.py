import requests
from typing import Dict, List

class TessieAPIManager:
    """Base API manager for Tessie API communication."""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tessie.com"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def get_vehicles(self) -> List[Dict]:
        """Fetch all vehicles data."""
        response = self.session.get(f"{self.base_url}/vehicles?only_active=false")
        return response.json()["results"]

    def get_battery_health(self) -> List[Dict]:
        """Fetch battery health data for all vehicles."""
        response = self.session.get(f"{self.base_url}/battery_health?distance_format=mi&only_active=false")
        return response.json()["results"]