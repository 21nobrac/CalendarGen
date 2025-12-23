from calendars.enums import Calendar

class Date():
    def __init__(self, calendar : Calendar, year : int, month : int, day : int):
        self.calendar = calendar
        self.year = year
        self.month = month
        self.day = day

    def get_date(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"
    
class CalendarAgnosticDate():
    def __init__(self, year : int, month : int, day : int):
        self.year = year
        self.month = month
        self.day = day

    def from_date(self, date : Date):
        self.year = date.year
        self.month = date.month
        self.day = date.day

class AnnualDate():
    def __init__(self, calendar : Calendar, month : int, day : int):
        self.calendar = calendar
        self.month = month
        self.day = day

    def matches(self, date : Date) -> bool:
        return self.calendar == date.calendar and self.month == date.month and self.day == date.day
