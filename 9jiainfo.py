import os
import sys
import json
import time
import schedule
from dingtalkchatbot.chatbot import DingtalkChatbot
from colorama import *

def job():
    try:
        citycode = sys.argv[1]
        print(Fore.GREEN + '输入的地区代码为: ' + citycode)
    except IndexError:
        print(Fore.RED + 'usage: python3 9jiainfo.py cd')
    try:    
        command = 'curl -H "Host: wxapidg.bendibao.com" -H "content-type: application/json" -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001034) NetType/4G Language/zh_CN" -H "Referer: https://servicewechat.com/wx2efc0705600eb6db/130/page-frame.html" --compressed "https://wxapidg.bendibao.com/smartprogram/zhuanti.php?platform=wx&version=21.12.06&action=jiujia&citycode={}"'.format(citycode)
    except UnboundLocalError:
        print(Fore.RED + '请输入地区代码，如成都为cd,北京为bj')
    try:
        print(Fore.GREEN +'执行curl命令为:\n' + command)
        a1 = os.popen(command)
        b1 = a1.read()
        print(Fore.GREEN + '[+]---------------初始化请求完毕，等待半个小时后进行第二次请求---------------[+]' + time.ctime())
        time.sleep(60) # 半个小时比较一次
        a2 = os.popen(command)
        b2 = a2.read()
        b2 = b2
        print(Fore.GREEN + '[+]---------------间隔时间后的第二次请求完毕，进行内容比较---------------[+]' + time.ctime())
        r = json.loads(b2)
        data = r['data']
        jiujia = data['website']
        place = jiujia['place']
        try:
            global c
            c = ''
            for i in range(0,5):
                c0 = '[+]---预约(抢)时间---[+]'+place[i]['yy_time'] +' '+ place[i]['name']+'    '+'[+]---数量---: '+place[i]['minge']+'   '+place[i]['method']+'---预约平台---[+]'+place[i]['platform']
                c += c0 + '\n'
        except IndexError:
                pass
        print(c)
        if b2 not in b1:
            print(Fore.GREEN + '[+]---------------九价信息更新了，将进行推送---------------[+]' + time.ctime())
        if b2 in b1:
            c = '九价信息暂未更新'
            print(Fore.RED + '[-]---------------九价信息暂未更新，推送未更新---------------[-]' + time.ctime())
        time.sleep(60) # 是否要在内容比较后，再进行时间等待
    except UnboundLocalError:
        sys.exit(2)

def push():
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=xxx'
    secret = 'xxx'  # 可选：创建机器人勾选“加签”选项时使用
    # 初始化机器人小丁
    # xiaoding = DingtalkChatbot(webhook)  # 方式一：通常初始化方式
    xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
    # xiaoding = DingtalkChatbot(webhook, pc_slide=True)  # 方式三：设置消息链接在PC端侧边栏打开（v1.5以上新功能）
    # Text消息@所有人
    xiaoding.send_text(msg=c, is_at_all=True)

schedule.every(2).minutes.do(push)
#schedule.every(1).hour.do(push) #  1个小时推送一次
def out():
    if int(time.strftime('%H',time.localtime())) < 8:
        print(Fore.RED + '[-]---------------休息时间，不进行推送---------------[-]' + time.ctime())
        sys.exit(0)   
    elif int(time.strftime('%H',time.localtime())) > 21:
        print(Fore.RED + '[-]---------------休息时间，不进行推送---------------[-]' + time.ctime())
        sys.exit(0)

while True:
    out()
    job()
    schedule.run_pending()
    time.sleep(1)