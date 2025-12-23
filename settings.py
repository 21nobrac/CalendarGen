from astronomy.enums import SolarMarker, MoonPhase

OUTPUT_FILE = "calendar_output.csv"

# --- Simulation settings  ---
INCLUDE_FIRST_MOON = True
INCLUDE_SECOND_MOON = True
INCLUDE_DOUBLE_SYZYGIES = True
INCLUDE_SOLAR_CALENDAR = True
INCLUDE_LUNISOLAR_CALENDAR = True
INCLUDE_LUNAR_CALENDAR_A = True
INCLUDE_LUNAR_CALENDAR_B = True
INCLUDE_RAW_PHASE_FIGURES = True
INCLUDE_SOLAR_PHASES = True
INCLUDE_LUNAR_PHASES = True

# --- Simulation length ---
SIM_START_LOG_DAY = 100
SIM_DAYS = 100 * 365

# --- Astronomical parameters ---
ASTRONOMICAL_YEAR = 365.2422
MOON_A_MONTH = 29.51         # synodic month (days)
MOON_B_MONTH = 19.7         # synodic month (days)

MOON_NAMES = [
    "Big",
    "Small",
]
SOLAR_MARKER_NAMES = {
    SolarMarker.WinterSolstice : "Winter Soltstice",
    SolarMarker.SpringEquinox : "Spring Equinox",
    SolarMarker.SummerSolstice : "Summer Solstice",
    SolarMarker.FallEquinox : "Fall Equinox"
}

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
STARTING_SOLAR_MARKER = SolarMarker.WinterSolstice # which solar marker the lunisolar calendar cares about
STARTING_MOON_PHASE = MoonPhase.Full
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