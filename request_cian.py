from sql_requests import DataBase

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
        xpath_link = []
        for i in range(1, self.__kol):
            path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[1]/a'
            el = self.__xml.xpath(path)
            if not el:
                xpath_link.append('nothing')
                continue
            xpath_link.append(el[0].get("href"))

        return xpath_link

    def __get_main_photo(self) -> list:
        xpath_photo = []
        for i in range(1, self.__kol+1):
            path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/a/div[1]/div/ul/li[1]/div/img'
            path_second_photo = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/a/div[3]/div[1]/div/picture/img'
            second_photo = self.__xml.xpath(path_second_photo)
            path_thirty_photo = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/a/div[3]/div[2]/div/picture/img'
            thirty_photo = self.__xml.xpath(path_thirty_photo)
            el = self.__xml.xpath(path)
            if not el:
                xpath_photo.append("nothing")
                continue
            if not second_photo and not thirty_photo:
                xpath_photo.append([el[0].get('src')])
            elif not second_photo:
                xpath_photo.append([el[0].get('src'), second_photo[0].get('src')])
            elif not thirty_photo:
                xpath_photo.append([el[0].get('src'), thirty_photo[0].get('src')])
            else:
                xpath_photo.append([el[0].get('src'), second_photo[0].get('src'), thirty_photo[0].get('src')])

        return xpath_photo

    def __get_underground(self) -> list[dict[str, str]]:
        underground = []
        for i in range(1, self.__kol+1):
            path = (f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[2]/div['
                    f'1]/a/div[2]')
            path_time = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[2]/div[1]/div'
            elem = self.__xml.xpath(path)
            time_metro = self.__xml.xpath(path_time)
            if not elem:
                path = (f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[3]/div['
                        f'1]/a/div[2]')
                path_time = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[3]/div[1]/div'
                elem = self.__xml.xpath(path)
                time_metro = self.__xml.xpath(path_time)
            if not elem:
                underground.append({
                    "metro": "nothing",
                    "time": "nothing"
                })
                continue
            underground.append({
                "metro": elem[0].text,
                "time": time_metro[0].text
            })

        return underground

    def __get_about_text(self) -> list[str]:
        about_ads = []
        for i in range(1, self.__kol+1):
            exits_about = False
            for j in range(4, 7):
                path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[{j}]/div[2]/p'
                elem = self.__xml.xpath(path)
                if elem:
                    about_ads.append(elem[0].text)
                    exits_about = True
                    break
            if not exits_about:
                about_ads.append("nothing")
        return about_ads

    def __get_description(self) -> list[str]:
        description = []
        for i in range(1, self.__kol+1):
            exits_description = False
            for j in range(1, 5):
                path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[{j}]/div[2]/p'
                el = self.__xml.xpath(path)
                if el:
                    exits_description = True
                    description.append(el[0].text)
                    break
            if not exits_description:
                description.append("nothing")

        return description

    def __get_price(self) -> list[str]:
        price = []
        for i in range(1, self.__kol+1):
            exist_price = False
            for j in range(1, 7):
                path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[{j}]/div[1]/span/span'
                el = self.__xml.xpath(path)
                if el:
                    exist_price = True
                    price.append(el[0].text)
                    break
            if not exist_price:
                price.append("nothing")

        return price

    def __get_geolocation(self) -> list[str]:
        geolocation = []
        for i in range(1, self.__kol+1):
            exists_address = False
            address = ''
            for j in range(1, 7):
                path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[{j}]/div[2]'
                if self.__xml.xpath(path):
                    exists_address = True
                    for k in range(1, 8):
                        path_total = path + f"/a[{k}]"
                        el = self.__xml.xpath(path_total)
                        if el:
                            address += el[0].text + " "
            if address != '':
                geolocation.append(address)
            if not exists_address:
                geolocation.append("nothing")

        return geolocation

    def parse_all_data(self):
        data_pars = []

        geolocation = self.__get_geolocation()
        price = self.__get_price()
        about_txt = self.__get_price()
        underground = self.__get_underground()
        photo = self.__get_main_photo()
        links = self.__get_link()

        db = DataBase()
        last_id = db.get_information()

        new_id = []
        for i in range(len(links)):
            if links[i] == "nothing":
                continue

            data = {
                "id": links[i].split("/")[-2],
                "link": links[i],
                "price": price[i],
                "photo": photo[i],
                "underground": f"{underground[i]['metro']} | {underground[i]['time']}",
                "no_commission": check_commission(about_txt[i]),
                "address": geolocation[i].strip()
            }

            if int(data["id"]) in last_id:
                continue

            new_id.append(int(data["id"]))
            data_pars.append(data)

        db.new_information(new_id)
        return data_pars


def main(url_resp: str, kol_adv: int):
    response = RequestCian(url_resp, kol_adv)
    for el in response.parse_all_data():
        print(el)


url = "https://cian.ru/cat.php?engine_version=2&p=1&with_neighbors=0&region=2&deal_type=rent&offer_type=flat&type=4"
main(url, 10)