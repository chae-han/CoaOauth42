
import urllib3
import json


class httpRequest(object):

    def __init__(self, method='GET', url='', headers={}, body={}):
        if body != {}:
            body = json.dumps(body).encode('utf-8')
        self.params = {'method': method, 'url': url, 'headers': headers, 'body': body}

    def httpRequestSet(self, **kwargs):
        for key in self.params:
            if key in kwargs:
                if key == 'body':
                    self.params[key] = json.dumps(kwargs[key]).encode('utf-8')
                else:
                    self.params[key] = kwargs[key]

    def httpRequestStart(self):
        http = urllib3.PoolManager()
        r = http.request(method=self.params['method'], url=self.params['url'], headers=self.params['headers'], body=self.params['body'])

        if r.status != 200:
            raise Exception(f'http request response error : {r.status}')
            return

        result = json.loads(r.data.decode('utf-8'))
        return result



# def httpRequest(**kwargs):#method:str, url:str, body:dict={}, header:dict={}
#     params = {'method':'GET', 'url':'', 'headers':{}, 'body':{}}
#
#     for key in params:
#         print(key)
#         if key in kwargs:
#             if key == 'body':
#                 kwargs[key] = json.dumps(kwargs[key]).encode('utf-8')
#
#             params[key] = kwargs[key]
#
#
#     http = urllib3.PoolManager()
#     r = http.request(method=params['method'], url=params['url'], headers=params['headers'], body=params['body'])
#     print(r.status)
#     return json.loads(r.data.decode('utf-8'))




