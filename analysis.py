from typing import List, Dict
from vehicle import Vehicle


class EnergyAndCostAnalyzer:
    """Analyzes energy efficiency and cost metrics for Tesla fleet."""
    def __init__(self, vehicles: List[Vehicle], kwh_rate: float = 0.36):
        self.vehicles = vehicles
        self.kwh_rate = kwh_rate

    def calculate_efficiency_metrics(self) -> Dict:
        """Calculate energy efficiency metrics for each vehicle and the fleet."""
        efficiency_data = []
        total_energy = 0
        total_miles = 0

        for vehicle in self.vehicles:
            metrics = vehicle.get_latest_metrics()
            if metrics.odometer:
                # Use actual lifetime energy
                if metrics.lifetime_energy_used:
                    efficiency = metrics.lifetime_energy_used / metrics.odometer
                    total_energy_used = metrics.lifetime_energy_used
                    source = "Actual"
                else:
                    # Use estimated efficiency for vehicles without lifetime energy data
                    if metrics.model_type.lower() == "modely":
                        efficiency = 0.285  # Model Y Long Range
                    else:
                        efficiency = 0.245  # Model 3 Standard Range
                    total_energy_used = metrics.odometer * efficiency
                    source = "Estimated"

                total_cost = total_energy_used * self.kwh_rate
                cost_per_mile = total_cost / metrics.odometer

                efficiency_data.append({
                    'name': vehicle.display_name,
                    'model': metrics.model_type,
                    'total_miles': metrics.odometer,
                    'total_energy': total_energy_used,
                    'efficiency': efficiency,
                    'total_cost': total_cost,
                    'cost_per_mile': cost_per_mile,
                    'source': source
                })

                total_energy += total_energy_used
                total_miles += metrics.odometer

        # Sort by efficiency
        efficiency_data.sort(key=lambda x: x['efficiency'])

        fleet_metrics = {
            'vehicles': efficiency_data,
            'fleet_summary': {
                'total_vehicles': len(self.vehicles),
                'total_energy_used': total_energy,
                'total_miles': total_miles,
                'fleet_efficiency': total_energy / total_miles if total_miles > 0 else 0,
                'total_cost': total_energy * self.kwh_rate,
                'average_cost_per_mile': (total_energy * self.kwh_rate) / total_miles if total_miles > 0 else 0
            }
        }

        return fleet_metrics

    def generate_text_report(self) -> str:
        """Generate a text-based report of energy efficiency and cost analysis."""
        metrics = self.calculate_efficiency_metrics()

        report = [
            "Energy Efficiency and Cost Analysis Report",
            "\nFleet Summary:",
            f"- Total Vehicles: {metrics['fleet_summary']['total_vehicles']}",
            f"- Total Energy Used: {metrics['fleet_summary']['total_energy_used']:,.2f} kWh",
            f"- Total Miles Driven: {metrics['fleet_summary']['total_miles']:,.2f} miles",
            f"- Fleet Average Efficiency: {metrics['fleet_summary']['fleet_efficiency']:.3f} kWh/mile",
            f"- Total Energy Cost: ${metrics['fleet_summary']['total_cost']:,.2f}",
            f"- Average Cost per Mile: ${metrics['fleet_summary']['average_cost_per_mile']:.3f}",
            "\nVehicle Rankings (by efficiency):"
        ]

        for idx, vehicle in enumerate(metrics['vehicles'], 1):
            report.append(
                f"\n{idx}. {vehicle['name']} ({vehicle['model']}) - {vehicle['source']} Data:"
                f"\n   - Efficiency: {vehicle['efficiency']:.3f} kWh/mile"
                f"\n   - Total Energy Used: {vehicle['total_energy']:,.1f} kWh"
                f"\n   - Total Cost: ${vehicle['total_cost']:,.2f}"
                f"\n   - Cost per Mile: ${vehicle['cost_per_mile']:.3f}"
            )

        return "\n".join(report)

    def save_text_report(self, filename: str = "energy_report.txt") -> None:
        """Save the text report to a file."""
        report = self.generate_text_report()
        with open(filename, 'w') as f:
            f.write(report)