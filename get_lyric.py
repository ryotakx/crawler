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
                with open('lyric1.json', 'r', encoding='utf8') as f:
                    output = json.load(f)
                    output.append(single)
                with open('lyric1.json', 'w', encoding='utf8') as f:
                    json.dump(output, f, indent=4)
            else:
                print('No_lyric_found.')
        else:
            print('error: {0}'.format(url))
    except ConnectionError:
        get_lyric(song_id, song_name, album_id, album_name, aid, name)
    except requests.ConnectTimeout:
        get_lyric(song_id, song_name, album_id, album_name, aid, name)


if __name__ == '__main__':
    songs = open('s_song2.txt', 'r', encoding='utf8').readlines()[:10000]
    for song in songs:
        time.sleep(0.8)
        sid, sname, album_id, album_name, aid, aname = song.strip().split('\t', maxsplit=6)
        get_lyric(sid, sname, album_id, album_name, aid, aname)