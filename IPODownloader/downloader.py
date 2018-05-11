from tqdm import tqdm
import requests
import os
import random
from time import sleep


class Downloader(object):
    """docstring for Downloader"""

    def __init__(self, dli, nli=None, outpath=os.path.join(os.getcwd(), 'download')):
        super(Downloader, self).__init__()
        self.dlist = dli
        self.outpath = outpath
        if not os.path.isdir(self.outpath):
            os.mkdir(self.outpath)
        if nli:
            self.namelist = nli
            # Ensure namelist has equal length with download list
            assert len(nli) == len(dli)
        else:
            self.namelist = []
            for i in range(len(dli)):
                self.namelist.append(str(i))

    def download(self, sleeptime=3):
        print(self.dlist, self.namelist)
        for i in range(len(self.dlist)):
            url = self.dlist[i]
            name = self.namelist[i]
            print('Now downloading ' + name + '...')
            print(os.path.join(self.outpath,
                               name + url[url.rfind('.'):]))
            response = requests.get(url, stream=True)
            if '.' in url:
                with open(os.path.join(self.outpath,
                                       name + url[url.rfind('.'):]), 'wb') as handle:
                    for data in tqdm(response.iter_content(), ncols=60):
                        handle.write(data)
                sleep(random.random() * sleeptime)

    # def downloadReq(self):
    #     for i in range(len(self.dlist)):
    #         url = self.dlist[i]
    #         name = self.namelist[i]
    #         print('Now downloading ' + name + '...')
    #         print(os.path.join(self.outpath,
    #                            name + url[url.rfind('.'):]))
    #         response = requests.get(url, stream=True)
    #         if '.' in url:
    #             with open(os.path.join(self.outpath,
    #                                    name + url[url.rfind('.'):]), 'wb') as handle:
    #                 for data in tqdm(response.iter_content(), ncols=60):
    #                     handle.write(data)


if __name__ == '__main__':
    dlist = [
        'http://www.hkexnews.hk/listedco/listconews/SEHK/2018/0130/LTN20180130046_C.pdf']
    nlist = ['域高国际']
    downloader = Downloader(dlist, nlist)
    print(downloader.outpath)
    downloader.download()
