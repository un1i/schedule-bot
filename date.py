import datetime


def get_date(date_change=0):
    date = datetime.date.today() + datetime.timedelta(days=date_change)
    date = date.strftime("%Y.%m.%d")
    return date


