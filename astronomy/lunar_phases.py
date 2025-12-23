from config import *
from astronomy.core_math import phase_crossed


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


def compute_phases(row, moons, include_raw=False):
    ma = moons[0].phase
    mb = moons[1].phase
    prev_ma = moons[0].prev_phase
    prev_mb = moons[1].prev_phase

    row["MoonA_Phase_Name"] = quantize_phase(ma)
    row["MoonB_Phase_Name"] = quantize_phase(mb)

    if include_raw:
        row["MoonA_Phase_Raw"] = round(ma, 6)
        row["MoonB_Phase_Raw"] = round(mb, 6)

    row["Moon_Phases_Aligned"] = syzygy_overlap(
        prev_ma, ma,
        prev_mb, mb,
        MOON_NAMES[0],
        MOON_NAMES[1]
    )
