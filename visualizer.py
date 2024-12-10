import plotly.graph_objects as go
from typing import List
from vehicle import Vehicle

class FleetVisualizer:
    def __init__(self, vehicles: List[Vehicle]):
        self.vehicles = vehicles

    def create_dashboard(self, output_file: str = "dashboard.html"):
        # Battery levels
        fig = go.Figure()
        for vehicle in self.vehicles:
            metrics = vehicle.get_latest_metrics()
            fig.add_trace(
                go.Bar(
                    name=vehicle.display_name,
                    x=[vehicle.display_name],
                    y=[metrics.battery_level],
                    text=[f"{metrics.battery_level}%"]
                )
            )
        fig.update_layout(title="Vehicle Battery Levels")
        fig.write_html(output_file)