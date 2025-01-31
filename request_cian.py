from lxml.etree import HTML
from requests import get
from bs4 import BeautifulSoup


def get_link(xml, kol: int) -> list:
    xpath_link = [
        xml.xpath(
            f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[1]/a'
        )[0].get("href") for i in range(1, kol) if xml.xpath(
            f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[1]/a'
        )
    ]
    return xpath_link


def get_main_photo(xml, kol: int) -> list:
    xpath_photo = [
        xml.xpath(
            f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/a/div[1]/div/ul/li[1]/div/img'
        )[0].get("src") for i in range(1, kol) if xml.xpath(
            f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/a/div[1]/div/ul/li[1]/div/img'
        )
    ]
    return xpath_photo


def get_underground(xml, kol: int):
    underground = []
    for i in range(1, kol):
        path = (f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[2]/div['
                f'1]/a/div[2]')
        elem = xml.xpath(path)
        if not elem:
            path = (f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[3]/div['
                    f'1]/a/div[2]')
            elem = xml.xpath(path)
        if not elem:
            continue

        underground.append(elem[0].text)

    return underground


def get_about_text(xml, kol):
    about_ads = []
    for i in range(1, kol):
        for j in range(1, 7):
            path = f'//*[@id="frontend-serp"]/div/div/div[4]/div[{i}]/div/article/div[1]/div/div[1]/div/div[{j}]/div[2]/p'
            elem = xml.xpath(path)
            if elem:
                about_ads.append(elem[0].text)
                break
    return about_ads

def parse_all_data(url):
    soup = BeautifulSoup(get(url).text, "html.parser")
    xml = HTML(str(soup))
    print(len(get_underground(xml, 20)))
    print(len(get_main_photo(xml, 20)))
    print(len(get_link(xml, 20)))
    print(len(get_about_text(xml, 20)))





if __name__ == "__main__":
    url_all = "https://cian.ru/cat.php?engine_version=2&p=1&with_neighbors=0&region=2&deal_type=rent&offer_type=flat&type=4"
    parse_all_data(url_all)