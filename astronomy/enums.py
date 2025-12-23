from enum import Enum

class MoonPhase(Enum):
    Full = 0
    New = 1

class SolarMarker(Enum):
    WinterSoltstice = 0
    SpringEquinox = 1
    SummerSolstice = 2
    FallEquinox = 3