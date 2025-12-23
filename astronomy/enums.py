from enum import Enum

class SyzygyType(Enum):
    Full = 0
    New = 1

class MoonPhase(Enum):
    New = 0
    WaxingCrescent = 1
    FirstQuarter = 2
    WaxingGibbous = 3
    Full = 4
    WaningGibbous = 5
    LastQuarter = 6
    WaningCrescent = 7

class SolarMarker(Enum):
    WinterSolstice = 0
    SpringEquinox = 1
    SummerSolstice = 2
    FallEquinox = 3
