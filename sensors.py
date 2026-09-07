"""
Telemetry simulation module modeling realistic hardware environmental and ultrasonic sensors.
"""
import random
import time
try:
    import psutil
except ImportError:
    psutil = None

_temp = 24.5
_humidity = 52.0
_distance = 85.0


def generate_telemetry() -> dict:
    """Generates drifting realistic telemetry readings."""
    global _temp, _humidity, _distance

    # Random walk simulation
    _temp += random.uniform(-0.3, 0.3)
    _temp = max(18.0, min(38.0, _temp))

    _humidity += random.uniform(-0.8, 0.8)
    _humidity = max(35.0, min(80.0, _humidity))

    _distance += random.uniform(-4.0, 4.0)
    _distance = max(15.0, min(250.0, _distance))

    if psutil:
        cpu = psutil.cpu_percent(interval=None)
    else:
        cpu = round(random.uniform(15.0, 65.0), 1)

    return {
        "temperature": round(_temp, 2),
        "humidity": round(_humidity, 1),
        "distance_cm": round(_distance, 1),
        "cpu_load": round(cpu, 1),
        "timestamp": time.strftime("%H:%M:%S")
    }
