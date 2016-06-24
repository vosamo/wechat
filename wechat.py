#!/usr/bin/env python
# coding=utf-8
import os
import urllib2
import json
import time
import datetime

# 公众平台测试号信息
APPID = 'xxxx'
APPSECRET = 'xxxx'
TOKEN_FILE = 'token.txt'

def build_time_interval(interval):
    now = datetime.datetime.now()
    delta = datetime.timedelta(seconds=interval)
    now_interval = now + delta
    return now_interval.strftime('%Y-%m-%d %H:%M:%S')

def save_token(TOKEN_FILE):
    '''
    通过请求token_url获取access_token;
    保存access_token和过期时间expires_in在TOKEN_FILE中
    :param TOKEN_FILE:
    :return:
    '''
    token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID,APPSECRET)
    f = urllib2.urlopen(token_url)
    j = json.loads(f.read())
    access_token = j['access_token']
    expires_in = j['expires_in']
    with open(TOKEN_FILE, 'w') as tf:
        # 将过期时间减去300s后加上当前时间保存
        content = '%s,%s' % (access_token, build_time_interval(int(expires_in)-300))
        tf.write(content)
    return access_token

def check_token_expire(expires_in):
    '''
    将当前时间与token过期时间比较判断token是否过期
    :param expires_in:
    :return:
    '''
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if curr_time > expires_in:
        return True
    else:
        return False


def load_token(TOKEN_FILE):
    '''
    从token文件中载入access_token，需要判度access_token是否过期；
    如果过期的话调用save_token()方法重新请求token_url获取新的access_token
    :param TOKEN_FILE:
    :return:
    '''
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), TOKEN_FILE)):
        access_token = save_token(TOKEN_FILE)
    with open(TOKEN_FILE,'r') as tf:
        line = tf.read()
        if line:
            access_token = line.split(',')[0]
            expires_in = line.split(',')[1]
            if check_token_expire(expires_in):
                access_token = save_token(TOKEN_FILE)
            return access_token
        else:
            access_token = save_token(TOKEN_FILE)
            return access_token

def weixin_push(content):
    '''
    向关注者群发消息
    :param content:
    :return:
    '''
    access_token = load_token(TOKEN_FILE)
    # 群发文字消息测试
    push_url = 'https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=' + access_token
    data = {
        "filter":{
                  "is_to_all":True,
               
        },
        "text":{
                  "content":content,
               
        },
            "msgtype":"text"

    }
    #f = urllib2.urlopen(push_url, data)
    f = urllib2.urlopen(push_url, json.dumps(data, ensure_ascii=False, indent=2))
    j = f.read()
    print j
if __name__ == '__main__':
    weixin_push('你好')
