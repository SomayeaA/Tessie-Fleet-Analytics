from tessie_api import TessieAPIManager
from vehicle import Vehicle
from fleet import FleetAnalytics
from visualizer import FleetVisualizer
from key import API_KEY


def main():
    """Main function to run the fleet analytics."""
    # Initialize API manager
    api_manager = TessieAPIManager(
        api_key=API_KEY,
    )

    # Get vehicles and battery health data
    vehicles_data = api_manager.get_vehicles()
    battery_health_data = api_manager.get_battery_health()

    # Create a mapping of VIN to battery health data
    health_map = {item['vin']: item for item in battery_health_data}

    # Initialize fleet analytics
    fleet = FleetAnalytics()

    # Create vehicle objects and add to fleet
    for vehicle_data in vehicles_data:
        vin = vehicle_data['vin']
        health_data = health_map.get(vin)
        vehicle = Vehicle(vehicle_data, health_data)
        fleet.add_vehicle(vehicle)

    # Get fleet summary
    summary = fleet.get_fleet_summary()
    print("Fleet Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    # Create visualizations
    visualizer = FleetVisualizer(fleet.vehicles)
    visualizer.create_dashboard("dashboard.html")


if __name__ == "__main__":
    main()