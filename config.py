from astronomy.enums import *

# --- Simulation length ---
SIM_START_LOG_DAY = 100
SIM_DAYS = 100 * 365

# --- Astronomical parameters ---
ASTRONOMICAL_YEAR = 365.2422
MOON_A_MONTH = 29.51         # synodic month (days)
MOON_B_MONTH = 19.7         # synodic month (days)

# --- Lunar calendar ---
LUNAR_A_DAY_START = 0 # the lunar A calendar will start on the next full moon after this day
LUNAR_A_MONTHS_PER_YEAR = 12
LUNAR_B_DAY_START = 300 # the lunar B calendar will start on the next full moon after this day
LUNAR_B_MONTHS_PER_YEAR = 18
LUNAR_A_MONTHS_NAMES = [
    "Snowen",
    "Erestri",
    "Mules",
    "Floria",
    "Ceren",
    "Honoria",
    "Shenca",
    "Forel",
    "Teir",
    "Vedi",
    "Postea",
    "Heca"
]
LUNAR_B_MONTHS_NAMES = [
    "Mesuta",
    "Doluzi",
    "Dutomo",
    "Mikos",
    "Bemas",
    "Milon",
    "Rebim",
    "Hubiz",
    "Ilmab",
    "Nuken",
    "Ara",
    "Ozi",
    "Aso",
    "Ivo",
    "Abos",
    "Esot",
    "Hasiz",
    "Melus"
]

# --- Solar calendar ---
SOLAR_CALENDAR_OFFSET = 22 # how many days the solar calendar started before or after the start of the simulation
SOLAR_CIVIL_YEAR = 365
SOLAR_MONTH_LENGTHS = [30] * 12 + [5] # adding a 5-day festival month at the end of the year
SOLAR_MONTH_NAMES = [
    "Snowen",
    "Erestri",
    "Mules",
    "Floria",
    "Ceren",
    "Honoria",
    "Shenca",
    "Forel",
    "Teir",
    "Vedi",
    "Postea",
    "Heca",
    "Festivius"
]

# --- Lunisolar calendar ---
LUNISOLAR_MONTH_NAMES = [
    "Snowen",
    "Erestri",
    "Mules",
    "Floria",
    "Ceren",
    "Honoria",
    "Shenca",
    "Forel",
    "Teir",
    "Vedi",
    "Postea",
    "Heca",
    "Lunarias",
    "LunariasB"
]
STARTING_SOLAR_MARKER = SolarMarker.WinterSoltstice
STARTING_MOON_PHASE = MoonPhase.Full

# --- Phase naming ---
PHASE_NAMES = [
    "New",
    "Waxing Crescent",
    "First Quarter",
    "Waxing Gibbous",
    "Full",
    "Waning Gibbous",
    "Last Quarter",
    "Waning Crescent"
]

# --- Solar markers (fraction of year) ---
SOLAR_MARKERS = {
    0.00: SolarMarker.WinterSoltstice,
    0.25: SolarMarker.SpringEquinox,
    0.50: SolarMarker.SummerSolstice,
    0.75: SolarMarker.FallEquinox
}
SOLAR_MARKER_NAMES = {
    SolarMarker.WinterSoltstice : "WinterSoltstice",
    SolarMarker.SpringEquinox : "SpringEquinox",
    SolarMarker.SummerSolstice : "SummerSolstice",
    SolarMarker.FallEquinox : "FallEquinox"
}

# --- Astronomical events ---
MOON_NAMES = [
    "Big",
    "Small",
]

# --- Eclipse mechanics ---
MOON_A_NODE_PERIOD = 6798.1
MOON_B_NODE_PERIOD = 842.3

TOTAL_ECLIPSE_LIMIT = 0.01
PARTIAL_ECLIPSE_LIMIT = 0.025
WEAK_PARTIAL_ECLIPSE_LIMIT = 0.045

OUTPUT_FILE = "calendar_output.csv"