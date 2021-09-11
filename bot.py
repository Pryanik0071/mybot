import logging
from datetime import date
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings


logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def position_planet_today(update, context):
    date_today = str(date.today().strftime('%Y/%m/%d'))
    planet_name = update.message.text.split()[-1]
    planets_list = {
        'Mars': ephem.Mars(date_today),  # Марс
        'Mercury': ephem.Mercury(date_today),  # Меркурий
        'Venus': ephem.Venus(date_today),  # Венера
        'Jupiter': ephem.Jupiter(date_today),  # Юпитер
        'Neptune': ephem.Neptune(date_today),  # Нептун
        'Saturn': ephem.Saturn(date_today),  # Сатурн
        'Uranus': ephem.Uranus(date_today),  # Уран
        'Pluto': ephem.Pluto(date_today)  # Плутон
    }
    constellation = ephem.constellation(planets_list[planet_name])
    constellation_short_name, constellation_name = constellation
    update.message.reply_text(
        f"""Сегодня планета {planet_name} в созвездии {constellation_name}""")


# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", position_planet_today))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    # Командуем боту начать ходить в Telegram за сообщениями
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()


# Вызываем функцию main() - именно эта строчка запускает бота
if __name__ == "__main__":
    main()
