from sql_requests import DataBase
from text_summary import summy_message

from lxml.etree import HTML
from requests import get
from bs4 import BeautifulSoup


def check_commission(text: str) -> bool:
    return True if "без комиссии" in text else False


class RequestCian:
    def __init__(self, url_input: str, kol_adv: int):
        self.__url = url_input
        self.__kol = kol_adv
        self.__create_response(url_input)

    def __create_response(self, url_input: str) -> None:
        soup = BeautifulSoup(get(url_input).text, "html.parser")
        xml = HTML(str(soup))
        self.__xml = xml

    def __get_link(self) -> list:
        xpath_link = [[] for _ in range(self.__kol)]
        for i in range(1, self.__kol):
            path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/a'
            el = self.__xml.xpath(path)
            if not el:
                continue
            xpath_link[i] = el[0].get("href")

        return xpath_link


    def __get_main_photo(self) -> list:
        ans = [[] for _ in range(self.__kol)]
        for i in range(self.__kol):
            main_photo = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/a/div[1]/div/ul/li[1]/div/img'
            second_photo = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/a/div[3]/div[1]/div/picture/img'
            third_photo = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/a/div[3]/div[2]/div/picture/img'
            fourth_photo = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/a/div[3]/div[3]/div[1]/picture/img'

            prom_arr = list(filter(lambda el: el,
                                   [self.__xml.xpath(main_photo), self.__xml.xpath(second_photo), self.__xml.xpath(third_photo),
                                    self.__xml.xpath(fourth_photo)]))

            all_photo_link = list(map(lambda el: el[0].get('src'), prom_arr))
            if len(all_photo_link) == 4:
                ans[i] = all_photo_link
        return ans

    def __get_underground(self) -> list[dict[str, str]]:
        underground = [{} for _ in range(self.__kol)]
        for i in range(1, self.__kol):
            path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/div/div[1]/div/div[2]/div[1]/a/div[2]'
            path_time = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/div/div[1]/div/div[2]/div[1]/div'
            elem = self.__xml.xpath(path)
            time_metro = self.__xml.xpath(path_time)
            if not elem:
                path = (f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[3]/div['
                        f'1]/a/div[2]')
                path_time = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[3]/div[1]/div'
                elem = self.__xml.xpath(path)
                time_metro = self.__xml.xpath(path_time)
            if not elem or not time_metro:
                continue
            underground[i] = {
                "metro": elem[0].text,
                "time": time_metro[0].text,
                "index": i
            }

        return underground

    def __get_about_text(self) -> list:
        about_ads = [[] for _ in range(self.__kol)]
        for i in range(1, self.__kol):
            exits_about = False
            for j in range(4, 10):
                path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/div/div[1]/div/div[{j}]/div[2]/p'
                elem = self.__xml.xpath(path)
                if elem:
                    about_ads[i] = elem[0].text
                    exits_about = True

            if not exits_about:
                continue
        return about_ads

    def __get_description(self) -> list:
        description = [[] for _ in range(self.__kol)]
        for i in range(1, self.__kol):
            for j in range(1, 4):
                path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/div/div[1]/div/div[{j}]/div[2]/p'
                path_second = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[{j}]/div[2]/p'
                el = self.__xml.xpath(path)
                el2 = self.__xml.xpath(path_second)
                if el:
                    description[i] = el[0].text
                    break
                elif el2:
                    description[i] = el2[0].text
                    break

        return description

    def __get_price(self) -> list:
        price = [[] for _ in range(self.__kol)]
        for i in range(1, self.__kol):
            for j in range(1, 7):
                path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/div/div[1]/div/div[{j}]/div[1]/span/span'
                el = self.__xml.xpath(path)
                if el:
                    price[i] = el[0].text
                    break


        return price

    def __get_geolocation(self) -> list:
        geolocation = [[] for _ in range(self.__kol)]
        for i in range(1, self.__kol):
            address = ''
            for j in range(1, 7):
                path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/article/div[1]/div/div[1]/div/div[{j}]/div[2]'
                if self.__xml.xpath(path):
                    for k in range(1, 8):
                        path_total = path + f"/a[{k}]"
                        el = self.__xml.xpath(path_total)
                        if el:
                            address += el[0].text + " "
            if address != '':
                geolocation[i] = address

        return geolocation

    def parse_all_data(self):
        data_pars = []

        geolocation = self.__get_geolocation()
        price = self.__get_price()
        description_txt = self.__get_price()
        underground = self.__get_underground()
        text_ads = self.__get_about_text()
        photo = self.__get_main_photo()
        links = self.__get_link()

        short_text = [summy_message(text=text) if text != [] else [] for text in text_ads]

        db = DataBase()
        last_id = db.get_information()

        new_id = []
        for i in range(len(links)):
            if not all([links[i], geolocation[i], price[i], description_txt[i], underground[i], text_ads[i]]):
                continue

            data = {
                "id": links[i].split("/")[-2],
                "link": links[i],
                "price": price[i],
                "photo": photo[i],
                "underground": f"{underground[i]['metro']} | {underground[i]['time']}",
                "no_commission": check_commission(description_txt[i]),
                "address": geolocation[i].replace("Санкт-Петербург", "").strip(),
                "add_text": short_text[i]
            }

            if int(data["id"]) in last_id:
                continue

            new_id.append(int(data["id"]))
            data_pars.append(data)

        db.new_information(new_id)
        return data_pars



if __name__ == "__main__":
    r = RequestCian("https://cian.ru/cat.php?engine_version=2&p=1&with_neighbors=0&region=2&deal_type=rent&offer_type=flat&type=4", 50)
    print(r.parse_all_data())