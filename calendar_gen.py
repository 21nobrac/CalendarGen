import csv
import click
from astronomy.celestial_bodies import Moon, Sun
from calendars.lunar_calendar import LunarCalendarState, compute_lunar_calendars
import config
from astronomy.lunar_phases import compute_phases as compute_lunar_phases
from astronomy.solar_phases import compute_phases as compute_solar_phases
from calendars.solar_calendar import compute_solar_calendar
from calendars.lunisolar_calendar import compute_lunisolar_state_tick as tick_ls_state, LunisolarState, compute_lunisolar_calendar
from user_defined_events import compute_user_defined_events as compute_events
from calendars.date import Date

def ask_yes_no(prompt: str) -> bool:
    while True:
        response = input(f"{prompt} [y/n]: ").strip().lower()
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")

def check_incompatible_setting(interactive: bool = True):
    """
    Check for incompatible settings and fix them.
    If interactive=True, ask the user. If False, use sensible defaults.
    """
    # --- Lunisolar calendar requires Moon A ---
    if config.INCLUDE_LUNISOLAR_CALENDAR and not config.INCLUDE_FIRST_MOON:
        if interactive and ask_yes_no("Lunisolar Calendar requires Moon A. Enable it?"):
            config.INCLUDE_FIRST_MOON = True
        else:
            click.echo("Lunisolar Calendar requires Moon A, but it's disabled. Disabling Lunisolar Calendar.")
            config.INCLUDE_LUNISOLAR_CALENDAR = False

    # --- Double syzygies require both moons ---
    if config.INCLUDE_DOUBLE_SYZYGIES and not (config.INCLUDE_FIRST_MOON and config.INCLUDE_SECOND_MOON):
        if interactive and ask_yes_no("Double Syzygies require both moons. Enable them?"):
            config.INCLUDE_FIRST_MOON = True
            config.INCLUDE_SECOND_MOON = True
        else:
            click.echo("Double Syzygies require both moons. Disabling Double Syzygies.")
            config.INCLUDE_DOUBLE_SYZYGIES = False

    # --- Lunar Calendar A requires Moon A ---
    if config.INCLUDE_LUNAR_CALENDAR_A and not config.INCLUDE_FIRST_MOON:
        if interactive and ask_yes_no("Lunar Calendar A requires Moon A. Enable it?"):
            config.INCLUDE_FIRST_MOON = True
        else:
            click.echo("Lunar Calendar A requires Moon A, but it's disabled. Disabling Lunar Calendar A.")
            config.INCLUDE_LUNAR_CALENDAR_A = False

    # --- Lunar Calendar B requires Moon B ---
    if config.INCLUDE_LUNAR_CALENDAR_B and not config.INCLUDE_SECOND_MOON:
        if interactive and ask_yes_no("Lunar Calendar B requires Moon B. Enable it?"):
            config.INCLUDE_SECOND_MOON = True
        else:
            click.echo("Lunar Calendar B requires Moon B, but it's disabled. Disabling Lunar Calendar B.")
            config.INCLUDE_LUNAR_CALENDAR_B = False

    # --- Lunar phases require at least one moon ---
    if config.INCLUDE_LUNAR_PHASES and not (config.INCLUDE_FIRST_MOON or config.INCLUDE_SECOND_MOON):
        click.echo("Lunar Phases require at least one moon, but none are enabled. Disabling Lunar Phases.")
        config.INCLUDE_LUNAR_PHASES = False

HEADERS = [
    "Day",
    "User_Defined_Events",
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

def generate_calendar(
    output_file: str,
    sim_days: int,
    moon_a_month: float,
    moon_b_month: float,
    astronomical_year: float,
    lunar_a_months_per_year: int,
    lunar_b_months_per_year: int,
    lunar_a_day_start: int,
    lunar_b_day_start: int,
    solar_calendar_offset: int,
    include_first_moon: bool,
    include_second_moon: bool,
    include_double_syzygies: bool,
    include_solar_calendar: bool,
    include_lunisolar_calendar: bool,
    include_lunar_calendar_a: bool,
    include_lunar_calendar_b: bool,
    include_raw_phase_figures: bool,
    include_solar_phases: bool,
    include_lunar_phases: bool,
    include_user_defined_events: bool,
    interactive: bool = False
):
    """
    Generate calendar with the given settings.
    """
    # --- Apply settings to config module ---
    config.INCLUDE_FIRST_MOON = include_first_moon
    config.INCLUDE_SECOND_MOON = include_second_moon
    config.INCLUDE_DOUBLE_SYZYGIES = include_double_syzygies
    config.INCLUDE_SOLAR_CALENDAR = include_solar_calendar
    config.INCLUDE_LUNISOLAR_CALENDAR = include_lunisolar_calendar
    config.INCLUDE_LUNAR_CALENDAR_A = include_lunar_calendar_a
    config.INCLUDE_LUNAR_CALENDAR_B = include_lunar_calendar_b
    config.INCLUDE_RAW_PHASE_FIGURES = include_raw_phase_figures
    config.INCLUDE_SOLAR_PHASES = include_solar_phases
    config.INCLUDE_LUNAR_PHASES = include_lunar_phases
    config.INCLUDE_USER_DEFINED_EVENTS = include_user_defined_events

    # --- Check for incompatible settings ---
    check_incompatible_setting(interactive=interactive)

    # --- Initialize celestial bodies and states ---
    moon_a = Moon(moon_a_month) if config.INCLUDE_FIRST_MOON else None
    moon_b = Moon(moon_b_month) if config.INCLUDE_SECOND_MOON else None
    sun = Sun(astronomical_year)
    ls_state = LunisolarState() if config.INCLUDE_LUNISOLAR_CALENDAR else None
    lc_state_a = LunarCalendarState(lunar_a_months_per_year, lunar_a_day_start) if config.INCLUDE_LUNAR_CALENDAR_A else None
    lc_state_b = LunarCalendarState(lunar_b_months_per_year, lunar_b_day_start) if config.INCLUDE_LUNAR_CALENDAR_B else None

    # --- Write to CSV ---
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)

        for day in range(sim_days):
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

            dates : list[Date] = []

            # --- build row ---
            row = {"Day": str(day)}
            if config.INCLUDE_LUNAR_PHASES:
                compute_lunar_phases(row, moon_a, moon_b, config.INCLUDE_RAW_PHASE_FIGURES)
            if config.INCLUDE_SOLAR_PHASES:
                compute_solar_phases(row, sun, config.INCLUDE_RAW_PHASE_FIGURES)
            if config.INCLUDE_SOLAR_CALENDAR:
                solar_date = compute_solar_calendar(row, day)
                dates.append(solar_date) if solar_date else None
            if ls_state: 
                Lunisolar_date = compute_lunisolar_calendar(row, ls_state)
                dates.append(Lunisolar_date) if Lunisolar_date else None
            if lc_state_a or lc_state_b:
                lunar_date_a, lunar_date_b = compute_lunar_calendars(row, lc_state_a, lc_state_b)
                dates.append(lunar_date_a) if lunar_date_a else None
                dates.append(lunar_date_b) if lunar_date_b else None
            if config.INCLUDE_USER_DEFINED_EVENTS:
                compute_events(row, dates)

            writer.writerow([row.get(h, "") for h in HEADERS])

    click.echo(f"✓ Calendar written to {output_file}")