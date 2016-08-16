from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'vp/index.html',locals())
def register(request):
    if request.method == 'GET':
        return render(request, 'vp/register.html',locals())
    elif request.method == 'POST':
        pass
def login(request):
    if request.method == 'GET':
        return render(request, 'vp/login.html',locals())
    elif request.method == 'POST':
        pass
def record(request):
    if request.method == 'GET':
        return render(request, 'vp/record.html',locals())
    elif request.method == 'POST':
        pass