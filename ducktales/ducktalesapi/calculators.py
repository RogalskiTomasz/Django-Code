import math


def zinsrechner(capital, interest_rate, unit, duration):
    if unit == 'm':
        duration = math.floor(duration / 12)
    elif unit == 'q':
        duration = math.floor(duration / 4)
    return capital * math.pow((1 + (interest_rate / 100)), duration)
