from time import sleep
from bs4 import BeautifulSoup
import re


def stringPurify(string, delChar=None):
    string = string.replace('\n', '')
    if delChar:
        for i in delChar:
            string = string.replace(i, '')
    return string.strip()


def UnicodeCorr(html):
    try:
        html = html.encode('gbk', 'ignore').decode('gbk', 'ignore')
    except UnicodeError:
        pass
    return html


def html2soup(html_txt):
    soup = None
    if '\n' in html_txt:
        soup = BeautifulSoup(html_txt, 'lxml')
    elif os.path.isfile(html_txt):
        with open(html_txt, encoding='gbk') as f:
            html = f.read()
            # try:
            #     html = html.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
            # except UnicodeError:
            #     pass
            start = time.clock()
            soup = BeautifulSoup(html, 'lxml')
            # soup = soup.prettify('gbk')
    else:
        raise ValueError('URL converted to soup error')
    return soup


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
