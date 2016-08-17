# -*- coding: utf-8 -*-
import random
import string
import hashlib
import json,os,time,urllib
from vp_wechat_web.settings import BASE_DIR
APP_ID="wx80799922d5db9a21"
SECREAT="053fa8096d34d3c18f2ec7fc19fc06bc"

class Sign:
    def __init__(self, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': self.getJsApiTicket(),
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())
    def getAccessToken(self):
        at_path=BASE_DIR+os.sep+"static"+os.sep+"json"+os.sep+"access_token.json"
        access_token_file=open(at_path,"r")
        acc_tok_str=access_token_file.readline()
        access_token_file.close()

        access_token_json=json.loads(acc_tok_str)
        now_time=time.time()
        if access_token_json["expire_time"] < now_time:
            params = urllib.urlencode({'grant_type':'client_credential','appid': APP_ID, 'secret': SECREAT})
            ac_str = urllib.urlopen("https://api.weixin.qq.com/cgi-bin/token?%s" % params).read()
            res_json=json.loads(ac_str)
            ac_token_hash={}
            access_token=res_json["access_token"]
            if access_token:
                expire_time=access_token_json["expire_time"]+5000
                ac_token_hash["access_token"]=res_json["access_token"]
                ac_token_hash["expire_time"]=expire_time
                res_str=json.dumps(ac_token_hash)
                ac_tok_wrt_file=open(at_path,"w")
                ac_tok_wrt_file.write(res_str)
                ac_tok_wrt_file.close()
        else:
            access_token=access_token_json["access_token"]
        return access_token
    def getJsApiTicket(self):
        jt_path=BASE_DIR+os.sep+"static"+os.sep+"json"+os.sep+"js_api_ticket.json"
        js_ticket_file=open(jt_path,"r")
        js_ticket_read_str=js_ticket_file.readline()
        js_ticket_file.close()
        js_ticket_read_json=json.loads(js_ticket_read_str)
        now_time=time.time()
        access_token=self.getAccessToken()
        if js_ticket_read_json["expire_time"] < now_time:
            params = urllib.urlencode({'type':'jsapi','access_token': access_token})
            jt_str = urllib.urlopen("https://api.weixin.qq.com/cgi-bin/ticket/getticket?%s" % params).read()
            res_json=json.loads(jt_str)
            js_ticket_hash={}
            js_ticket=res_json["ticket"]
            if js_ticket:
                expire_time=js_ticket_read_json["expire_time"]+5000
                js_ticket_hash["jsapi_ticket"]=res_json["ticket"]
                js_ticket_hash["expire_time"]=expire_time
                res_str=json.dumps(js_ticket_hash)
                js_tick_wrt_file=open(jt_path,"w")
                js_tick_wrt_file.write(res_str)
                js_tick_wrt_file.close()
        else:
            js_ticket=js_ticket_read_json["jsapi_ticket"]
        return js_ticket

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret