from config import PHASE_NAMES

def phase(day, period):
    """Raw phase in [0,1)."""
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