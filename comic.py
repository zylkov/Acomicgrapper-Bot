import requests, re, json
from bs4 import BeautifulSoup

url=r"https://acomics.ru/"

type_info ={
    "Автор оригинала:":"authors",
    "Авторы оригинала:":"authors",
    "Авторы:":"authors",
    "Автор:":"authors",
    "Переводчики:":"authors_translation",
    "Переводчик:":"authors_translation",
    "Количество выпусков:":"count_pages",
    "Количество подписчиков:":"count_subscribes",
    "Официальный сайт:":"site",
    "Сайт:":"site",
    "Возрастной рейтинг:":"rating",
    "Лицензия:":"license"
}

def remove_tag(select):
    if select.name is not None: 
        return select.text
    return select

def get_comic(name):
    page = requests.get(url+'~'+name+"/about")
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.find(id="contentMargin")
    data={}
    data["name"] = name
    data["title"] = content.find("h2").text
    
    about_summary = content.find("div", class_="about-summary")

    data["categories"] = []
    for info in about_summary.find("div").find_all("a"):
        data["categories"].append(info.contents[1])

    for info in about_summary.find_all("p"):
        if len(info.contents) > 1 and info.b is not None:
            # индекс определяеться по славарю
            name_data = type_info.get(info.contents[0].text.strip())
            # Если такая инфа зарегистрирована в словаре то записать
            if name_data is not None:
                # у данных все теги удалються и в дату записываеться строка
                info_withaut_tag = list(map(remove_tag, info.contents[1:]))
                data[name_data] = "".join([i.strip() for i in info_withaut_tag])
    
    if data.get("authors_translation") is not None:
        data["type_comic"] = "translation"
    else:
        data["type_comic"] = "original"

    return data

def get_icon(name):
    page = requests.get(url+'~'+name+"/banner")
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.find(id="contentMargin").find(class_="serial-content")
    icons=[]
    for item in content.find_all("p"):
        data = {}
        data["link"] = url + item.find("img").get("src")
        data["size"] = item.find_previous().text
        icons.append(data)
    return icons


def main():
    # comic_data = get_comic("doodle-time")
    # print(json.dumps(comic_data, indent=4))
    baners = get_icon("DarkForestOnline")
    print(baners)


if __name__ == '__main__':
    main()