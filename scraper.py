from bs4 import BeautifulSoup
import requests
import csv


sources = ['this-season', 'next-season']
for source in sources:
    source = requests.get('https://anilist.co/search/anime/' + source).text
    soup = BeautifulSoup(source, 'lxml')


def anime_list():
    file_list = []
    post_list = []
    post_url_list = []
    img_url_list = []
    with open('posted_titles.txt') as f:
        file_list = f.readlines()
    for card in soup.find_all('div', class_='media-card'):
        title = card.find('a', class_='title').text
        post_url = card.find('a', class_='title')['href']
        post_url = 'https://anilist.co'+ post_url
        title = title[1:-1]
        img_url = card.img['src']
        if title+'\n' not in file_list:
            post_list.append(title)
            img_url_list.append(img_url)
            post_url_list.append(post_url)
            # with open('posted_titles.txt', 'a') as f:
            #     f.write(title+'\n')
    return post_list, img_url_list, post_url_list


def save_file(title):
    with open('posted_titles.txt', 'a') as f:
        f.write(title+'\n')


def get_airing_date(post_url):
    # self.post_url = post_url
    try:
        source = requests.get(post_url).text
        soup = BeautifulSoup(source, 'lxml')
        card = soup.find('div', class_='countdown value')
        v = card.text.replace(' ','').replace('\n', '').replace(':',' airing in ').lstrip()
    except Exception as e:
        v = ''

    return v