from lxml.etree import HTML
from requests import get
from bs4 import BeautifulSoup


def get_link(xml, kol: int) -> list:
    xpath_link = []
    for i in range(1, kol):
        path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[1]/a'
        el = xml.xpath(path)
        if not el:
            xpath_link.append('nothing')
            continue
        xpath_link.append(el[0].get("href"))

    return xpath_link


def get_main_photo(xml, kol: int) -> list:
    xpath_photo = []
    for i in range(1, kol):
        path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/a/div[1]/div/ul/li[1]/div/img'
        el = xml.xpath(path)
        if not el:
            xpath_photo.append("nothing")
            continue
        xpath_photo.append(el[0].get('src'))

    return xpath_photo


def get_underground(xml, kol: int) -> list[dict]:
    underground = []
    for i in range(1, kol):
        path = (f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[2]/div['
                f'1]/a/div[2]')
        path_time = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[2]/div[1]/div'
        elem = xml.xpath(path)
        time_metro = xml.xpath(path_time)
        if not elem:
            path = (f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[3]/div['
                    f'1]/a/div[2]')
            path_time = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[3]/div[1]/div'
            elem = xml.xpath(path)
            time_metro = xml.xpath(path_time)
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


def get_about_text(xml, kol: int) -> list[str]:
    about_ads = []
    for i in range(1, kol):
        exits_about = False
        for j in range(1, 7):
            path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[{j}]/div[2]/p'
            elem = xml.xpath(path)
            if elem:
                about_ads.append(elem[0].text)
                exits_about = True
                break
        if not exits_about:
            about_ads.append("nothing")
    return about_ads


def check_commission(text: str) -> bool:
    return True if "без комиссии" in text else False


def get_description(xml, kol: int) -> list[str]:
    description = []
    for i in range(1, kol):
        exits_description = False
        for j in range(1, 8):
            path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[{j}]/div[2]/p'
            el = xml.xpath(path)
            if el:
                exits_description = True
                description.append(el[0].text)
                continue
        if not exits_description:
            description.append("nothing")

    return description


def parse_all_data(url):
    soup = BeautifulSoup(get(url).text, "html.parser")
    xml = HTML(str(soup))
    [print(el) for el in get_underground(xml, 20)]
    print("\n\n\n")
    [print(el) for el in get_main_photo(xml, 20)]
    print("\n\n\n")
    [print(el) for el in get_link(xml, 20)]
    print("\n\n\n")
    [print(el) for el in get_about_text(xml, 20)]
    print("\n\n\n")
    [print(el) for el in get_description(xml, kol=20)]





if __name__ == "__main__":
    url_all = "https://cian.ru/cat.php?engine_version=2&p=1&with_neighbors=0&region=2&deal_type=rent&offer_type=flat&type=4"
    parse_all_data(url_all)