import datetime


def get_date(date_change=0):
    date = datetime.date.today() + datetime.timedelta(days=date_change)
    date = date.strftime("%Y.%m.%d")
    return date


def get_week(next_week=False):
    if not next_week:
        start_week = get_date(-1 * datetime.date.weekday(datetime.date.today()))
        finish_week = get_date(6 - datetime.date.weekday(datetime.date.today()))
    else:
        start_week = get_date(7 - datetime.date.weekday(datetime.date.today()))
        finish_week = get_date(13 - datetime.date.weekday(datetime.date.today()))
    return start_week, finish_week


def check_date(str_date):
    date_format = "%d.%m.%Y"
    try:
        datetime.datetime.strptime(str_date, date_format)
        return True
    except ValueError:
        return False


def reverse_date(date):
    old_format = "%d.%m.%Y"
    new_format = "%Y.%m.%d"
    new_date = datetime.datetime.strptime(date, old_format)
    new_date = new_date.strftime(new_format)
    return new_date


def date_addition(date):
    year = datetime.date.today().timetuple()[0]
    if date[-1] != '.':
        date += '.'
    new_date = date + str(year)
    return new_date


def string_date(date, day_of_week):
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября",
              "ноября", "декабря"]
    date_sep = date.split('.')
    month = int(date_sep[1]) - 1
    day = int(date_sep[2])
    return f"[{day} {months[month]}] {day_of_week}"
