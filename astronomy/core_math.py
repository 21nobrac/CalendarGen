def phase(day : int, period : float):
    """Raw phase in [0,1)."""
    return (day / period) % 1.0

def phase_crossed(prev : float, curr : float, target : float):
    """
    Returns True if phase crosses target between prev and curr.
    Handles wraparound correctly.
    """
    if prev <= curr:
        return prev < target <= curr
    else:
        # wraparound (e.g. 0.95 -> 0.02)
        return prev < target or target <= curr