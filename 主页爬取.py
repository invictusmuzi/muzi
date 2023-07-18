#抖音某一博主主页所有视频爬取（实例url：https://www.douyin.com/user/MS4wLjABAAAANNFp-QTeUoKhsIUY9_xNomy6rz3lZRmDQ6nHDnvKt0M?showTab=post）
import requests
import re
import time
import json
import os

#文件保存路径
SAVE_ROOT = "D:/..."

class CarwlMajority:
    def __init__(self):
        self.id = 0
        self.video_info_list = []  # 视频列表
        self.picture_info_list = []  # 图片列表
        self.author_name = ''
        self.sec_uid = ''
        self.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; ''Nexus 5 Build/MRA58N) AppleWebKit/537.36 ('
                                      'KHTML, '
                                      'like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
                        'referer': 'https://www.douyin.com/',
                        'cookie': '自己的 cookie'
                        }

    def acquire_id(self):
        self.id += 1
        return self.id

    def get_url(self, user_in):
        sec_uid = re.findall('douyin.com/user/(.*)\?', user_in)
        if len(sec_uid) == 0:
            sec_uid = re.findall('douyin.com/user/(.*)', user_in)
        if len(sec_uid) == 0:
            raise Exception("url格式异常,请查看")
        self.sec_uid = sec_uid[0]

    def get_video_info(self):
        max_cursor = 0
        print('解析页面中...')
        while 1:
            pageurl = f'https://www.douyin.com/aweme/v1/web/aweme/post/?aid=6383&sec_user_id={self.sec_uid}&count=10&max_cursor={max_cursor}&publish_video_strategy_type=2'
            listpage = requests.get(url=pageurl, headers=self.headers).text
            listpage = json.loads(listpage)
            if listpage["has_more"] == 0:
                break
            if max_cursor == 0:
                self.author_name = listpage['aweme_list'][0]['author']['nickname']  # 获取作者名称
            max_cursor = listpage["max_cursor"]  # 当页页码
            for i1 in listpage["aweme_list"]:
                #  视频收集
                if i1["images"] is None:
                    url = i1["video"]["play_addr"]["url_list"][0]
                    self.video_info_list.append(url)
                #  图片收集
                else:
                    self.picture_info_list += list(map(lambda x: x["url_list"][-1], i1["images"]))
        print('共解析到' + str(len(self.video_info_list)) + '个视频,' + str(len(self.picture_info_list)) + '张图片')

    def download(self, url):
        data = requests.get(url=url, headers=self.headers).content
        with open(f'{self.acquire_id()}.mp4', 'wb') as f:  # 存入当前目录
            f.write(data)

    def download_pic(self, url):
        data = requests.get(url=url, headers=self.headers).content
        with open(f'{self.acquire_id()}.jpg', 'wb') as f:  # 存入当前目录
            f.write(data)

    def crawl_main(self, user_in):
        start_time = time.time()
        print('程序启动...')
        self.get_url(user_in)
        self.get_video_info()
        save_folder = os.path.join(SAVE_ROOT, self.author_name)
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        os.chdir(save_folder)
        print('正在批量下载,请耐心等待...')
        for url in self.video_info_list:
            self.download(url)
        for url in self.picture_info_list:
            self.download_pic(url)
        end_time = time.time()
        cost_time = format(end_time - start_time, '.2f')
        print('下次完成，共花费时间' + cost_time + 's')

if __name__ == '__main__':
    userurl = input('---------------请在此粘贴您的链接---------------\n')
    a = CarwlMajority()
    a.crawl_main(userurl)
