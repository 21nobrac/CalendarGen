from calendars.date import AnnualDate, Date
from calendars.enums import Calendar

USER_DEFINED_EVENTS : dict[str, AnnualDate] = {
    "Traditional Lunar New Year": AnnualDate(Calendar.LunarA, 1, 2),
    "Salvation Day": AnnualDate(Calendar.LunarB, 1, 1),
    "Harvest Festival": AnnualDate(Calendar.Solar, 9, 28),
    "Lunisolar New Year": AnnualDate(Calendar.Lunisolar, 1, 1),
    "New Year's Day": AnnualDate(Calendar.Solar, 1, 1),
}

def compute_user_defined_events(row : dict[str, str], dates : list[Date]):
    row["User_Defined_Events"] = ""
    for event, date in USER_DEFINED_EVENTS.items():
        for comp_date in dates:
            if date.matches(comp_date):
                row["User_Defined_Events"] += f", {event}" if row["User_Defined_Events"] else event