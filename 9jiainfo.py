import os
import re
import time
import schedule
from dingtalkchatbot.chatbot import DingtalkChatbot

def job():

    command = 'curl -H "Host: wxapidg.bendibao.com" -H "content-type: application/json" -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001034) NetType/4G Language/zh_CN" -H "Referer: https://servicewechat.com/wx2efc0705600eb6db/130/page-frame.html" --compressed "https://wxapidg.bendibao.com/smartprogram/zhuanti.php?platform=wx&version=21.12.06&action=jiujia&citycode=cd"'
    a = os.popen(command)
    b = a.read()
    c = b.encode('utf-8').decode('unicode_escape')
    res = re.match("<span[^>]*>",c)
    print(res)
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=62d1d50be827620e9d4f60c4176d45a8ba782a55b0d4ef4db6f83841496bc2eb'
    secret = 'SEC03aa8dc5345a448f8cf01899547945444cdfdfcc2686b2eea0f0f2bd2ab6f87a'  # 可选：创建机器人勾选“加签”选项时使用
    # 初始化机器人小丁
    # xiaoding = DingtalkChatbot(webhook)  # 方式一：通常初始化方式
    xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
    # xiaoding = DingtalkChatbot(webhook, pc_slide=True)  # 方式三：设置消息链接在PC端侧边栏打开（v1.5以上新功能）
    # Text消息@所有人
    xiaoding.send_text(msg=c, is_at_all=True)
    print("I'am working……")

schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
