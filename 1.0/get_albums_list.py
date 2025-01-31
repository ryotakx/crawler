import requests
import time
from bs4 import BeautifulSoup


headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.181 Safari/537.36'
        }


def get_index(url, name, aid):
    try:
        resp = requests.get(url, timeout=5, headers=headers)
        if resp.status_code == 200:
            print('start parse {}'.format(url))
            soup = BeautifulSoup(resp.text, "html.parser")
            data = soup.find_all('a', class_='tit s-fc0')
            print(len(data))
            for p in data:
                album_id = p['href'][10:]
                album_name = p.get_text()
                f.write(album_id + '\t' + album_name + '\t' + aid + '\t' + name)
                f.write('\n')
        else:
            print('error: {0}'.format(url))
    except ConnectionError:
        get_index(url, name, aid)


if __name__ == '__main__':
    artists = open('s_artist.txt', 'r', encoding='utf8').readlines()[100:]
    f = open('s_albums.txt', 'a', encoding='utf-8')
    for arti in artists:
        aid, name = arti.strip().split('\t', maxsplit=2)
        url = "https://music.163.com/artist/album?id=" + aid + "&limit=150&offset=0"
        get_index(url, name, aid)
        time.sleep(4)


