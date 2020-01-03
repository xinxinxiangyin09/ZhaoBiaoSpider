# coding=gbk

'''管道文件，将数据写入excel文件'''

import xlwt

import sys
sys.path.append('..')
from Settings import filename, SearchType

def settle(data):
    '''
    数据整理
    :param data: 要写入的数据
    :param searchType: 搜索类型
    :return: 整理后的数据
    '''
    if SearchType == 1:
        searchType = '关键字搜索'
    elif SearchType == 2:
        searchType = 'URL搜索'
    elif SearchType == 3:
        searchType = '关键字+URL搜索'

    result = [['跳转链接', '标题', '简介', '发布时间', '发布人', '检索关键字', '信息来源', '检索方式']]
    for d in data:
        for value in d['value']:
            if value['data'] == '搜索无数据':
                result.append(['搜索无数据', '搜索无数据', '搜索无数据', '搜索无数据', '搜索无数据', value['keyword'], d['name'], searchType])
            else:
                for info in value['data']:
                    result.append([info['url'], info['title'], info['synopsis'], info['create_time'], info['name'], value['keyword'], d['name'], searchType])
    write(result)

def write(result):
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')

    row = 0
    for item in result:
        cow = 0
        for info in item:
            sheet.write(row, cow, info)
            cow += 1
        row += 1

    book.save(filename)
    print('文件已保存至', filename)


# if __name__ == '__main__':
#     data = [{'name': '宁夏政府采购网', 'value': [{'keyword': '雷达', 'data': [{'url': 'http://www.ccgp-ningxia.gov.cn/public/NXGPPNEW/dynamic/contents/CGGG/ZBGG/content.jsp?id=04be87a5-42aa-474b-b8ce-68a3451e8c27&cid=316&sid=1&type=101', 'title': '基础测绘软硬件采购(雷达数据处理软件）', 'synopsis': '未提供简介', 'create_time': '2019-06-03', 'name': '未提供发布人'}, {'url': 'http://www.ccgp-ningxia.gov.cn/public/NXGPPNEW/dynamic/contents/CGGG/ZBGG/content.jsp?id=1b43a88d-8544-47f4-a197-79f944417c05&cid=316&sid=1&type=101', 'title': '宁夏回族自治区基础测绘院软件采购采编一体化软件、空三加密及立体测图软件、雷达数据处理及编辑软件', 'synopsis': '未提供简介', 'create_time': '2017-06-30', 'name': '未提供发布人'}]}, {'keyword': '天气雷达', 'data': '搜索无数据'}]}]
#     settle(data)