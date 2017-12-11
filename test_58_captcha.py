import requests

url = 'http://verifycode.58.com/captcha/captcha_img?rid=841be76bd777452cab8cb57341d472db&it=_puzzle'
refer = 'http://callback.58.com/firewall/valid/920593415.do'

headers = {
    'Referer': refer,
    'Accept': 'mage/webp,image/apng,image/*,*/*;q=0.8',
}

rsp = requests.get(url, headers=headers)
print rsp.text
