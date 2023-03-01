#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import abc
import logging
import requests
from urllib import parse
from typing import Optional
from bs4 import BeautifulSoup

class LiveSpider(object):
    default_spider = 'foodieguide'
    page = None
    def __init__(self, spider = None) -> None:
        spiderclass = str.capitalize(spider or self.default_spider) + 'Spider'
        self.spider: Spider = globals()[spiderclass]()
        self.logger = logging.getLogger(__name__)
    def set_page(self, page):
        self.page = page
    def search(self, channel: str):
        return self.spider.search(channel).limit_page(self.page).run()

    
class Spider(metaclass = abc.ABCMeta):
    url = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    def request(self, url: str) -> requests.Response:
        self.logger.warning('正在抓取页面链接：' + url)
        response = requests.get(url, headers=self.headers)
        response.encoding = response.apparent_encoding
        return response
    def search(self, keyword):
        self.search_keyword = keyword
        return self
    def limit_page(self, page = None):
        self.page = page
        return self
    def request_live_data(self, url, params: Optional[dict|str] = ''):
        if isinstance(params, dict):
            params = '?' + parse.unquote(parse.urlencode(params))
        return BeautifulSoup(self.request(url+params).text, 'html.parser')
    @abc.abstractmethod
    def paser_live_data(self, soup):
        pass
    @abc.abstractmethod
    def run(sefl):
        pass

class FoodieguideSpider(Spider):
    url = f'https://www.foodieguide.com/iptvsearch/'
    def __init__(self, search = None, page = None) -> None:
        self.search_keyword = search
        self.page = page
        self.logger = logging.getLogger(__name__)
    def paser_live_data(self, soup):
        tr_tags = soup.find_all('tr')
        result=[]
        for tr_tag in tr_tags:
            td_tags = tr_tag.find_all('td')
            if len(td_tags)>=3:
                channel = re.search(r'\w+', td_tags[0].text)
                checked = re.search(r'\d{2}-\d{2}-\d{4}', td_tags[0].text)
                live_url = td_tags[2].text
                live_data = {'search':self.search_keyword, 'channel': channel.group(), 'checked': checked.group(), 'url': live_url, 'respone_time': None}
                self.logger.info(live_data)
                result.append(live_data)
        return result
    def run(self):
        data = []
        curr_page = 1
        def get_data(data, page):
            params = f'?s={self.search_keyword}&page={page}'
            soup = self.request_live_data(self.url, params)
            return data + self.paser_live_data(soup), soup
        data,soup = get_data(data, curr_page)
        last_page = soup.select_one('div[style="display:flex;justify-content:center;"]>a:last-of-type')
        if last_page is None:
            return data
        max_page = self.page or re.search(r'\d+', last_page.attrs['href']).group()
        for page in range(2, int(max_page) + 1):
            curr_page = page
            data,soup = get_data(data, curr_page)
        return data

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(thread)d %(levelname)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
    data = LiveSpider().search("广东")
    print(data)