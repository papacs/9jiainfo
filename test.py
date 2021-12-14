import time

print(int(time.strftime('%H',time.localtime())))

if int(time.strftime('%H',time.localtime())) < 8:
    print('休息时间，不进行进行推送')
elif int(time.strftime('%H',time.localtime())) > 22:
    print('休息时间，不进行推送')
