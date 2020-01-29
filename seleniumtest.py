from selenium import webdriver
import time

url = "https://music.163.com/artist/album?id=122455&limit=1500&offset=7500"
browser = webdriver.Firefox()
browser.get(url)
browser.switch_to.frame('g_iframe')
a = browser.find_elements_by_xpath("//ul[@id='m-song-module']"
                                   "/li/p[@class='dec dec-1 f-thide2 f-pre']"
                                   "/a[@class='tit s-fc0']")
f = open('new_albums.txt', 'a', encoding='utf8')
for i in a:
    aid = i.get_attribute('href')[31:]
    name = i.text
    f.write(aid + '\t' + name + '\t' + '122455\t群星\n')

