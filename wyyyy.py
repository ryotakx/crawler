import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml_tools import prettify
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}


def get_url(sid, type='lyric'):
    api = 'https://api.imjad.cn/cloudmusic/?type=' + type + '&id=' + str(sid)
    return api


def usable_url(sid):
    url = get_url(sid, 'album')
    print(url)
    data = requests.get(url, timeout=5, headers=headers)
    if data.status_code == 200:
        dic = data.json()
        if 'uncollected' not in dic.keys():
            print(dic)


usable_url(72316676)