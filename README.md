# 通过Python调用微信公众号发送消息

## 实施步骤：

首先，你要申请一个微信公众号，可以是订阅号、服务号或者企业号。不过微信的接口权限限制较为严格，为了测试方便我们可以申请一个公众平台测试帐号，测试帐号允许你调用微信公众平台的高级接口，比如群发接口。
本例中就以一个测试帐号来测试公众号的群发接口。

第二步，将源文件中的APPID 和APPSECRET替换成你自己申请的测试帐号的APPID和APPSECRET，然后执行脚本即可。

## 原理介绍：

微信公众号有唯一的APPID和APPSECRET，在获取access_token时会用到；

微信公众号接口的调用凭证是access_token，这个access_token可以通过固定接口获取，access_token的有效期默认为2小时，过期之后要重新申请；

获取access_token:GET方法请求https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID,APPSECRET)

至于发消息的接口和消息格式参考微信公众平台开发文档。
