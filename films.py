import pandas
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiogram.utils.markdown as fmt


class Films:
    def __init__(self, df: pandas.DataFrame):
        self.df = df

    @staticmethod
    def from_file(path: str):
        try:
            return Films(pandas.read_csv(path))
        except FileNotFoundError:
            df = pandas.DataFrame({'title': [], 'link': [], 'img_link': [], 'description': []})
            df.to_csv(path, encoding='utf-8', index=False)
            return Films(df)

    def parse(self):
        response = requests.get('https://www.superspisok.ru/filmy-pro-basketbol/',
                                headers={'User-agent': UserAgent().chrome}).content
        soup = BeautifulSoup(response, 'html.parser')
        titles = soup('h3')
        data = soup('p')[3:]
        descriptions = []
        img_links = []
        film_links = []
        for i in range(len(data)):
            if i % 2:
                img_links.append(data[i].img['src'])
            else:
                descriptions.append(data[i].text.strip())
        for i in range(len(titles)):
            film_links.append(titles[i].next_sibling['href'])
            titles[i] = titles[i].text
        self.df = pandas.DataFrame({'title': titles, 'link': film_links, 'img_link': img_links,
                                    'description': descriptions})
        self.df.to_csv('films.csv', encoding='utf-8', index=False)

    @staticmethod
    def beautify(data: pandas.Series):
        return f'{fmt.hide_link(data["img_link"])}' + '<a href="' + data['link'] + '"><b>' + data['title'] +\
               '</b></a>\n\n' + data['description']


films = Films.from_file('films.csv')
# films.parse()
