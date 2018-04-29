import openpyxl
from openpyxl import Workbook
import os
import os.path as osp
import string
import random


def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


def num2col(num):
    def zero2l(num, l):
        if num == 0:
            return int(l)
        else:
            return int(num)
    a = ord('A')
    z = ord('Z')
    l = z - a + 1
    colnum = []
    power = 0
    while num >= (l ** (power - 1)):
        power += 1
        # print('Iter  start', power, num, colnum)
        # print(zero2l(num % (l ** power), l ** power))
        # print((l ** (power - 1)))
        # print(zero2l(num % (l ** power), l ** power) / (l ** (power - 1)))
        colnum.append(
            int(zero2l(num % (l ** power), l ** power) / (l ** (power - 1))))
        num -= colnum[-1] * (l ** (power - 1))
        # print('Iter  end', power, num, colnum)

    colnum.reverse()
    col = ''
    if len(colnum) == 1:
        col = chr(ord('A') + colnum[0] - 1)
        # print(col)
        # print('*' * 30)
        return col

    for i in range(len(colnum)):
        # if i == 0 and colnum[0] == 1:
        #     col += chr(ord('A') + colnum[i] - 1)
        # else:
        col += chr(ord('A') + colnum[i] - 1)
    # print(col)
    # print('*' * 30)
    return col


class ExcelWriter(object):
    """docstring for ExcelWriter"""

    def write_excel(self, path=os.getcwd(), filename='_output.xlsx'):
        if filename == '_output.xlsx':
            filename = self.target + filename
        with open(osp.join(path, filename), 'w') as csv_file:
            table_writer = csv.writer(csv_file)
            for row in self.data:
                table_writer.writerow(row)

    def __init__(self, fileHandle):
        super(ExcelWriter, self).__init__()
        self.fh = fileHandle

    def write(self, data):
        row_counter = 0


if __name__ == '__main__':
    # print(col2num('AA'))
    for i in range(1, 200):
        rand = random.randint(1, 1000000)
        txt = num2col(rand)
        txtrand = col2num(num2col(rand))
        if rand != txtrand:
            raise ValueError('Error')
            print('Error')
            print(rand, txt, txtrand)

    print(num2col(689))
