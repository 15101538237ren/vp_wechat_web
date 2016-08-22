from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
import json,urllib2,os,threading,time
from django.contrib import auth
from voiceprint.handler import check_reg,json_response,check_log,get_request_full_url,ARTICLE_LIST,convert_to_enroll,pure_download_media,verify_user,convert_verify_user
from voiceprint.models import User
from wechat_sign import Sign,APP_ID
from vp_wechat_web.settings import BASE_DIR
from django.core.urlresolvers import reverse
# Create your views here.
TOTAL_STEP = 3
Threshold=1.0
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
        print message_json
        if message_json:
            message=json.dumps(message_json)
            return json_response(1,message)
        else:
            User.objects.create_user(first_name=name,password=password,username=email,phone_num=phone,step=1)
            user=auth.authenticate(username=email, password=password)
            auth.login(request,user)
            url_of_record=reverse('voiceprint:record')
            return json_response(0,url_of_record)
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
            if user.step == TOTAL_STEP:
                url_of_record=reverse('voiceprint:verify')
            else:
                url_of_record=reverse('voiceprint:record')
            return json_response(0,url_of_record)
def download_media(request):
    pure_download_media(request)
    user_id=request.user.id
    now_step=request.user.step
    if now_step < TOTAL_STEP:
        user = get_object_or_404(User, pk=user_id)
        user.step=now_step+1
        user.save()
        url_of_record=reverse('voiceprint:record')
        return json_response(0,url_of_record)
    else:
        threading.Thread(target=convert_to_enroll, args=(user_id,)).start()
        url_of_verify=reverse('voiceprint:verify')
        return json_response(1,url_of_verify)
def verify(request):
    if request.method == 'GET':
        media_id=request.GET.get("media_id",'')
        if media_id=='':
            req_url=get_request_full_url(request)
            sign = Sign(req_url)
            sign_dict=sign.sign()
            appid=APP_ID
            now_step=request.user.step
            article=ARTICLE_LIST[0]
            return render(request, 'vp/verify.html',locals())
        else:
            time_stamp=pure_download_media(request,1)
            user_id=request.user.id
            #threading.Thread(target=convert_verify_user, args=(user_id,time_stamp)).start()
            convert_verify_user(user_id,time_stamp)
            score = verify_user(user_id,time_stamp)
            score_res = float(score)
            print "score: %f" % score_res
            if score_res > 1.4:
                rej_or_acc="Accepted!"
            else:
                rej_or_acc="Rejected!"
            res = rej_or_acc+'<br/> Score: '+score
            return json_response(0,res)
@require_GET
def record(request):
    req_url=get_request_full_url(request)
    sign = Sign(req_url)
    sign_dict=sign.sign()
    appid=APP_ID
    total_step=TOTAL_STEP
    now_step=request.user.step
    article=ARTICLE_LIST[now_step]
    print "nowstep:"+str(now_step)
    print sign_dict['jsapi_ticket']
    return render(request, 'vp/record.html',locals())