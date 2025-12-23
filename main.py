import csv
from astronomy.celestial_bodies import Moon, Sun
from calendars.lunar_calendar import LunarCalendarState, compute_lunar_calendars
from config import *
from astronomy.core_math import phase
from astronomy.lunar_phases import compute_phases as compute_lunar_phases
from astronomy.solar_phases import compute_phases as compute_solar_phases
from calendars.solar_calendar import compute_solar_calendar
from calendars.lunisolar_calendar import compute_lunisolar_state_tick as tick_ls_state, LunisolarState, compute_lunisolar_calendar

HEADERS = [
    "Day",
    "MoonA_Phase_Raw",
    "MoonA_Phase_Name",
    "MoonB_Phase_Raw",
    "MoonB_Phase_Name",
    "Moon_Phases_Aligned",
    "Eclipse_Event",
    "Solar_Phase_Raw",
    "Solar_Marker",
    "Solar_Year",
    "Solar_Month_#",
    "Solar_Month",
    "Solar_Day",
    "Lunisolar_Year",
    "Lunisolar_Month_#",
    "Lunisolar_Month",
    "Lunisolar_Day",
    "LunarA_Year",
    "LunarA_Month_#",
    "LunarA_Month",
    "LunarA_Day",
    "LunarB_Year",
    "LunarB_Month_#",
    "LunarB_Month",
    "LunarB_Day"
]

INCLUDE_RAW = True


def main():
    moon_A = Moon(MOON_A_MONTH)
    moon_B = Moon(MOON_B_MONTH)
    sun = Sun(ASTRONOMICAL_YEAR)
    moons = [ moon_A, moon_B ]
    ls_state = LunisolarState()
    lc_state_a = LunarCalendarState(LUNAR_A_MONTHS_PER_YEAR, LUNAR_A_DAY_START)
    lc_state_b = LunarCalendarState(LUNAR_B_MONTHS_PER_YEAR, LUNAR_B_DAY_START)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)

        for day in range(SIM_DAYS):
            # --- tick moons and sun ---
            moon_A.tick_day()
            moon_B.tick_day()
            sun.tick_day()

            # --- tick lunar calendars ---
            lc_state_a.tick(moon_A, day)
            lc_state_b.tick(moon_B, day)

            # --- update lunisolar state ---
            tick_ls_state(ls_state, moon_A, sun)

            # --- build row ---
            row = {"Day": day}

            compute_lunar_phases(row, moons, INCLUDE_RAW)
            compute_solar_phases(row, sun, INCLUDE_RAW)
            compute_solar_calendar(row, day)
            compute_lunisolar_calendar(row, ls_state)
            compute_lunar_calendars(row, lc_state_a, lc_state_b)

            writer.writerow([row.get(h, "") for h in HEADERS])

    print(f"Calendar written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()