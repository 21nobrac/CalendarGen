from config import SOLAR_CIVIL_YEAR as YEAR, SOLAR_MONTH_LENGTHS as MONTH_LENGTHS, SOLAR_MONTH_NAMES as MONTH_NAMES, SOLAR_CALENDAR_OFFSET as OFFSET

def find_month_and_day(year_day):
    consumed_days = 0
    month = 0
    for ml in MONTH_LENGTHS:
        if year_day >= consumed_days and year_day < (consumed_days + ml):
            month_day = year_day - consumed_days
            return month, month_day
        month += 1
        consumed_days += ml

def compute_solar_calendar(row, day):
    day -= OFFSET # account for the offset
    year = day // YEAR
    yd = day - (YEAR * year)
    mi, month_day = find_month_and_day(yd)
    month = mi+1
    month_name = MONTH_NAMES[mi]
    row["Solar_Year"] = year
    row["Solar_Month_#"] = month
    row["Solar_Month"] = month_name
    row["Solar_Day"] = month_day