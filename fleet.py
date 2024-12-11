from typing import List, Dict, Any
from datetime import datetime
from vehicle import Vehicle
import pandas as pd

class FleetAnalytics:
    """Class for analyzing fleet-wide metrics."""
    def __init__(self):
        self.vehicles: List[Vehicle] = []

    def add_vehicle(self, vehicle: Vehicle):
        """Add a vehicle to the fleet."""
        self.vehicles.append(vehicle)

    def get_fleet_summary(self) -> Dict[str, Any]:
        """Get current fleet-wide summary metrics."""
        active_vehicles = [v for v in self.vehicles if v.get_latest_metrics().is_active]

        return {
            "total_vehicles": len(self.vehicles),
            "active_vehicles": len(active_vehicles),
            "total_fleet_miles": sum(v.get_latest_metrics().odometer for v in self.vehicles),
            "average_battery_level": sum(v.get_latest_metrics().battery_level for v in self.vehicles) / len(
                self.vehicles),
            "vehicles_charging": sum(
                1 for v in self.vehicles if v.get_latest_metrics().charging_state.value == "Charging")
        }
