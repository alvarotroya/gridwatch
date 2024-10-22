from enum import Enum


class ComponentType(str, Enum):
    TRANSFORMER = "transformer"
    CONNECTION = "connection"


class DeviceType(str, Enum):
    EDGE = "edge"
    SENSOR_1 = "sensor_1"


class HealthStatus(str, Enum):
    OK = "ok"
    DETERIORATED = "deteriorated"
    UNREACHABLE = "unreachable"
