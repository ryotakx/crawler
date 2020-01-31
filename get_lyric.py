import requests
import json
import time


def get_lyric(song_id, song_name, album_id, album_name, aid, name):
    url = 'http://localhost:3000/lyric?id=' + song_id
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
                single['album_id'] = album_id
                single['album_name'] = album_name
                single['artist_id'] = aid
                single['artist_name'] = name
                single['lyric'] = lyric
                return single
            else:
                print('No_lyric_found.')
                return None
        else:
            print('error: {0}'.format(url))
            return None
    except ConnectionError:
        get_lyric(song_id, song_name, album_id, album_name, aid, name)
    except requests.ConnectTimeout:
        get_lyric(song_id, song_name, album_id, album_name, aid, name)


def get_lyric_by_range(song_list, min_index, max_index, output_file):
    output_list = []
    start = time.time()
    with open(output_file, 'w', encoding='utf8') as f_out:
        json.dump([], f_out, ensure_ascii=False, indent=4)
    for song_index in range(min_index, max_index):
        sid, sname, album_id, album_name, aid, aname = song_list[song_index].strip().split('\t', maxsplit=6)
        print('Index: {0}, {1} of 10'.format(song_index, len(output_list) + 1))
        single = get_lyric(sid, sname, album_id, album_name, aid, aname)
        if single:
            output_list.append(single)
        if len(output_list) >= 10:
            print('<-- Write into file -->')
            with open(output_file, 'r+', encoding='utf8') as f1:
                output = json.load(f1)
                output.extend(output_list)
                f1.seek(0)
                json.dump(output, f1, ensure_ascii=False, indent=4)
            output_list.clear()
            print('Cost time: {0}'.format(time.time() - start))
            start = time.time()
    with open(output_file, 'r+', encoding='utf8') as f2:
        output = json.load(f2)
        output.extend(output_list)
        f2.seek(0)
        json.dump(output, f2, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    songs2 = open('s_song2.txt', 'r', encoding='utf8').readlines()
    get_lyric_by_range(songs2, 30000, 40000, 'lyric_part4.json')
    get_lyric_by_range(songs2, 40000, 50000, 'lyric_part5.json')
