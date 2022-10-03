import requests
from bs4 import BeautifulSoup as BS

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
}

HOST = "https://doramy.club/genre/kriminal"


def get_html(URL):
    request = requests.get(url=URL, headers=HEADERS)
    return request


def get_data_dorama(html):
    soup = BS(html, "html.parser")
    items = soup.find_all("div", class_="post-home")
    doramas = []
    for i in items:
        doramas.append({

               "link": i.find("a").get("href"),
                'title':i.find("a").find("span").get_text(),
                "image": i.find("a").find("img").get("src")}

        )
    return doramas

def parser_func_dorama():
    html = get_html(HOST)
    if html.status_code == 200:
        dorama = []
        for i in range(1, 183):
            html = get_html(f"https://doramy.club/strana/yuzhnaya-koreya/page/{i}")
            dorama.extend(get_data_dorama(html.text))
            return dorama
    else:
        raise Exception("Error in parser function dorama")


def parser_func():
    html = get_html(HOST)
    if html.status_code == 200:
        doramas = []
        doramas.extend(get_data_dorama(html.text))
        return doramas
    else:
        raise Exception("Error in parser function")


parser_func()