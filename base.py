from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class ChargingState(Enum):
    CHARGING = "Charging"
    DISCONNECTED = "Disconnected"
    STOPPED = "Stopped"
    COMPLETE = "Complete"

@dataclass
class BatteryHealth:
    """Battery health metrics"""
    max_range: float
    max_ideal_range: float
    capacity: float
    original_capacity: float
    degradation_percent: float
    health_percent: float


@dataclass
class VehicleMetrics:
    """Vehicle metrics dataclass."""
    # Basic info
    timestamp: datetime
    is_active: bool
    display_name: str
    vin: str

    # Battery and charging
    battery_level: int
    battery_range: float
    charging_state: ChargingState
    lifetime_energy_used: Optional[float]

    # Battery health
    battery_health: Optional[BatteryHealth]

    # Location and power
    latitude: float
    longitude: float
    speed: Optional[float]
    power: float
    odometer: float

    # Climate
    inside_temp: float
    outside_temp: float
    is_climate_on: bool

    # Model info
    model_type: str
    performance_package: str
    trim_badging: str
    efficiency_package: str