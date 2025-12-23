from config import SOLAR_MARKERS
from settings import STARTING_MOON_PHASE, STARTING_SOLAR_MARKER, LUNISOLAR_MONTH_NAMES
from astronomy.core_math import phase_crossed
from astronomy.enums import *

class LunisolarState:
    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.awaiting_new_year = False

def compute_lunisolar_state_tick(ls_state, moon, sun):
    ls_state.day += 1 # tick a day

    inverted_dict = {value: key for key, value in SOLAR_MARKERS.items()}
    looking_for = inverted_dict[STARTING_SOLAR_MARKER]

    if phase_crossed(sun.prev_phase, sun.phase, looking_for):
        ls_state.awaiting_new_year = True
    
    mp = None
    if phase_crossed(moon.prev_phase, moon.phase, 0.5):
        mp = MoonPhase.Full
    elif phase_crossed(moon.prev_phase, moon.phase, 0):
        mp = MoonPhase.New
    if mp == STARTING_MOON_PHASE: # if at the start of a month, tick months and reset days
        ls_state.month += 1
        ls_state.day = 0
        if ls_state.awaiting_new_year:
            ls_state.month = 0
            ls_state.year += 1
            ls_state.awaiting_new_year = False

def compute_lunisolar_calendar(row, ls_state):
    month = ls_state.month
    month_name = LUNISOLAR_MONTH_NAMES[month]
    
    row["Lunisolar_Year"] = ls_state.year + 1
    row["Lunisolar_Month_#"] = month + 1
    row["Lunisolar_Month"] = month_name
    row["Lunisolar_Day"] = ls_state.day + 1