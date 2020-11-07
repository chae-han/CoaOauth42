
import urllib3
import json


def httpRequest(**kwargs):#method:str, url:str, body:dict={}, header:dict={}
    params = {'method':'GET', 'url':'', 'headers':{}, 'body':{}}

    for key in params:
        print(key)
        if key in kwargs:
            if key == 'body':
                kwargs[key] = json.dumps(kwargs[key]).encode('utf-8')

            params[key] = kwargs[key]


    http = urllib3.PoolManager()
    r = http.request(method=params['method'], url=params['url'], headers=params['headers'], body=params['body'])
    print(r.status)
    return json.loads(r.data.decode('utf-8'))




