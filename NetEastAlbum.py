import requests
from bs4 import BeautifulSoup
import time
import os

from selenium import webdriver  # 导入Selenium的webdriver


class GetPic():

    def __init__(self, url, path):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        self.url = url
        self.path = path

    def scroll_down(self, driver, times):
        for i in range(times):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(10)

    def letsgo(self):
        driver = webdriver.PhantomJS()
        driver.get(self.url)
        driver.switch_to.frame('g_iframe')
        html = driver.page_source
        self.make_dir(self.path)
        os.chdir(self.path)
        all_pic = BeautifulSoup(html, 'lxml').find('ul', id='m-song-module').find_all('li')

        for pic in all_pic:
            img = pic.find('img')['src']
            name = pic.find('p')['title']
            time = pic.find('span', class_='s-fc3').get_text()
            img_url = img[:img.index('?')]
            pic_name = name + time + '.jpg'
            self.save_img(img_url, pic_name)
            print('yes')

    def make_dir(self, path):
        path = path.strip()
        if os.path.exists(path):
            return False
        else:
            os.makedirs(path)
            return True

    def request(self, url):
        return requests.get(url)

    def save_img(self, url, name):
        img = self.request(url)
        f = open(name, 'ab')
        f.write(img.content)
        f.close()

zhangyu = GetPic('https://music.163.com/#/artist/album?id=12107534&limit=120&offset=0','D:\python\pic')
zhangyu.letsgo()