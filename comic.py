import requests, re, json
from bs4 import BeautifulSoup

url=r"https://acomics.ru/"

def get_comic(name):
    page = requests.get(url+'~'+name+"/about")
    soup = BeautifulSoup(page.text, 'html.parser')
    print(page)

def main():
    get_comic("randowis")


if __name__ == '__main__':
    main()