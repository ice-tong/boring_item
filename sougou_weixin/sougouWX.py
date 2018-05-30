# -*- coding: utf-8 -*-
"""
Created on Wed May 30 18:10:01 2018

@author: icetong
"""

import requests, re, time, datetime
from bs4 import BeautifulSoup as BS

class API(object):
    
    query_url = 'http://weixin.sogou.com/weixin'
    params = {
        'type': '1',
        's_from': 'input',
        'query': '库客音乐',
        'ie': 'utf8',
        '_sug_': 'n',
        '_sug_type_': ''} 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple\
           WebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    mp_url = 'https://mp.weixin.qq.com/'
    
    def __init__(self, key_word='库客音乐'):
        self.key_word = key_word
        self.params['query'] = self.key_word
        self.msg_list = list()
        
    def _get_datetime(self, ts):
        d = datetime.datetime.fromtimestamp(int(ts))
        s = '{}年{}月{}日'.format(d.year, d.month, d.day)
        return s

    def _get_response(self, url, params=dict(), 
                      recu_num=0, recu_max=3) -> requests.models.Response:
        try:
            r = requests.get(url, params=params, timeout=5,
                         headers=self.headers, verify=False)
        except:
            if recu_num >= recu_max:
                r = None
            else:
                recu_num += 1
                r = self._get_response(url, params=params, recu_num=recu_num)
        finally:
            r.encoding = 'utf-8'
            return r
    
class ArticleAPI(API):
    
    
    def __init__(self, key_word='库客音乐', t=0):
        self.key_word = key_word
        self.params['query'] = self.key_word
        self.params['type'] = '2'
        self.msg_list = list()
        self.num = 0
        self.t = t
        
    def _extract_li(self, li) -> dict:
        info = dict()
        info['tilte'] = li.h3.get_text()
        info['content_url'] = li.a['href']
        info['digest'] = li.p.get_text()
        s_p = li.find(class_="s-p")
        info['account_name'] = s_p.a.get_text()
        info['account_url'] = s_p.a['href']
        info['datetime'] = self._get_datetime(s_p['t'])
        return info
    
    def news_result(self, page_num=1):
        
        for i in range(1, page_num+1):
            self.params['page'] = i
            r = self._get_response(self.query_url, params=self.params)
            if not r:
                self.msg_list.append('error')
                break
            soup = BS(r.text, 'html.parser')
            mun = soup.find(class_='mun').get_text()
            self.num = re.findall(r'(\d+)', mun)[0]
            ul = soup.find(class_="news-list")
            for li in ul.find_all('li'):
                msg_info = self._extract_li(li)
                self.msg_list.append(msg_info)
            time.sleep(self.t)
        return self.msg_list
        

class AccountAPI(API):
    
    def __init__(self, key_word='库客音乐'):
        self.key_word = key_word
        self.params['query'] = self.key_word
        self.params['type'] = '1'
        self.msg_list = list()
        self.raw_msg_list = list()
    
    def _get_msg_info(self, url) -> dict:
        r = self._get_response(url.replace('&amp;', '&'))
        if not r:
            return 'connect error with url: {}'.format(url)
        pattern = r'var msgList = (\{"list":\[[^<>]*?\]\});'
        try:
            msg_data = re.findall(pattern, r.text)[0]
        except:
            return "match error!"
        msg_info = msg_data.replace('"', "'")
        return eval(msg_info)
    
    def _get_account_url(self) ->list:
        r = self._get_response(self.query_url, params=self.params)
        if not r:
            return 'connect error with url: {}'.format(self.query_url)
        href_list = re.findall(r'href="(http://mp.weixin.qq.com/profile?[^""]*?)"',
                           r.text)
        if not href_list:
            return 'qury {} without result'.format(self.key_word)
        else:
            return href_list

    def _extract_msg_list(self, raw_msg_list) -> list:
        
        msg_list = list()
        for item in raw_msg_list:
            info = dict()
            info['author'] = item['app_msg_ext_info']['author']
            info['content_url'] = self.mp_url + item['app_msg_ext_info']['content_url']
            info['title'] = item['app_msg_ext_info']['title']
            info['digest'] = item['app_msg_ext_info']['digest']
            info['datetime'] = self._get_datetime(
                    item['comm_msg_info']['datetime'])
            info['key_word'] = self.key_word
            msg_list.append(info)
        return msg_list
    
    def new_push(self, count=10, isRaw=False):
        
        if count >= 10:
            count = 10
            
        result = dict()
        href_list = self._get_account_url()
        if type(href_list) != list:
            result['status'] = 0
            result['error_msg'] = href_list
            return result
        
        msg_info = self._get_msg_info(href_list[0])
        if type(msg_info) != dict:
            result['status'] = 0
            result['error_msg'] = msg_info
            return result
        
        self.raw_msg_list = msg_info['list']
        self.msg_list = self._extract_msg_list(self.raw_msg_list)
        result['status'] = 1
        if not isRaw:
            result['msg_list'] = self.msg_list[:count]
        else:
            result['msg_list'] = msg_info['list']
        return result
        
if __name__=="__main__":
    api_1 = AccountAPI()
    a_1 = api_1.new_push()
    api_2 = ArticleAPI()
    a_2 = api_2.news_result()
    pass