import asyncio
import aiohttp
import time
import json
from bs4 import BeautifulSoup
from aiomultiprocess import Pool

headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'api.imjad.cn',
            'Referer': 'https://api.imjad.cn/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.181 Safari/537.36'
        }

async def get(url, album_id, album_name, artist_id, artist_name):
    session = aiohttp.ClientSession()

    try:
        resp = await session.get(url, timeout=5, headers=headers, allow_redirects=True)
        if resp.status == 200:
            print('start parse {}'.format(url))
            result = await resp.json()
            if 'uncollected' not in result.keys() and 'songs' in result.keys():
                print(len(result['songs']))
                f = open('song.txt', 'a', encoding='utf8')
                for song in result['songs']:
                    song_id = str(song['id'])
                    song_name = str(song['name'])
                    f.write(song_id + '\t' + song_name + '\t' + album_id + '\t' +
                            album_name + '\t' + artist_id + '\t' + artist_name)
                    f.write('\n')
        else:
            await get(url, album_id, album_name, artist_id, artist_name)
    except ConnectionError:
        await get(url, album_id, album_name, artist_id, artist_name)
    except asyncio.TimeoutError:
        await get(url, album_id, album_name, artist_id, artist_name)
    except aiohttp.ClientConnectorError:
        await get(url, album_id, album_name, artist_id, artist_name)
    await session.close()

async def request():
    albums = open('albums.txt', 'r', encoding='utf8').readlines()[0:10000]
    args = []
    for album in albums:
        print(album)
        album_id, album_name, artist_id, artist_name = album.strip().split('\t', maxsplit=4)
        url = get_url(album_id, 'album')
        args.append((url, album_id, album_name, artist_id, artist_name))
    async with Pool() as pool:
        await pool.starmap(get, args)

def get_url(sid, url_type='lyric'):
    api = 'https://api.imjad.cn/cloudmusic/?type=' + url_type + '&id=' + str(sid)
    return api


if __name__ == '__main__':
    start = time.time()
    coroutine = request()
    task = asyncio.ensure_future(coroutine)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)

    end = time.time()
    print('Cost time:', end - start)
