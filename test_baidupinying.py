# -*- coding:utf-8 -*-
import requests
import json
import sys


def test(pinyin):
    url = 'http://olime.baidu.com/py'
    data = {
        'input' : pinyin, 
        'inputtype' : 'py', # 这个地方写py应该是拼音的意思
        'bg': '0', # 暂时不清楚什么鬼
        'ed': '20', # 暂时不清楚什么鬼
        'result': 'hanzi', # 暂时不清楚什么鬼
        'resultcoding' : 'unicode', # 字符编码,当前试出来的有utf-8和Unicode
        'ch_en': '0', #  暂时不清楚什么鬼,可能有跟英文备选相关的东西
        'clientinfo' : 'web', # 肯定的要web,其他client可能会有桌面的
        'version': '1', # 没试过其他的
    }
    rs = requests.post(url, data=data)
    result = rs.json()['result']
    for r1 in result:
        for r2 in r1:
            print(r2[0])


if __name__ == '__main__':
    pinyin = sys.argv[1]
    test(pinyin)
