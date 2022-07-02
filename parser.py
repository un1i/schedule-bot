import json
import requests

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
    group_id = inf.json()[0]['id']
    return group_id


def get_schedule(group_id, start, finish):
    url = f'https://portal.unn.ru/ruzapi/schedule/group/{group_id}?start={start}&finish={finish}&lng=1'  # 2022.06.27
    inf = requests.get(url=url, headers=headers)
    return inf.json()


def print_schedule(schedule):
    if len(schedule) == 0:
        text = "Пар нет"
        return text
    text = ''
    for item in schedule:
        text += item['discipline'] + '\n' + item['beginLesson'] + '-' + item['endLesson'] + '\n' + item['auditorium']
        text += '\n' + item['lecturer']
        text += '\n\n' + '/'*20 + '\n\n'
    return text

