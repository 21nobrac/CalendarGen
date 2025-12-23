from astronomy.enums import MoonPhase
from astronomy.core_math import phase_crossed
from astronomy.celestial_bodies import Moon
from localization import MOON_PHASE_NAMES, MOON_NAMES

def moon_syzygy(prev_phase : float, curr_phase : float):
    if phase_crossed(prev_phase, curr_phase, 0.0):
        return "New"
    if phase_crossed(prev_phase, curr_phase, 0.5):
        return "Full"
    return None


def syzygy_overlap(prev_a : float, curr_a : float, prev_b : float, curr_b : float, moon_a_name : str, moon_b_name : str):
    a_event = moon_syzygy(prev_a, curr_a)
    b_event = moon_syzygy(prev_b, curr_b)

    if not a_event or not b_event:
        return ""

    if a_event == b_event:
        return f"Double {a_event}"

    if a_event == "Full":
        return f"{moon_a_name} Full"
    else:
        return f"{moon_b_name} Full"


def quantize_phase(p : float):
    n = len(MoonPhase)
    index = int((p * n) + 0.5) % n
    phase = MoonPhase(index)
    return MOON_PHASE_NAMES[phase]


def compute_phases(row : dict[str, str], moon_a : Moon | None, moon_b : Moon | None, include_raw : bool = False, include_overlap : bool = True):
    ma = None
    prev_ma = None
    mb = None
    prev_mb = None
    if moon_a:
        ma = moon_a.phase
        prev_ma = moon_a.prev_phase
        row["MoonA_Phase_Name"] = quantize_phase(ma)
        if include_raw:
            row["MoonA_Phase_Raw"] = str(round(ma, 6))
    if moon_b:
        mb = moon_b.phase
        prev_mb = moon_b.prev_phase
        row["MoonB_Phase_Name"] = quantize_phase(mb)
        if include_raw:
            row["MoonB_Phase_Raw"] = str(round(mb, 6))
    if ma and prev_ma and mb and prev_mb and include_overlap:
        row["Moon_Phases_Aligned"] = syzygy_overlap(
            prev_ma, ma,
            prev_mb, mb,
            MOON_NAMES[0],
            MOON_NAMES[1]
        )
