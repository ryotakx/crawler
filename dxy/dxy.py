import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml_tools import prettify
import time

root_url = "https://dxy.com/diseases/buxian/?page="
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

def search_disease_list_by_pages(page):
    url = root_url + str(page)
    print(url)
    data = requests.get(url, timeout=10, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")
    links = soup.find('div', class_='lr-container-left').find_all('a', class_='disease-card-info-title has-url')
    with open('item.txt', 'a+', encoding='utf8') as f:
        for index, link in enumerate(links):
            # id = str((page - 1) * 10 + index)
            # f.write(id)
            # f.write(' ')
            f.write(link.get_text())
            f.write(' ')
            f.write(link['href'])
            f.write('\n')

    time.sleep(8)


# for i in range(1, 176):
#     search_disease_list_by_pages(i)


def search_item():
    root = Element('root')

    with open('item.txt', 'r', encoding='utf8') as f:
        for i in f.readlines()[:200]:
            item = SubElement(root, 'item')
            item_id = SubElement(item, 'id')
            item_title = SubElement(item, 'title')
            item_url = SubElement(item, 'url')
            item_class = SubElement(item, 'class')
            item_description = SubElement(item, 'description')
            item_details = SubElement(item, 'details')

            item_index, disease, url = i.split(maxsplit=3)
            print(i)
            item_id.text = item_index
            item_title.text = disease
            item_url.text = url
            data = requests.get(url, timeout=9, headers=headers)
            soup = BeautifulSoup(data.text, "html.parser")
            try:
                class_ = soup.find('div', class_='bread-crumb').find_all('li', class_='bread-crumb-nav-item')[2].find('a').get_text()
                item_class.text = class_
            except AttributeError:
                item_class.text = ''
            description = soup.find("div", class_='disease-card-info-content').get_text()
            item_description.text = description
            clauses = soup.find_all("div", class_='disease-detail-card')
            for clause in clauses:
                title = clause.h3.string
                content = clause.find("div", class_='disease-detail-card-deatil').get_text()
                item_detail = SubElement(item_details, 'detail')
                detail_title = SubElement(item_detail, 'detail_title')
                detail_title.text = title
                detail_content = SubElement(item_detail, 'detail_content')
                detail_content.text = content
            time.sleep(10)
            with open('dxy.xml', 'a+', encoding='utf8') as file:
                file.write(prettify(item))
            # with open('dxy.txt', 'a+', encoding='utf8') as f:
            #     f.write(prettify(root))

            # tree = ElementTree.ElementTree(root)
            # tree.write('dxy.xml', encoding='utf8')


search_item()



