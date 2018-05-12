from selenium import webdriver

from time import sleep
from bs4 import BeautifulSoup
import os
import os.path as osp
import random
import re
import decoder
import translator
from tableExtractor import Extractor
from utils import *
from selenium.common.exceptions import WebDriverException


class HKEXSearchAgent(object):
    """docstring for HKEXSearch
    hkexAgent = HKEXSearchAgent()
    # 搜索指定上市公司的招股书
    url = hkexAgent.searchForFile(Stock_name, ['股份', '配售', '全球', '預覽資料集'])
    """

    def __init__(self):
        super(HKEXSearchAgent, self).__init__()
        self.searchEngine = 'http://www.hkexnews.hk/listedco/listconews/advancedsearch/search_active_main_c.aspx'
        self._browser = webdriver.Chrome()

    @property
    def browser(self):
        return self._browser

    def close(self):
        self._browser.close()

    def searchForFile(self, stock_name, filenameList, key_word=None):
        # TODO: Enable multi level 
        self.browser.get(self.searchEngine)
        input_stock_name = self.browser.find_element_by_name(
            'ctl00$txt_stock_name')
        input_key_word = self.browser.find_element_by_name('ctl00$txtKeyWord')
        input_select_docs = self.browser.find_element_by_name(
            'ctl00$rdo_SelectDocType')
        input_select_docs.click()

        select_docs_type = self.browser.find_element_by_xpath(
            '//select[@name="ctl00$sel_tier_1"]/option[text()="上市文件"]')
        select_docs_type.click()
        select_docs_subtype = self.browser.find_element_by_xpath(
            '//select[@name="ctl00$sel_tier_2"]/option[text()="發售以供認購"]')
        select_docs_subtype.click()
        input_stock_name.send_keys(stock_name)
        if key_word:
            input_key_word.send_keys(key_word)
        search_btn = self.browser.find_element_by_xpath(
            '//img[@src="/image/search_c.gif"]')
        search_btn.click()
        try:
            jsalert = self.browser.switch_to.alert
            jsalert.accept()
            return []
        except WebDriverException:
            pass
        txt = UnicodeCorr(GetHtmlTxt(self.browser))
        try:
            result = self.fileUrlExtractor(filenameList, txt)
        except IndexError:
            return []
        if result == -1:
            return []
        else:
            return result

    def fileUrlExtractor(self, filenameList, txt):
        soup = decoder.url2soup(txt)
        data = soup.find_all(attrs={'id': 'ctl00_gvMain'})
        table = Extractor(data[0])
        table.parse()
        tablelist = table.return_list()
        resultlist = []
        for i in tablelist:
            if len(i) < 4:
                return -1
            if isinstance(i[3], (list, tuple)):
                if len(i[3]) > 1:
                    filenameFlag = False
                    for fn in filenameList:
                        if fn in i[3][0]:
                            filenameFlag = True
                    if 'PDF' not in i[3][0]:
                        continue
                    if filenameFlag:
                        resultlist.append(i[3][1])
        for i in range(len(resultlist)):
            txt = resultlist[i]
            base = self.browser.current_url
            base = base.replace('//', '$')
            base = base[:base.find('/')]
            base = base.replace('$', '//')
            resultlist[i] = base + txt
        return resultlist


def test():
    hkexAgent = HKEXSearchAgent()
    print(hkexAgent.searchForFile('域高國際', '發售以供認購'))


if __name__ == '__main__':
    # browser = webdriver.Chrome()
    # browser.get(
    #     'http://www.hkexnews.hk/listedco/listconews/advancedsearch/search_active_main_c.aspx')
    # input_stock_name = browser.find_element_by_name('ctl00$txt_stock_name')
    # input_key_word = browser.find_element_by_name('ctl00$txtKeyWord')

    # input_stock_name.send_keys('域高國際')
    # input_key_word.send_keys('股份發售')
    # search_btn = browser.find_element_by_xpath(
    #     '//img[@src="/image/search_c.gif"]')
    # search_btn.click()
    # txt = UnicodeCorr(GetHtmlTxt(browser))
    # print(txt)
    # # print(search_btn)

    # soup = decoder.url2soup(txt)
    # data = soup.find_all(attrs={'id': 'ctl00_gvMain'})
    # table = Extractor(data[0])
    # table.parse()
    # tablelist = table.return_list()
    # for i in tablelist:
    #     print(i[3])
    hkexAgent = HKEXSearchAgent()
    print(hkexAgent.searchForFile('金盾控股', ['股份', '全球', '預覽資料集']))
    try:
        jsalert = hkexAgent.browser.switch_to.alert
        jsalert.accept()
    except WebDriverException:
        pass
    # hkexAgent.close()
