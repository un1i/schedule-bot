import telebot
from config import token
from parser import get_schedule, print_schedule


def telegram_bot():
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Бот, отправляющий расписание с портала unn.')

    @bot.message_handler(content_types=["text"])
    def send_today_schedule(message):
        if "сегодня" in message.text:
            schedule = get_schedule('', '2022.07.01', '2022.07.01')
            bot.send_message(message.chat.id, print_schedule(schedule))
    bot.polling()


if __name__ == '__main__':
    telegram_bot()