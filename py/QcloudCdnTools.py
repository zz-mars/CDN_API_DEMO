#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import hashlib
import urllib
import requests
import binascii
import hmac
import copy
import random
import sys
import time
from pprint import pprint
from optparse import OptionParser

reload(sys)
sys.setdefaultencoding("utf-8")

try: import simplejson as json
except: import json


class Sign:
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey

    def make(self, requestHost, requestUri, params, method = 'GET'):
        srcStr = method.upper() + requestHost + requestUri + '?' + "&".join(k.replace("_",".") + "=" + str(params[k]) for k in sorted(params.keys()))
        hashed = hmac.new(self.secretKey, srcStr, hashlib.sha1)
        return binascii.b2a_base64(hashed.digest())[:-1]

class Request:
    timeout = 10
    version = 'Python_Tools'
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey

    def send(self, requestHost, requestUri, params, files = {}, method = 'GET', debug = 0):
        params['RequestClient'] = Request.version
        params['SecretId'] = self.secretId
        sign = Sign(self.secretId, self.secretKey)
        params['Signature'] = sign.make(requestHost, requestUri, params, method)

        url = 'https://%s%s' % (requestHost, requestUri)

        if debug:
            print method.upper(), url
            print 'Request Args:'
            pprint(params)
        if method.upper() == 'GET':
            req = requests.get(url, params=params, timeout=Request.timeout)
        else:
            req = requests.post(url, data=params, files=files, timeout=Request.timeout)

        if debug:
            print "Response:", req.status_code, req.text
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        rsp = {}
        try:
            rsp = json.loads(req.text)
        except:
            raise ValueError, "Error: response is not json\n%s" % req.text

        code = rsp.get("code", -1)
        message = rsp.get("message", req.text)
        if rsp.get('code', -404) != 0:
            raise ValueError, "Error: code=%s, message=%s" % (code, message)
        if rsp.get('data', None) is None:
            print 'request is success.'
        else:
            print rsp['data']




def Name(name):
    up = False
    new_name = ""
    for i in name:
        if i == '_':
            up = True
            continue
        if up:
            new_name += i.upper()
        else:
            new_name += i
        up = False
    return new_name


class Cdn:
    def __init__(self):
        self.params = {
                'Region': 'gz',
                'Nonce': random.randint(1, sys.maxint),
                'Timestamp': int(time.time()),
                }
        self.files = {}
        self.host = 'cdn.api.qcloud.com'
        self.uri = '/v2/index.php'
        self.method = "POST"
        self.debug = 1

    def parse_args(self):
        actions = []
        for method in dir(self):
            if method[0].isupper():
                actions.append( method )

        usage='usage: %prog Action [options]\nThis is a command line tools to access Qcloud API.\n\nSupport Actions:\n    '+"\n    ".join(actions)
        self.parser = OptionParser(usage=usage)
        from sys import argv
        if len(argv) < 2 or argv[1] not in actions:
            self.parser.print_help()
            return 0

        action = argv[1]
        self.params['Action'] = action
        usage='usage: %%prog Action [options]\n\nThis is help message for action "%s"\nMore Usage: http://www.qcloud.com/wiki/v2/%s' % (action, action)
        self.parser = OptionParser(usage=usage)
        self.parser.add_option('--debug', dest='debug', action="store_true", default=False, help='Print debug message')
        self.parser.add_option('-u', '--secret_id', dest='secret_id', help='Secret ID from <https://console.qcloud.com/capi>')
        self.parser.add_option('-p', '--secret_key', dest='secret_key', help='Secret Key from <https://console.qcloud.com/capi>')
        getattr(self, action)()
        if len(argv) == 2:
            self.parser.print_help()
            return 0

        (options, args) = self.parser.parse_args() # parse again
        self.debug = options.debug
        for key in dir(options):
            if not key.startswith("__") and getattr(options, key) is None:
                raise KeyError, ('Error: Please provide options --%s' % key)


        for option in self.parser.option_list:
            opt = option.dest
            if opt not in [None, 'secret_id', 'secret_key', 'debug']:
                self.params[ Name(opt) ] = getattr(options, opt)

        self.options = options
        method = 'get_params_' + action
        if hasattr(self, method): getattr(self, method)()

        # format params
        for key, value in self.params.items():
            if isinstance(value, list):
                del self.params[key]
                for idx, val in enumerate(value):
                    self.params["%s.%s"%(key, idx)] = val

        request = Request(options.secret_id, options.secret_key)
        return request.send(self.host, self.uri, self.params, self.files, self.method, self.debug)


    def DescribeCdnHosts(self):
        pass

    def RefreshCdnUrl(self):
        self.parser.add_option('--urls', dest='urls', default=[], action="append", help="Flush the cache of these URLs(use multi --urls)")
        self.parser.add_option('--urls-from', dest='urls_from', default="", metavar="FILE", help="Flush the cache of these URLs(one url per line)")

    def get_params_RefreshCdnUrl(self):
        if self.options.urls_from:
            f = open(self.options.urls_from)
            self.params["urls"] = [p.strip() for p in f.readlines()]
        elif not self.options.urls:
            raise ValueError, "Please provide --urls or --urls-from"
        del self.params['urlsFrom']

    def GetCdnRefreshLog(self):
        self.parser.add_option('--start_date', dest='start_date', help="Start Date, eg '2015-04-20 00:00:00'")
        self.parser.add_option('--end_date', dest='end_date', help="end Date, eg '2015-04-20 23:59:59'")
        self.parser.add_option('--url', dest='url', default="", help="optional search url")

    def UpdateCdnHost(self):
        self.parser.add_option('--origin', dest='origin', help="CDN origin server address")
        self.parser.add_option('--host', dest='host', help="CDN host")
        self.parser.add_option('--host_id', dest='host_id', help="CDN host ID")

    def DeleteCdnHost(self):
        self.parser.add_option('--host_id', dest='host_id', help="CDN host ID")

    def DescribeCdnHostDetailedInfo(self):
        self.parser.add_option('--start_date', dest='start_date', help="Start Date, eg '2015-04-20 00:00:00'")
        self.parser.add_option('--end_date', dest='end_date', help="end Date, eg '2015-04-20 23:59:59'")
        self.parser.add_option('--stat_type', dest='stat_type', choices=['bandwidth','flux','requests','ip_visits','cache'], help="stat type")
        self.parser.add_option('--hosts', dest='hosts', default=[], action="append", help="Options Filter by these hosts(use multi --hosts)")
        self.parser.add_option('--projects', dest='projects', default=['0'], action="append", help="Optional Filter by these project ids(use multi --projects)")

    def DescribeCdnHostInfo(self):
        self.parser.add_option('--start_date', dest='start_date', help="Start Date, eg '2015-04-20 00:00:00'")
        self.parser.add_option('--end_date', dest='end_date', help="end Date, eg '2015-04-20 23:59:59'")
        self.parser.add_option('--stat_type', dest='stat_type', choices=['bandwidth','flux','requests','ip_visits','cache'], help="stat type")
        self.parser.add_option('--hosts', dest='hosts', default=[], action="append", help="Options Filter by these hosts(use multi --hosts)")
        self.parser.add_option('--projects', dest='projects', default=['0'], action="append", help="Optional Filter by these project ids(use multi --projects)")

    def AddCdnHost(self):
        self.parser.add_option('--host', dest='host', help="CDN host")
        self.parser.add_option('--origin', dest='origin', help="CDN origin server address")
        self.parser.add_option('--host_type', dest='host_type', choices=["cname", "ftp"], help="host type: cname or ftp")
        self.parser.add_option('--project_id', dest='project_id', default=0, help="Attach the host to specific project.")
        pass

    def UpdateCdnProject(self):
        self.parser.add_option('--host_id', dest='host_id', help="CDN host ID")
        self.parser.add_option('--project_id', dest='project_id', help="new project id")

    def UpdateCache(self):
        self.parser.add_option('--host_id', dest='host_id', default="", help="CDN host ID")
        self.parser.add_option('--cache', dest='cache', help="new cache rule. Read the webpage for more details <http://www.qcloud.com/wiki/v2/UpdateCache> ")

    def OfflineHost(self):
        self.parser.add_option('--host_id', dest='host_id', help="CDN host ID")

    def OnlineHost(self):
        self.parser.add_option('--host_id', dest='host_id', help="CDN host ID")

    def GenerateLogList(self):
        self.parser.add_option('--host_id', dest='host_id', help="CDN host ID")

    def GetCdnMiddleSourceList(self):
        pass

    def EAddCdnHost(self):
        self.parser.add_option('--host', dest='host', help="CDN host")
        self.parser.add_option('--origin', dest='origin', help="CDN origin server address")
        self.parser.add_option('--host_type', dest='host_type', choices=["cname", "ftp"], help="host type: cname or ftp")
        self.parser.add_option('--project_id', dest='project_id', default=0, help="Attach the host to specific project.")
        self.parser.add_option('--middle_resource', dest='middle_resource', default='off', choices=['on', 'off'], help="TODO")
        self.parser.add_option('--cache_mode', dest='cache_mode', choices=['simple', 'custom'], default='simple', help='simple or custom, learn more by visting -> http://www.qcloud.com/wiki/CDN%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C#CDN.E9.85.8D.E7.BD.AE.E7.AE.A1.E7.90.86.EF.BC.9A.E7.BC.93.E5.AD.98.E6.97.B6.E9.97.B4')
        self.parser.add_option('--cache', dest='cache', default='[[0,"all", 2592000]]', help='TODO')
        self.parser.add_option('--refer', dest='refer', default='[0,[]]', help='TODO')
        self.parser.add_option('--fwd_host', dest='fwd_host', help='the host header when cdn server request origin with')
        self.parser.add_option('--full_url', dest='full_url', choices=['on', 'off'], default='on', help='the requested resource will be stored on cdn server with the full uri as key if this option is turned on, otherwise uri without arguments will be the key')

    def CdnPusher(self):
        self.parser.add_option('--host', dest='host', help="CDN host")
        self.parser.add_option('--pathesfromfile', dest='pathesfromfile', help="pathes from file")

    def get_params_CdnPusher(self):
        if self.options.pathesfromfile:
            f = open(self.options.pathesfromfile)
            self.params["urlInfos"] = [p.strip() for p in f.readlines()]
            f.close()
        elif not self.options.pathesfromfile:
            raise ValueError, "Please provide --pathesfromfile"

    def GetCdnPushStatus(self):
        self.parser.add_option('--task_id', dest='task_id', help="task id")

    def GetHostInfoByHost(self):
        self.parser.add_option('--hosts', dest='hosts', default=[], action="append", help="CDN host ID(use multi --hosts)")

    def GetHostInfoById(self):
        self.parser.add_option('--host_id', dest='host_id', default=[], action="append", help="CDN host ID(use multi --host_id)")

def main():
    cdn = Cdn()
    try:
        cdn.parse_args()
    except Exception as e:
        print e
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())

