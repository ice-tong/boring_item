# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 22:34:54 2018

@author: icetong
"""

import requests
import time
import hmac
import json
import re

class ZhiHuLogin(object):
    
    def __init__(self, username, password, 
                 client_id='c3cef7c66a1843f8b3a9e6a1e3160e20',
                 key=b'd1b964811afb40118a12068ff74a12f4'):
        
        self.login_url = 'https://www.zhihu.com/signup?next=%2F'
        self.captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
        self.sign_in_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        self.captcha_flag = 1
        self.sess = None
        self.key = key
        
        self.form_data = {}
        self.form_data['username'] = username
        self.form_data['password'] = password
        self.form_data['client_id'] = client_id
        self.form_data['grant_type'] = 'password'
        self.form_data['source'] = 'com.zhihu.web'
        self.form_data['captcha'] = None
        self.form_data['lang'] = 'en'
        self.form_data['ref_source'] = 'homepage'
        self.form_data['utm_source'] = None
        self.form_data['timestamp'] = str(int(time.time()))
        
        self.headers = self.get_headers()
    
        
    def get_headers(self):
        
        return {'User-Agent': 'Mozilla/5.0(WindowsNT10.0;WOW64;rv',
                'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}

    def get_sess(self):
        
        i = 1
        while self.captcha_flag:
            
            print('开始尝试第{}次'.format(i))
            i += 1
            
            self.headers = self.get_headers()
            self.sess = requests.Session()
            response = self.sess.get(self.login_url, headers=self.headers)
            x_udid = re.findall(r'{&quot;xUDID&quot;:&quot;([^;&]*)&quot;}',
                                   response.text)[0]
            if not x_udid:
                continue
            self.headers['x-udid'] = x_udid
            cap_response = self.sess.get(self.captcha_url, 
                                       headers=self.headers, verify=True)
            dic = json.loads(cap_response.text)
            print(dic)
            if not dic['show_captcha']:
                self.captcha_flag = 0
        return True
            
    def get_signature(self):
        
        myhmac = hmac.new(self.key, None, 'sha1')
        myhmac.update(bytes(self.form_data['grant_type'], 'utf-8'))
        myhmac.update(bytes(self.form_data['client_id'], 'utf-8'))
        myhmac.update(bytes(self.form_data['source'], 'utf-8'))
        myhmac.update(bytes(self.form_data['timestamp'], 'utf-8'))
        return myhmac.hexdigest()
    
    def sign_in(self):
        
        signature = self.get_signature()
        self.form_data['signature'] = signature
        print(signature)
        
        self.get_sess()
        
        response = self.sess.post(self.sign_in_url, data=self.form_data, 
                                  headers=self.headers)
        print(response.text)
        
if __name__=="__main__":
    username = "+86########"
    password = "#####"
    login = ZhiHuLogin(username, password)
    login.sign_in()
