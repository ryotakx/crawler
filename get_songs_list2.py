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


def get_index(url, album_id, album_name, artist_id, artist_name):
    try:
        resp = requests.get(url, timeout=15, headers=headers)
        if resp.status_code == 200:
            print('start parse {}'.format(url))
            result = resp.json()
            if 'uncollected' not in result.keys() and 'songs' in result.keys():
                print(len(result['songs']))
                f_song = open('s_song2.txt', 'a', encoding='utf8')
                for song in result['songs']:
                    song_id = str(song['id'])
                    song_name = str(song['name'])
                    f_song.write(song_id + '\t' + song_name + '\t' + album_id + '\t' +
                                 album_name + '\t' + artist_id + '\t' + artist_name)
                    f_song.write('\n')
        else:
            print('error: {0}'.format(url))
    except ConnectionError:
        get_index(url, album_id, album_name, artist_id, artist_name)


if __name__ == '__main__':
    start = time.time()
    albums = open('s_albums.txt', 'r', encoding='utf8').readlines()[5177:]
    for album in albums:
        print(album)
        album_id, album_name, artist_id, artist_name = album.strip().split('\t', maxsplit=4)
        url = "http://localhost:3000/album?id=" + album_id
        get_index(url, album_id, album_name, artist_id, artist_name)
        time.sleep(1)
    end = time.time()
    print('Cost time:', end - start)
