# -*- coding: utf-8 -*-
"""
Created on Sat May 26 12:09:16 2018

@author: icetong
"""

import requests
from pypg import PyProgress

def down(url, file_path='test.pdf', headers={}):
    
    r = requests.get(url, headers=headers, stream=True)
    pg = PyProgress(total=int(r.headers['Content-Length'])/1024, isIpy=False)
    with open(file_path, 'wb') as f:
        n = 0
        pg.update(n)
        for chunk in r.iter_content(1024):
            n += len(chunk)/1024
            f.write(chunk)
            pg.update(n)

if __name__=="__main__":
    
    url = 'https://102.alibaba.com/downloadFile.do?file=1517812754285/reinforcement_learning.pdf'
    down(url)
    pass

