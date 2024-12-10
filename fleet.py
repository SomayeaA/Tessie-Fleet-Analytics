from vehicle import Vehicle

class FleetAnalytics:
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)

    def get_fleet_summary(self) -> dict:
        return {
            "total_vehicles": len(self.vehicles),
            "total_miles": sum(v.get_latest_metrics().odometer for v in self.vehicles),
            "average_battery": sum(v.get_latest_metrics().battery_level for v in self.vehicles) / len(self.vehicles)
        }