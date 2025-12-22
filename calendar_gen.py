import csv

# ============================================================
# ===================== CONFIGURATION ========================
# ============================================================

# --- Simulation length ---
SIM_DAYS = 100 * 365

# --- Astronomical parameters ---
ASTRONOMICAL_YEAR = 365.2422
MOON_A_MONTH = 29.51         # synodic month (days)
MOON_B_MONTH = 19.7         # synodic month (days)

# --- Lunar calendar ---

LUNAR_A_MONTHS_PER_YEAR = 12
LUNAR_B_MONTHS_PER_YEAR = 18
LUNAR_A_MONTHS_NAMES = [
    "Snowen",
    "Erestri",
    "Mules",
    "Floria",
    "Ceren",
    "Honoria",
    "Shenca",
    "Forel",
    "Teir",
    "Vedi",
    "Postea",
    "Heca"
]
LUNAR_B_MONTHS_NAMES = [
    "Mesuta",
    "Doluzi",
    "Dutomo",
    "Mikos",
    "Bemas",
    "Milon",
    "Rebim",
    "Hubiz",
    "Ilmab",
    "Nuken",
    "Ara",
    "Ozi",
    "Aso",
    "Ivo",
    "Abos",
    "Esot",
    "Hasiz",
    "Melus"
]

# --- Solar calendar ---
SOLAR_CIVIL_YEAR = 365
SOLAR_MONTH_LENGTHS = [30] * 12 + [5] # adding a 5-day festival month at the end of the year
SOLAR_MONTH_NAMES = [
    "Snowen",
    "Erestri",
    "Mules",
    "Floria",
    "Ceren",
    "Honoria",
    "Shenca",
    "Forel",
    "Teir",
    "Vedi",
    "Postea",
    "Heca",
    "Festivius"
]

# --- Lunisolar calendar ---
LUNISOLAR_MONTH_NAMES = [
    "Snowen",
    "Erestri",
    "Mules",
    "Floria",
    "Ceren",
    "Honoria",
    "Shenca",
    "Forel",
    "Teir",
    "Vedi",
    "Postea",
    "Heca",
    "Lunarias",
    "LunariasB"
]

# --- Phase naming ---
PHASE_NAMES = [
    "New",
    "Waxing Crescent",
    "First Quarter",
    "Waxing Gibbous",
    "Full",
    "Waning Gibbous",
    "Last Quarter",
    "Waning Crescent"
]

# --- Solar markers (fraction of year) ---
SOLAR_MARKERS = {
    0.00: "Winter Solstice",
    0.25: "Spring Equinox",
    0.50: "Summer Solstice",
    0.75: "Autumn Equinox"
}

# --- Astronomical events ---
MOON_NAMES = [
    "Big",
    "Small",
]

# --- Eclipse mechanics ---
MOON_A_NODE_PERIOD = 6798.1
MOON_B_NODE_PERIOD = 842.3

TOTAL_ECLIPSE_LIMIT = 0.01
PARTIAL_ECLIPSE_LIMIT = 0.025
WEAK_PARTIAL_ECLIPSE_LIMIT = 0.045

OUTPUT_FILE = "calendar_output.csv"

# ============================================================
# ====================== CORE MATH ===========================
# ============================================================

def phase(day, period):
    """Raw phase in [0,1)."""
    return (day / period) % 1.0

def quantize_phase(p):
    """Convert raw phase to named phase."""
    index = int((p * 8) + 0.5) % 8
    return PHASE_NAMES[index]

def solar_phase(day):
    return (day / ASTRONOMICAL_YEAR) % 1.0

def node_phase(day, period):
    """Returns node phase in [0,1)."""
    return (day / period) % 1.0

def node_distance(p):
    """
    Angular distance from nearest node.
    0.0 or 0.5 are nodes.
    Returns normalized distance [0, 0.25].
    """
    return min(
        abs(p),
        abs(p - 0.5),
        abs(p - 1.0)
    )


# ============================================================
# =================== EVENT DETECTION ========================
# ============================================================

def crossed(prev, curr, target):
    """Detect upward crossing of a fractional target."""
    if prev <= curr:
        return prev < target <= curr
    else:
        # wraparound case
        return prev < target or target <= curr

def solar_marker(prev_phase, curr_phase):
    for k, name in SOLAR_MARKERS.items():
        if crossed(prev_phase, curr_phase, k):
            return name
    return ""

def is_full_moon(prev_phase, curr_phase):
    return crossed(prev_phase, curr_phase, 0.5)

def phase_crossed(prev, curr, target):
    """
    Returns True if phase crosses target between prev and curr.
    Handles wraparound correctly.
    """
    if prev <= curr:
        return prev < target <= curr
    else:
        # wraparound (e.g. 0.95 -> 0.02)
        return prev < target or target <= curr

def moon_syzygy(prev_phase, curr_phase):
    """
    Returns:
        "New" if new moon occurs
        "Full" if full moon occurs
        None otherwise
    """
    if phase_crossed(prev_phase, curr_phase, 0.0):
        return "New"
    if phase_crossed(prev_phase, curr_phase, 0.5):
        return "Full"
    return None

def syzygy_overlap(
    prev_a, curr_a,
    prev_b, curr_b,
    moon_a_name="Big",
    moon_b_name="Small"
):
    """
    Returns a string describing syzygy overlap, or "" if none.
    """

    a_event = moon_syzygy(prev_a, curr_a)
    b_event = moon_syzygy(prev_b, curr_b)

    if not a_event or not b_event:
        return ""

    # Both have syzygy today
    if a_event == b_event:
        return f"Double {a_event}"

    # Mixed case
    if a_event == "Full":
        return f"{moon_a_name} Full"
    else:
        return f"{moon_b_name} Full"
    
def classify_eclipse(syzygy_type, node_dist):
    """
    Returns eclipse classification or None.
    """
    if node_dist <= TOTAL_ECLIPSE_LIMIT:
        return f"Total {syzygy_type} Eclipse"
    if node_dist <= PARTIAL_ECLIPSE_LIMIT:
        return f"Partial {syzygy_type} Eclipse"
    if node_dist <= WEAK_PARTIAL_ECLIPSE_LIMIT:
        return f"Weak Partial {syzygy_type} Eclipse"
    return None

def moon_eclipse(prev_phase, curr_phase, node_p):
    """
    Detects and classifies eclipse for one moon.
    """
    nd = node_distance(node_p)

    if phase_crossed(prev_phase, curr_phase, 0.0):
        return classify_eclipse("Solar", nd)

    if phase_crossed(prev_phase, curr_phase, 0.5):
        return classify_eclipse("Lunar", nd)

    return None

def double_moon_eclipse(
    a_prev, a_curr, a_node,
    b_prev, b_curr, b_node
):
    ea = moon_eclipse(a_prev, a_curr, a_node)
    eb = moon_eclipse(b_prev, b_curr, b_node)

    if ea and eb:
        return f"Double Eclipse ({ea} + {eb})"
    return ea or eb or ""



# ============================================================
# ===================== CALENDARS ============================
# ============================================================

def solar_calendar_date(day):
    year = int(day // SOLAR_CIVIL_YEAR)
    day_of_year = int(day % SOLAR_CIVIL_YEAR)

    month = 0
    while day_of_year >= SOLAR_MONTH_LENGTHS[month]:
        day_of_year -= SOLAR_MONTH_LENGTHS[month]
        month += 1

    return year + 1, month + 1, day_of_year + 1

def lunar_calendar_date(day, month_length, months_per_year):
    total_months = int(day // month_length)

    year = total_months // months_per_year
    month = total_months % months_per_year
    day_in_month = int(day % month_length)

    return year + 1, month + 1, day_in_month + 1

# ============================================================
# ============== LUNISOLAR YEAR COMPUTATION =================
# ============================================================

def compute_lunisolar_year_starts():
    """
    Lunisolar year starts on the first FULL Moon A
    after the winter solstice.
    """
    starts = [0]

    prev_solar = solar_phase(0)
    prev_moon = phase(0, MOON_A_MONTH)

    day = 1
    while day < SIM_DAYS:
        curr_solar = solar_phase(day)
        curr_moon = phase(day, MOON_A_MONTH)

        # Detect winter solstice (solar phase wrap)
        if prev_solar > curr_solar:
            # Find next full Moon A
            d = day
            while d < SIM_DAYS:
                p0 = phase(d - 1, MOON_A_MONTH)
                p1 = phase(d, MOON_A_MONTH)
                if is_full_moon(p0, p1):
                    starts.append(d)
                    break
                d += 1

        prev_solar = curr_solar
        prev_moon = curr_moon
        day += 1

    return starts

def lunisolar_date(day, year_starts):
    year_index = max(i for i, d in enumerate(year_starts) if d <= day)
    year_start = year_starts[year_index]

    day_in_year = day - year_start
    month = int(day_in_year // MOON_A_MONTH)
    day_in_month = int(day_in_year % MOON_A_MONTH)

    return year_index + 1, month + 1, day_in_month + 1

# ============================================================
# ======================= MAIN ===============================
# ============================================================

def main():
    year_starts = compute_lunisolar_year_starts()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
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
        ])

        prev_ma = phase(0, MOON_A_MONTH)
        prev_mb = phase(0, MOON_B_MONTH)
        prev_solar = solar_phase(0)

        for day in range(SIM_DAYS):
            ma = phase(day, MOON_A_MONTH)
            mb = phase(day, MOON_B_MONTH)
            sp = solar_phase(day)
            syz_overlap = syzygy_overlap(
                prev_ma, ma,
                prev_mb, mb,
                moon_a_name="Big",
                moon_b_name="Small"
            )
            node_a = node_phase(day, MOON_A_NODE_PERIOD)
            node_b = node_phase(day, MOON_B_NODE_PERIOD)
            eclipse_event = double_moon_eclipse(
                prev_ma, ma, node_a,
                prev_mb, mb, node_b
            )
            solar_y, solar_m_num, solar_d = solar_calendar_date(day)
            solar_m = SOLAR_MONTH_NAMES[solar_m_num-1]
            lunarA_y, lunarA_m_num, lunarA_d = lunar_calendar_date(day, MOON_A_MONTH, LUNAR_A_MONTHS_PER_YEAR)
            lunarA_m = LUNAR_A_MONTHS_NAMES[lunarA_m_num-1]
            lunarB_y, lunarB_m_num, lunarB_d = lunar_calendar_date(day, MOON_B_MONTH, LUNAR_B_MONTHS_PER_YEAR)
            lunarB_m = LUNAR_B_MONTHS_NAMES[lunarB_m_num-1]
            lsy, lsm_num, lsd = lunisolar_date(day, year_starts)
            lsm = LUNISOLAR_MONTH_NAMES[lsm_num-1]

            writer.writerow([
                day,
                round(ma, 6),
                quantize_phase(ma),
                round(mb, 6),
                quantize_phase(mb),
                syz_overlap,
                eclipse_event,
                round(sp, 6),
                solar_marker(prev_solar, sp),
                solar_y,
                solar_m_num,
                solar_m,
                solar_d,
                lsy,
                lsm_num,
                lsm,
                lsd,
                lunarA_y,
                lunarA_m_num,
                lunarA_m,
                lunarA_d,
                lunarB_y,
                lunarB_m_num,
                lunarB_m,
                lunarB_d
            ])

            prev_solar = sp
            prev_ma = ma
            prev_mb = mb

    print(f"Calendar written to {OUTPUT_FILE}")

# ============================================================

if __name__ == "__main__":
    main()
