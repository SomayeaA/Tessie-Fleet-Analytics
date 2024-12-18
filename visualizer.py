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
        fig_battery = go.Figure()
        for vehicle in self.vehicles:
            metrics = vehicle.get_latest_metrics()
            fig_battery.add_trace(
                go.Bar(
                    name=vehicle.display_name,
                    x=[vehicle.display_name],
                    y=[metrics.battery_level],
                    text=[f"{metrics.battery_level}%"]
                )
            )
        fig_battery.update_layout(
            title="Vehicle Battery Levels",
            yaxis_title="Battery Level (%)"
        )

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

        # Battery Health Comparison
        fig_health = go.Figure()
        fig_health.add_trace(
            go.Bar(
                name="Health",
                x=[v.display_name for v in self.vehicles],
                y=[v.get_latest_metrics().battery_health.health_percent for v in self.vehicles],
                text=[f"{v.get_latest_metrics().battery_health.health_percent}%" for v in self.vehicles],
                textposition='auto',
                marker_color='green'
            )
        )
        fig_health.add_trace(
            go.Bar(
                name="Degradation",
                x=[v.display_name for v in self.vehicles],
                y=[v.get_latest_metrics().battery_health.degradation_percent for v in self.vehicles],
                text=[f"{v.get_latest_metrics().battery_health.degradation_percent}%" for v in self.vehicles],
                textposition='auto',
                marker_color='red'
            )
        )
        fig_health.update_layout(
            title="Battery Health vs Degradation",
            yaxis_title="Percentage",
            barmode='group'
        )

        # Battery Capacity Comparison
        fig_capacity = go.Figure()
        for vehicle in self.vehicles:
            metrics = vehicle.get_latest_metrics()
            health = metrics.battery_health
            fig_capacity.add_trace(
                go.Bar(
                    name=vehicle.display_name,
                    x=['Current', 'Original'],
                    y=[health.capacity, health.original_capacity],
                    text=[f"{health.capacity:.1f} kWh", f"{health.original_capacity:.1f} kWh"],
                    textposition='auto',
                )
            )
        fig_capacity.update_layout(
            title="Battery Capacity Comparison",
            yaxis_title="Capacity (kWh)",
            barmode='group'
        )

        # Range vs Odometer Scatter
        fig_range = go.Figure()
        fig_range.add_trace(
            go.Scatter(
                x=[v.get_latest_metrics().odometer for v in self.vehicles],
                y=[v.get_latest_metrics().battery_health.max_range for v in self.vehicles],
                mode='markers+text',
                text=[v.display_name for v in self.vehicles],
                textposition="top center",
                marker=dict(
                    size=12,
                    color=[v.get_latest_metrics().battery_health.health_percent for v in self.vehicles],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Health %")
                )
            )
        )
        fig_range.update_layout(
            title="Maximum Range vs Odometer",
            xaxis_title="Odometer (miles)",
            yaxis_title="Maximum Range (miles)"
        )

        # Model Comparison Table
        model_data = []
        for vehicle in self.vehicles:
            metrics = vehicle.get_latest_metrics()
            health = metrics.battery_health
            model_data.append([
                vehicle.display_name,
                metrics.model_type,
                metrics.performance_package,
                f"{metrics.odometer:,.0f}",
                f"{health.health_percent:.1f}%",
                f"{health.max_range:.0f}",
                f"{health.capacity:.1f}"
            ])

        fig_models = go.Figure(data=[go.Table(
            header=dict(
                values=['Vehicle', 'Model', 'Performance', 'Odometer', 'Health', 'Max Range', 'Capacity'],
                fill_color='paleturquoise',
                align='left'
            ),
            cells=dict(
                values=list(zip(*model_data)),
                fill_color='lavender',
                align='left'
            )
        )])
        fig_models.update_layout(title="Vehicle Comparison")

        # Export to HTML
        with open(output_file, 'w') as f:
            f.write("""
            <html>
            <head>
                <title>Tesla Fleet Dashboard</title>
                <style>
                    .dashboard {
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        grid-gap: 20px;
                        padding: 20px;
                        max-width: 1400px;
                        margin: 0 auto;
                    }
                    .plot {
                        width: 100%;
                        height: 500px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        padding: 10px;
                    }
                    .wide-plot {
                        grid-column: 1 / -1;
                        height: auto !important;
                        min-height: 400px;
                    }
                    h1 {
                        text-align: center;
                        color: #333;
                        padding: 20px;
                    }
                    .section-title {
                        grid-column: 1 / -1;
                        text-align: center;
                        margin: 20px 0;
                        color: #666;
                    }
                    footer {
                        text-align: center;
                        padding: 20px;
                        background-color: #f1f1f1;
                        color: #333;
                    position: fixed;
                    width: 100%;
                    bottom: 0;
                    }
                </style>
            </head>
            <body>
                <h1>Tesla Fleet Analytics Dashboard</h1>
                <div class="dashboard">
                    <div class="section-title"><h2>Current Status</h2></div>
                    <div class="plot">
            """)
            f.write(fig_battery.to_html(full_html=False, include_plotlyjs='cdn'))
            f.write('</div><div class="plot">')
            f.write(fig_map.to_html(full_html=False, include_plotlyjs=False))
            f.write('</div><div class="plot">')
            f.write(fig_energy.to_html(full_html=False, include_plotlyjs=False))
            f.write('</div><div class="section-title"><h2>Battery Health Analysis</h2></div>')
            f.write('<div class="plot">')
            f.write(fig_health.to_html(full_html=False, include_plotlyjs=False))
            f.write('</div><div class="plot">')
            f.write(fig_capacity.to_html(full_html=False, include_plotlyjs=False))
            f.write('</div><div class="plot">')
            f.write(fig_range.to_html(full_html=False, include_plotlyjs=False))
            f.write('</div><div class="wide-plot">')
            f.write(fig_models.to_html(full_html=False, include_plotlyjs=False))            
            f.write('</div></div><footer>Created by Group 7 - CIS3120</footer></body></html>')
            
