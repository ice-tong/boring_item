# -*- coding: utf-8 -*-
"""
Created on Mon May 21 10:12:01 2018

@author: icetong
"""

import wxpy
import re
from PIL import Image
import numpy as np
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def get_friends_signature(bot:wxpy.Bot) -> dict:
    
    signature_data = {}
    friends = bot.friends()
    for friend in friends:
        signature_data[friend.nick_name] = friend.signature
    return signature_data

def clean_str(s:str) -> str:
    
    s = s.replace('\n', '。').replace('\t', ' ').replace('\r', ' ')
    flag = re.findall('\d{11}', s)
    if flag:
        for f in flag:
            s = s.replace(f, f[:3]+'****'+f[-4:])
    s = re.sub(r'<[^<>]*>', '', s)
    return s

def get_bk_img(img_path='./background_img/bkn.jpg') -> np.array :
    
    img = Image.open(img_path)
    img = img.resize((600, 300))
    return np.array(img)

def build_word_colud(word_list:list, isJieba=True) -> WordCloud.generate:
    
    if isJieba:
        word_list = [' '.join(jieba.cut(item)) for item in word_list]
    
    bk = get_bk_img()
    wc = WordCloud(font_path='./font/simhei.ttf', 
                   background_color='white', mask=bk,
                   max_font_size=40, min_font_size=5)
    img = wc.generate(' '.join(word_list))
    return img
    
def main():
    
    bot = wxpy.Bot()
    data = get_friends_signature(bot)
    bot.logout()
    word_list = []
    for k, v in data.items():
        if not v:
            continue
        word_list.append(clean_str(v))
#    print(word_list)
    img_1 = build_word_colud(word_list, isJieba=False)
    img_2 = build_word_colud(word_list)
    plt.imshow(img_1)
    plt.imshow(img_2)
    plt.show()
    plt.imsave('./result/1.ipg', img_1)
    plt.imsave('./result/2.jpg', img_2)
    
    pass

if __name__=="__main__":
    
    
    main()
    pass