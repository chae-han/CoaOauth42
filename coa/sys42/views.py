from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from api.security import en_decrypt
from sys42 import models
from login.models import Oauth42
from datetime import datetime

TIMELIMIT_PER_COMMAND = 10 * 60

def sys42(request):
    try:
        result = en_decrypt.check_active_cookie(request)
        if result == -1:
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'sys42/index.html')
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/login/')

def iscsi(request):
    try:
        login = en_decrypt.check_active_cookie(request)

        if login == -1:
            return HttpResponseRedirect('/login/')
        else:
            artist = Oauth42.objects.get(login=login)
            q_set, flag = models.Iscsi.objects.get_or_create(login=artist, issue='IS')

            if flag: # created!
                q_set.save()
                # iscsi target error handle
                return HttpResponse("command commit1")
            else:
                if datetime.now().timestamp() - q_set.updated_at.timestamp() > TIMELIMIT_PER_COMMAND:
                    db = models.Iscsi(login=artist)
                    db.save()
                    # iscsi target error handle
                    return HttpResponse("command commit2")

            return HttpResponse("wait!")
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/sys42/')