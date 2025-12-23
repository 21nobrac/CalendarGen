import csv
from astronomy.celestial_bodies import Moon, Sun
from calendars.lunar_calendar import LunarCalendarState, compute_lunar_calendars
import settings
from settings import MOON_A_MONTH, MOON_B_MONTH, ASTRONOMICAL_YEAR, LUNAR_A_MONTHS_PER_YEAR, LUNAR_B_MONTHS_PER_YEAR, OUTPUT_FILE, LUNAR_A_DAY_START, LUNAR_B_DAY_START, SIM_DAYS
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

def ask_yes_no(prompt: str) -> bool:
    while True:
        response = input(f"{prompt} [y/n]: ").strip().lower()
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")

def check_incompatible_setting():
    # --- Lunisolar calendar requires Moon A ---
    if settings.INCLUDE_LUNISOLAR_CALENDAR and not settings.INCLUDE_FIRST_MOON:
        print("Lunisolar Calendar is enabled, but Moon A is disabled.")
        if ask_yes_no("Enable Moon A?"):
            settings.INCLUDE_FIRST_MOON = True
        else:
            settings.INCLUDE_LUNISOLAR_CALENDAR = False

    # --- Double syzygies require both moons ---
    if settings.INCLUDE_DOUBLE_SYZYGIES and not (settings.INCLUDE_FIRST_MOON and settings.INCLUDE_SECOND_MOON):
        print("Double Syzygies are enabled, but Moon A or Moon B is disabled.")
        if ask_yes_no("Enable both moons?"):
            settings.INCLUDE_FIRST_MOON = True
            settings.INCLUDE_SECOND_MOON = True
        else:
            settings.INCLUDE_DOUBLE_SYZYGIES = False

    # --- Lunar Calendar A requires Moon A ---
    if settings.INCLUDE_LUNAR_CALENDAR_A and not settings.INCLUDE_FIRST_MOON:
        print("Lunar Calendar A is enabled, but Moon A is disabled.")
        if ask_yes_no("Enable Moon A?"):
            settings.INCLUDE_FIRST_MOON = True
        else:
            settings.INCLUDE_LUNAR_CALENDAR_A = False

    # --- Lunar Calendar B requires Moon B ---
    if settings.INCLUDE_LUNAR_CALENDAR_B and not settings.INCLUDE_SECOND_MOON:
        print("Lunar Calendar B is enabled, but Moon B is disabled.")
        if ask_yes_no("Enable Moon B?"):
            settings.INCLUDE_SECOND_MOON = True
        else:
            settings.INCLUDE_LUNAR_CALENDAR_B = False

    # --- Lunar phases require at least one moon ---
    if settings.INCLUDE_LUNAR_PHASES and not (settings.INCLUDE_FIRST_MOON or settings.INCLUDE_SECOND_MOON):
        print("Lunar Phases are enabled, but no moons are enabled.")

        enable_a = ask_yes_no("Enable Moon A?")
        enable_b = ask_yes_no("Enable Moon B?")

        if enable_a:
            settings.INCLUDE_FIRST_MOON = True
        if enable_b:
            settings.INCLUDE_SECOND_MOON = True

        if not (enable_a or enable_b):
            settings.INCLUDE_LUNAR_PHASES = False

def main():
    check_incompatible_setting()
    moon_a = Moon(MOON_A_MONTH) if settings.INCLUDE_FIRST_MOON else None
    moon_b = Moon(MOON_B_MONTH) if settings.INCLUDE_SECOND_MOON else None
    sun = Sun(ASTRONOMICAL_YEAR)
    ls_state = LunisolarState() if settings.INCLUDE_LUNISOLAR_CALENDAR else None
    lc_state_a = LunarCalendarState(LUNAR_A_MONTHS_PER_YEAR, LUNAR_A_DAY_START) if settings.INCLUDE_LUNAR_CALENDAR_A else None
    lc_state_b = LunarCalendarState(LUNAR_B_MONTHS_PER_YEAR, LUNAR_B_DAY_START) if settings.INCLUDE_LUNAR_CALENDAR_B else None

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)

        for day in range(SIM_DAYS):
            # --- tick moons and sun ---
            moon_a.tick_day() if moon_a else None
            moon_b.tick_day() if moon_b else None
            sun.tick_day()

            # --- tick lunar calendars ---
            if lc_state_a and moon_a:
                lc_state_a.tick(moon_a, day)
            if lc_state_b and moon_b:
                lc_state_b.tick(moon_b, day)
                    
            # --- update lunisolar state ---
            if ls_state and moon_a:
                tick_ls_state(ls_state, moon_a, sun)                    

            # --- build row ---
            row = {"Day": str(day)}
            
            if settings.INCLUDE_LUNAR_PHASES:
                compute_lunar_phases(row, moon_a, moon_b, settings.INCLUDE_RAW_PHASE_FIGURES)
            if settings.INCLUDE_SOLAR_PHASES:
                compute_solar_phases(row, sun, settings.INCLUDE_RAW_PHASE_FIGURES)
            if settings.INCLUDE_SOLAR_CALENDAR:
                compute_solar_calendar(row, day)
            if ls_state: 
                compute_lunisolar_calendar(row, ls_state)
            if lc_state_a or lc_state_b:
                compute_lunar_calendars(row, lc_state_a, lc_state_b)

            writer.writerow([row.get(h, "") for h in HEADERS])

    print(f"Calendar written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()