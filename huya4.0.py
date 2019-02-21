#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import requests
import re
import os
import threading
import time
import datetime
import random

class HuyaLive():
    def __init__(self,url):
        # 必须的访问地址和访问头
        self.url = url
        self.headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}

    def prepare(self):
        # 获得页面html字符串
        response = requests.get(self.url,headers=self.headers)
        html = response.content.decode()

        # 加载json
        json_script = re.search('"stream": ({.+?})\s*};', html).group(1)
        print(json_script)
        data = json.loads(json_script)

        # 获取视频流
        room_info = data['data'][0]['gameLiveInfo']
        stream_info = random.choice(data['data'][0]['gameStreamInfoList'])
        sFlvUrl = stream_info['sFlvUrl']
        sStreamName = stream_info['sStreamName']
        sFlvUrlSuffix = stream_info['sFlvUrlSuffix']
        sFlvAntiCode = stream_info['sFlvAntiCode']
        flv_url = '{}/{}.{}?{}'.format(sFlvUrl, sStreamName, sFlvUrlSuffix, sFlvAntiCode)
        # 打印视频流地址
        print("current url = ",flv_url)

        # 利用ffmpeg进行录屏
        filename = datetime.datetime.today()
        filename = filename.strftime('%Y-%m-%d%H:%M:%S')
        filename = filename + '.flv'
        print(filename) # 文件名称类似'%Y-%m-%d%H:%M:%S.flv'格式
        # 文件保存的目录，我把文件存在硬盘上面了
        file_path = "/media/ych/Seagate\ Backup\ Plus\ Drive/zhibo"
        os.system('ffmpeg -user-agent "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36" -i {} -c copy {}'.format('"%s"' % flv_url, os.path.join(file_path,filename)))


    def run(self):
        # 判断是否开播
        global anchor_status # 是否开播的标记
        response = requests.get(self.url, headers=self.headers)
        html = response.content.decode()
        anchor_status = re.findall("上次开播(.*?)</span>" , html)
        # 开播返回None，不开播返回列表
        if anchor_status:
            print("尚未开播")
        else:
            print("正在直播")


    def change_status(self):
        # 判断是否开播的线程
        print("------change------")
        while True:
            try:
                self.run()
                # 随机对直播间进行访问，为防止爬虫被封
                time.sleep(random.randint(10,30))
            except:
                # 如果ip被封或报错，休息60s后继续访问
                time.sleep(60)



    def recording(self):
        global flag,anchor_status
        # 进行录屏的线程
        while True:
            print("-------recoding-------")
            print(len(anchor_status) == 0)
            print(flag)
            time.sleep(5)
            if len(anchor_status) == 0 and flag:
                print("---get into self prepare")
                # 进行录屏
                try:
                    self.prepare()
                    flag = False
                except:
                    pass
            elif len(anchor_status) != 0:
                flag = True



anchor_status = ["1"]
flag = True


if __name__ == '__main__':
    temp_url = "http://www.huya.com/{}"
    room_name = input("请输入直播间房间号，例如“920710”：")
    request_url = temp_url.format(room_name)
    site = HuyaLive(request_url)
    change = threading.Thread(target=site.change_status)
    ffm = threading.Thread(target=site.recording)
    # 开始运行程序
    change.start()
    ffm.start()

