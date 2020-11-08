from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from api.security import en_decrypt

def sys42(request):
    result = en_decrypt.check_active_cookie(request)
    if result == -1:
        return render(request, 'login/index.html')
    else:
        return HttpResponse("hello3")


def iscsi(request):
    pass