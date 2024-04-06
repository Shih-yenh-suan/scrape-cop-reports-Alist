# -*- encoding: utf-8 -*-
import requests
import re
import datetime
import os
import tempfile
import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from constant import *
from utils import *


class FuncScraper:
    def __init__(self, customer_req):
        self.file_type = customer_req["file_type"]
        self.root_file_path = customer_req["root_file_path"]
        self.使用关键词而非巨潮分类 = customer_req["使用关键词而非巨潮分类"]
        self.start_date = customer_req["start_date"]
        self.end_date = customer_req["end_date"]
        self.interval = customer_req["interval"]
        self.reverseInterval = customer_req["reverseInterval"]
        self.ifMultiThread = customer_req["ifMultiThread"]
        self.is_duplicate_not_allowed = FILE_INFO_JSON[self.file_type]["is_duplicate_not_allowed"]
        self.cnInfoColumn = FILE_INFO_JSON[self.file_type]["cn_info_column"]
        self.cnInfoCategory = FILE_INFO_JSON[self.file_type]["cn_info_category"]
        self.must_contain_word = list(set(
            word for item in FILE_INFO_JSON[self.file_type]["search_keys"] for word in jieba.lcut(item)))

    def process_page_for_downloads(self, pageNum):
        """处理指定页码的公告信息并下载相关文件"""
        DATA['pageNum'] = pageNum
        DATA['column'] = self.cnInfoColumn
        if self.使用关键词而非巨潮分类 == 0:
            DATA['category'] = self.cnInfoCategory
        # 向网站获取内容和总页数，必须分开获取，否则容易报错
        result = retry_on_failure(lambda:
                                  requests.post(URL, data=DATA, headers=HEADERS).json()['announcements'])
        maxpage = retry_on_failure(lambda:
                                   requests.post(URL, data=DATA, headers=HEADERS).json()['totalpages']) + 1
        if result is None or pageNum > maxpage:
            print(f"第 {pageNum} 页已无内容或超出最大页数，退出")
            return False

        # 决定是否开启多线程
        if self.ifMultiThread == 1:
            # 开启多线程处理
            print(f'多线程处理第 {pageNum} 页，共 {maxpage} 页')
            with ThreadPoolExecutor(max_workers=20) as executor:
                executor.map(self.process_announcements, result)
            return True
        else:
            print(f'单线程处理第 {pageNum} 页，共 {maxpage} 页')
            for i in result:
                self.process_announcements(i)

    def process_announcements(self, i):
        """处理返回的json文件"""
        # 处理标题
        title = i['announcementTitle']
        title = re.sub(r'(<em>|</em>|[\/:*?"<>| ])', '', title)
        # 获取下载链接
        downloadUrl = 'http://static.cninfo.com.cn/' + i['adjunctUrl']
        # 处理时间
        announcementTime = i["announcementTime"]/1000
        announcementTime = datetime.datetime.fromtimestamp(
            announcementTime).strftime('%Y-%m-%d')
        # 处理简称
        secName = i['secName'] if i['secName'] is not None else 'None'
        secName = re.sub(r'\*ST', '＊ST', secName)
        secName = re.sub(r'(<em>|</em>|em|[\/:*?"<>| ])', '', secName)
        secName = re.sub(r'Ａ', 'A', secName)
        secName = re.sub(r'Ｂ', 'B', secName)
        # 处理代码。如果代码为空，则从企业唯一的id获得
        secCode = i['secCode']
        if secCode == None:
            secCode = i['orgId'][5:11]
        # 处理文件后缀
        file_suffix = 'html' if i['adjunctType'] == None else 'pdf'
        # 处理会计年度
        seYear = re.search(r'20\d{2}', title)
        seYear = str(int(announcementTime[0:4]) -
                     1) if seYear is None else seYear.group()
        # 整合文件名
        # fileName：保存到本地的文件名
        # fileShortName：输出打印时显示的名字
        if any(word in self.file_type for word in ["社会责任", "ESG", "CSR"]):
            # 对于CSR报告，处理后缀
            csr_tag = get_CSR_tag(title)
            if csr_tag == "":
                return
            fileShortName = rf'{secCode}_{seYear}_{csr_tag}_{secName}'
            fileName = rf'{fileShortName}_{title}_{announcementTime}.{file_suffix}'
        elif self.is_duplicate_not_allowed == 1:
            # is_duplicate_not_allowed时，用企业-年份作为主键
            # 默认从标题中检索年份数据，
            # 如果标题中没说，就从发布日期中减1
            # 因为一年发布一份的报告一般是次年更新，所以年份减1
            fileShortName = f'{secCode}_{seYear}_{secName}'
            fileName = f'{fileShortName}_{title}_{announcementTime}.{file_suffix}'
        else:
            fileShortName = f'{secCode}_{announcementTime}_{secName}'
            fileName = f'{fileShortName}_{title}.{file_suffix}'

        # 接下来开始执行下载前的判断
        # 1. 对于标题包含停用词的报告，跳过下载
        if any(re.search(k, title) for k in FILE_INFO_JSON[self.file_type]["stopwords_list"]):
            print(f'{fileShortName}：\t包括停用词 ({title})')
            return

        # 2. 如果要求标题中带有关键词，则跳过下载不包含关键词的报告
        if self.使用关键词而非巨潮分类 == 1:
            if not any(re.search(k, title) for k in self.must_contain_word):
                print(f'{fileShortName}：\t不含关键词 ({title})')
                return

        # 3. 对于当前目录下已经存在的报告，跳过下载
        SAVING_PATH = f'{self.root_file_path}\{self.file_type}'
        if not os.path.exists(SAVING_PATH):
            os.makedirs(SAVING_PATH)
        filePath = os.path.join(SAVING_PATH, fileName)
        if os.path.exists(filePath):
            # # 判断是否存在
            print(f'{fileShortName}：\t已存在，跳过下载')
            return

        # 4. 对于记录在文件中的报告，跳过下载
        LOCK_FILE_PATH = f'{self.root_file_path}\{self.file_type}\{self.file_type}.txt'
        if not os.path.exists(LOCK_FILE_PATH):
            with open(LOCK_FILE_PATH, 'w') as file:
                pass
        with open(LOCK_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as lock_file:
            downloaded_files = lock_file.readlines()
            if f'{fileName}\n' in downloaded_files:
                print(f'{fileShortName}：\t已记录在文件中')
                return

        # 5. 在不允许年度重复的情况下，对于没有记录但是已经有同一代码、同一时间报告的文件，比对日期，如果日期更新则下载，否则不下载
        if self.is_duplicate_not_allowed == 1:
            compare_latest_report(
                downloaded_files, announcementTime, fileShortName)
        # 6. 一切都符合要求，分块下载文件，并只在下载完成后才保存到本地
        try:
            with requests.get(downloadUrl, stream=True) as r:
                r.raise_for_status()
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            tmp_file.write(chunk)
                    temp_name = tmp_file.name
            shutil.move(temp_name, filePath)
            print(f'{fileShortName}：\t已下载到 {filePath}')
            # 下载完成后，保存文件名到记录中。
            with open(LOCK_FILE_PATH, 'a', encoding='utf-8', errors='ignore') as lock_file:
                lock_file.write(f'{fileName}\n')
        except Exception as e:
            print(f'{fileShortName}： \t下载失败: {e}')

    def CircleScrape(self, DATA_RANGE):
        for i, seDate in enumerate(DATA_RANGE):
            DATA['seDate'] = seDate
            print(f"当前爬取区间：{seDate}，为列表第 {i+1}/{len(DATA_RANGE)} 个")
            pageNum = 1
            while True:
                if not self.process_page_for_downloads(pageNum):
                    break
                # 有时候会出现奇怪的bug导致迟迟无法结束，故设定500页的最大值强行停止
                if pageNum >= 500:
                    break
                pageNum += 1
            if seDate[3] != seDate[14]:
                print(f'{seDate[:4]} 年的年报已下载完毕.')
