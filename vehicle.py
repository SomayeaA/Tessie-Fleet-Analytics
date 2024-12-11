from datetime import datetime
from typing import Dict
from base import VehicleMetrics, ChargingState, BatteryHealth

class Vehicle:
    """Class representing a single Tesla vehicle."""
    def __init__(self, vehicle_data: Dict, battery_health_data: Dict = None):
        self.vin = vehicle_data["vin"]
        self.display_name = vehicle_data["last_state"]["display_name"]
        self.vehicle_type = vehicle_data["last_state"]["vehicle_config"]["car_type"]
        self.metrics_history = []

        self.battery_health = None
        if battery_health_data:
            self.update_battery_health(battery_health_data)
        self.update_metrics(vehicle_data["last_state"])

    def update_battery_health(self, health_data: Dict):
        """Update battery health data."""
        self.battery_health = BatteryHealth(
            max_range=health_data['max_range'],
            max_ideal_range=health_data['max_ideal_range'],
            capacity=health_data['capacity'],
            original_capacity=health_data['original_capacity'],
            degradation_percent=health_data['degradation_percent'],
            health_percent=health_data['health_percent']
        )

    def update_metrics(self, state_data: Dict) -> VehicleMetrics:
        """Update vehicle metrics from state data."""
        config = state_data['vehicle_config']
        charge_state = state_data['charge_state']

        lifetime_energy = (
            charge_state.get('lifetime_energy_used')
            if charge_state.get('lifetime_energy_used') is not None
            else 0.0
        )

        metrics = VehicleMetrics(
            timestamp=datetime.fromtimestamp(state_data['drive_state']['timestamp'] / 1000),
            is_active=state_data['state'] == 'online',
            display_name=state_data['display_name'],
            vin=self.vin,

            battery_level=charge_state['battery_level'],
            battery_range=charge_state['battery_range'],
            charging_state=ChargingState(charge_state['charging_state']),
            lifetime_energy_used=lifetime_energy,

            battery_health=self.battery_health,

            latitude=state_data['drive_state']['latitude'],
            longitude=state_data['drive_state']['longitude'],
            speed=state_data['drive_state']['speed'],
            power=state_data['drive_state']['power'] or 0,
            odometer=state_data['vehicle_state']['odometer'],

            inside_temp=state_data['climate_state']['inside_temp'],
            outside_temp=state_data['climate_state']['outside_temp'],
            is_climate_on=state_data['climate_state']['is_climate_on'],

            model_type=config['car_type'],
            performance_package=config['performance_package'],
            trim_badging=config['trim_badging'],
            efficiency_package=config['efficiency_package']
        )
        self.metrics_history.append(metrics)
        return metrics

    def get_latest_metrics(self):
        """Get the latest vehicle metrics."""
        return self.metrics_history[-1] if self.metrics_history else None