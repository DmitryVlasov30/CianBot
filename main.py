from sql_requests import create_main_table
from request_cian import parse_all_data
from telebot import TeleBot
from json import load
from threading import Timer

from loguru import logger


with open("config.json") as config:
    information = load(config)
    token = information["token"]
    interval = information["interval"]
    admin = information["admin"]
    city = information["city_tg"]
    path_to_log = information["loger_path"]

url = "https://cian.ru/cat.php?engine_version=2&p=1&with_neighbors=0&region=2&deal_type=rent&offer_type=flat&type=4"

logger.add(path_to_log, level="DEBUG")
name_lst = []
bot = TeleBot(token=token)

try:
    @logger.catch
    def start_timer(message):
        Timer(interval, posting_message).start()
        pass


    @logger.catch
    def format_message(data_massage: dict) -> str:
        message = (f'Сдается квартира, метро: {data_massage["underground"]}\n'
                   f'Цена: {data_massage["price"]}\n'
                   f'Адрес: {data_massage["address"]}')
        return message

    @bot.message_handler(commands=["start"])
    def main(message):
        bot.send_message(admin, "start")

        create_main_table()
        start_timer(message)


    def posting_message():
        data = parse_all_data(url)
        for el in data:
            message = format_message(el)
            if el["photo"] != "nothing":
                bot.send_photo(chat_id=admin, photo=el["photo"], caption=message)
                continue
            bot.send_message(chat_id=admin, text=message)





except Exception as all_mistake:
    logger.error(all_mistake)


print("bot worked")
bot.infinity_polling(timeout=10, long_polling_timeout=150)
logger.info("bot stop")

