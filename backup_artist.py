import requests
from bs4 import BeautifulSoup
from testaio import headers
from selenium import webdriver
import time
import json

def get_artist_list_selenium():
    url = "https://music.163.com/#/discover/artist/cat?id=1003&initial=-1"
    browser = webdriver.Firefox()
    browser.get(url)
    browser.switch_to.frame('g_iframe')
    a = browser.find_elements_by_xpath("//ul[@id='m-artist-box']/li/a[@class='nm nm-icn f-thide s-fc0']")
    b = browser.find_elements_by_xpath("//ul[@id='m-artist-box']/li/p"
                                       "/a[@class='nm nm-icn f-thide s-fc0']")

    f = open('s_artist.txt', 'a', encoding='utf8')
    for i in (a + b):
        link = i.get_attribute('href').strip()[32:]
        name = i.text
        f.write(link + '\t' + name + '\n')

def get_50_songs_selenium(aid, name):
    url = 'https://music.163.com/#/artist?id=' + aid
    browser = webdriver.Firefox()
    browser.get(url)
    browser.switch_to.frame('g_iframe')
    a = browser.find_elements_by_xpath("//table[@class='m-table m-table-1 m-table-4']"
                                       "/tbody/tr/td/div[@class='f-cb']/div/div/span/a")
    b = browser.find_elements_by_xpath("//table[@class='m-table m-table-1 m-table-4']"
                                       "/tbody/tr/td/div[@class='f-cb']/div/div/span/a/b")
    f = open('s_song.txt', 'a', encoding='utf8')
    for i in range(len(a)):
        link = a[i].get_attribute('href')[30:]
        song = b[i].get_attribute('title')
        f.write(link + '\t' + song + '\t' + aid + '\t' + name + '\n')

def get_50_songs(aid, name):
    url = 'http://api.imjad.cn/cloudmusic/?type=artist&id=' + aid
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            result = resp.json()
            print('start parse {}'.format(url))
            f = open('s_song.txt', 'a', encoding='utf8')
            for song in result['hotSongs']:
                song_id = str(song['id'])
                song_name = str(song['name'])
                f.write(song_id + '\t' + song_name + '\t' + aid + '\t' +
                        name)
                f.write('\n')
        else:
            print('error: {0}'.format(url))
    except ConnectionError:
        get_50_songs(aid, name)

def get_lyric(song_id, song_name, aid, name):
    url = 'http://api.imjad.cn/cloudmusic/?type=lyric&id=' + song_id
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            result = resp.json()
            print('start parse {}'.format(url))
            if 'lrc' in result.keys() and 'lyric' in result['lrc'].keys() and result['lrc']['lyric']:
                lyric = result['lrc']['lyric']
                single = dict()
                single['song_id'] = song_id
                single['song_name'] = song_name
                single['artist_id'] = aid
                single['artist_name'] = name
                single['lyric'] = lyric
                with open('lyric3.json', 'r', encoding='utf8') as f:
                    output = json.load(f)
                    output.append(single)
                with open('lyric3.json', 'w', encoding='utf8') as f:
                    json.dump(output, f, indent=4)
            else:
                print('No_lyric_found.')
        else:
            print('error: {0}'.format(url))
    except ConnectionError:
        get_lyric(song_id, song_name, aid, name)
    except requests.ConnectTimeout:
        get_lyric(song_id, song_name, aid, name)


if __name__ == '__main__':
    # get_artist_list_selenium()

    # artists = open('s_artist.txt', 'r', encoding='utf8').readlines()
    # for arti in artists:
    #     time.sleep(2)
    #     aid, name = arti.strip().split('\t', maxsplit=2)
    #     get_50_songs(aid, name)

    songs = open('s_song.txt', 'r', encoding='utf8').readlines()[8500:]
    for song in songs:
        time.sleep(1)
        sid, sname, aid, aname = song.strip().split('\t', maxsplit=4)
        get_lyric(sid, sname, aid, aname)

    # get_lyric('1407358755', '好想爱这个世界啊', '861777', '华晨宇')


