import asyncio
import aiohttp
import time
import random
import json
from proxy_pool import get_proxy, delete_proxy, get_proxy_num

start = time.time()


async def fetch(session, url):
    try:
        async with session.get(url, timeout=20) as response:
            if response.status == 200:
                return await response.json()
            else:
                print('status code error')
                return None
    except Exception:
        print('time out error')
        return None


async def request(song_id, song_name, album_id, album_name, aid, name, output_file):
    async with aiohttp.ClientSession() as session:
        retry_time = 20
        proxy = get_proxy().get("proxy")
        result = None
        while retry_time > 0 and not result:
            url = 'http://localhost:3000/lyric?id=' + song_id + "&proxy=http://" + proxy
            print('start parse {}'.format(url))
            result = await fetch(session, url)
            if not result:
                retry_time -= 1
        if not result:
            delete_proxy(proxy)
            await request(song_id, song_name, album_id, album_name, aid, name, output_file)

        if result and 'lrc' in result.keys() and 'lyric' in result['lrc'].keys() and result['lrc']['lyric']:
            print('found lyric! {0} proxy remain'.format(get_proxy_num()))
            lyric = result['lrc']['lyric']
            single = dict()
            single['song_id'] = song_id
            single['song_name'] = song_name
            single['album_id'] = album_id
            single['album_name'] = album_name
            single['artist_id'] = aid
            single['artist_name'] = name
            single['lyric'] = lyric
            with open(output_file, 'r+', encoding='utf8') as f1:
                output = json.load(f1)
                output.append(single)
                f1.seek(0)
                json.dump(output, f1, ensure_ascii=False, indent=4)
        else:
            print('No lyric found.')


def request_by_range(song_list, min_index, max_index, output_file):
    tasks = []
    for song_index in range(min_index, max_index):
        sid, sname, album_id, album_name, aid, aname = song_list[song_index].strip().split('\t', maxsplit=6)
        print('Prepare Index: {0}'.format(song_index))
        tasks.append(asyncio.ensure_future(request(sid, sname, album_id, album_name, aid, aname, output_file)))
    return tasks


def run_task(song_list, min_index, max_index, output_file):
    tasks = request_by_range(song_list, min_index, max_index, output_file)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    songs2 = open('s_song2.txt', 'r', encoding='utf8').readlines()

    run_task(songs2, 124000, 124144, 'lyric_part13.json')

    # for i in range(0, 8):
    #     start2 = time.time()
    #     run_task(songs2, 120000 + 500 * i, 120500 + 500 * i, 'lyric_part13.json')
    #     print('Cost time:', time.time() - start2)
    #     for j in range(20):
    #         print(str(i) + 'sleep: ' + str(j))
    #         time.sleep(1)

    end = time.time()
    print('Cost time:', end - start)
