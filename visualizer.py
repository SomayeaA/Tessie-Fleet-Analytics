import plotly.graph_objects as go
from typing import List
from vehicle import Vehicle

class FleetVisualizer:
    """Class for creating fleet data visualizations."""
    def __init__(self, vehicles: List[Vehicle]):
        self.vehicles = vehicles

    def create_dashboard(self, output_file: str = "dashboard.html"):
        """Create an interactive dashboard of fleet metrics."""
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

        # Vehicle locations
        fig_map = go.Figure()
        fig_map.add_trace(
            go.Scattermapbox(
                lat=[v.get_latest_metrics().latitude for v in self.vehicles],
                lon=[v.get_latest_metrics().longitude for v in self.vehicles],
                mode='markers+text',
                marker=dict(size=12),
                text=[v.display_name for v in self.vehicles],
                name="Vehicle Locations"
            )
        )
        fig_map.update_layout(
            title="Vehicle Locations",
            mapbox=dict(
                style="carto-positron",
                zoom=10,
                center=dict(
                    lat=sum(v.get_latest_metrics().latitude for v in self.vehicles) / len(self.vehicles),
                    lon=sum(v.get_latest_metrics().longitude for v in self.vehicles) / len(self.vehicles)
                )
            )
        )

        # Lifetime Energy Usage
        fig_energy = go.Figure()
        for vehicle in self.vehicles:
            metrics = vehicle.get_latest_metrics()
            if metrics.lifetime_energy_used is not None:
                fig_energy.add_trace(
                    go.Bar(
                        name=vehicle.display_name,
                        x=[vehicle.display_name],
                        y=[metrics.lifetime_energy_used],
                        text=[f"{metrics.lifetime_energy_used:,.0f} kWh"],
                        textposition='auto',
                    )
                )
        fig_energy.update_layout(
            title="Lifetime Energy Usage",
            yaxis_title="Energy Used (kWh)"
        )
        fig.write_html(output_file)
