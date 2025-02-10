from sql_requests import create_main_table
from request_cian import parse_all_data

from telebot import TeleBot
from telebot.types import InputMediaPhoto
from json import load
from threading import Timer
from random import shuffle, randint

from loguru import logger


with open("config.json") as config:
    information = load(config)
    TOKEN = information["token"]
    INTERVAL = information["interval"]
    ADMIN = information["admin"]
    city = information["city_tg"]
    PATH_TO_LOG = information["loger_path"]

url = "https://cian.ru/cat.php?engine_version=2&p=1&with_neighbors=0&region=2&deal_type=rent&offer_type=flat&type=4"

logger.add(PATH_TO_LOG, level="DEBUG")

NAME_LST = [
    "Лев", "София", "Артем", "Матвей", "Максим", "Роман",
    "Даниил", "Анастасия", "Алиса", "Милана" , "Виктория",
    "Анна", "Дмитрий", "Мария", "Иван", "Илья", "Кирилл",
    "Виктор", "Александр", "Алексей", "Сергей", "Елизавета"
]

bot = TeleBot(token=TOKEN)

try:
    @logger.catch
    def start_timer(message):
        Timer(INTERVAL, posting_message).start()


    @logger.catch
    def format_message(data_massage: dict) -> str:
        shuffle(NAME_LST)
        name = NAME_LST[randint(0, len(NAME_LST) - 1)]
        return (f'Сдается квартира от <a href="{data_massage["link"]}">{name}</a>, метро: {data_massage["underground"]}\n'
                   f'Цена: {data_massage["price"]}\n'
                   f'Адрес: {data_massage["address"]}')


    @bot.message_handler(commands=["start"])
    def main(message):
        bot.send_message(ADMIN, "start")

        create_main_table()
        start_timer(message)


    @logger.catch
    def posting_message():
        data = parse_all_data(url)
        for el in data:
            message = format_message(el)
            if el["photo"] == "nothing":
                bot.send_message(chat_id=ADMIN, text=message, parse_mode='html')
                continue
            if len(el["photo"]) == 1:
                bot.send_photo(chat_id=ADMIN, photo=el["photo"][0], caption=message, parse_mode='html')
                continue
            if len(el["photo"]) > 1:
                media = []
                for i, photo in enumerate(el["photo"]):
                    if not i:
                        media.append(InputMediaPhoto(media=photo, caption=message, parse_mode="html"))
                        continue
                    media.append(InputMediaPhoto(media=photo))

                bot.send_media_group(chat_id=ADMIN, media=media)


except Exception as all_mistake:
    logger.error(all_mistake)


print("bot worked")
bot.infinity_polling(timeout=10, long_polling_timeout=150)
logger.info("bot stop")
