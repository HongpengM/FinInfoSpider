# coding:utf-8
import bs4
from bs4 import BeautifulSoup
from tableExtractor import Extractor
import time
import re
__PRINT_INFO__ = False
import os


def stringPurify(string, delChar=None):
    string = string.replace('\n', '')
    if delChar:
        for i in delChar:
            string = string.replace(i, '')
    return string.strip()


def url2soup(url):
    if isinstance(url, str):
        soup = BeautifulSoup(url, 'lxml')
    elif os.path.isfile(url):
        with open(url, encoding='gbk') as f:
            html = f.read()
            # try:
            #     html = html.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
            # except UnicodeError:
            #     pass
            start = time.clock()
            soup = BeautifulSoup(html, 'lxml')
            # soup = soup.prettify('gbk')
    else:
        print('URL converted to soup error')
    return soup


def decodeHKEX(url):
    soup = url2soup(url)
    data = soup.find_all('table',
                         attrs={'class': 'table_grey_border ms-rteTable-BlueTable_CHI'})
    print(len(data))
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
    extractor.filter_output(filterFun)
    results = extractor.return_list()

    return results


def decodeNASDAQ(url):
    soup = url2soup(url)
    data = soup.find_all(attrs={'class': 'genTable'})
    # print(len(data))
    print(data[0])

    # def tableParser(table):
    #     tableHeader = []
    #     for i in table.thead.tr.contents:
    #         if i.string.strip():
    #             tableHeader.append(i.string.strip())

    #     tableBody = []
    #     tb = table.tbody
    #     for i in table.tbody:
    #         _ = []
    #         print(type(i))
    #         if isinstance(i, bs4.element.Tag):
    #             for j in i.contents:
    #                 if isinstance(j, bs4.element.Tag):
    #                     if not j.string:
    #                         _.append(
    #                             (j.a.string.strip(), j.a.attrs['href']))
    #                     else:
    #                         _.append(j.string.strip())

    #         if _:
    #             tableBody.append(_)
    #     if __PRINT_INFO__:
    #         print('Table Header')
    #         print(len(tableHeader), tableHeader)
    #         print('Table Body')
    #         print(len(tableBody), len(tableBody[0]), tableBody)
    #     return (tableHeader, tableBody)

    return tableParser(data[0].table)


def decodeNYSE(url):
    soup = url2soup(url)

    deals = {'Expected Deals': None, 'Amended Deals': None,
             'Filed Deals': None, 'Withdrawn Deals': None}
    deals_candidate = soup.find_all(name='h2')
    # print(soup)
    for can in deals_candidate:
        for i in deals.keys():
            if re.match(i, can.string.strip()):
                deals[i] = can
    startPoint = deals['Expected Deals']
    sibs = list(enumerate(startPoint.next_siblings))
    print(len(list(enumerate(sibs))))
    deals_table = {'Expected Deals': sibs[1][1],
                   'Expected Deals Time': sibs[3][1],
                   'Amended Deals': sibs[11][1],
                   'Amended Deals Time': sibs[13][1],
                   'Filed Deals': sibs[21][1],
                   'Filed Deals Time': sibs[23][1],
                   'Withdrawn Deals': sibs[31][1],
                   'Withdrawn Deals Time': sibs[33][1]}
    # print(deals_table['Withdrawn Deals'])

    def tableParser(table):
        tableHeader = []
        for i in table.tr.contents:
            if i.string.strip():
                tableHeader.append(i.string.strip())

        tableBody = []
        tb = table.tbody
        for i in table.tbody:
            _ = []
            if str(type(i)) == '<class \'bs4.element.Tag\'>':
                # print(i)
                for j in i.contents:
                    try:
                        if str(type(j)) == '<class \'bs4.element.Tag\'>':
                            if j.string.strip():
                                _.append(j.string.strip())
                    except AttributeError:
                        _.append(j.strong.string.strip())
            if _:
                tableBody.append(_)
        if __PRINT_INFO__:
            print('Table Header')
            print(len(tableHeader), tableHeader)
            print('Table Body')
            print(len(tableBody), len(tableBody[0]), tableBody)
        return (tableHeader, tableBody)
        # print(len(tableBody), tableBody)

        def timeParser(time):
            ampm = ['am', 'pm']
            time = stringPurify(str(time))

            for i in time.split('--'):
                for j in ampm:
                    if j in i:
                        time = stringPurify(i, ['<', '>', '!'])
            if __PRINT_INFO__:
                print('Time info')
                print(time)
            return time

        output_Dict = {}
        for i in deals_table.keys():
            if not 'Time' in i:
                output_Dict[i] = tableParser(deals_table[i])
            else:
                output_Dict[i] = timeParser(deals_table[i])
        # print(output_Dict)
        return output_Dict
        # tableParser(sibs[1][1])
        # timeParser(sibs[3][1])


if __name__ == '__main__':
    __PRINT_INFO__ = True
    # decodeNYSE('nyse.html')
    # decodeNASDAQFile('nasdaq.html')
    # decodeHKEXFile('hkex.html')
