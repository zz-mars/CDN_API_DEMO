#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import time
import random
import hmac
import hashlib
import base64
import json

# 需要填写你的密钥，可从  https://console.qcloud.com/capi 获取 SecretId 及 $secretKey
secretId = 'YOUR_SECRET_ID'
secretKey = 'YOUR_SECRET_KEY'
action = 'CdnPusher'

httpUrl = 'cdn.api.qcloud.com'
httpMethod = 'POST'
isHttps = True
privateParams = {
    'host': 'ping.cdn.qcloud.com',
    'urlInfos.0': '/ping/t0.css',
    'urlInfos.1': '/ping/t1.css'
}
commonParams = {
    'Nonce': random.random(),
    'Timestamp': time.time(),
    'Action': action,
    'SecretId': secretId
}


def create_request():
    full_http_url = httpUrl + '/v2/index.php'
    req_params = dict(privateParams.items() + commonParams.items())
    sorted_params = sorted(req_params.items(), key=lambda d: d[0])
    sig_txt = httpMethod + full_http_url + '?'
    is_first = True
    for key, value in sorted_params:
        if not is_first:
            sig_txt += '&'
        is_first = False

        if key.find('_'):
            key.replace('_', '.')
        sig_txt = sig_txt + key + '=' + str(value)

    signature = hmac.new(secretKey, sig_txt, hashlib.sha1).digest().encode('base64').rstrip()
    req_params['Signature'] = signature

    if isHttps:
        rsp = requests.post('https://' + full_http_url, req_params)
    else:
        rsp = requests.post('http://' + full_http_url, req_params)

    print json.loads(rsp.text)

if __name__ == '__main__':
    create_request()
