from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ChargingState(Enum):
    CHARGING = "Charging"
    DISCONNECTED = "Disconnected"
    STOPPED = "Stopped"
    COMPLETE = "Complete"

@dataclass
class VehicleMetrics:
    timestamp: datetime
    battery_level: int
    charging_state: ChargingState
    battery_range: float
    latitude: float
    longitude: float
    odometer: float
    inside_temp: float
    outside_temp: float