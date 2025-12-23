from astronomy.enums import SolarMarker

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
    0.00: SolarMarker.WinterSolstice,
    0.25: SolarMarker.SpringEquinox,
    0.50: SolarMarker.SummerSolstice,
    0.75: SolarMarker.FallEquinox
}
