from selenium import webdriver
browser = webdriver.Chrome()
from time import sleep
from bs4 import BeautifulSoup
import os.path as osp
import random
import decoder


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


if __name__ == '__main__':
    url = 'https://www.nyse.com/ipo-center/filings'
    save_file = 'nyse.html'
    # GetHtml(url, saveFile)
    # GetHtml(
    # 'https://www.nasdaq.com/markets/ipos/activity.aspx?tab=pricings', 'nasdaq.html')
    # GetHtml('http://www.hkexnews.hk/APP/SEHKAPPMainIndex_c.htm', 'hkex.html')
    html = GetHtmlTxt(
        'http://www.hkexnews.hk/APP/SEHKAPPMainIndex_c.htm')
    print(decoder.decodeHKEX(html))
