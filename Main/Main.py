'''主文件'''

from concurrent.futures import ThreadPoolExecutor

import sys
sys.path.append('..')

from Spider.spider import *
from Settings import *
from Pipeline.pipeline import settle
from Map.url_map import Map, getClass

def keyword(keyword_list, object_list):
    '''关键字搜索模式'''
    print('配置的关键字为 %s' % keyword_list)
    data = []
    pool = ThreadPoolExecutor(max_workers=int(MaxWorkThread))
    for fn in object_list:
        try:
            s = pool.submit(fn.main, keyword_list).result()
            data.append(s)
            print(s['name'], 'OK')
        except KeyError:
            continue

    pool.shutdown(wait=True)
    settle(data)

def url(url, default):
    '''URL搜索模式'''
    for info in Map:
        if url[0] in info['url']:
            name = info['name']
            print('配置的URL为%s，本地识别结果：%s' % (url[0], name))
            sample = getClass(name=name)
        else:
            sample = None

    print('搜索关键字为：', default)
    data = []
    if sample:
        data.append(sample.main(keyword_list=default))
    else:
        print('请检查配置文件')
    settle(data=data)

def UrlKey(keyword, url):
    print(keyword, url)
    for info in Map:
        if url in info['url']:
            name = info['name']
            print('关键字：%s， 搜索网站：%s' % (keyword, name))
            sample = getClass(name)
        else:
            sample = None

    data = []
    if sample:
        data.append(sample.main([keyword, ]))
    else:
        print('请检查配置文件')
    settle(data)

def get_object():
    '''获取所有爬虫类生成的实例对象'''
    china = China()
    whole = Whole()
    army = Army()
    beijing = Beijing()
    tianjin = Tianjin()
    # shanghai = Shanghai() # 该网站延迟过高，未招找到搜索接口
    chongqing = Chongqing()
    heibei = Hebei()
    shanxi = Shanxi()
    shaanxi = Shaanxi()
    shandong = Shandong()
    henan = Henan()
    liaoning = Liaoning()
    jilin = Jilin()
    heilongjiang = Heilongj()
    jiangsu = Jiangsu()
    zhejiang = Zhejiang()
    anhui = Anhui()
    jiangxi = Jiangxi()
    fujian = Fujian()
    hubei = Hubei()
    hunan = Hunan()
    sichuan = Sichuan()
    guizhou = Guizhou()
    yunnan = Yunnan()
    guangdong = Guangdong()
    hainan = Hainan()
    gansu = Gansu()
    qinghai = Qinghai()
    neimeng = Neimeng()
    xinjiang = Xinjiang()
    xizang = Xizang()
    guangxi = Guangxi()
    ningxia = Ningxia()

    object_list = []
    object_list.append(china)
    object_list.append(whole)
    object_list.append(army)
    object_list.append(beijing)
    object_list.append(tianjin)
    object_list.append(chongqing)
    object_list.append(heibei)
    object_list.append(shanxi)
    object_list.append(shaanxi)
    object_list.append(shandong)
    object_list.append(henan)
    object_list.append(liaoning)
    object_list.append(jilin)
    object_list.append(heilongjiang)
    object_list.append(jiangsu)
    object_list.append(zhejiang)
    object_list.append(anhui)
    object_list.append(jiangxi)
    object_list.append(fujian)
    object_list.append(hubei)
    object_list.append(hunan)
    object_list.append(sichuan)
    object_list.append(guizhou)
    object_list.append(yunnan)
    object_list.append(guangdong)
    object_list.append(hainan)
    object_list.append(gansu)
    object_list.append(qinghai)
    object_list.append(neimeng)
    object_list.append(xinjiang)
    object_list.append(xizang)
    object_list.append(guangxi)
    object_list.append(ningxia)
    return object_list

def get_config():
    default = Default
    object_list = get_object()
    print('开启线程数为：', MaxWorkThread)
    # 判断检索方式
    if SearchType == 1:
        print('启动关键字搜索')
        return keyword(keyword_list=Info, object_list=object_list)
    elif SearchType == 2:
        print('启动网址搜索')
        return url(url=Info, default=default)
    elif SearchType == 3:
        print('启动关键字+网址搜索')
        key = InfoCombination['keyword']
        url_ = InfoCombination['url']
        return UrlKey(keyword=key, url=url_)
    else:
        print('程序停止，请检查Settings.py')


if __name__ == '__main__':
    get_config()