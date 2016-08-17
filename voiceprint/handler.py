from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from voiceprint.models import User

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


def get_request_full_url(request):
    return request.build_absolute_uri('?')
if __name__ == '__main__':
    pass