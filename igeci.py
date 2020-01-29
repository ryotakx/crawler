import requests
from bs4 import BeautifulSoup
from testaio import headers
from selenium import webdriver
import time


def get_artist_list():
    url = 'http://www.igeci.cn/geshou/'
    resp = requests.get(url, timeout=5, headers=headers, allow_redirects=True)
    data = BeautifulSoup(resp.text, 'html.parser')
    result = data.find_all('ul', class_='lyric-star')
    print(data)

def get_artist_list_selenium():
    url = "http://www.igeci.cn/geshou/"
    browser = webdriver.Firefox()
    browser.get(url)
    a = browser.find_elements_by_xpath("//ul[@class='lyric-star']/li/a")
    f = open('igeci_artist.txt', 'a', encoding='utf8')
    for i in a:
        link = i.get_attribute('href')
        name = i.text
        f.write(link + '\t' + name + '\n')

def get_song_list_selenium(url, artist):
    for page in range(1, 21):
        time.sleep(3)
        link = url + 'geci_' + str(page)
        browser = webdriver.Firefox()
        browser.get(link)
        a = browser.find_elements_by_xpath("//ul[@class='lyric-list']/li/a")
        f = open('igeci_song.txt', 'a', encoding='utf8')
        for i in a:
            slink = i.get_attribute('href')
            name = i.get_attribute('title').split()[0]
            f.write(slink + '\t' + name + '\t' + artist + '\n')


if __name__ == '__main__':
    lines = open('igeci_artist.txt', 'r').readlines()[:1]
    for line in lines:
        url, artist = line.strip().split('\t')
        get_song_list_selenium(url, artist)

