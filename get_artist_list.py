import requests
from bs4 import BeautifulSoup

class ArtistSpider():
    def __init__(self):
        self.headers = {
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

    def get_index(self, url):
        try:
            resp = requests.get(url, timeout=5, headers=self.headers)
            if resp.status_code == 200:
                self.parse_re(resp.text)
            else:
                print('error: {0}'.format(url))
        except ConnectionError:
            self.get_index(url)

    def parse_re(self, resp):
        print('start parse {}'.format(url))
        soup = BeautifulSoup(resp, "html.parser")
        print(soup)
        data = soup.find('div', class_='m-sgerlist').find_all('a', class_='nm nm-icn f-thide s-fc0')
        tag = soup.find('span', class_='f-ff2 d-flag').get_text()
        f = open('s_artist.txt', 'a', encoding='utf-8')
        for p in data:
            aid = p['href'].strip()[11:]
            name = p.get_text()
            f.write(aid + '\t' + name + '\t' + tag)
            f.write('\n')


if __name__ == '__main__':
    # 歌手分类id
    list1 = [1001, 1002, 1003, 2001, 2002, 2003, 6001, 6002, 6003, 7001, 7002, 7003, 4001, 4002, 4003]
    # initial的值
    list2 = [0, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
    for i in list1[:3]:
        url = 'http://music.163.com/#/discover/artist/cat?id=' + str(i) + '&initial=-1'
        print('start spider {}'.format(url))
        ArtistSpider().get_index(url)
