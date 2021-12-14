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
        time.sleep(1800) # 半个小时比较一次
        a2 = os.popen(command)
        b2 = a2.read()     
        print(Fore.GREEN + '[+]---------------间隔时间后的第二次请求完毕，进行内容比较---------------[+]' + time.ctime())
        r = json.loads(b2)
        data = r['data']
        jiujia = data['website']
        place = jiujia['place']
        c0 = "[+]---预约(抢)时间---[+]"+place[0]['yy_time']+' '+ place[0]['name']+'    '+"[+]---数量---: "+place[0]['minge']+'   '+place[0]['method']+"---预约平台---[+]"+place[0]['platform']
        c1 = "[+]---预约(抢)时间---[+]"+place[1]['yy_time']+' '+ place[1]['name']+'    '+"[+]---数量---: "+place[1]['minge']+'   '+place[1]['method']+"---预约平台---[+]"+place[1]['platform']
        c2 = "[+]---预约(抢)时间---[+]"+place[2]['yy_time']+' '+ place[2]['name']+'    '+"[+]---数量---: "+place[2]['minge']+'   '+place[2]['method']+"---预约平台---[+]"+place[2]['platform']
        c3 = "[+]---预约(抢)时间---[+]"+place[3]['yy_time']+' '+ place[3]['name']+'    '+"[+]---数量---: "+place[3]['minge']+'   '+place[3]['method']+"---预约平台---[+]"+place[3]['platform']
        c4 = "[+]---预约(抢)时间---[+]"+place[4]['yy_time']+' '+ place[4]['name']+'    '+"[+]---数量---: "+place[4]['minge']+'   '+place[4]['method']+"---预约平台---[+]"+place[4]['platform']
        global c
        c = c0 + '\n' + c1 + '\n' + c2 + '\n' + c3+ '\n' + c4
        print(c)
        if b2 not in b1:
            print(Fore.GREEN + '[+]---------------九价信息更新了，将进行推送---------------[+]' + time.ctime())
        if b2 in b1:
            c = '九价信息暂未更新'
            print(Fore.RED + '[-]---------------九价信息暂未更新，推送未更新---------------[-]' + time.ctime())
        time.sleep(1800) # 是否要在内容比较后，再进行时间等待
    except UnboundLocalError:
        sys.exit(2)

def push():
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=62d1d50be827620e9d4f60c4176d45a8ba782a55b0d4ef4db6f83841496bc2eb'
    secret = 'SEC03aa8dc5345a448f8cf01899547945444cdfdfcc2686b2eea0f0f2bd2ab6f87a'  # 可选：创建机器人勾选“加签”选项时使用
    # 初始化机器人小丁
    # xiaoding = DingtalkChatbot(webhook)  # 方式一：通常初始化方式
    xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
    # xiaoding = DingtalkChatbot(webhook, pc_slide=True)  # 方式三：设置消息链接在PC端侧边栏打开（v1.5以上新功能）
    # Text消息@所有人
    xiaoding.send_text(msg=c, is_at_all=True)

#schedule.every(2).minutes.do(push)
schedule.every(1).hour.do(push) #  1个小时推送一次
def out():
    if int(time.strftime('%H',time.localtime())) < 8:
        print(Fore.RED + '[-]---------------休息时间，不进行推送---------------[-]' + time.ctime())
        sys.exit(0)
    elif int(time.strftime('%H',time.localtime())) > 22:
        print(Fore.RED + '[-]---------------休息时间，不进行推送---------------[-]' + time.ctime())
        sys.exit(0)

while True:
    out()
    job()
    schedule.run_pending()
    time.sleep(1)