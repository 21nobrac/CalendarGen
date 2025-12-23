from localization import LUNAR_A_MONTHS_NAMES, LUNAR_B_MONTHS_NAMES
from astronomy.core_math import phase_crossed
from astronomy.celestial_bodies import Moon

class LunarCalendarState:
    def __init__(self, month_num : int = 12, start_day : int = 0):
        self.month_num = month_num
        self.start_day= start_day
        self.year = 0
        self.month = 0
        self.day = 0
        self.started = False
    def tick(self, moon : Moon, day : int):
        full = phase_crossed(moon.prev_phase, moon.phase, 0.5)
        if self.started is False and day >= self.start_day and full:
            self.started = True
        if self.started is False: return

        self.day += 1
        if full:
            self.month += 1
            self.day = 0
        if self.month > self.month_num-1:
            self.month = 0
            self.year += 1

def compute_lunar_calendars(row : dict[str, str], lc_state_a : LunarCalendarState | None, lc_state_b : LunarCalendarState | None):
    if lc_state_a and lc_state_a.started:
        month = lc_state_a.month
        month_name = LUNAR_A_MONTHS_NAMES[month]
        
        row["LunarA_Year"] = str(lc_state_a.year + 1)
        row["LunarA_Month_#"] = str(month + 1)
        row["LunarA_Month"] = month_name
        row["LunarA_Day"] = str(lc_state_a.day + 1)
    
    if lc_state_b and lc_state_b.started:
        month = lc_state_b.month
        month_name = LUNAR_B_MONTHS_NAMES[month]
        
        row["LunarB_Year"] = str(lc_state_b.year + 1)
        row["LunarB_Month_#"] = str(month + 1)
        row["LunarB_Month"] = month_name
        row["LunarB_Day"] = str(lc_state_b.day + 1)