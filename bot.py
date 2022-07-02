import telebot
from db import init_db, get_user_group, edit_user_group, add_new_user, check_exists_user
from config import token
from parser import get_schedule, print_schedule, get_group_id
from date import get_date


def telegram_bot():
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Бот, отправляющий расписание с портала unn.')

    @bot.message_handler(content_types=["text"])
    def send_schedule(message):
        text = message.text.split()
        telegram_id = message.from_user.id

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

        if 'сегодня' or 'завтра' or 'неделя' or 'следующая' or 'дата' in text[0]:
            if check_exists_user(telegram_id=telegram_id):
                group_id = get_user_group(telegram_id=telegram_id)
            else:
                bot.send_message(message.chat.id, 'Сначала нужно ввести название группы')
                return

        if 'сегодня' or 'завтра' in text[0]:
            diff = 0
            if 'завтра' in text[0]:
                diff = 1
            date = get_date(diff)
            schedule = get_schedule(group_id, date, date)
            bot.send_message(message.chat.id, print_schedule(schedule))
        elif 'неделя' in text[0]:
            pass
        elif 'следующая' in text[0]:
            pass

    bot.polling()


if __name__ == '__main__':
    init_db(force=False)
    telegram_bot()