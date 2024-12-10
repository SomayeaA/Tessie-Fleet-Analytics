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

    def export_metrics(self, filename: str):
        """Export current fleet metrics to CSV."""
        data = []
        for vehicle in self.vehicles:
            metrics = vehicle.get_latest_metrics()
            data.append({
                "timestamp": metrics.timestamp,
                "vehicle_name": vehicle.display_name,
                "vehicle_type": vehicle.vehicle_type,
                "battery_level": metrics.battery_level,
                "battery_range": metrics.battery_range,
                "is_active": metrics.is_active,
                "charging_state": metrics.charging_state.value,
                "odometer": metrics.odometer,
                "inside_temp": metrics.inside_temp,
                "outside_temp": metrics.outside_temp
            })

        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
