from datetime import datetime


def datetime_format(value: datetime, format="%H:%M %d-%m-%y"):
    return value.strftime(format)
