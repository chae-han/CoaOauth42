from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
# Create your views here.


def sys42(request):
    return HttpResponse("hello3")


def iscsi(request):
    pass