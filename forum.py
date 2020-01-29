import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml_tools import prettify
import time

url = 'http://neuro.dxy.cn/bbs/board/46'
