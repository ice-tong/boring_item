# -*- coding: utf-8 -*-
"""
Created on Sat May 26 09:01:20 2018

@author: icetong
"""
import time

class PyProgress(object):
    
    def __init__(self, total:int, now=0, lenght=20, sign='#', 
                 name='progress', delay=0.01, isIpy=True):
        self.total = total
        self.now = now
        self.sign = sign
        self.lenght = lenght
        self.name = name
        self.delay = delay
        self.isIpy = isIpy
        
        self.n_sign = '-'
        self.cursor = 0
        self.b_num = 0
        
    def ipy_show(self, out):
        print('\b'*self.b_num, end='')
        time.sleep(self.delay)
        print(out, end='')
        self.b_num = len(out)
        
    def show(self, out):
        print(out, end='\r')
        
    def update(self, now):
        
        self.now = now
        
        f = (self.now/self.total)*self.lenght
        if f-1 >= self.cursor:
            self.cursor+=1
        out = self.sign*self.cursor + (self.lenght-self.cursor)*self.n_sign
        out += ' {}/{}'.format(self.now, self.total)
        out += ' {:.2f}%'.format((self.now/self.total)*100)
        out = self.name+': '+out
        
        if self.isIpy:
            self.ipy_show(out)
        else:
            self.show(out)
            

def test(total=150, t=0.1):
    
    p = PyProgress(total, isIpy=True)
    for i in range(total+1):
        time.sleep(t)
        p.update(i)
        
if __name__=="__main__":
    
    test()
    pass