def within_1d(time, schedule):
    """Determines if schedule is relevant for the current data"""
    return (schedule['day'] == 'weekdays' and time.tm_wday <= 5
            or schedule['day'] == time.tm_wday)

def convert_to_s(delta):
    """"""
    return delta.hours*60*60 + delta.minutes*60 + delta.seconds