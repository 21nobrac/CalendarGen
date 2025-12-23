import csv
import click
import json
from astronomy.celestial_bodies import Moon, Sun
from calendars.lunar_calendar import LunarCalendarState, compute_lunar_calendars
import config
from settings import MOON_A_MONTH, MOON_B_MONTH, ASTRONOMICAL_YEAR, LUNAR_A_MONTHS_PER_YEAR, LUNAR_B_MONTHS_PER_YEAR, OUTPUT_FILE, LUNAR_A_DAY_START, LUNAR_B_DAY_START, SIM_DAYS
from astronomy.lunar_phases import compute_phases as compute_lunar_phases
from astronomy.solar_phases import compute_phases as compute_solar_phases
from calendars.solar_calendar import compute_solar_calendar
from calendars.lunisolar_calendar import compute_lunisolar_state_tick as tick_ls_state, LunisolarState, compute_lunisolar_calendar
from user_defined_events import compute_user_defined_events as compute_events
from calendars.date import Date

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


def main():
    pass


@click.group()
def cli():
    """CalendarGen: Generate customizable fantasy calendar systems."""
    pass

def load_profile(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


DEFAULTS = {
    "output_file": OUTPUT_FILE,
    "sim_days": SIM_DAYS,
    "moon_a_month": MOON_A_MONTH,
    "moon_b_month": MOON_B_MONTH,
    "astronomical_year": ASTRONOMICAL_YEAR,
    "lunar_a_months_per_year": LUNAR_A_MONTHS_PER_YEAR,
    "lunar_b_months_per_year": LUNAR_B_MONTHS_PER_YEAR,
    "lunar_a_day_start": LUNAR_A_DAY_START,
    "lunar_b_day_start": LUNAR_B_DAY_START,
    "solar_calendar_offset": 22,
    "include_first_moon": True,
    "include_second_moon": True,
    "include_double_syzygies": True,
    "include_solar_calendar": True,
    "include_lunisolar_calendar": True,
    "include_lunar_calendar_a": True,
    "include_lunar_calendar_b": True,
    "include_raw_phase_figures": True,
    "include_solar_phases": True,
    "include_lunar_phases": True,
    "include_user_defined_events": True,
    "interactive": False,
}

CLI_TO_CONFIG = {
    "output": "output_file",
    "days": "sim_days",
    "moon_a_month": "moon_a_month",
    "moon_b_month": "moon_b_month",
    "year_length": "astronomical_year",
    "lunar_a_months": "lunar_a_months_per_year",
    "lunar_b_months": "lunar_b_months_per_year",
    "lunar_a_start": "lunar_a_day_start",
    "lunar_b_start": "lunar_b_day_start",
    "solar_offset": "solar_calendar_offset",
    "moon_a": "include_first_moon",
    "moon_b": "include_second_moon",
    "double_syzygies": "include_double_syzygies",
    "solar": "include_solar_calendar",
    "lunisolar": "include_lunisolar_calendar",
    "lunar_a": "include_lunar_calendar_a",
    "lunar_b": "include_lunar_calendar_b",
    "raw_phases": "include_raw_phase_figures",
    "solar_phases": "include_solar_phases",
    "lunar_phases": "include_lunar_phases",
    "user_events": "include_user_defined_events",
    "interactive": "interactive",
}

@cli.command()
@click.option('--profile', '-p', type=click.Path(exists=True), help='Profile JSON file')
@click.option('--output', '-o', default=None)
@click.option('--days', '-d', default=None, type=int)
@click.option('--moon-a-month', default=None, type=float)
@click.option('--moon-b-month', default=None, type=float)
@click.option('--year-length', default=None, type=float)
@click.option('--lunar-a-months', default=None, type=int)
@click.option('--lunar-b-months', default=None, type=int)
@click.option('--lunar-a-start', default=None, type=int)
@click.option('--lunar-b-start', default=None, type=int)
@click.option('--solar-offset', default=None, type=int)

@click.option('--moon-a/--no-moon-a', default=None)
@click.option('--moon-b/--no-moon-b', default=None)
@click.option('--double-syzygies/--no-double-syzygies', default=None)
@click.option('--solar/--no-solar', default=None)
@click.option('--lunisolar/--no-lunisolar', default=None)
@click.option('--lunar-a/--no-lunar-a', default=None)
@click.option('--lunar-b/--no-lunar-b', default=None)
@click.option('--raw-phases/--no-raw-phases', default=None)
@click.option('--solar-phases/--no-solar-phases', default=None)
@click.option('--lunar-phases/--no-lunar-phases', default=None)
@click.option('--user-events/--no-user-events', default=None)
@click.option('--interactive/--non-interactive', default=None)
def generate(**cli_args):
    """Generate a calendar with the specified settings."""
    profile_path = cli_args.pop('profile')

    # 1. Start with hard defaults
    config = DEFAULTS.copy()

    # 2. Overlay profile
    if profile_path:
        click.echo(f"Loading profile: {profile_path}")
        profile_data = load_profile(profile_path)
        config.update(profile_data)

    # 3. Overlay CLI overrides
    for cli_key, value in cli_args.items():
        if value is not None:
            config_key = CLI_TO_CONFIG[cli_key]
            config[config_key] = value

    try:
        generate_calendar(**config)
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        raise


@cli.command()
def defaults():
    """Show default settings from settings.py"""
    click.echo("\n=== Default Settings ===\n")
    click.echo(f"Output file:              {OUTPUT_FILE}")
    click.echo(f"Simulation days:          {SIM_DAYS}")
    click.echo(f"\nMoon A synodic month:     {MOON_A_MONTH}")
    click.echo(f"Moon B synodic month:     {MOON_B_MONTH}")
    click.echo(f"Astronomical year:        {ASTRONOMICAL_YEAR}")
    click.echo(f"\nLunar A months/year:      {LUNAR_A_MONTHS_PER_YEAR}")
    click.echo(f"Lunar B months/year:      {LUNAR_B_MONTHS_PER_YEAR}")
    click.echo(f"Lunar A start day:        {LUNAR_A_DAY_START}")
    click.echo(f"Lunar B start day:        {LUNAR_B_DAY_START}")
    click.echo()

@cli.command()
@click.option('--profile', '-p', default='profile.json', help='Profile JSON file path')
@click.option('--output', '-o', default=OUTPUT_FILE, help='Output CSV file path')
@click.option('--days', '-d', default=SIM_DAYS, type=int, help='Number of days to simulate')
@click.option('--moon-a-month', default=MOON_A_MONTH, type=float, help='Moon A synodic month length (days)')
@click.option('--moon-b-month', default=MOON_B_MONTH, type=float, help='Moon B synodic month length (days)')
@click.option('--year-length', default=ASTRONOMICAL_YEAR, type=float, help='Astronomical year length (days)')
@click.option('--lunar-a-months', default=LUNAR_A_MONTHS_PER_YEAR, type=int)
@click.option('--lunar-b-months', default=LUNAR_B_MONTHS_PER_YEAR, type=int)
@click.option('--lunar-a-start', default=LUNAR_A_DAY_START, type=int)
@click.option('--lunar-b-start', default=LUNAR_B_DAY_START, type=int)
@click.option('--solar-offset', default=22, type=int)
@click.option('--moon-a/--no-moon-a', default=True)
@click.option('--moon-b/--no-moon-b', default=True)
@click.option('--double-syzygies/--no-double-syzygies', default=True)
@click.option('--solar/--no-solar', default=True)
@click.option('--lunisolar/--no-lunisolar', default=True)
@click.option('--lunar-a/--no-lunar-a', default=True)
@click.option('--lunar-b/--no-lunar-b', default=True)
@click.option('--raw-phases/--no-raw-phases', default=True)
@click.option('--solar-phases/--no-solar-phases', default=True)
@click.option('--lunar-phases/--no-lunar-phases', default=True)
@click.option('--user-events/--no-user-events', default=True)
@click.option('--interactive/--non-interactive', default=False)
def create_profile(
    profile,
    output,
    days,
    moon_a_month,
    moon_b_month,
    year_length,
    lunar_a_months,
    lunar_b_months,
    lunar_a_start,
    lunar_b_start,
    solar_offset,
    moon_a,
    moon_b,
    double_syzygies,
    solar,
    lunisolar,
    lunar_a,
    lunar_b,
    raw_phases,
    solar_phases,
    lunar_phases,
    user_events,
    interactive,
):
    """Create a new profile with custom settings."""

    click.echo(f"Creating profile: {profile}")

    profile_data = {
        "output_file": output,
        "sim_days": days,
        "moon_a_month": moon_a_month,
        "moon_b_month": moon_b_month,
        "astronomical_year": year_length,
        "lunar_a_months_per_year": lunar_a_months,
        "lunar_b_months_per_year": lunar_b_months,
        "lunar_a_day_start": lunar_a_start,
        "lunar_b_day_start": lunar_b_start,
        "solar_calendar_offset": solar_offset,

        "include_first_moon": moon_a,
        "include_second_moon": moon_b,
        "include_double_syzygies": double_syzygies,
        "include_solar_calendar": solar,
        "include_lunisolar_calendar": lunisolar,
        "include_lunar_calendar_a": lunar_a,
        "include_lunar_calendar_b": lunar_b,
        "include_raw_phase_figures": raw_phases,
        "include_solar_phases": solar_phases,
        "include_lunar_phases": lunar_phases,
        "include_user_defined_events": user_events,

        "interactive": interactive,
    }

    with open(profile, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=4)

    click.echo("Profile created successfully ✔")


if __name__ == "__main__":
    cli()