from time import sleep
from bs4 import BeautifulSoup
import re


def UnicodeCorr(html):
    try:
        html = html.encode('gbk', 'ignore').decode('gbk', 'ignore')
    except UnicodeError:
        pass
    return html


def GetHtml(browser, saveFile, url=None):
    if url:
        browser.get(url)
    html = BeautifulSoup(browser.page_source, 'lxml')
    html = html.prettify()
    html = UnicodeCorr(html)
    with open(saveFile, 'w') as page:
        page.write(html)


def GetHtmlTxt(browser, url=None):
    if url:
        browser.get(url)
    html = BeautifulSoup(browser.page_source, 'lxml')
    html = html.prettify()
    return html


def GetBrowserTxt(browser):
    html = BeautifulSoup(browser.page_source, 'lxml')
    html = html.prettify()
    return html


def containChinese(txt):

    if re.findall(r'[\u4e00-\u9fff]+', txt):
        return True
    else:
        return False
