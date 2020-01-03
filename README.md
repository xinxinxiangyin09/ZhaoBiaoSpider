# 项目说明

> author：素心

## 一、环境说明

### 系统环境

- [ ] windows xp

- [x] windows 7 x64 及以上
- [x] windows 8 x64 及以上
- [x] windows 10 x64 及以上
- [x] Linux 系统皆可兼容

### 解释器

- [ ] python 2.7
- [ ] python 3.5
- [x] python 3.6
- [x] python 3.7



## 二、项目结构

爬虫文件为`master/Spider/spider.py`，爬虫列表如下：

|  序号  |    类名     |     名称      |                 官网                 |                    接口                    |  备注  |
| :--: | :-------: | :---------: | :--------------------------------: | :--------------------------------------: | :--: |
|  01  |   China   |   中国政府采购网   |      http://www.ccgp.gov.cn/       |    http://search.ccgp.gov.cn/bxsearch    | 可采集  |
|  02  |   Whole   | 全军武器装备采购信息网 |      http://www.weain.mil.cn/      | http://www.weain.mil.cn/api/rest/api/v1.0/app/global/search | 可采集  |
|  03  |   Army    |    军队采购网    |        https://www.plap.cn/        | https://www.plap.cn/index/solrSearch1.html | 可采集  |
|  04  |  Beijing  |  北京市政府采购网   |  http://www.ccgp-beijing.gov.cn/   | http://fwxt.czj.beijing.gov.cn/was5/web/search | 可采集  |
|  05  |  Tianjin  |  天津市政府采购网   |  http://www.ccgp-tianjin.gov.cn/   | http://www.ccgp-tianjin.gov.cn/portal/topicView.do | 可采集  |
|  06  | Shanghai  |  上海市政府采购网   |     http://www.zfcg.sh.gov.cn/     |                                          | 延迟过高 |
|  07  | Chongqing |  重庆市政府采购网   | https://www.ccgp-chongqing.gov.cn/ | https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/new | 可采集  |
|  08  |   Hebei   |   河北政府采购网   |   http://www.ccgp-hebei.gov.cn/    | http://search.hebcz.cn:8080/was5/web/search | 可采集  |
|  09  |  Shanxi   |   山西政府采购网   |   http://www.ccgp-shanxi.gov.cn/   |  http://www.ccgp-shanxi.gov.cn/view.php  | 可采集  |
|  10  |  Shaanxi  |   陕西政府采购网   |  http://www.ccgp-shaanxi.gov.cn/   | http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do | 可采集  |
|  11  | Shandong  |   山东政府采购网   |  http://www.ccgp-shandong.gov.cn/  | http://www.ccgp-shandong.gov.cn/sdgp2017/site/listsearchall.jsp | 可采集  |
|  12  |   Henan   |   河南政府采购网   |      http://www.hngp.gov.cn/       |   http://www.hngp.gov.cn/henan/search    | 可采集  |
|  13  | Liaoning  |   辽宁政府采购网   |  http://www.ccgp-liaoning.gov.cn/  | http://www.ccgp-liaoning.gov.cn/portalindex.do | 可采集  |
|  14  |   Jilin   |   吉林政府采购网   |   http://www.ccgp-jilin.gov.cn/    | http://139.215.205.246:7080/solr/ext/search/search.action | 可采集  |
|  15  | Heilongj  |  黑龙江政府采购网   |      http://www.hljcg.gov.cn/      | http://www.hljcg.gov.cn/xwzs!queryGd.action | 可采集  |
|  16  |  Jiangsu  |   江苏政府采购网   |  http://www.ccgp-jiangsu.gov.cn/   | http://www.ccgp-jiangsu.gov.cn/was5/web/search | 可采集  |
|  17  | Zhejiang  |   浙江政府采购网   |     http://www.zjzfcg.gov.cn/      | http://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results | 可采集  |
|  18  |   Anhui   |   安徽政府采购网   |   http://www.ccgp-anhui.gov.cn/    | http://www.ccgp-anhui.gov.cn/searchNewsController/searchNews.do | 可采集  |
|  19  |  Jiangxi  |   江西政府采购网   |  http://www.ccgp-jiangxi.gov.cn/   | http://www.ccgp-jiangxi.gov.cn/jxzfcg/services/JyxxWebservice/getList | 可采集  |
|  20  |  Fujian   |   福建政府采购网   |   http://zfcg.czt.fujian.gov.cn/   |  http://zfcg.czt.fujian.gov.cn/search/   | 可采集  |
|  21  |   Hubei   |   湖北政府采购网   |   http://www.ccgp-hubei.gov.cn/    | http://www.ccgp-hubei.gov.cn:8050/quSer/search | 可采集  |
|  22  |   Hunan   |   湖南政府采购网   |   http://www.ccgp-hunan.gov.cn/    | http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do | 可采集  |
|  23  |  Sichuan  |   四川政府采购网   |  http://www.ccgp-sichuan.gov.cn/   | http://www.ccgp-sichuan.gov.cn/CmsNewsController.do | 可采集  |
|  24  |  Guizhou  |   贵州政府采购网   |  http://www.ccgp-guizhou.gov.cn/   | http://www.ccgp-guizhou.gov.cn/article-search.html | 可采集  |
|  25  |  Yunnan   |   云南政府采购网   |   http://www.ccgp-yunnan.gov.cn/   | http://www.ccgp-yunnan.gov.cn/bulletin.do | 可采集  |
|  26  | Guangdong |   广东政府采购网   |      http://www.gdgpo.gov.cn/      | http://www.gdgpo.gov.cn/queryMoreInfoList.do | 可采集  |
|  27  |  Hainan   |   海南政府采购网   |   http://www.ccgp-hainan.gov.cn/   | http://www.ccgp-hainan.gov.cn/cgw/cgw_list.jsp | 可采集  |
|  28  |   Gansu   |   甘肃政府采购网   |   http://www.ccgp-gansu.gov.cn/    | http://www.ccgp-gansu.gov.cn/web/doSearchmxarticle.action | 可采集  |
|  29  |  Qinghai  |   青海政府采购网   |  http://www.ccgp-qinghai.gov.cn/   | http://www.ccgp-qinghai.gov.cn/front/search/category | 可采集  |
|  30  |  Neimeng  |  内蒙古政府采购网   |      http://www.nmgp.gov.cn/       | http://www.nmgp.gov.cn/zfcgwslave/web/index.php | 可采集  |
|  31  | Xinjiang  |   新疆政府采购网   |  http://www.ccgp-xinjiang.gov.cn/  | http://www.ccgp-xinjiang.gov.cn/front/search/category | 可采集  |
|  32  |  Xizang   |   西藏政府采购网   |   http://www.ccgp-xizang.gov.cn/   | http://www.ccgp-xizang.gov.cn/front/cmsArticle/searchArticle.action | 可采集  |
|  33  |  Guangxi  |   广西政府采购网   |      http://zfcg.gxzf.gov.cn/      | http://zfcg.gxzf.gov.cn/front/search/category | 可采集  |
|  34  |  Ningxia  |   宁夏政府采购网   |  http://www.ccgp-ningxia.gov.cn/   | http://www.ccgp-ningxia.gov.cn/public/NXGPPNEW/dynamic/contents/CGGG/index.jsp | 可采集  |
|  35  |           |     香港      |                                    |                                          |      |
|  36  |           |     澳门      |                                    |                                          |      |
|  37  |           |     台湾      |                                    |                                          |      |

###  文件结构说明

```
├─.idea
│  └─inspectionProfiles
├─Main 主文件
├─Map 映射文件
│  └─__pycache__
├─Pipeline 管道文件
│  └─__pycache__
├─Spider 爬虫文件
│  └─__pycache__
├─test 测试文件
└─__pycache__
```

## 三、项目配置

- 安装依赖

  `pip install -r requirements.txt -i https://pypi.douban.com/simple`

- 设置项目

  `在Settings.py文件有做详细说明`

- 扩展，在需要添加其他的网址的时候配置

  - 在Spider/spider.py文件中添加爬虫类，返回的数据均为

  `{'name': '网站名称', 'value': [{'keyword': '检索关键字', 'data': [{'url': '跳转链接', 'title': '标题', 'synopsis': '简介', 'create_time': '发布时间', 'name': ' 发布人'}, {...}, ...]}`

  - Map/url_map.py中添加映射关系
  - Main/main.py中添加需要生成的实例

## 四、启动项目

`python Main/main.py`

在指定的目录下生成需要的数据