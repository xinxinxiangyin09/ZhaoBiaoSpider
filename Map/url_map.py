'''URL映射关系表'''

import sys
sys.path.append('..')
from Spider.spider import *

Map = [
    {'name': '中国政府采购网', 'url': 'http://www.ccgp.gov.cn/', '_class': 'China'},
    {'name': '全军武器装备采购信息网', 'url': 'http://www.weain.mil.cn/', '_class': 'Whole'},
    {'name': '军队采购网', 'url': 'https://www.plap.cn/', '_class': 'Army'},
    {'name': '北京市政府采购网', 'url': 'http://www.ccgp-beijing.gov.cn/', '_class': 'Beijing'},
    {'name': '天津市政府采购网', 'url': 'http://www.ccgp-tianjin.gov.cn/', '_class': 'Tianjin'},
    {'name': '上海市政府采购网', 'url': 'http://www.zfcg.sh.gov.cn/', '_class': 'Shanghai'},
    {'name': '重庆市政府采购网', 'url': 'https://www.ccgp-chongqing.gov.cn/', '_class': 'Chongqing'},
    {'name': '河北政府采购网', 'url': 'http://www.ccgp-hebei.gov.cn/', '_class': 'Hebei'},
    {'name': '山西政府采购网', 'url': 'http://www.ccgp-shanxi.gov.cn/', '_class': 'Shanxi'},
    {'name': '陕西政府采购网', 'url': 'http://www.ccgp-shaanxi.gov.cn/', '_class': 'Shaanxi'},
    {'name': '山东政府采购网', 'url': 'http://www.ccgp-shandong.gov.cn/', '_class': 'Shandong'},
    {'name': '河南政府采购网', 'url': 'http://www.hngp.gov.cn/', '_class': 'Henan'},
    {'name': '辽宁政府采购网', 'url': 'http://www.ccgp-liaoning.gov.cn/', '_class': 'Liaoning'},
    {'name': '吉林政府采购网', 'url': 'http://www.ccgp-jilin.gov.cn/', '_class': 'Jilin'},
    {'name': '黑龙江政府采购网', 'url': 'http://www.hljcg.gov.cn/', '_class': 'Heilongj'},
    {'name': '江苏政府采购网', 'url': 'http://www.ccgp-jiangsu.gov.cn/', '_class': 'Jiangsu'},
    {'name': '浙江政府采购网', 'url': 'http://www.zjzfcg.gov.cn/', '_class': 'Zhejiang'},
    {'name': '安徽政府采购网', 'url': 'http://www.ccgp-anhui.gov.cn/', '_class': 'Anhui'},
    {'name': '江西政府采购网', 'url': 'http://www.ccgp-jiangxi.gov.cn/', '_class': 'Jiangxi'},
    {'name': '福建政府采购网', 'url': 'http://zfcg.czt.fujian.gov.cn/', '_class': 'Fujian'},
    {'name': '湖北政府采购网', 'url': 'http://www.ccgp-hubei.gov.cn/', '_class': 'Hubei'},
    {'name': '湖南政府采购网', 'url': 'http://www.ccgp-hunan.gov.cn/', '_class': 'Hunan'},
    {'name': '四川政府采购网', 'url': 'http://www.ccgp-sichuan.gov.cn/', '_class': 'Sichuan'},
    {'name': '贵州政府采购网', 'url': 'http://www.ccgp-guizhou.gov.cn/', '_class': 'Guizhou'},
    {'name': '云南政府采购网', 'url': 'http://www.ccgp-yunnan.gov.cn/', '_class': 'Yunnan'},
    {'name': '广东政府采购网', 'url': 'http://www.gdgpo.gov.cn/', '_class': 'Guangdong'},
    {'name': '海南政府采购网', 'url': 'http://www.ccgp-hainan.gov.cn/', '_class': 'Hainan'},
    {'name': '甘肃政府采购网', 'url': 'http://www.ccgp-gansu.gov.cn/', '_class': 'Gansu'},
    {'name': '青海政府采购网', 'url': 'http://www.ccgp-qinghai.gov.cn/', '_class': 'Qinghai'},
    {'name': '内蒙古政府采购网', 'url': 'http://www.nmgp.gov.cn/', '_class': 'Neimeng'},
    {'name': '新疆政府采购网', 'url': 'http://www.ccgp-xinjiang.gov.cn/', '_class': 'Xinjiang'},
    {'name': '西藏政府采购网', 'url': 'http://www.ccgp-xizang.gov.cn/', '_class': 'Xizang'},
    {'name': '广西政府采购网', 'url': 'http://zfcg.gxzf.gov.cn/', '_class': 'Guangxi'},
    {'name': '宁夏政府采购网', 'url': 'http://www.ccgp-ningxia.gov.cn/', '_class': 'Ningxia'},
]

def getClass(name):
    if name == '中国政府采购网':
        return China()
    elif name == '全军武器装备采购信息网':
        return Whole()
    elif name == '军队采集网':
        return Army()
    elif name == '北京市政府采购网':
        return Beijing()
    elif name == '天津市政府采购网':
        return Tianjin()
    elif name == '重庆市政府采购网':
        return Chongqing()
    elif name == '中国河北政府采购网':
        return Hebei()
    elif name == '中国山西政府采购网':
        return Shanxi()
    elif name == '陕西省政府采购网':
        return Shaanxi()
    elif name == '山东省政府采购网':
        return Shandong()
    elif name == '河南省政府采购网':
        return Henan()
    elif name == '辽宁政府采购网':
        return Liaoning()
    elif name == '吉林省政府采购网':
        return Jilin()
    elif name == '黑龙江省政府采购网':
        return Heilongj()
    elif name == '江苏政府采购':
        return Jiangsu()
    elif name == '浙江政府采购网':
        return Zhejiang()
    elif name == '安徽省政府采购网':
        return Anhui()
    elif name == '江西省政府采购网':
        return Jiangxi()
    elif name == '福建政府采购网':
        return Fujian()
    elif name == '湖北政府采购网':
        return Hubei()
    elif name == '湖南政府采购网':
        return Hunan()
    elif name == '四川政府采购网':
        return Sichuan()
    elif name == '贵州省政府采购网':
        return Guizhou()
    elif name == '云南政府采购网':
        return Yunnan()
    elif name == '广东省政府采购网':
        return Guangdong()
    elif name == '海南省政府采购网':
        return Hainan()
    elif name == '甘肃政府采购网':
        return Gansu()
    elif name == '青海政府采购网':
        return Qinghai()
    elif name == '内蒙古政府采购网':
        return Neimeng()
    elif name == '新疆政府采购网':
        return Xinjiang()
    elif name == '西藏政府采购网':
        return Xizang()
    elif name == '广西政府采购网':
        return Guangxi()
    elif name == '宁夏政府采购网':
        return Ningxia()

# if __name__ == '__main__':
#     print(getClass('中国政府采购网'))

'''添加另外的网址的时候，按照如上的规则添加'''