from bs4 import BeautifulSoup, Tag
import os
import csv
import pdb
import numpy as np


class Extractor(object):
    def __init__(self, table, id_=None, **kwargs):
        # input is Tag
        if isinstance(table, Tag):
            if id_:
                self._table = table.find(id=id_)
            else:
                self._table = table
        # input is str/unicode
        elif isinstance(table, str) or isinstance(table, unicode):
            if id_:
                self._table = BeautifulSoup(table, 'html.parser').find(id=id_)
            else:
                self._table = BeautifulSoup(table, 'html.parser')
        else:
            raise Exception('unrecognized type')

        if 'transformer' in kwargs:
            self._transformer = kwargs['transformer']
        else:
            self._transformer = str

        self._output = []

    def parse(self):
        self._output = []
        row_ind = 0
        col_ind = 0
        # print(len(list(self._table.find_all('tr'))))
        for row in self._table.find_all('tr'):
            # record the smallest row_span, so that we know how many rows
            # we should skip
            smallest_row_span = 1
            # print(row)
            for cell in row.children:
                # print(cell.name)
                if cell.name in ('td', 'th'):
                    __hyperlink = False
                    # check multiple rows
                    # pdb.set_trace()
                    # print('*' * 30)
                    # print(cell)
                    # print(list(cell.children))

                    for i in cell.children:
                        if isinstance(i, Tag) and i.name == 'a':
                            __hyperlink = True
                            try:
                                hyperlink = i.attrs['href']
                            except KeyError:
                                pass
                            # print(i.get_text().strip(), hyperlink)

                    row_span = int(cell.get('rowspan')) if cell.get(
                        'rowspan') else 1

                    # try updating smallest_row_span
                    smallest_row_span = min(smallest_row_span, row_span)

                    # check multiple columns
                    col_span = int(cell.get('colspan')) if cell.get(
                        'colspan') else 1

                    # find the right index
                    while True:
                        if self._check_cell_validity(row_ind, col_ind):
                            break
                        col_ind += 1

                    # insert into self._output
                    try:
                        if self._transformer == str:
                            txt = self._transformer(cell.get_text()).strip()
                            txt = txt.replace('\n', '')
                            txt = txt.strip()
                            if __hyperlink:
                                txt = (txt, hyperlink)
                            self._insert(row_ind, col_ind, row_span,
                                         col_span, txt)
                        else:
                            self._insert(row_ind, col_ind, row_span,
                                         col_span, self._transformer(cell.get_text()))
                    except UnicodeEncodeError:
                        raise Exception(
                            'Failed to decode text; you might want to specify kwargs transformer=unicode')

                    # update col_ind
                    col_ind += col_span

            # update row_ind
            row_ind += smallest_row_span
            col_ind = 0
        return self

    def return_list(self):
        return self._output

    def filter(self, fun):
        self._output = fun(self._output)

    def write_to_csv(self, filename='output.csv', path='.'):
        with open(os.path.join(path, filename), 'w') as csv_file:
            table_writer = csv.writer(csv_file)
            for row in self._output:
                table_writer.writerow(row)
        return

    def _check_validity(self, i, j, height, width):
        """
        check if a rectangle (i, j, height, width) can be put into self.output
        """
        return all(self._check_cell_validity(ii, jj) for ii in range(i, i + height) for jj in range(j, j + width))

    def _check_cell_validity(self, i, j):
        """
        check if a cell (i, j) can be put into self._output
        """
        if i >= len(self._output):
            return True
        if j >= len(self._output[i]):
            return True
        if self._output[i][j] is None:
            return True
        return False

    def _insert(self, i, j, height, width, val):
        # pdb.set_trace()
        for ii in range(i, i + height):
            for jj in range(j, j + width):
                self._insert_cell(ii, jj, val)

    def _insert_cell(self, i, j, val):
        while i >= len(self._output):
            self._output.append([])
        while j >= len(self._output[i]):
            self._output[i].append(None)

        if self._output[i][j] is None:
            self._output[i][j] = val
