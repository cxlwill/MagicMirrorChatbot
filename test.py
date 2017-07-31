# -*- coding: utf-8 -*-
import urllib
import json
import sys
import urllib2
import json
import uuid
import base64
import os
import time
reload(sys)
sys.setdefaultencoding('utf8')

class Chatbot:
    #百度token
    appid=7647466
    apikey="urSY5fP22GsR1ARF4oFmzyTv"
    secretkey="44102aef059a899a429d9e92556d1b96"
    baidu_url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apikey + "&client_secret=" + secretkey;
    y_post=urllib2.urlopen(baidu_url)
    y_read=y_post.read()
    y_token=json.loads(y_read)['access_token']

    # 语音识别
    def luyin():
            print '开始录音'
            os.system('arecord  -D plughw:1,0 -c 1 -d 4  1.wav -r 8000 -f S16_LE 2>/dev/null')
    def asr():
            mac_address="cxlwill"
            with open("1.wav",'rb') as f:
                s_file = f.read()

            speech_base64=base64.b64encode(s_file).decode('utf-8')
            speech_length=len(s_file)
            data_dict = {'format':'wav', 'rate':8000, 'channel':1, 'cuid':mac_address, 'token':y_token, 'lan':'zh', 'speech':speech_base64, 'len':speech_length}
            json_data = json.dumps(data_dict).encode('utf-8')
            json_length = len(json_data)
            asr_server = 'http://vop.baidu.com/server_api'
            request = urllib2.Request(url=asr_server)
            request.add_header("Content-Type", "application/json")
            request.add_header("Content-Length", json_length)
            fs = urllib2.urlopen(url=request, data=json_data)
            result_str = fs.read().decode('utf-8')
            json_resp = json.loads(result_str)
            if json_resp.has_key('result'):
                    out_txt=json_resp['result'][0]
            else:
                    out_txt="Null"
            return out_txt.encode("utf-8")
    # 语音合成
    def getHtml(url):
        page = urllib.urlopen(url)
        html = page.read()
        return html

    def hecheng(text):
        geturl="http://tsn.baidu.com/text2audio?tex="+ text+"&lan=zh&per=3&pit=9&spd=5&cuid=CCyo6UGf16ggKZGwGpQYL9Gx&ctp=1&tok="+y_token
        return os.system('mpg123 "%s"'%(geturl))
    # 图灵机器人
    def tuling(info):
        key = 'cb5824964a874ecbb62313892b2fe056'
        api = 'http://www.tuling123.com/openapi/api?key=' + key + '&userid=master&loc=福建省厦门市&info='
        request = api + info
        response = getHtml(request)
        dic_json = json.loads(response)
        text = dic_json['text']
        return text

if __name__ == '__main__':
    while True:
        Chatbot.luyin()
        out=Chatbot.asr()
        if out != 'Null' :
            print '我:'.decode('utf-8') + out
            text = Chatbot.tuling(out)
            print '魔镜: '.decode('utf-8') + text
            Chatbot.hecheng(text)
            time.sleep(1)
            Chatbot.luyin()
            out=Chatbot.asr()
        else:
                print '我:'.decode('utf-8') + out
                print '聊天结束'
        

