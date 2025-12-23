from settings import SOLAR_CIVIL_YEAR as YEAR, SOLAR_MONTH_LENGTHS as MONTH_LENGTHS, SOLAR_MONTH_NAMES as MONTH_NAMES, SOLAR_CALENDAR_OFFSET as OFFSET

def find_month_and_day(year_day: int):
    consumed_days = 0
    month = 0
    for ml in MONTH_LENGTHS:
        if year_day >= consumed_days and year_day < (consumed_days + ml):
            month_day = year_day - consumed_days
            return month, month_day
        month += 1
        consumed_days += ml
    return None, None

def compute_solar_calendar(row: dict[str, str], day: int):
    day -= OFFSET # account for the offset
    year = day // YEAR
    yd = day - (YEAR * year)
    mi, month_day = find_month_and_day(yd)
    month = mi + 1 if mi is not None else None
    month_name = MONTH_NAMES[mi] if mi and mi < len(MONTH_NAMES) else None
    row["Solar_Year"] = str(year)
    row["Solar_Month_#"] = str(month)
    row["Solar_Month"] = str(month_name)
    row["Solar_Day"] = str(month_day)