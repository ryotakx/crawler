import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml_tools import prettify
import time
import re
import pickle

root_url = "https://www.haodf.com"
target_url = "https://www.haodf.com/jibing/list.htm"
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}


def search_subject_list(url):
    data = requests.get(url, timeout=5, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")
    divs = soup.find_all("div", class_='kstl')
    links = [div.find("a")["href"] for div in divs]
    names = [div.find("a").get_text() for div in divs]
    with open('subject.txt', 'w', encoding='utf8') as f:
        for index, link in enumerate(links):
            f.write(names[index])
            f.write(' ')
            f.write(root_url + link)
            f.write('\n')


# search_subject_list(target_url)

def search_class_list():
    with open('subject.txt', 'r', encoding='utf8') as f:
        for i in f.readlines():
            subject, url = i.split()
            print(subject, url)
            data = requests.get(url, timeout=5, headers=headers)
            soup = BeautifulSoup(data.text, "html.parser")
            try:
                divs = soup.find("div", class_='ksbd').find_all("a")
                links = [div["href"] for div in divs]
                names = [div.get_text() for div in divs]
            except AttributeError:
                links = [url]
                names = [subject]
            with open('class.txt', 'a', encoding='utf8') as f_class:
                for index, link in enumerate(links):
                    f_class.write(subject)
                    f_class.write(' ')
                    f_class.write(names[index])
                    f_class.write(' ')
                    f_class.write(root_url + link)
                    f_class.write('\n')
            time.sleep(2)

# search_class_list()


def search_item_list():
    with open('class.txt', 'r', encoding='utf8') as f:
        for i in f.readlines()[:]:
            subject, class_, url = i.split()
            print(i)
            data = requests.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(data.text, "html.parser")
            divs = soup.find("div", id='el_result_content').find("div", class_='ct').find_all("a")
            links = [div["href"] for div in divs]
            names = [div.get_text() for div in divs]
            with open('item.txt', 'a', encoding='utf8') as f_item:
                for index, link in enumerate(links):
                    f_item.write(subject)
                    f_item.write(' ')
                    f_item.write(class_)
                    f_item.write(' ')
                    f_item.write(names[index])
                    f_item.write(' ')
                    f_item.write(root_url + link)
                    f_item.write('\n')
            time.sleep(2)
# search_item_list()


def search_item():
    root = Element('root')

    with open('item.txt', 'r', encoding='utf8') as f:
        for i in f.readlines()[:10]:
            item = SubElement(root, 'item')
            item_id = SubElement(item, 'id')
            item_title = SubElement(item, 'title')
            item_url = SubElement(item, 'url')
            item_class = SubElement(item, 'class')
            item_subclass = SubElement(item, 'subclass')
            item_description = SubElement(item, 'description')
            item_details = SubElement(item, 'details')

            item_index, subject, class_, disease, url = i.split()
            item_id.text = item_index
            item_title.text = disease
            item_class.text = subject
            item_subclass.text = class_
            print(i)
            url = url[:-4] + '/jieshao.htm'
            item_url.text = url
            data = requests.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(data.text, "html.parser")
            description = soup.find("div", class_='hot_recommend').find("p").get_text()
            item_description.text = description
            clauses = soup.find_all("div", class_='recommend_main')
            for clause in clauses:
                title = clause.h2.string
                content = clause.find("p", class_='js-longcontent')
                content_str = str(content)[48:-4].replace('<br/>', '\n')
                item_detail = SubElement(item_details, 'detail')
                detail_title = SubElement(item_detail, 'detail_title')
                detail_title.text = title
                detail_content = SubElement(item_detail, 'detail_content')
                detail_content.text = content_str
            time.sleep(2)
    with open('hdf.txt', 'w', encoding='utf8') as f:
        f.write(prettify(root))
    tree = ElementTree.ElementTree(root)
    tree.write('hdf.xml', encoding='utf8')


search_item()
