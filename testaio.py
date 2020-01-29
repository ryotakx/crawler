import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from aiomultiprocess import Pool

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

async def get(url, name, aid):
    session = aiohttp.ClientSession()

    try:
        resp = await session.get(url, timeout=5, headers=headers)
        print('start parse {}'.format(url))
        result = await resp.text()
        soup = BeautifulSoup(result, "html.parser")
        data = soup.find_all('a', class_='tit s-fc0')
        print(len(data))
        if soup.find_all('div', class_='u-page'):
            exception = open('exception2.txt', 'a', encoding='utf-8')
            exception.write(aid + '\t' + name)
            exception.write('\n')

        elif len(data) == 0:
            exception = open('exception.txt', 'a', encoding='utf-8')
            exception.write(aid + '\t' + name)
            exception.write('\n')

        else:
            f = open('albums.txt', 'a', encoding='utf-8')
            for p in data:
                album_id = p['href'][10:]
                album_name = p.get_text()
                f.write(album_id + '\t' + album_name + '\t' + aid + '\t' + name)
                f.write('\n')
    except ConnectionError:
        await get(url, name, aid)
    except asyncio.TimeoutError:
        await get(url, name, aid)
    except aiohttp.ClientConnectorError:
        await get(url, name, aid)

    await session.close()

async def request():

    artists = open('artists.txt', 'r', encoding='utf8').readlines()
    args = []
    for arti in artists:
        print(arti)
        aid, name, tag = arti.split('\t', maxsplit=3)
        url = "https://music.163.com/artist/album?id=" + aid + "&limit=150&offset=0"
        args.append((url, name, aid))
    async with Pool() as pool:
        await pool.starmap(get, args)


if __name__ == '__main__':
    start = time.time()
    coroutine = request()
    task = asyncio.ensure_future(coroutine)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)

    end = time.time()
    print('Cost time:', end - start)