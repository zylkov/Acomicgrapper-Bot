import requests, re, json
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

class CraperPage:
    _url_site = r"https://acomics.ru/"
    _jar = requests.cookies.RequestsCookieJar()
    _jar.set('ageRestrict', '18', domain='acomics.ru', path='/')

    def __init__(self, name):
        self.name = name

    def _get_soup(self, prefix):
        page = requests.get(self._url_site + '~' + self.name + prefix, cookies=self._jar)
        return BeautifulSoup(page.text, 'html.parser')

class Comic(CraperPage):
    _type_info = {
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
    
    def __init__(self, name):
        CraperPage.__init__(self, name)
        self.info = self._get_info()
        self.icons = self._get_icon()
    

    def _remove_tag(self, select):
        if select.name is not None: 
            return select.text
        return select
    
    def _get_info(self):
        soup = self._get_soup("/about")
        content = soup.find(id="contentMargin")
        data={}
        data["name"] = self.name
        data["title"] = content.find("h2").text
        
        about_summary = content.find("div", class_="about-summary")

        data["categories"] = []
        for info in about_summary.find("div").find_all("a"):
            data["categories"].append(info.contents[1])

        for info in about_summary.find_all("p"):
            if len(info.contents) > 1 and info.b is not None:
                # индекс определяеться по славарю
                name_data = self._type_info.get(info.contents[0].text.strip())
                # Если такая инфа зарегистрирована в словаре то записать
                if name_data is not None:
                    # у данных все теги удалються и в дату записываеться строка
                    info_withaut_tag = list(map(self._remove_tag, info.contents[1:]))
                    data[name_data] = "".join([i.strip() for i in info_withaut_tag])
        
        if data.get("authors_translation") is not None:
            data["type_comic"] = "translation"
        else:
            data["type_comic"] = "original"

        return data
    
    def _get_icon(self):
        soup = self._get_soup("/banner")
        content = soup.find(id="contentMargin").find(class_="serial-content")
        icons=[]
        for item in content.find_all("p"):
            data = {}
            data["link"] = self._url_site + item.find("img").get("src")
            data["size"] = item.find_previous().text
            icons.append(data)
        return icons
    
    def get_page(self, number_page):
        return Page(self.name, number_page)


class Page(CraperPage):
    
    def __init__(self, name, page):
        CraperPage.__init__(self, name)
        self.page = page
        self.src = self._get_page()

    def _get_soup(self):
        return CraperPage._get_soup(self, "/" + str(self.page))
    
    def _get_page(self):
        soup = self._get_soup()
        return self._url_site + soup.find("img", id="mainImage").get("src")
    
    def get_info(self):
        soup = self._get_soup()
        content = soup.find(id="content")
        data={}
        upper_content = content.find("div", class_="serial-nomargin")
        data["title"] = upper_content.find("img", id="mainImage").get("alt")
        data["image"] = self._url_site + upper_content.find("img", id="mainImage").get("src")
        
        add_info = soup.find(id="contentMargin").find("article", class_="authors")
        data["author"] = add_info.find("a", class_="username").text
        data["author_url"] = self._url_site + add_info.find("a", class_="username").get("href")
        data["page_url"] = self._url_site+'~'+self.name+"/"+ str(self.page)
        return data
    

def main():
    comic = Comic("Prophecy")
    # print(json.dumps(comic.get_info(), indent=4))
    print(comic.info)
    print(comic.get_page(3).src)

if __name__ == '__main__':
    main()