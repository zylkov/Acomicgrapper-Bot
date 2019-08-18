import requests, re, json
from bs4 import BeautifulSoup

class Search:
    _url_site = r"https://acomics.ru/"
    _jar = requests.cookies.RequestsCookieJar()
    _jar.set('ageRestrict', '18', domain='acomics.ru', path='/')

    def __init__(self, page=1, categories=None, ratings=[2,3,4,5]):
        self.page = page
        self.categories = categories
        self.ratings = ratings
    
    def get(self):
        skip = (self.page - 1) * 10
        payload ={'skip':skip, 'categories':self.categories, 'ratings[]':self.ratings}
        page = requests.get(self._url_site+'comics', params=payload, cookies=self._jar)
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

            data_comics.append(data)
        return data_comics

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
    
    def go(self):
        pass

if __name__ == '__main__':
    comic_list = Search(categories= Search.cheack_categories(["животные","игры"]), page=1)
    data = comic_list.get()
    print(json.dumps(data, indent=4))
    print(len(data))