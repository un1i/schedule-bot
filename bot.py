import telebot
from db import init_db, get_user_group, edit_user_group, add_new_user, check_exists_user
from config import token
from parser import get_schedule, print_schedule, get_group_id
from date import get_date, get_week, check_date, reverse_date, date_addition


def telegram_bot():
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Бот, отправляющий расписание с портала unn.')

    @bot.message_handler(content_types=["text"])
    def send_schedule(message):
        text = message.text.split()
        telegram_id = message.from_user.id
        schedule_commands = ['сегодня', 'завтра', 'неделя', 'следующая', 'дата']

        if 'группа' in text[0]:
            group_id = get_group_id(text[1])
            try:
                if check_exists_user(telegram_id=telegram_id):
                    edit_user_group(telegram_id=telegram_id, group_id=group_id)
                    bot.send_message(message.chat.id, 'Группа успешно изменена')
                else:
                    add_new_user(telegram_id=telegram_id, group_id=group_id)
                    bot.send_message(message.chat.id, 'Группа успешно добавлена')
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, 'Что-то пошло не так')
            return

        if any(s in text[0] for s in schedule_commands):
            if check_exists_user(telegram_id=telegram_id):
                group_id = get_user_group(telegram_id=telegram_id)
            else:
                bot.send_message(message.chat.id, 'Сначала нужно ввести название группы')
                return

        if 'сегодня' in text[0] or 'завтра' in text[0]:
            diff = 0
            if 'завтра' in text[0]:
                diff = 1
            date = get_date(diff)
            schedule = get_schedule(group_id, date, date)
            bot.send_message(message.chat.id, print_schedule(schedule))
        elif 'неделя' in text[0] or 'следующая' in text[0]:
            next_week = False
            if 'следующая' in text[0]:
                next_week = True
            start_week, finish_week = get_week(next_week)
            schedule = get_schedule(group_id, start_week, finish_week)
            bot.send_message(message.chat.id, print_schedule(schedule))
        elif 'дата' in text[0]:
            date = text[1]
            if len(date.split('.')) == 2 or len(date.split('.')[-1]) == 0:
                date = date_addition(date)
            if check_date(date):
                date = reverse_date(date)
                schedule = get_schedule(group_id, date, date)
                bot.send_message(message.chat.id, print_schedule(schedule))
            else:
                bot.send_message(message.chat.id, "Некорректная дата")

    bot.polling()


if __name__ == '__main__':
    init_db(force=False)
    telegram_bot()
