from constants import SOLAR_MARKERS as SM
from localization import SOLAR_MARKER_NAMES as SMN
from astronomy.core_math import phase_crossed
from astronomy.celestial_bodies import Sun

def solar_marker(prev_phase : float, curr_phase : float):
    for k, name in SM.items():
        if phase_crossed(prev_phase, curr_phase, k):
            return name
    return None

def compute_phases(row : dict[str, str], sun : Sun, include_raw : bool = False):
    sm = solar_marker(sun.prev_phase, sun.phase)
    if include_raw:
        row["Solar_Phase_Raw"] = str(sun.phase)
    row["Solar_Marker"] = SMN[sm] if sm is not None else ""
