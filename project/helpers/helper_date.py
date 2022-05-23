from datetime import date, datetime


DATE_FORMAT = "%d/%m/%y"
DATE_FORMAT_COMPLETE = "%d/%m/%y %H:%M:%S"


def date_to_str(value: "datetime"):
    return value.strftime(DATE_FORMAT)


def today():
    return datetime.now().date()
