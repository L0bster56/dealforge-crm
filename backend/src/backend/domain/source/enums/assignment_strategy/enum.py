from enum import StrEnum

class AssignmentStrategyType(StrEnum):
    manual = "manual"
    round_robin = "round_robin"
    least_loaded = "least_loaded"