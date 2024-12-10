from tessie_api import TessieAPIManager
from vehicle import Vehicle
from fleet import FleetAnalytics
from visualizer import FleetVisualizer
from key import API_KEY

def main():
    api = TessieAPIManager(API_KEY)
    fleet = FleetAnalytics()

    for vehicle_data in api.get_vehicles():
        vehicle = Vehicle(vehicle_data)
        fleet.add_vehicle(vehicle)

    summary = fleet.get_fleet_summary()
    print("Fleet Summary:", summary)

    visualizer = FleetVisualizer(fleet.vehicles)
    visualizer.create_dashboard()

if __name__ == "__main__":
    main()