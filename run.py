# coding:utf-8
import requests
from Crypto.Cipher import AES
from m3u8 import parser
import sys
import ConfigParser
import json

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.cfg')
    userAgent = config.get('http','user_agent')
    referer = config.get('http','referer')
    with open('data.json') as f:
        dataConfig = json.load(f)
    headers = {}
    headers['User-Agent'] = userAgent
    headers['Referer'] = referer
    for item in dataConfig['urls']:
        url = item['url']
        output = item['output']
        fp = open(output,'wb')
        prefix = '/'.join(url.split('/')[0:-1]) + '/'
        r = requests.get(url,headers = headers)
        r.encode = 'utf-8'
        playList = parser.parse(r.text)
        i = 0
        count = len(playList['segments'])
        print 'starting...'
        print 'total segments:%d' % (count)
        for item in playList['segments'] :
            print 'downloading segments %d' % (i)
            i += 1
            url = prefix + item['uri']
            r = requests.get(url,headers = headers)
            data = r.content
            keyUrl = item['key']['uri']
            k = requests.get(keyUrl,headers = headers)
            key = k.content
            cryptor = AES.new(key, AES.MODE_CBC, key)
            data = cryptor.decrypt(data)
            fp.write(data)
        fp.close()
        print 'output:%s' % (output)    
 