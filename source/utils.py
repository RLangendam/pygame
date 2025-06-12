def clamp(x, min_value, max_value):
    """Clamp the value x between min_value and max_value."""
    return max(min_value, min(x, max_value))
