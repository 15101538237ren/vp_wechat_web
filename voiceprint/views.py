from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib import auth
from voiceprint.handler import check_reg,json_response,check_log,get_request_full_url,ARTICLE_LIST
from voiceprint.models import User
from wechat_sign import Sign,APP_ID
# Create your views here.
def index(request):

    return render(request, 'vp/index.html',locals())

def register(request):
    if request.method == 'GET':
        return render(request, 'vp/register.html',locals())
    elif request.method == 'POST':
        json_obj=json.loads(request.POST['json_str'])
        name = str(json_obj['name'])
        email = str(json_obj['email'])
        password = str(json_obj['password'])
        repassword = str(json_obj['repassword'])
        phone = str(json_obj['phone'])
        message_json=check_reg(name,email,password,repassword,phone)
        if message_json:
            message=json.dumps(message_json)
            return json_response(1,message)
        else:
            user=User.objects.create_user(first_name=name,password=password,username=email,phone_num=phone)
            return json_response(0,"Register succeed!")
def login(request):
    if request.method == 'GET':
        return render(request, 'vp/login.html',locals())
    elif request.method == 'POST':
        json_obj=json.loads(request.POST['json_str'])
        email = str(json_obj['email'])
        password = str(json_obj['password'])
        message_json=check_log(email,password)
        if message_json:
            message=json.dumps(message_json)
            return json_response(1,message)
        else:
            user=auth.authenticate(username=email, password=password)
            auth.login(request,user)
            return json_response(0,"Login succeed!")
def record(request):
    if request.method == 'GET':
        req_url=get_request_full_url(request)
        sign = Sign(req_url)
        sign_dict=sign.sign()
        appid=APP_ID
        article=ARTICLE_LIST[1]
        print sign_dict['jsapi_ticket']
        return render(request, 'vp/record.html',locals())
    elif request.method == 'POST':
        pass