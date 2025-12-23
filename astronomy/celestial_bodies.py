class Moon:
    def __init__(self, synodic_month : float = 29.53):
        self.synodic_month = synodic_month
        self.phase = 0
        self.prev_phase = 0

    def tick_day(self):
        self.prev_phase = self.phase
        per_day_tick = 1 / self.synodic_month
        self.phase = (self.phase + per_day_tick) % 1.0

class Sun:
    def __init__(self, solar_year : float = 365.24):
        self.solar_year = solar_year
        self.phase = 0
        self.prev_phase = 0

    def tick_day(self):
        self.prev_phase = self.phase
        per_day_tick = 1 / self.solar_year
        self.phase = (self.phase + per_day_tick) % 1.0
