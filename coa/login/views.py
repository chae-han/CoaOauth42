from django.shortcuts import render
from login.security import en_decrypt
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from login.httpReqests import httpRequests as httpr
import os

uid = os.environ.get('OAUTHUID')
sec = os.environ.get('OAUTHSEC')
redirect_uri = 'http://localhost:8000/login/oauth42/'


def login(request:HttpRequest):
    result = en_decrypt.had_active_cookie(request)
    if result == -1:
        return render(request, 'login/index.html')
    else:
        return HttpResponseRedirect('/sys42/')


def oauth42(request:HttpRequest):
    try:
        login = ''
        access_token = ''

        raw_url = request.get_raw_uri()
        arr = raw_url.split('?')

        if len(arr) != 2 or arr[1].startswith('code=') != True:
            raise Exception('error')

        code = arr[1].split(' ')[0].split('=')[1]

        req = httpr.httpRequest()

        body_data = {"grant_type":"authorization_code", "client_id":uid, "client_secret":sec, "code":code, "redirect_uri":redirect_uri}
        req.httpRequestSet(method='POST', url='https://api.intra.42.fr/oauth/token', headers={'Content-Type': 'application/json'}, body=body_data)
        r = req.httpRequestStart()
        # r = httpr.httpRequest(method='POST', url='https://api.intra.42.fr/oauth/token', headers={'Content-Type': 'application/json'}, body=body_data)

        access_token = r['access_token']
        req.httpRequestSet(method='GET', url='https://api.intra.42.fr/v2/me', headers={'Authorization': 'Bearer ' + access_token})
        r = req.httpRequestStart()
        # r = httpr.httpRequest(method='GET', url='https://api.intra.42.fr/v2/me', headers={'Authorization': 'Bearer ' + access_token})

        login = r['login']
        result = en_decrypt.set_active_cookie(request, login, access_token)

        return HttpResponseRedirect('/sys42/')

    except Exception as e:
        print(e)
        return HttpResponseRedirect('/login/')


