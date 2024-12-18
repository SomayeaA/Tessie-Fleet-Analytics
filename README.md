# Tesla Fleet Analytics Dashboard

## Overview
A Python-based analytics dashboard that leverages the Tessie API to track and analyze data from Tesla vehicles. The application provides real-time monitoring of vehicle metrics, battery health analysis, and interactive visualizations for fleet management.

## Features
- Real-time vehicle status monitoring
- Battery health and degradation tracking
- Location tracking with interactive maps
- Energy consumption analysis
- Model specifications comparison
- Interactive visualizations using Plotly
- Energy Efficiency and Cost Analysis

## Project Structure
```
tesla_fleet/
├── base.py          # Core data structures and types
├── vehicle.py       # Vehicle class implementation
├── fleet.py         # Fleet analytics implementation
├── tessie_api.py    # API communication handler
├── visualizer.py    # Data visualization module
├── analysis.py      # Energy Efficiency and Cost analyzer
├── key.py           # API credentials (not included in repo)
└── main.py          # Main application script
```

## Requirements
- Python 3.8+
- Tessie API access and API key
- Required Python packages:
  ```
  requests
  pandas
  plotly
  ```

## Installation
1. Clone the repository
```bash
git clone https://github.com/ri5e/Tessie-Fleet-Analytics.git
cd Tessie-Fleet-Analytics
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Create a `key.py` file with your Tessie API credentials
```python
API_KEY = "your_api_key_here"
```

## Usage
1. Update your API credentials in `key.py`
2. Run the main script:
```bash
python main.py
```

## Dashboard Features
### Current Status Section
- Battery levels across fleet
- Real-time vehicle locations
- Vehicle activity status

### Battery Analysis
- Battery health percentages
- Degradation tracking
- Range estimates
- Energy consumption patterns

### Model Comparison
- Vehicle specifications
- Performance metrics
- Configuration details
- Efficiency metrics

## Data Points Tracked
- Battery level and range
- Charging status
- Location data
- Vehicle state information
- Model specifications
- Energy consumption metrics

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Security Note
- Never commit your `key.py` file containing API credentials
- Add `key.py` to your `.gitignore` file
- Use proper API key management in production environments

## Acknowledgments
- Built using the [Tessie API](https://tessie.com/)
- Visualization powered by [Plotly](https://plotly.com/)
