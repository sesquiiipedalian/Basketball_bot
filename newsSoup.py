import pandas
from bs4 import BeautifulSoup
import requests
import aiogram.utils.markdown as fmt


class newsDF:
    def __init__(self, df: pandas.DataFrame):
        self.df = df

    @staticmethod
    def from_file(path: str):
        try:
            return newsDF(pandas.read_csv(path))
        except FileNotFoundError:
            df = pandas.DataFrame({'title': [], 'link': [], 'img_link': [], 'description': []})
            df.to_csv(path, encoding='utf-8', index=False)
            return newsDF(df)

    @staticmethod
    def empty_get():
        df = pandas.DataFrame({'title': [], 'link': [], 'img_link': [], 'description': []})
        return df

    def update(self):
        print('Updating')
        response = requests.get('https://allbasketball.org/news/')
        soup = BeautifulSoup(response.content, 'html.parser')
        news = soup('div', 'post-item-wrapper mt-3')
        df = newsDF.empty_get()
        for i in range(len(news) - 1, -1, -1):
            link = news[i].a['href']
            title = news[i]('a')[1].text.strip()
            img_link = 'https://allbasketball.org' + news[i].a.img['data-src']
            decription = news[i]('div', 'post-text')[0].text.strip()
            if self.df[self.df.link == link].empty:
                df = df.append({'title': title, 'link': link, 'img_link': img_link, 'description': decription},
                               ignore_index=True)
        self.df = pandas.concat([self.df, df])
        self.df.to_csv('news.csv', encoding='utf-8', index=False)
        return df

    @staticmethod
    def beautify(data: pandas.Series):
        return f'{fmt.hide_link(data["img_link"])}' + '<a href="' + data['link'] + '"><b>' + data['title'] +\
               '</b></a>\n\n' + data['description']


news = newsDF.from_file('news.csv')
