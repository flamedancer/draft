# -*- coding:utf-8 -*-
from urlparse import urlparse
from urlparse import parse_qs

url_str = "http://www.163.com/mail/index.htm?key=果果&a=3"
print urlparse(url_str)
url = urlparse(url_str).query
print url
print { key: value[0] for key, value in parse_qs(url).items() }
print dir(url)
print 'protocol:',url.scheme
print 'hostname:',url.hostname
print 'port:',url.port
print 'path:',url.path
print 'params:',url.params


