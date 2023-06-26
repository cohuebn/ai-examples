from datetime import datetime, time


def start_of_day(value: datetime) -> datetime:
    """Get a timestamp for the start of the day of the given datetime"""
    return datetime.combine(value, time.min)


def end_of_day(value: datetime) -> datetime:
    """Get a timestamp for the end of the day of the given datetime"""
    return datetime.combine(value, time.max)
