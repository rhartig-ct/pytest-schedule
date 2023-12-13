from enum import Enum


class ScheduleType(Enum):
    RoundRobin = "round robin"
    Snake = "snake"
    ShortestGroup = "shortest group"
    Default = "default"
