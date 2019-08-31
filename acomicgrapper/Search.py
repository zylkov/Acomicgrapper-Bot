import requests, re, json
from bs4 import BeautifulSoup
from Comic import Comic

#https://acomics.ru/comics?categories=12&ratings%5B%5D=2&ratings%5B%5D=3&ratings%5B%5D=4&ratings%5B%5D=5&type=0&updatable=0&issue_count=2&sort=last_update&skip=0
#type - тип комикса
# Значения:
# 0 - все типы
# trans - переведенные
# orig - оригиналы
# updatable - статус
# 0 - все
# no - завершенные
# yes - продолжающие
# issue_count - минимум страниц знач число
# sort - сортировка
# last_update - по дате обновления
# subscr_count - по кол подписчиков
# issue_count - по кол страниц
# serial_name - по алфавиту

class SearchBase:
    _url_site = r"https://acomics.ru/"
    _jar = requests.cookies.RequestsCookieJar()
    _jar.set('ageRestrict', '18', domain='acomics.ru', path='/')

    def get(self):
        pass
    
    def _get_list_link(self, page):
        soup = BeautifulSoup(page.text, 'html.parser')

        # Парсим
        tags = soup.find_all('table', class_='catalog-elem list-loadable')
        data_comics=[]
        for tag in tags:
            data = {}
            comic_tag = tag.contents[1]

            image_tag = comic_tag.find('td', class_='catdata1')
            data['icon'] = self._url_site + image_tag.img.get('src')

            info_tag = comic_tag.find('td', class_='catdata2')
            data['title'] = info_tag.a.text
            data['link'] = info_tag.a.get('href')
            data['name'] = data['link'][20:]
            data['about'] = info_tag.find('div', class_='about').text
            data['rating'] = info_tag.find('a', href="/rating").text

            add_info_tag = comic_tag.find('td', class_='catdata3')
            data['total'] = add_info_tag.find('span', class_='total').text.split(" ")[0]
            data['status'] = add_info_tag.find_all('span')[2].text  # Уверен что сломаеться

            data['subscribe'] = comic_tag.find('td', class_='catdata4').span.text

            data_comics.append(LinkComic(data['link'],data))
        return data_comics


class SearchWord(SearchBase):

    def __init__(self, keyword):
        SearchBase.__init__(self)
        self.keyword = keyword

    def get(self):
        payload ={ 
            "keyword":self.keyword}
        page = requests.get(self._url_site+'search', params=payload, cookies=self._jar)
        return SearchBase._get_list_link(self, page)

class SearchCat(SearchBase):

    def __init__(self, page=1, categories=None, ratings=[2,3,4,5], comic_type=0, updatable=0, issue_count=2, comic_sort="last_update"):
        SearchBase.__init__(self)
        self.page = page
        self.categories = categories
        self.ratings = ratings
        self.comic_type = comic_type
        self.updatable = updatable
        self.issue_count = issue_count
        self.comic_sort = comic_sort

    
    def get(self):
        skip = (self.page - 1) * 10
        payload ={
            'skip':skip, 
            'categories':self.categories, 
            'ratings[]':self.ratings, 
            'type':self.comic_type,
            'updatable':self.updatable,
            'issue_count':self.issue_count,
            'sort':self.comic_sort}
        page = requests.get(self._url_site+'comics', params=payload, cookies=self._jar)
        return SearchBase._get_list_link(self, page)

    # Проверка перменной категории
    @staticmethod
    def cheack_categories(categories):
        categories_name ={'животные': 1,
                      'furry': 1,
                      'драма': 2,
                      'drama': 2,
                      'фэнтези': 3,
                      'fantasy': 3,
                      'игры': 4,
                      'games': 4,
                      'юмор': 5,
                      'humor': 5,
                      'журнал': 6,
                      'magazine': 6,
                      'паранормальное': 7,
                      'supernatural': 7,
                      'конец света': 8,
                      'post apocalypse': 8,
                      'романтика': 9,
                      'romance': 9,
                      'фантастика': 10,
                      'fantastic': 10,
                      'бытовое': 11,
                      'domestic': 11, # не уверен что правильно так надо называть
                      'стимпанк': 12,
                      'steampunk': 12,
                      'супергерои': 13,
                      'superheroes': 13}

        if categories is None:
            return None
        elif type(categories) is int:
            if categories > 0 and categories < 14:
                return categories
            else:
                print("categories Error value. Нет такой категории.",categories)
                return None
        elif type(categories) is str:
            categories.lower()
            try:
                return categories_name[categories]
            except KeyError:
                print('categories Error value. Нет такой категории',categories)
                return None
        elif type(categories) is list:
            for i in range(len(categories)):
                if type(categories[i]) is int:
                    if categories[i] > 0 and categories[i] < 7:
                        pass
                    else:
                        print('categories Error value. Нет такой категории',categories[i])
                        categories[i] = None
                elif type(categories[i]) is str:
                    categories[i].lower()
                    try:
                        categories[i] = categories_name[categories[i]]
                    except KeyError:
                        print('categories Error value. Нет такой категории', categories[i])
                        categories[i] = None
                else:
                    print('categories Error value. Неизвестный тип данных ', categories[i])
                    categories[i] = None
            categories = list(set(categories))
            return ','.join([str(i) for i in categories if i is not None])
        else:
            print('categories Error value. Неизвестный тип данных categories', categories)
            return None

    @staticmethod
    def cheack_ratings(ratings):
        ratings_name ={
            'nr': 1,
            'g': 2,
            'pg': 3,
            'pg-13': 4,
            'r': 5,
            'nc-17': 6
        }
        if ratings is None:
            return None
        elif type(ratings) is int:
            if ratings > 0 and ratings < 7:
                return ratings
            else:
                print("ratings Error value. Нет такого рейтинга.",ratings)
                return None
        elif type(ratings) is str:
            ratings.lower()
            try:
                return ratings_name[ratings]
            except KeyError:
                print('ratings Error value. Нет такого рейтинга ratings',ratings)
                return None
        elif type(ratings) is list:
            for i in range(len(ratings)):
                if type(ratings[i]) is int:
                    if ratings[i] > 0 and ratings[i] < 7:
                        pass
                    else:
                        print('ratings Error value. Нет такого рейтинга ratings',ratings[i])
                        ratings[i] = None
                elif type(ratings[i]) is str:
                    ratings[i].lower()
                    try:
                        ratings[i] = ratings_name[ratings[i]]
                    except KeyError:
                        print('ratings Error value. Нет такого рейтинга ratings', ratings[i])
                        ratings[i] = None
                else:
                    print('ratings Error value. Неизвестный тип данных ratings', ratings[i])
                    ratings[i] = None
            return list(set(ratings))
        else:
            print('ratings Error value. Неизвестный тип данных ratings', ratings)
            return None

class LinkComic:
    def __init__(self, link, info):
        self.link = link
        self.info = info
    
    def open(self):
        name = self.link[self.link.rfind('~')+1:]
        return Comic(name)


def main():
    test_search_catigoris()


def test_search_key():
    comic_list = SearchWord("игра")
    data = comic_list.get()
    data_info = [i.info for i in data]
    print(json.dumps(data_info, indent=4))
    print(len(data))

def test_search_catigoris():
    comic_list = SearchCat(categories= SearchCat.cheack_categories(["животные","игры"]), page=1, comic_type="trans", comic_sort="serial_name")
    data = comic_list.get()
    data_info = [i.info for i in data]
    print(json.dumps(data_info, indent=4))
    #print([i.info for i in data])
    print(len(data))
    comic = data[0].open()
    print(comic.info)

if __name__ == '__main__':
    main()