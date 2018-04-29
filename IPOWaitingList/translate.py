import http.client
from hashlib import md5 as md5
import urllib


import random
import json
import re
# _appid = 
# _key = 


def TranslateByBaidu(text, appid=_appid, secretKey=_key, fromLang='auto', toLang='zh'):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = text
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    m1 = md5()
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + \
        urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + \
        toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result = response.read().decode('utf-8')
        data = json.loads(result)
        return data["trans_result"][0]["dst"]
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


if __name__ == '__main__':
    txt = 'This is a pig'

    print(TranslateByBaidu(txt))
