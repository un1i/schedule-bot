import requests
from date import string_date
from cache import timed_lru_cache

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru,en;q=0.9",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.706 Yowser/2.5 Safari/537.36",
}


def get_group_id(group_name):
    url = f'https://portal.unn.ru/ruzapi/search?term={group_name}&type=group'
    inf = requests.get(url=url, headers=headers)
    if len(inf.json()) > 1 or len(inf.json()) == 0:
        return None
    group_id = inf.json()[0]['id']
    return group_id


@timed_lru_cache(1800)
def get_schedule(group_id, start, finish):
    url = f'https://portal.unn.ru/ruzapi/schedule/group/{group_id}?start={start}&finish={finish}&lng=1'  # 2022.06.27
    inf = requests.get(url=url, headers=headers)
    return inf.json()


def print_schedule(schedule):
    size = len(schedule)
    if size == 0:
        text = "Пар нет"
        return text
    text = ''
    for i in range(0, size):
        if i == 0 or schedule[i - 1]["date"] != schedule[i]["date"]:
            text = string_date(schedule[i]['date'], schedule[i]["dayOfWeekString"]) + '\n'
        text += schedule[i]['discipline'] + '\n' + schedule[i]['kindOfWork'] + '\n' + schedule[i]['beginLesson'] + '-'\
                + schedule[i]['endLesson'] + '\n' + schedule[i]['auditorium'] + " (" + schedule[i]["building"] + ")" \
                + '\n' + schedule[i]['lecturer'] + '\n\n' + '/' * 20 + '\n\n'
    return text
