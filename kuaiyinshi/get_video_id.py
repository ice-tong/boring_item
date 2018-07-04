# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 16:53:10 2018

@author: icetong
"""

'''

https://kys.tqdn.cn/js/main.js?t=1530178376
https://kys.tqdn.cn/js/public.js?t=1529140999

'''


Key = "A0MjZfMTY0NDA3Mj"

def kuaiyinshi_id(video_id, key=Key):
    A = [ord(k) for k in key]
    id_list = video_id.split(':')
    del id_list[0]
    B = [(int(i)-(255 & A[(k)%len(A)])) for k, i in enumerate(id_list)]
    return ''.join([chr(b) for b in B])


if __name__=="__main__":
    video_id = ''':183:96:127:154:138:204:175:184:137:96:126:116:163:
            149:188:161:167:105:178:214:193:159:183:200:139:152:128:
                    124:114:162:183:154'''.replace('\n\t', '')
    new_id = kuaiyinshi_id(video_id)
    print(new_id)