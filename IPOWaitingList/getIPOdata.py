from selenium import webdriver
browser = webdriver.Chrome()
from time import sleep
from bs4 import BeautifulSoup
import os
import os.path as osp
import random
import decoder
import csv
import excel


def GetHtml(url, saveFile):
    browser.get(url)
    html = BeautifulSoup(browser.page_source, 'lxml')
    html = html.prettify()
    try:
        html = html.encode('gbk', 'ignore').decode('gbk', 'ignore')
    except UnicodeError:
        pass
    with open(saveFile, 'w') as page:
        page.write(html)


def GetHtmlTxt(url):
    browser.get(url)
    html = BeautifulSoup(browser.page_source, 'lxml')
    html = html.prettify()
    return html


class SiteSpider(object):
    """docstring for SiteSpider"""

    def __init__(self, target):
        super(SiteSpider, self).__init__()
        self._siteBaseDict = {
            'nyse': 'https://www.nyse.com/ipo-center/filings',
            'nasdaq': 'https://www.nasdaq.com/markets/ipos/activity.aspx?tab=###',
            'hkex': 'http://www.hkexnews.hk/APP/SEHKAPPMainIndex_c.htm'
        }
        self._spiderDict = {
            'nyse': self.spiderNYSE,
            'nasdaq': self.spiderNASDAQ,
            'hkex': self.spiderHKEX
        }
        if target in self._spiderDict.keys():
            self.target = target
            self.spiderMethod = self._spiderDict[self.target]
        else:
            raise ValueError('Site spider not implemented')

    def write_csv(self, path=os.getcwd(), filename='_output.csv'):
        if filename == '_output.csv':
            filename = self.target + filename
        with open(osp.join(path, filename), 'w') as csv_file:
            table_writer = csv.writer(csv_file)
            for row in self.data:
                table_writer.writerow(row)
        return

    def write_excel(self, path=os.getcwd(), filename='_output.xlsx'):
        if filename == '_output.xlsx':
            filename = self.target + filename
        excelWriter = excel.ExcelWriter(osp.join(path, filename))
        excelWriter.write(self.data, filename)

    def spider(self):
        return self.spiderMethod()

    def spiderNYSE(self):
        html = GetHtmlTxt(self._siteBaseDict[self.target])
        de = decoder.PageDecoder(self.target)
        de.decode(html)
        self.data = de.data()
        return self.data

    def spiderNASDAQ(self):

        self.data = []
        replace_list = ['pricings', 'upcoming', 'filings', 'withdrawn']
        for i in replace_list:
            html = GetHtmlTxt(
                self._siteBaseDict[self.target].replace('###', i))
            de = decoder.PageDecoder(self.target)
            de.decode(html)
            self.data += de.data()
            sleep()
        return self.data

    def spiderHKEX(self):
        html = GetHtmlTxt(self._siteBaseDict[self.target])
        de = decoder.PageDecoder(self.target)
        de.decode(html)
        self.data = de.data()
        return self.data


if __name__ == '__main__':
    url = 'https://www.nyse.com/ipo-center/filings'
    save_file = 'nyse.html'
    # GetHtml(url, saveFile)
    # GetHtml(
    # 'https://www.nasdaq.com/markets/ipos/activity.aspx?tab=withdrawn', 'nasdaq.html')
    # GetHtml('http://www.hkexnews.hk/APP/SEHKAPPMainIndex_c.htm', 'hkex.html')
    # html = GetHtmlTxt(
    #     'http://www.hkexnews.hk/APP/SEHKAPPMainIndex_c.htm')
    # print(decoder.decodeHKEX(html))
    spider = SiteSpider('hkex')
    print(spider.spider())
    spider.write_excel()
