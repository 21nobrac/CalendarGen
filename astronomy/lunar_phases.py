from config import PHASE_NAMES
from astronomy.core_math import phase_crossed
from settings import MOON_NAMES


def moon_syzygy(prev_phase, curr_phase):
    if phase_crossed(prev_phase, curr_phase, 0.0):
        return "New"
    if phase_crossed(prev_phase, curr_phase, 0.5):
        return "Full"
    return None


def syzygy_overlap(prev_a, curr_a, prev_b, curr_b, moon_a_name, moon_b_name):
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


def quantize_phase(p):
    n = len(PHASE_NAMES)
    index = int((p * n) + 0.5) % n
    return PHASE_NAMES[index]


def compute_phases(row, moon_a, moon_b, include_raw=False, include_overlap=True):
    if moon_a:
        ma = moon_a.phase
        prev_ma = moon_a.prev_phase
        row["MoonA_Phase_Name"] = quantize_phase(ma)
        if include_raw:
            row["MoonA_Phase_Raw"] = round(ma, 6)
    if moon_b:
        mb = moon_b.phase
        prev_mb = moon_b.prev_phase
        row["MoonB_Phase_Name"] = quantize_phase(mb)
        if include_raw:
            row["MoonB_Phase_Raw"] = round(mb, 6)
    if moon_a and moon_b and include_overlap:
        row["Moon_Phases_Aligned"] = syzygy_overlap(
            prev_ma, ma, # type: ignore
            prev_mb, mb, # type: ignore
            MOON_NAMES[0],
            MOON_NAMES[1]
        )
