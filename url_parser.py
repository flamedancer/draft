# -*- coding:utf-8 -*-
from urllib.parse import urlparse
from urllib.parse import parse_qs

url_str = "http://www.163.com/mail/index.htm?key=果果&a=3"


def get_parse_info(url_str):
    parse_info = urlparse(url_str)
    return parse_info


def echo_parse_info(parse_info):
    info = {}
    print(parse_info)
    for key in dir(parse_info):
        if key.startswith('_'):
            continue
        value = getattr(parse_info, key)
        if hasattr(value, '__call__'):
            continue
        if key == 'query':
            value = { key: value[0] for key, value in list(parse_qs(value).items()) }
        info[key] = value
    print(info)
    return info



if __name__ == '__main__':
    echo_parse_info(get_parse_info(url_str))
