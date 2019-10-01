#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2019/10/1 2:53
#@Author: 林先森
#@File  : ReBuild.py

import requests #导入requests库
from bs4 import BeautifulSoup

# 获得文本（应该是返回一个response好一点但是为了目的性更强我还是决定返回文本，毕竟都是在处理文本
def getText(url):
    # 头部，伪装
    head = {
        "User-Agent": "Mozilla/5.0" # 火狐内核
    }
    # 开始发起请求request并获得回应response,设置超时时间为30s
    response = requests.get(url=url, params=head, timeout = 30)
    # 打印状态码，200表示成功连接
    print(response.status_code)
    # 成功连接返回正确文本
    if (response.status_code == 200):
        # response返回的文件可能不是gbk/utf-8（远古网站写代码用的是什么码完全不确定）,解码会得到乱码，所以要转码
        response.encoding = response.apparent_encoding
        # 打印一下试试
        print(response.encoding) # response预计的第一种解码格式
        print(response.apparent_encoding) # response预计的第二种解码格式
        # 从这里开始我们就获得了完整的html文本  resp.text
        return response.text
        # print(response.text) #太长就不打印了
    #如果连接不成功，返回空
    else:
        return None

# 通过文本获得我们要的表文本区域
def getTable(text):
    # 这个时候通过BeautifulSoup函数煮一锅汤
    soup = BeautifulSoup(text, "html.parser")  # 它会帮我们把文本转换为树结构，根据后面给的解析器参数
    # print(soup.prettify())  页面更友好的显示

    # 从这一步我们就获得了网页右键检查元素可查看到的树状结构文本

    # 接下来就是得到我们要的内容(以下全部要靠观察)
    # 先得到包着热榜的框框
    hotDiv = soup.find(name = 'div', attrs={'id' : 'pl_top_realtimehot'}) # soup.find会找到第一个匹配到的文本块，速度和find_all一样
    # 获得框框里面的表(有点像excel,有我们不要的表头)
    hotTable = hotDiv.find(name = 'table')
    return hotTable
    # 我们要的excel表已经有了，让我们分开处理，表头和主体

# 获得表头数据
def getHeads(hotTable):
    header = hotTable.find(name = 'thead')  # 表头藏在thead里面
    headerTr = header.find(name = 'tr') # 还藏在thead里面的tr里
    headers = headerTr.find_all(name = 'th') # 终于找到了，这个find_all会返回给我们一个存着所有的表头数据(但还是带着html标签这是我们不要的数据)的列表
    # print(headers) # 可以看到很丑，但是快得到了
    # 题外话:一般为了快会直接连起来写
    # headers = hotTable.find('thead').find('tr').find_all('th')
    #处理列表
    for tr in headers:
        if tr.string != None:
            headers[headers.index(tr)] = tr.string
        else: #如果标签里面没有内容，为了防止抛出空指针异常，手动赋值一个长度为0的字符串
            headers[headers.index(tr)] = ''
    # print(headers) #打印以下查看处理完的表头
    return headers

# 获得主体数据
def getDatas(hotTable):
    SINA_URL = r'https://s.weibo.com/'
    #处理主体
    datas = hotTable.find('tbody').find_all('tr')
    #看看我们获得了什么
    # for item in datas:
    #     print(item.prettify())
    #可以看到第一项是置顶的，我们可以把它单独拿出来
    highest = datas[0].find('a').string #直接找到链接
    print(highest)
    highest_url = SINA_URL + datas[0].find('a').attrs['href'] #观察链接，都是只有后半部分，需要有主域名连接
    print(highest_url)
    #不过这里我们只是看看，不打算用

    #把刚刚那个扔出我们的队列,不扔出的话等下会空指针异常
    datas.pop(0)

    #接下来干正事，获得一个列表包含着排名，名称，url，和点击量
    hotDataList = []  # 列表包含着各个项目（列表）
    for data in datas:
        details = [] # 一个列表包含着一个项目的排名，名称，url，和点击量
        details.append(data.find(attrs = {'class' : 'td-01 ranktop'}).string) # 存放排名
        a = data.find('a')  # 一个a标签存放着名称和url
        details.append(a.string) # 存放名称
        details.append(SINA_URL + a.attrs['href']) # 存放url
        details.append(data.find('span').string) # 存放点击量
        #最后放进hotDataList里面
        hotDataList.append(details)
    # for data in hotDataList:
    #     print(data)
    return hotDataList

#写入excel表格
from Excel import write_excel


# 主函数部分
if __name__ == '__main__':
    # 新浪热搜榜链接
    sinaHotUrl = r"https://s.weibo.com/top/summary?cate=realtimehot"
    # 获得文本
    text = getText(sinaHotUrl)
    # 从这里开始我们就获得了完整的html文本
    # 当然了如果没有成功连接会返回空，这样子就要结束程序了，一般可以打印一下刚才的response.text看看是什么问题
    if text == None:
        exit()

    # 通过文本获得我们要的表文本区域
    hotTable = getTable(text)
    # 我们要的excel表已经有了，让我们分开处理，表头和主体

    #表头
    headers = getHeads(hotTable)

    #主体
    datas = getDatas(hotTable)

    #那个表头其实没什么用和我们要用的相差甚远。。重写一个
    headers = [['序号', '关键词', 'url', '点击量']]
    excelData = headers + datas
    # print(excelData)
    #写入excel
    write_excel(excelData, '../file/sinaHot.xls')
