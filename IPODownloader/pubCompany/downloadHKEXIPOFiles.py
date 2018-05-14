from siteSpider import SiteSpider
from searchAgent import HKEXSearchAgent
from utils import *
from time import sleep
import excel
from selenium.common.exceptions import WebDriverException
from downloader import Downloader
import random

spider = SiteSpider('hkex')
data = spider.spider('http://www.hkexnews.hk/APP/SEHKYear2017_c.htm')
# print(data)
# spider.write_excel()
spider.close()
nameList = []

for i in data:
    if i[2] == '已上市':
        stock_name = i[1][0]
        if ' Limited' in stock_name:
            stock_name = stock_name.replace(' Limited', '')
        if ' Ltd' in stock_name:
            stock_name = stock_name.replace(' Ltd', '')
        if len(stock_name) > 20:
            if containChinese(stock_name):
                nameList.append([stock_name, stock_name[:20]])
            else:
                short_name = stock_name

                while len(short_name) > 20:
                    short_name = short_name[:short_name.rfind(' ')]
                    nameList.append([stock_name, short_name])
        else:
            nameList.append([stock_name])
# for i in nameList:
#     print(len(i))
print(nameList)
hkexAgent = HKEXSearchAgent()
download_name_list = []
download_url_list = []
undownload_name_list = []
for i in nameList:
    print('Searching ' + i[-1])
    url = hkexAgent.searchForFile(i[-1], ['股份', '配售', '全球', '預覽資料集'])
    print(i, url)
    if not url:
        undownload_name_list.append(i)
    else:
        download_name_list.append(i[0])
        download_url_list.append(*url)
    sleep(2 * random.random())
excelwriter = excel.ExcelWriter()
excelwriter.write(download_name_list, 'dname.xlsx')
excelwriter.write(download_url_list, 'durl.xlsx')
excelwriter.write(undownload_name_list, 'udname.xlsx')

downloader = Downloader(download_url_list, download_name_list)
downloader.download()
# hkexAgent.close()
