from django.http import HttpResponse, JsonResponse
import json
from django.contrib import auth
from voiceprint.models import User
def check_reg(name,email,password,repassword,phone):
    message={}
    if name=="":
        message["name"]="Name required!"
    if email=="":
        message["email"]="Email required!"
    else:
        username=User.objects.filter(username=email)
        if len(username):
            message["email"]="Email has been registered!"
    if password=="":
        message["password"]="Password required!"
    if repassword=="":
        message["repassword"]="Re-Password required!"
    if phone=="":
        message["phone"]="Phone required!"
    elif len(phone)<11:
        message["phone"]="Phone number length 8-11!"
    if password and repassword and (password != repassword):
        message["passcons"]="Passwords are inconsistent!"
    return message
def check_log(email,password):
    message={}
    if email=="":
        message["email"]="Email required!"
    if password=="":
        message["password"]="Password required!"
    if not message:
        user=auth.authenticate(username=email, password=password)
        if user is None:
            message["vali_pass"]="Email or Password incorrect!"
        elif not user.is_active:
            message["vali_pass"]="User is inactive!"
    return message
def json_response(code=0,message=None):
    return JsonResponse({"code": code, "message": message})