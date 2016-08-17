# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from voiceprint.models import User
import shlex,datetime,subprocess,time,os,urllib2,time
from vp_wechat_web.settings import BASE_DIR
from wechat_sign import Sign,APP_ID
TOTAL_STEP = 3
DIR_PATH_ROOT = "/root/Voice/voices/"
TIME_OUT_OF_EXEC=3000

ARTICLE_LIST=[
    'If I were a boy again, I would practise perseverance more often, and never give up a thing because it was hard or inconvenient. If we want light, we must conquer darkness. Perseverance can sometimes equal genius in its results.',
    'This is my room. Near the window there is a desk. I often do my homework at it. You can see some books, some flowers in a vase, a ruler and a pen. On the wall near the desk there is a picture of a cat.',
    'Computers are changing our life. You can do a lot of things with a computer. Such as, you can use a computer to write articles, watch video CDs, play games and do office work.',
    'Mom bought me a pair of skating shoes at my fifth birthday. From then on, I developed the hobby of skating. It not only makes me stronger and stronger, but also helps me know many truths of life.',
]
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
def pure_download_media(request,verify=0):
    dist_dir=BASE_DIR+os.sep+"static"+os.sep+"download"+os.sep

    media_id=request.GET["media_id"]
    req_url=get_request_full_url(request)
    sign = Sign(req_url)
    access_token=sign.getAccessToken()
    url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token="+access_token+"&media_id="+media_id

    #print url
    time_stamp=0
    user_id=request.user.id
    now_step=request.user.step
    if verify==1:
        time_stamp=int(time.time())
        file_name = str(user_id)+"_verify_"+str(time_stamp)+".amr"
    else:
        file_name = str(user_id)+"_"+str(now_step)+".amr"
    u = urllib2.urlopen(url)

    f = open(dist_dir+file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()
    print "%s download completed" %file_name
    if verify==1:
        return time_stamp
def get_request_full_url(request):
    return request.build_absolute_uri('?')
def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    """执行一个SHELL命令
            封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
           参数:
        cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
        timeout: 超时时间，秒，支持小数，精度0.1秒
        shell: 是否通过shell运行
    Returns: return_code
    Raises:  Exception: 执行超时
    """
    end_time=0
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    #没有指定标准输出和错误输出的管道，因此会打印到屏幕上；
    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE,shell=shell,bufsize=4096)

    #subprocess.poll()方法：检查子进程是否结束了，如果结束了，设定并返回码，放在subprocess.returncode变量中
    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s"%cmdstring)
    print "returnCode:"+str(sub.returncode)
    return str(sub.returncode)
def convert_for_user(user_id):
    source_pre=BASE_DIR+os.sep+"static"+os.sep+"download"+os.sep+str(user_id)+"_"
    dist_pre=BASE_DIR+os.sep+"static"+os.sep+"wav"+os.sep+str(user_id)+"_"
    for i in range(1,TOTAL_STEP+1):
        source_path=source_pre+str(i)+".amr"
        dist_path=dist_pre+str(i)+".wav"
        ret_code=audio_convert(source_path,dist_path)
        if ret_code == 0:
            print "user: " + str(user_id) + "s" + str(i) + "-th amr converted to wav!"
    print "user: " + str(user_id) + "s amr converted to wav!"
def wrt_enroll_wav_list(user_id):
    dist_pre=BASE_DIR+os.sep+"static"+os.sep+"wav"+os.sep+str(user_id)+"_"

    enroll_wav_list_file_path=BASE_DIR+os.sep+"static"+os.sep+"voiceprint"+os.sep+"EnrollWavList_"+str(user_id)+".txt"
    enroll_wav_list_file=open(enroll_wav_list_file_path,"w")
    wav_list=[]
    for i in range(1,TOTAL_STEP+1):
        wav_path=dist_pre+str(i)+".wav"
        wav_list.append(wav_path)
    wrt_str="\n".join(wav_list)
    enroll_wav_list_file.write(wrt_str)
    enroll_wav_list_file.close()
    print "user: " + str(user_id) + "s wavlist file write done!"
def enroll_user(user_id):
    enroll_wav_list_file_path=BASE_DIR+os.sep+"static"+os.sep+"voiceprint"+os.sep+"EnrollWavList_"+str(user_id)+".txt"
    out_model_path=BASE_DIR+os.sep+"static"+os.sep+"model"+os.sep+str(user_id)+".model"
    ret_code=enroll_voiceprint(enroll_wav_list_file_path,out_model_path)
    if ret_code == 0:
        print "user: " + str(user_id) + "s enrollment done!"
    else:
        print "user: " + str(user_id) + "s enrollment has some error, rtn_code:"+str(ret_code)
def convert_to_enroll(user_id):
    convert_for_user(user_id)
    wrt_enroll_wav_list(user_id)
    enroll_user(user_id)
def audio_convert(source_path,dist_path):
    cmd='avconv -i '+source_path+' '+dist_path
    returncode=execute_command(cmd,cwd=DIR_PATH_ROOT,timeout=TIME_OUT_OF_EXEC)
    return returncode
def convert_verify_user(user_id,time_stamp):
    source_amr=BASE_DIR+os.sep+"static"+os.sep+"download"+os.sep+str(user_id)+"_verify_"+str(time_stamp)+".amr"
    dist_wav=BASE_DIR+os.sep+"static"+os.sep+"wav"+os.sep+str(user_id)+"_verify_"+str(time_stamp)+".wav"
    audio_convert(source_amr,dist_wav)
    time.sleep(0.5)
def verify_user(user_id,time_stamp):
    dist_wav=BASE_DIR+os.sep+"static"+os.sep+"wav"+os.sep+str(user_id)+"_verify_"+str(time_stamp)+".wav"
    model_path=BASE_DIR+os.sep+"static"+os.sep+"model"+os.sep+str(user_id)+".model"
    score_path=BASE_DIR+os.sep+"static"+os.sep+"score"+os.sep+str(user_id)+"_verify_"+str(time_stamp)+".txt"
    if os.path.exists(model_path):
        verify_voiceprint(wav_path=dist_wav,vp_model_path=model_path,score_file_path=score_path)
        time.sleep(0.5)
        score_file=open(score_path,"r")
        score=score_file.readline()
        print "score:"+score
        score_file.close()
        return score
def enroll_voiceprint(wavlistpath,output_model_path):
    cmd="./enroll "+wavlistpath+" "+output_model_path+" universal.model"
    returncode=execute_command(cmd,cwd=DIR_PATH_ROOT,timeout=TIME_OUT_OF_EXEC)
    return returncode
def verify_voiceprint(wav_path,vp_model_path,score_file_path):
    cmd="./verify "+wav_path+" "+vp_model_path+" "+score_file_path+" universal.model"
    returncode=execute_command(cmd,cwd=DIR_PATH_ROOT,timeout=TIME_OUT_OF_EXEC)
    return returncode