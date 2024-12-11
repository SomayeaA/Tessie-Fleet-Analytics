from datetime import datetime
from typing import Dict
from base import VehicleMetrics, ChargingState

class Vehicle:
    def __init__(self, vehicle_data: Dict):
        self.vin = vehicle_data["vin"]
        self.display_name = vehicle_data["last_state"]["display_name"]
        self.metrics_history = []
        self.update_metrics(vehicle_data["last_state"])

    def update_metrics(self, state_data: Dict) -> VehicleMetrics:
        metrics = VehicleMetrics(
            timestamp=datetime.fromtimestamp(state_data['drive_state']['timestamp'] / 1000),
            battery_level=state_data['charge_state']['battery_level'],
            charging_state=ChargingState(state_data['charge_state']['charging_state']),
            battery_range=state_data['charge_state']['battery_range'],
            latitude=state_data['drive_state']['latitude'],
            longitude=state_data['drive_state']['longitude'],
            odometer=state_data['vehicle_state']['odometer'],
            inside_temp=state_data['climate_state']['inside_temp'],
            outside_temp=state_data['climate_state']['outside_temp']
        )
        self.metrics_history.append(metrics)
        return metrics

    def get_latest_metrics(self):
        return self.metrics_history[-1] if self.metrics_history else None