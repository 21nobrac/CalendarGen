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
from calendar_gen import generate_calendar

def main():
    pass


@click.group()
def cli():
    """CalendarGen: Generate customizable fantasy calendar systems."""
    pass

def load_profile(path):
    """Load and validate a profile JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            profile = json.load(f)
    except FileNotFoundError:
        click.echo(f"✗ Profile file not found: {path}", err=True)
        raise
    except json.JSONDecodeError as e:
        click.echo(f"✗ Invalid JSON in profile: {e}", err=True)
        raise
    
    # Validate that only expected keys are present
    invalid_keys = set(profile.keys()) - set(DEFAULTS.keys())
    if invalid_keys:
        click.echo(f"⚠ Warning: Unknown settings in profile: {invalid_keys}", err=True)
    
    return profile


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