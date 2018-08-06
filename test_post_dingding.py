import requests



def send_dingding():
    token = '6d6befd1ac53f1671b310803804f3807dbf7fd15f9adc4c1a160ac85de75e7f3'

    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % token
    info = {
        "msgtype": "text",
        "text": {
            "content": 'just for test', 
        },
        "at": {
            "atMobiles": [],
            "isAtAll": False
        }
    }
    ret = requests.post(url, json=info)
    print('ding:',ret.text)

send_dingding()

