from config import SOLAR_MARKERS as SM
from settings import SOLAR_MARKER_NAMES as SMN

from astronomy.core_math import phase_crossed

def solar_marker(prev_phase, curr_phase):
    for k, name in SM.items():
        if phase_crossed(prev_phase, curr_phase, k):
            return name
    return None

def compute_phases(row, sun, include_raw=False):
    sm = solar_marker(sun.prev_phase, sun.phase)
    if include_raw:
        row["Solar_Phase_Raw"] = sun.phase
    row["Solar_Marker"] = SMN[sm] if sm is not None else ""
