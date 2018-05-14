# coding:utf-8
import bs4
from bs4 import BeautifulSoup

import time
import re
__PRINT_INFO__ = False
import os
try:
    from .tableExtractor import Extractor
    from .utils import html2soup, stringPurify
except Exception:
    from tableExtractor import Extractor
    from utils import html2soup, stringPurify


class PageDecoder(object):
    """docstring for PageDecoder"""

    def __init__(self, target):
        super(PageDecoder, self).__init__()
        self._decoderDict = {
            'nyse': self.decodeNYSENew,
            'nasdaq': self.decodeNASDAQ,
            'hkex': self.decodeHKEX
        }

        if str.lower(target) in self._decoderDict.keys():
            self.target = target
            self.decoder = self._decoderDict[self.target]
        else:
            raise ValueError('Target site not supported by now')

    def decode(self, url):
        self.result = self.decoder(url)

    def data(self):
        return self.result

    def decodeHKEX(self, url):
        soup = html2soup(url)
        data = soup.find_all('table',
                             attrs={'class': 'table_grey_border ms-rteTable-BlueTable_CHI'})
        # print(data)
        # print(data[0])
        extractor = Extractor(data[0])
        extractor.parse()

        def filterFun(results):
            _ = []
            for i in results:
                if isinstance(i, list):
                    __ = []
                    _replaced = False
                    for j in i:
                        if '/' in j:
                            _replaced = True
                            replace = j.replace('/', '').strip()
                            __.append(replace)
                        else:
                            __.append(j)
                    if _replaced:
                        _.append(__)
                    else:
                        _.append(i)
            return _
        extractor.filter(filterFun)
        results = extractor.return_list()

        return results

    def decodeNASDAQ(self, url):
        soup = html2soup(url)
        data = soup.find_all(attrs={'class': 'genTable'})
        # print(len(data))
        table = Extractor(data[0])
        table.parse()
        return table.return_list()

    def decodeNYSENew(self, url):
        soup = html2soup(url)
        data = soup.find_all('table',
                             attrs={'class': 'table table-data table-condensed spacer-lg'})
        # print(data)
        # print(data[0])
        header = soup.find_all(name='h2', attrs={'class': 'section-header'})
        _ = []
        for i in range(len(data)):
            head = header[i].get_text().strip()
            contents = Extractor(data[i])
            contents.parse()
            _ += [[head]] + contents.return_list()
        return _


if __name__ == '__main__':
    __PRINT_INFO__ = True
    # decodeNYSE('nyse.html')
    # decodeNASDAQFile('nasdaq.html')
    # decodeHKEXFile('hkex.html')
    de = PageDecoder('nasdaq')
    de.decode('nasdaq.html')
    print(de.data())
