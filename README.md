# 9jiainfo, 钉钉群聊机器人推送九价实时信息



## 效果

![](assets/16392866149648.jpg)


电脑端
![](assets/16392866914408.jpg)


手机端
![](assets/16392866448279.jpg)


配置

- 需要安装额外两个库:

```
python3 -m pip install schedule
python3 -m pip install dingtalkchatbot
```

![](assets/16392079543425.jpg)

- 修改webhook和secret为自己创建钉钉群聊机器人时，系统默认分配的


## 运行

`python3 9jiainfo.py`

或者挂在vps上

`nohup python3 9jiainfo.py`

## 更新

切换到项目文件夹的目录下，执行:

```
git pull
```

## 更新日志

- V0.0.1 demo version，开源GitHub

- V0.0.2 修改信息源，即更新请求的URL
- V0.0.3 
  - 增加内容更新判断
  - 增加地区选择



## 问题

- 欢迎提交issues，贴上完整的报错以及截图

## Todo

- [x] 内容更新判断
- [x] 地区选择

- [ ] 简化内容(格式化获取到的内容)