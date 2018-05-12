# IPO Downloader

根据列表搜索并爬取港交所HKEX的上市公司的指定文档

## Functions功能

1. 搜索并下载港交所上市公司的指定文档

### searchAgent.py

class HKEXSearchAgent 搜索港交所指定公司并获取指定文档的pdf下载链接

```python
hkexAgent = HKEXSearchAgent()
# 搜索指定上市公司的招股书
url = hkexAgent.searchForFile(Stock_name, ['股份', '配售', '全球', '預覽資料集'])
```

### Downloader.py

下载指定链接文件并自动命名

```
downloader = Downloader(url_list, savefile_name_list)
downloader.download()
```



### excel.py

list转换成xlsx

```python
excelwriter = excel.ExcelWriter()
excelwriter.write(a_list, 'name.xlsx')
```

## Requirement

```python
selenium,bs4,tqdm
```

