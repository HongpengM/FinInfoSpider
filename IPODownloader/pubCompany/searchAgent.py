from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from time import sleep
from bs4 import BeautifulSoup
import os
import os.path as osp
from functools import partial
import random
import re
import zhconv
from fuzzywuzzy import fuzz, process
try:
    from tableExtractor import Extractor
    from utils import *
    import decoder
except Exception:
    from .tableExtractor import Extractor
    from .utils import *
    from . import decoder


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
        self.hkex_docs_types = {
            "所有": None,
            "公告及通告": ["所有", "公司狀況變動及委員會/公司變動", "新上市（上市發行人/新申請人）",
                      "會議/表決", "證券/股本", "財務資料", "重組/股權變動/主要改動/公眾持股量/上市地位",
                      "關連交易", "雜項", "須予公布的交易"],
            "通函": ["所有", "公司狀況變動及委員會/公司變動", "會議/表決", "證券/股本", "重組/股權改動/主要改動/公眾持股量/上市地位",
                   "關連交易", "雜項", "須予公布的交易"],
            "上市文件": ["所有", "交換證券或取代原證券", "介紹", "供股", "公開招股", "其他", "按《上市規則》規定視為新上市", "發售以供認購", "發售現有證券",
                     "補充上市文件", "認可集體投資計劃", "資本化發行", "配售上市後的新證券類別"],
            "財務報表/環境、社會及管治資料": ["所有", "中期/半年度報告", "季度報告", "年報", "環境、社會及管治資料/報告"],
            "翌日披露報表": ["所有", "其他", "股份購回"],
            "月報表": None,
            "委任代表表格": None,
            "公司資料報表（GEM）": None,
            "憲章文件": None,
            "債券及結構性產品": ["所有", "債務證券", "牛熊證", "結構性產品發行人的資料", "股票掛鉤票據", "衍生權證", ],
            "交易所買賣基金的交易資料": None,
            "監管者發出的公告及消息": None,
            "股份購回報告 (2009年1月1日前)": None,
            "合併守則 - 交易披露": None,
            "申請版本及聆訊後資料集": ["所有", "申請版本或相關材料", "聆訊後資料集或相關材料"],
            "槓桿及反向產品的交易資料": None,
        }

    @property
    def browser(self):
        '''
        browser used by search Agent
        '''
        return self._browser

    def close(self):
        '''
        close browser 
        '''
        self._browser.close()

    def translate2hk(self, *args):
        '''
        translate zh-hans to zh-hk
        '''
        _result = []
        for i in range(len(args)):
            if args[i]:
                if isinstance(args[i], str):
                    _result.append(zhconv.convert(args[i], 'zh-hk'))
                elif isinstance(args[i], (list, tuple)):
                    _c = []
                    for word in args[i]:
                        _c.append(zhconv.convert(word, 'zh-hk'))
                    _result.append(_c)
            else:
                _result.append(args[i])
        return _result

    def enhanceSearchKeywords(self, stock_name, key_word, docs_type, docs_subtype, fuzzy, translate):
        '''
            Do fuzzy search and translate zh-hans to zh-hk
            ---------------------------------------------
            TODO: enable stock name fuzzy search
        '''
        if translate:
            stock_name, key_word, docs_type, docs_subtype = self.translate2hk(stock_name,
                                                                              key_word, docs_type, docs_subtype)
            # for i in range(len(canconvert)):
            #     if canconvert[i]:
            #         if isinstance(canconvert[i], str):
            #             canconvert[i] = zhconv.convert(canconvert[i], 'zh-hk')
            #         elif isinstance(canconvert[i], (list, tuple)):
            #             _c = []
            #             for word in canconvert[i]:
            #                 _c.append(zhconv.convert(word, 'zh-hk'))
            #             canconvert[i] = _c
            # stock_name,  key_word, docs_type, docs_subtype = canconvert
        if fuzzy:

            if docs_type:
                key_choices = list(self.hkex_docs_types.keys())
                docs_type = process.extractOne(docs_type, key_choices)[0]
                if self.hkex_docs_types[docs_type]:
                    key_choices = list(self.hkex_docs_types[docs_type])
                    docs_subtype = process.extractOne(
                        docs_subtype, key_choices)[0]
                else:
                    docs_subtype = None
            if docs_type == "所有":
                docs_type = None
            if docs_subtype == "所有":
                docs_subtype = None
        print(stock_name, key_word, docs_type, docs_subtype)
        return (stock_name, key_word, docs_type, docs_subtype)

    def search(self, stock_name, key_word, docs_type, docs_subtype, fuzzy=True, translate=True):
        '''
        Advanced Search use HKEXnews engine
        '''
        # TODO: Enable multi level
        stock_name, key_word, docs_type, docs_subtype = self.enhanceSearchKeywords(stock_name,
                                                                                   key_word, docs_type, docs_subtype, fuzzy, translate)
        self.browser.get(self.searchEngine)
        input_stock_name = self.browser.find_element_by_name(
            'ctl00$txt_stock_name')
        input_key_word = self.browser.find_element_by_name(
            'ctl00$txtKeyWord')
        input_select_docs = self.browser.find_element_by_name(
            'ctl00$rdo_SelectDocType')

        # Enter stock name
        input_stock_name.send_keys(stock_name)
        # Enter keyword
        if key_word:
            input_key_word.send_keys(key_word)
        # Select specific docs
        if docs_type:
            input_select_docs.click()
            docs_type_option = '//select[@name="ctl00$sel_tier_1"]/option[text()=\"' + \
                docs_type + '\"]'
            select_docs_type = self.browser.find_element_by_xpath(
                docs_type_option)
            select_docs_type.click()
            if docs_subtype:
                docs_subtype_option = '//select[@name="ctl00$sel_tier_2"]/option[text()=\"' + \
                    docs_subtype + '\"]'
                select_docs_subtype = self.browser.find_element_by_xpath(
                    docs_subtype_option)

                select_docs_subtype.click()
        # Click and search
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
        return txt

    def searchForFile(self, filenameList):
        '''
        Get table element of web page and search for download link
        '''
        txt = UnicodeCorr(GetHtmlTxt(self.browser))
        filenameList = self.translate2hk(*tuple(filenameList))
        try:
            result = self.fileUrlExtractor(filenameList, txt)
        except IndexError:
            return []
        if result == -1:
            return []
        else:
            return result

    def search_docs_type(self, stock_name, docs_type, docs_subtype, fuzzy=True, translate=True):
        return self.search(stock_name=stock_name,
                           docs_type=docs_type, docs_subtype=docs_subtype, fuzzy=True, translate=True, key_word=None)

    def search_keyword(self, stock_name, key_word, fuzzy=True, translate=True):
        return self.search(stock_name=stock_name,
                           key_word=key_word, fuzzy=True, translate=True, docs_type=None, docs_subtype=None)

    def fileUrlExtractor(self, filenameList, txt):
        '''
        Extract download url from web page
        '''
        soup = html2soup(txt)
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

    '''
    # ---------------Search Test---------------------------------
    hkexAgent = HKEXSearchAgent()
    print(hkexAgent.searchForFile('金盾控股', ['股份', '全球', '預覽資料集']))
    try:
        jsalert = hkexAgent.browser.switch_to.alert
        jsalert.accept()
    except WebDriverException:
        pass
    hkexAgent.close()
    '''
    hkexAgent = HKEXSearchAgent()
    hkexAgent.search_docs_type(
        '金盾控股', '上市文件', '发售以供认购', True, True)
    hkexAgent.searchForFile(['股份', '全球', '预览资料集'])

    '''
    docs_dict = {

        "所有": None,
        "公告及通告": ["所有", "公司狀況變動及委員會/公司變動", "新上市（上市發行人/新申請人）",
                  "會議/表決", "證券/股本", "財務資料", "重組/股權變動/主要改動/公眾持股量/上市地位",
                  "關連交易", "雜項", "須予公布的交易"],
        "通函": ["所有", "公司狀況變動及委員會/公司變動", "會議/表決", "證券/股本", "重組/股權改動/主要改動/公眾持股量/上市地位",
               "關連交易", "雜項", "須予公布的交易"],
        "上市文件": ["所有", "交換證券或取代原證券", "介紹", "供股", "公開招股", "其他", "按《上市規則》規定視為新上市", "發售以供認購", "發售現有證券",
                 "補充上市文件", "認可集體投資計劃", "資本化發行", "配售上市後的新證券類別"],
        "財務報表/環境、社會及管治資料": ["所有", "中期/半年度報告", "季度報告", "年報", "環境、社會及管治資料/報告"],
        "翌日披露報表": ["所有", "其他", "股份購回"],
        "月報表": None,
        "委任代表表格": None,
        "公司資料報表（GEM）": None,
        "憲章文件": None,
        "債券及結構性產品": ["所有", "債務證券", "牛熊證", "結構性產品發行人的資料", "股票掛鉤票據", "衍生權證", ],
        "交易所買賣基金的交易資料": None,
        "監管者發出的公告及消息": None,
        "股份購回報告 (2009年1月1日前)": None,
        "合併守則 - 交易披露": None,
        "申請版本及聆訊後資料集": ["所有", "申請版本或相關材料", "聆訊後資料集或相關材料"],
        "槓桿及反向產品的交易資料": None,
    }

    input_txt = input()
    conved_txt = zhconv.convert(input_txt, 'zh-hk')
    key_choices = list(docs_dict.keys())
    result = process.extract(conved_txt, key_choices, limit=3)
    print(result)
    '''
