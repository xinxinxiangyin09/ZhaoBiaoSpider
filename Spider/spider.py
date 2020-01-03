import datetime
import time
import requests
import re
import json

class China(object):
    '''中国采购网'''
    def __init__(self):
        self.url = 'http://search.ccgp.gov.cn/bxsearch'

    def get_count_page(self, keyword, page):
        '''获取总页码'''
        params = {
            'searchtype': 2,
            'page_index': page,
            'dbselect': 'bidx',
            'kw': keyword,
            'timeType': 2,
        }
        html = requests.get(url=self.url, params=params).text
        count = re.findall('<span style="color:#c00000">(\d+)</span>', html)[0]  # 根据总条数计算页数
        if int(count) % 20 == 0:
            return int(int(count) / 20)
        else:
            return int(int(count) // 20) + 1

    def get_html(self, keyword, page, proxy):
        '''获取源码'''
        params = {
            'searchtype': 2,
            'page_index': page,
            'dbselect': 'bidx',
            'kw': keyword,
            'timeType': 2,
        }
        if proxy is not None:
            proxy = {'http':'https://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        html = requests.get(url=self.url, params=params, proxies=proxy).text

        return self.parse(html=html)

    def parse(self, html):
        result = re.findall(r'<li>(.*?)</li>', html, re.S)[3:]

        info = []
        for item in result:
            item = item.replace('  ', '')
            # 跳转链接
            url = re.findall('<a href="(.*?)"', item)[0]
            # 标题
            title = re.findall('\n(.*?)\r\n</a>', item)[0]
            title = re.sub('<.*?>', '', title)
            # 简介
            synopsis = re.findall('<p>(.*?)</p>', item)[0]
            synopsis = re.sub('	', '', synopsis)
            synopsis = re.sub('<.*?>', '', synopsis)

            # 其他信息
            tmp_info = re.findall('<span>(.*?)</span>', item, re.S)[0]
            tmp_info = re.sub('\r\n', '', tmp_info)
            tmp_info = re.sub('<.*?>', '', tmp_info)

            # 发布时间
            create_time = tmp_info.split('|')[0]

            # 发布人
            name = tmp_info.split('|')[1]

            info.append({'url': url, 'title': title, 'synopsis': synopsis, 'create_time':create_time, 'name': name})
        return info

    def main(self, keyword_list, proxy=None):
        result = []
        for keyword in keyword_list:
            # 每页获取20条信息
            count_page = self.get_count_page(keyword=keyword, page=1)

            info_list = []
            for page in range(1, count_page+1):
                info_list.extend(self.get_html(keyword=keyword, page=page, proxy=proxy))

            # 搜索为空
            if not len(info_list):
                result.append({'keyword': keyword, 'data': '搜索为空'})
            else:
                result.append({'keyword':keyword, 'data': info_list})

        return {'name':'中国政府采购网', 'value': result}

class Whole(object):

    '''全军武器装备采购信息网'''
    def __init__(self):
        self.url = 'http://www.weain.mil.cn/api/rest/api/v1.0/app/global/search'

    def get_html(self, keyword, page, proxy):
        '''获取源码，这里是搜索接口，直接返回json数据'''
        if proxy is not None:
            proxy = {'http':'http://%s' % proxy,'https':'https://%s' % proxy}
        data = {
            'pageNo': page,
            'pageSize': 8,
            'keyword': keyword,
        }
        html = requests.post(url=self.url, data=data, proxies=proxy).json()
        # 不另外封装了，直接提取信息即可
        data = []
        for item in html['ret']['list']:
            url = 'http://www.weain.mil.cn' + item['pcUrl']
            title = re.sub('<.*?>', '', item['title'])
            data.append({'url': url, 'title': title, 'synopsis': item['content'], 'create_time': item['publishTime'], 'name': item['publicUnitName']})
        return data

    def main(self, keyword_list, proxy=None):
        '''每页获取8条数据，拼接'''
        info_data = []
        for keyword in keyword_list:
            info = []
            page = 1
            while True:
                data = self.get_html(keyword=keyword, page=page, proxy=proxy)
                page += 1
                if not len(data):
                    break
                else:
                    info.extend(data)
            info_data.append({'keyword': keyword, 'data':info})

        return {'name':'全军武器装备采购信息网', 'value': info_data}

class Army(object):
    '''军队采集网'''
    def __init__(self):
        self.url = 'https://www.plap.cn/index/solrSearch1.html'

    def get_count(self, keyword):
        '''获取总页数'''
        params = {
            'page': 1,
            'condition': keyword
        }
        html = requests.get(url=self.url, params=params).text
        count = re.findall('total : "(\d+)",', html)[0]
        if int(count) % 20 == 0:
            return int(int(count) / 20)
        else:
            return (int(count) // 20) + 1

    def get_html(self, keyword, page, proxy):
        '''获取源码'''
        params = {
            'page': page,
            'condition':keyword
        }
        if proxy is not None:
            proxy = {'http':'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        html = requests.get(url=self.url, params=params, proxies=proxy).text
        return self.parse(html=html)

    def parse(self, html):
        '''解析网页，提取数据'''
        result = re.findall('<li>(.*?)</li>', html, re.S)[2:]

        data = []
        for item in result:
            url, title = re.findall('<a href="(.*?)" title="(.*?)" target="_self"', item)[0]
            url = 'https://www.plap.cn' + url
            create_time = re.findall('<span class="col-md-2 col-sm-5 col-xs-12">(.*?)</span>', item)[0]
            data.append({'url':url, 'title': title, 'synopsis':'网站未提供', 'create_time': create_time, 'name': '网站未提供'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            count = self.get_count(keyword=keyword)
            data = []

            for page in range(1, count+1):
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                data.extend(result)

            if len(data):
                info_data.append({'keyword': keyword, 'data': data})
            else:
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})

        return {'name':'军队采集网', 'value': info_data}

class Beijing(object):
    '''北京市政府采购网'''
    def __init__(self):
        self.url = 'http://fwxt.czj.beijing.gov.cn/was5/web/search'

    def get_html(self, keyword, page, proxy):
        params = {
            'searchword': keyword,
            'channelid': 212555,
            'page': page
        }
        if proxy is not None:
            proxy = {
                'http':'http://{}'.format(proxy),
                'https':'https://{}'.format(proxy),
            }
        html = requests.get(url=self.url, params=params, proxies=proxy).text
        return self.parse(html)

    def parse(self, html):
        '''提取相关的信息'''
        li_list = re.findall('<li>(.*?)</li>', html, re.S)
        if not len(li_list):
            return None
        else:
            data = []
            for item in li_list:
                # 提取跳转链接以及标题
                url, title = re.findall('<a href="(.*?)" class="searchresulttitle" target="_blank">(.*?)</a>', item)[0]
                title = re.sub('<.*?>', '', title)
                # 提取简介
                synopsis = re.findall('<div style="margin-top:5px;">(.*?)</div>', item, re.S)[0]
                synopsis = synopsis.replace('\n', '').strip()
                synopsis = re.sub('\u3000', '', synopsis)
                # 提取发布时间
                create_time = re.findall('<div class="pubtime">(.*?)</div>', item)[0].replace('.', '-')
                data.append({'url': url, 'title': title, 'synopsis':synopsis, 'create_time':create_time, 'name': '网站未提供'})

            return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if result is None:
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})

        return {'name': '北京市政府采购网', 'value': info_data}

class Tianjin(object):
    '''天津市政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do'

    def trans_format(self, time_string):
        '''
        时间格式转换 CST时间转GMT
        :param from_format: 时间字符串
        :param to_format:
        :return:
        '''
        time_struct = time.strptime(time_string, '%a %b %d %H:%M:%S CST %Y')
        times = time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
        return times

    def get_count(self, keyword):
        '''获取总页码数'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
        }
        data = {'pageCount': 15, 'px': 2, 'method': 'findbyfind', 'name': keyword, 'pageCount1': 15, 'page': 1}
        # proxy = {'http':'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        html = requests.post(url=self.url, data=data, headers=headers).text
        count = re.findall('共<b>(\d+)</b>页', html)[0]
        return int(count)

    def get_html(self, keyword, page, proxy):
        '''
        获取源码
        :param keyword: 关键字
        :param page: 页码
        :param proxy: 代理IP
        :return: 源码
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
        }
        data = {
            'pageCount': 15,
            'px': 2,
            'method': 'findbyfind',
            'name': keyword,
            'pageCount1': 15,
            'page': page
        }
        if proxy is not None:
            proxy = {'http':'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        html = requests.post(url=self.url, data=data, headers=headers, proxies=proxy).text
        return self.parse(html)

    def parse(self, html):
        li_list = re.findall('<li class="oneData">(.*?)</li>', html, re.S)
        data = []
        for item in li_list:
            base_url = 'http://www.ccgp-tianjin.gov.cn/portal/documentView.do?method=view&'
            url = base_url + re.findall('<a href="/viewer.do\?(.*?)"', item)[0]
            title = re.findall('title="(.*?)"', item)[0]
            create_time = re.findall('<span>(.*?)</span>', item)[0]
            create_time = self.trans_format(create_time)
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            count = self.get_count(keyword)
            data = []
            for page in range(1, count+1):
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '天津市政府采购网', 'value': info_data}

# 该网站延迟过高 http://www.zfcg.sh.gov.cn/ 上海市政府采购网站
# class Shanghai(object):
#     '''上海市政府采购网'''
#     pass

class Chongqing(object):
    '''重庆市政府采购网'''
    def __init__(self):
        self.url = 'https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/new'

    def get_html(self, keyword, page, proxy):
        '''获取源码，接口数据，返回json'''
        if proxy is not None:
            proxy = {'http':'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        params = {
            'endDate': datetime.datetime.now().strftime('%Y-%m-%d'),
            'keyword': keyword,
            'pi': page,
            'ps': '20',
            'startDate': (datetime.datetime.now()+datetime.timedelta(days=-90)).strftime("%Y-%m-%d"),
        }
        headers = {
            'Cookie': 'Hm_lvt_a41ec8f07afa1805aa0eaeec292c8be0=1577239179; Hm_lpvt_a41ec8f07afa1805aa0eaeec292c8be0=1577484697',
            'Host': 'www.ccgp-chongqing.gov.cn',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
        }
        jsonData = requests.get(url=self.url, params=params, headers=headers, proxies=proxy).json()
        if jsonData['msg'] == 'success':
            return self.parse(html=jsonData)
        else:
            return None

    def parse(self, html):
        '''解析数据'''

        data = []
        for item in html['notices']:
            url = 'https://www.ccgp-chongqing.gov.cn/notices/detail/' + item['id']
            title = item.get('title', None)
            create_time = item.get('issueTime', None)
            synopsis = '未提供简介'
            name = item['creatorOrgName']
            data.append({'url': url, 'title': title, 'create_time': create_time, 'synopsis': synopsis, 'name': name})

        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            data = []
            page = 0
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            info_data.append({'keyword': keyword, 'data': data})
        return {'name': '重庆市政府采购网', 'value': info_data}

class Hebei(object):
    '''中国河北政府采购网'''
    def __init__(self):
        self.url = 'http://search.hebcz.cn:8080/was5/web/search'

    def get_html(self, keyword, page, proxy):
        params = {
            'channelid': '240117',
            'lanmu': 'zbgg',
            'sydoctitle': keyword,
            'titlename': keyword,
            'page': page,
            'perpage': 50
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}
        html = requests.get(url=self.url, headers=headers, params=params, proxies=proxy).text
        return self.parse(html)

    def parse(self, html):
        tr_list = re.findall('<tr id="biaoti">(.*?</tr>.*?)</tr>', html, re.S)
        if not len(tr_list):
            return None
        else:
            data = []
            for item in tr_list:
                url, title = re.findall('<a href="(.*?)" class="a3" target="_blank">(.*?)</a>', item, re.S)[0]
                title = title.strip()
                title = re.sub('<.*?>', '', title)

                synopsis = '未提供简介'
                tmp_info = re.findall('<span class="txt">(.*?)</span>', item, re.S)
                create_time = tmp_info[0].strip()
                name = tmp_info[2].strip()
                data.append({'url':url, 'title': title, 'synopsis': synopsis, 'create_time': create_time, 'name': name})
            return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if result is None:
                    break
                data.extend(result)
            info_data.append({'keyword': keyword, 'data': data})
        return {'name': '中国河北政府采购网', 'value': info_data}

class Shanxi(object):
    '''中国山西政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-shanxi.gov.cn/view.php'

    def get_count(self, keyword):
        '''获取页码'''
        params = {
            'ntype': 'fnotice',
            'title': keyword,
            'type': '招标公告',
            'page': 1,
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}
        html = requests.get(url=self.url, headers=headers, params=params).text
        count = re.findall(r'/(\d+)页', html)[0]
        return int(count)

    def get_html(self, keyword, page, proxy):
        '''获取源码信息'''
        params = {
            'ntype': 'fnotice',
            'title': keyword,
            'type': '招标公告',
            'page': page,
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}
        html = requests.get(url=self.url, headers=headers, proxies=proxy, params=params).text
        return self.parse(html)

    def parse(self, html):
        html = html.replace("'", '"')
        result = re.findall('<a href="(view.*?)" target="_blank" title="(.*?)">.*?</a></td><td nowrap width="10%">(.*?)</td><td nowrap width="15%">.*?</td><td nowrap><font color=".*?">.*?</font></td><td width="15%" nowrap>\[(.*?)\]</td>', html, re.S)
        data = []
        for item in result:
            url, title, name, create_time = item
            url = 'http://www.ccgp-shanxi.gov.cn/' + url
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            data = []
            for page in range(1, self.get_count(keyword=keyword) + 1):
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                data.extend(result)
            info_data.append({'keyword': keyword, 'data': data})
        return {'name': '中国山西政府采购网', 'value': info_data}

class Shaanxi(object):
    '''陕西省政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do'

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http': 'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        params = {'noticetype': 3}
        data = {
            'page.pageNum': page,
            "parameters['title']": keyword,
            "parameters['regionguid']": 610001,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '_gscu_614399700=77239224v26p0t98; _gscbrs_614399700=1; JSESSIONID=CB3114AFC076DCE3FFCA21CA10BC9163; HasLoaded=true; _gscs_614399700=t77360761hcksmd56|pv:5',
            'Host': 'www.ccgp-shaanxi.gov.cn',
            'Origin': 'http://www.ccgp-shaanxi.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
        }
        response = requests.post(url=self.url, headers=headers, params=params, data=data, proxies=proxy)
        return self.parse(html=response.text)

    def parse(self, html):
        result = re.findall('<tr>(.*?)</tr>', html, re.S)[1:]
        data = []
        for item in result:
            name = re.findall('<td align="center">\[(.*?)\]</td>', html)[0]
            title = re.findall('<td title="(.*?)"', item)[0].strip()
            url = re.findall('href="(.*?)"', item)[0]
            create_time = re.findall('>(\d+-\d+-\d+)<', item)[0]
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        '''该网站即使页码超标也会显示最后一页，所以这里和前一次提取的数据做比较，相同则停止'''
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if result[0] in data:
                    break
                else:
                    data.extend(result)

            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '陕西省政府采购网', 'value': info_data}

class Shandong(object):
    '''中国山东政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/listsearchall.jsp'
        self.headers = {
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=7D3F142DBB9050714551876C2ACAD1CE; insert_cookie=35333146',
            'Host': 'www.ccgp-shandong.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
        }

    def get_count(self, keyword):
        params = {'subject': keyword, 'colcode': '02', 'curpage': 1}
        html = requests.get(url=self.url, params=params, headers=self.headers).text
        count = re.findall('</font>/(\d+)</strong>页', html)[0]
        return int(count)

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http': 'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        params = {'subject': keyword, 'colcode': '02', 'curpage': page}
        html = requests.get(url=self.url, params=params, headers=self.headers, proxies=proxy).text
        return self.parse(html)

    def parse(self, html):
        result = re.findall("<a class='five' href='(.*?)' title='.*?' class='aa'>\n(.*?)</a>.*?(\d+-\d+-\d+)</td></tr>", html, re.S)
        data = []
        for item in result:
            url, title, create_time = item
            url = 'http://www.ccgp-shandong.gov.cn/' + url
            data.append({'url': url, 'title':title, 'synopsis': '网站未提供', 'create_time': create_time, 'name': '网站未提供'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            count = self.get_count(keyword=keyword)
            data = []
            for page in range(1, count+1):
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                data.extend(result)
            info_data.append({'keyword': keyword, 'data': data})

        return {'name': '山东省政府采购网', 'value': info_data}

class Henan(object):
    '''河南省政府采购网'''
    def __init__(self):
        self.url = 'http://www.hngp.gov.cn/henan/search'

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http':'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        headers = {
            'Cookie': 'sId=3b47d6eb17ef458f9e00192ca049f7b6; SERVERID=652ffb8a9d83d5f9f7fe4e4ca4b6cd8a|1577416325|1577416176',
            'Host': 'www.hngp.gov.cn',
            'Referer': 'http://www.hngp.gov.cn/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        }
        params = {
            'pageSize': '15',
            'q': keyword,
            'ctk': '3b47d6eb17ef458f9e00192ca049f7b6',
            'pageNo': page,
        }
        html = requests.get(url=self.url, headers=headers, params=params, proxies=proxy).text
        return self.parse(html)

    def parse(self, html):
        result = re.findall('<li>\n(.*?)</li>', html, re.S)
        data = []
        for item in result:
            url, title = re.findall('<a href="(.*?)">(.*?)</a>', item)[0]
            url = 'http://www.hngp.gov.cn' + url
            create_time = re.findall('(\d{4}-\d{2}-\d{2})', item)[0]
            try:
                name = re.findall('<span class="\w+">(\w+)</span>', item)[0]
            except IndexError:
                name = '网站未提供'
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            info_data.append({'keyword': keyword, 'data': data})
        return {'name': '河南省政府采购网', 'value': info_data}

class Liaoning(object):
    '''辽宁政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do'

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http':'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        params = {
            'method': 'getPubInfoList',
            't_k': 'null',
        }
        data = {
            'current': page,
            'rowCount': 10,
            'infoTypeCode': 'null',
            'title': keyword,
            'queryType': 'znss',
        }
        headers = {
            'Connection': 'keep-alive',
            'Content-Length': '93',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=B4289084560FE973FB884FED46741FD2; sto-id-20480=HMKMMFDLCJCD',
            'Host': 'www.ccgp-liaoning.gov.cn',
            'Origin': 'http://www.ccgp-liaoning.gov.cn',
            'Referer': 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=goZNSS&znss=%E9%9B%B7%E8%BE%BE',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        }
        jsonData = requests.post(url=self.url, params=params, data=data, proxies=proxy, headers=headers).json()
        data = []
        for item in jsonData['rows']:
            name = item['editor']
            url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoViewOpen&infoId=' + item['id']
            title = item['title']
            create_time = item['releaseDate']
            data.append({'url': url, 'title': title, 'synopsis': '网站未提供简介', 'create_time': create_time, 'name':name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            data = []
            page = 0
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)

            if not len(data):
                info_data.append({'keyword': keyword, 'value': '未搜索到数据'})
            else:
                info_data.append({'keyword': keyword, 'value': data})

        return {'name': '辽宁政府采购网', 'value': info_data}

class Jilin(object):
    '''吉林省政府采购网'''
    def __init__(self):
        self.url = 'http://139.215.205.246:7080/solr/ext/search/search.action'

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http':'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        params = {
            'categoryId': 0,
            'cityCode': 0,
            'pager.keyword': '%u96F7%u8FBE',
            'pager.pageNumber': page,
            'txt': keyword,
        }
        html = requests.get(url=self.url, params=params, proxies=proxy).text
        return self.parse(html)

    def parse(self, html):
        result = re.findall('<a style="margin-left:10px;"(.*?)</span> ', html, re.S)
        data = []
        for item in result:
            url, title = re.findall('href="(.*?)">(.*?)</a>', item)[0]
            create_time = re.findall('<span>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', item)[0]
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': '未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '吉林省政府采购网', 'value': info_data}

class Heilongj(object):
    '''黑龙江政府采购网'''
    def __init__(self):
        self.url = 'http://www.hljcg.gov.cn/xwzs!queryGd.action'

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http': 'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'JSESSIONID=lnvMpFgCxHwks2rQcp1T4zLpjM12z7LpvdtxkRNgFCKv6hQWvFvQ!-782965579',
            'Host': 'www.hljcg.gov.cn',
            'Origin': 'http://www.hljcg.gov.cn',
            'Referer': 'http://www.hljcg.gov.cn/xwzs!queryGd.action',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        }
        data = {
            'id': 110,
            'xwzsPage.LBBH': 99,
            'xwzsPage.zlbh': '',
            'xwzsPage.GJZ': keyword,
            'xwzsPage.pageNo': page,
            'xwzsPage.pageSize': 20
        }
        html = requests.post(url=self.url, data=data, proxies=proxy, headers=headers).text
        return self.parse(html)

    def parse(self, html):
        result = re.findall('<div class="xxei">(.*?)</div>', html, re.S)
        data = []
        for item in result:
            url = re.findall("href='(.*?)'", item)[0]
            url = 'http://www.hljcg.gov.cn/' + url
            title = re.findall('" >(.*?)<', item)[0]
            create_time = re.findall('<span class="sjej">(\d{4}-\d{2}-\d{2})</span>', item)[0]
            name = re.findall('<span class="nrej">(\w+)</span>', item)[0]
            data.append({'url': url,'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            data = []
            page = 0
            while True:
                page += 1
                try:
                    original_data = data[-1]
                except IndexError:
                    original_data = []
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)

                if original_data in result:
                    break
                elif not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': data})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '黑龙江省政府采购网', 'value': info_data}

class Jiangsu(object):
    '''江苏政府采购'''
    def __init__(self):
        self.url = 'http://www.ccgp-jiangsu.gov.cn/was5/web/search'

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http':'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        params = {
            'page': page,
            'channelid': 204408,
            'searchword': keyword,
            'keyword': keyword,
            'was_custom_expr': 'doctitle=(%s)' % keyword,
            'perpage': 10,
            'outlinepage': 10,
            'searchscope': 'doctitle',
            'orderby': '-DocrelTime',
        }
        html = requests.get(url=self.url, params=params, proxies=proxy)
        return self.parse(html.text)

    def parse(self, html):
        result = re.findall('<li>(.*?)</li>', html, re.S)
        data = []
        for item in result:
            url, title = re.findall('<a href="(.*?)" class="searchresulttitle" target="_blank">(.*?)</a>', item, re.S)[0]
            title = re.sub('<.*?>', '', title)
            synopsis = re.findall('<input type=".*?" id="\w+" value=\'(.*?)\'/>', item, re.S)[0]
            synopsis = synopsis.replace('\n', '').replace('\u3000', '')
            create_time = re.findall('<div class="\w+">(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})</div>', item)[0]
            create_time = re.sub('\.', '-', create_time)

            data.append({'url': url, 'title': title, 'synopsis': synopsis, 'create_time': create_time, 'name': '未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if result:
                    data.extend(result)
                elif not len(result):
                    break
            info_data.append({'keyword': keyword, 'data': data})
        return {'name': '江苏政府采购', 'value': info_data}

class Zhejiang(object):
    '''浙江政府采购网'''
    def __init__(self):
        self.url = 'http://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results'

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http':'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}

        params = {
            'pageNo': page,
            'pageSize': 15,
            'keyword': keyword,
            'type': 0,
            'isExact': 0,
            'url': 'fullTestCearch',
            'beginDate': (datetime.datetime.now()+datetime.timedelta(days=-90)).strftime("%Y-%m-%d"),
            'endDate': datetime.datetime.now().strftime("%Y-%m-%d"),
        }
        jsonData = requests.get(url=self.url, params=params, proxies=proxy).json()

        data = []
        for item in jsonData['articles']:
            url = item['url']
            title = item['title']
            title = re.sub('<.*?>', '', title)
            synopsis = item['keywords']
            # 这里时间戳转换日期，去掉结尾的三个0
            timestamp = item['pubDate'][:-3]
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))
            name = item['mainBidMenuName']
            data.append({'url': url, 'title': title, 'synopsis': synopsis, 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '浙江政府采购网', 'value': info_data}

class Anhui(object):
    '''安徽政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-anhui.gov.cn/searchNewsController/searchNews.do'

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http': 'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        params = {
            'operType': 'search',
            'keywords': keyword,
            'pageNum': page,
            'numPerPage': 20,
            'channelCode': 'sjcg_cggg',
        }
        html = requests.get(url=self.url, params=params, proxies=proxy).text
        return self.parse(html)

    def parse(self, html):
        result = re.findall('<tr>(.*?)</tr>', html, re.S)
        data = []
        for item in result:
            url = 'http://www.ccgp-anhui.gov.cn' + re.findall('href="(.*?)"', item)[0]
            title = re.findall('<a title="(.*?)"', item)[0]
            create_time = re.findall('\[(\d{4}-\d{2}-\d{2})\]', item)[0]
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': '未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            data = []
            page = 0
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '安徽省政府采购网', 'value': info_data}

class Jiangxi(object):
    '''江西政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-jiangxi.gov.cn/jxzfcg/services/JyxxWebservice/getList'

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http':'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        params = {
            'response': 'application/json',
            'pageIndex': page,
            'pageSize': '22',
            'xxTitle': keyword,
            'categorynum': '002006001',
        }
        jsonData = requests.get(url=self.url, params=params, proxies=proxy).json()
        return self.parse(jsonData=eval(jsonData['return']))

    def parse(self, jsonData):
        data = []
        for item in jsonData['Table']:
            title = item['title']
            title = re.sub('<.*?>', '', title)
            # http://www.ccgp-jiangxi.gov.cn/web/jyxx/002006/002006001/20191228/fe858c2a-c9e4-437f-91aa-47fe4f8fe26a.html
            create_time = item['postdate']
            query = re.findall('(\d{4})-(\d{2})-(\d{2})', create_time)[0]
            query = ''.join(query)
            url = 'http://www.ccgp-jiangxi.gov.cn/web/jyxx/002006/002006001/' + query + '/' + item['infoid'] + '.html'
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': '未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            data = []
            page = 0
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '江西省政府采购网', 'value': info_data}

class Fujian(object):
    '''福建省政府采购网'''
    def __init__(self):
        self.url = 'http://zfcg.czt.fujian.gov.cn/3500/noticelist/e8d2cd51915e4c338dc1c6ee2f02b127/'

    def get_html(self, keyword, page, proxy):
        if proxy is not None:
            proxy = {'http': 'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        params = {
            'page': page,
            'title': keyword,
            'notice_type': '463fa57862ea4cc79232158f5ed02d03',
        }
        headers = {
            'Cookie': 'csrftoken=5e2qKl8TtrwMfj79EukRsLFjGxFGw2dnn7NxNEfDZQid40UM5AEHTVxtGlLibkIp; sessionid=lcnxmulbpfepa688dc567secq8za3njc',
            'Host': 'zfcg.czt.fujian.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }
        html = requests.get(url=self.url, params=params, proxies=proxy, headers=headers)
        return self.parse(html.content.decode('utf-8'))

    def parse(self, html):
        result = re.findall('<li style="list-style: inside;padding-top: 1%;">(.*?)</li>', html, re.S)
        data = []
        for item in result:
            url = 'http://zfcg.czt.fujian.gov.cn' + re.findall('href="(.*?)"', item)[0]
            title = re.findall('title="(.*?)"', item)[0]
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': '未提供发布时间', 'name': '未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)

            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})

        return {'name': '福建政府采购网', 'value': info_data}

class Hubei(object):
    '''湖北政府采购'''
    def __init__(self):
        self.url = 'http://www.ccgp-hubei.gov.cn:8050/quSer/search'

    def trans_format(self, time_string):
        '''
        时间格式转换 CST时间转GMT
        :param from_format: 时间字符串
        :param to_format:
        :return:
        '''
        time_struct = time.strptime(time_string, '%a %b %d %H:%M:%S CST %Y')
        times = time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
        return times

    def get_html(self, keyword, page, proxy):
        if proxy:
            proxy = {'http': 'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        data = {
            'queryInfo.type': 'xmgg',
            'queryInfo.key': keyword,
            'queryInfo.gglx': '招标公告',
            'queryInfo.qybm': '420001',
            'queryInfo.begin': (datetime.datetime.now()+datetime.timedelta(days=-90)).strftime("%Y/%m/%d"),
            'queryInfo.end': datetime.datetime.now().strftime('%Y/%m/%d'),
            'queryInfo.pageNo': page,
            'queryInfo.pageSize': '15',
            'queryInfo.pageTotle': '3',
        }
        headers = {
            'Cookie': 'JSESSIONID=E3EE280F265FE28FB4126250D208DFA9',
        }
        html = requests.post(url=self.url, data=data, proxies=proxy, headers=headers).text
        return self.parse(html)

    def parse(self, html):
        result = re.findall('<li>(.*?)</li>', html, re.S)[2:]
        data = []
        for item in result:
            url = re.findall('href="(.*?)"', item)[0]
            title = re.findall('target="_blank">(.*?)</a><span>', item)[0]
            title = re.sub('<.*?>', '', title)
            ctime = re.findall('<span>(.*?)</span>', item)[0]
            create_time = self.trans_format(time_string=ctime)
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name':'未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if result:
                    data.extend(result)
                else:
                    break
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '湖北政府采购网', 'value': info_data}

class Hunan(object):
    '''湖南政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do'

    def get_html(self, keyword, page, proxy):
        if proxy:
            proxy = {'http': 'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        data = {
            'nType': 'prcmNotices',
            'prcmPrjName': keyword,
            'startDate': (datetime.datetime.now()+datetime.timedelta(days=-90)).strftime("%Y-%m-%d"),
            'endDate': datetime.datetime.now().strftime('%Y-%m-%d'),
            'page': page,
            'pageSize': 18,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        jsonData = requests.post(url=self.url, data=data, proxies=proxy, headers=headers).json()
        data = []
        for item in jsonData['rows']:
            url = 'http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp?noticeId=' + str(item['NOTICE_ID'])
            title = item['NOTICE_TITLE']
            name = item['ORG_NAME']
            create_time = item['NEWWORK_DATE']
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})

        return {'name': '湖南政府采购网', 'value': info_data}

class Sichuan(object):
    '''四川政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do'

    def get_html(self, keyword, page, proxy):
        params = {
            'method': 'search',
            'chnlCodes': '8a817eb738e5e70c0138e62ab6430c0a',
            'title': keyword,
            'pageSize': 10,
            'curPage': page,
            'searchResultForm': 'search_result_anhui.ftl',
            'startTime': (datetime.datetime.now() + datetime.timedelta(days=-90)).strftime("%Y-%m-%d"),
            'endTime': datetime.datetime.now().strftime('%Y-%m-%d')
        }
        html = requests.get(url=self.url, params=params, proxies=proxy).text
        return self.parse(html)

    def parse(self, html):
        result = re.findall('<li>(.*?)</li>', html, re.S)
        data = []
        for item in result:
            url = re.findall('<a href="(.*?)">', item)[0]
            title = re.findall('<div class="title">(.*?)</div>', item)[0]
            day, year, mon = re.findall('<span>(\d{2})</span>(\d{4})-(\d{2})', item)[0]
            create_time = year + '-' + mon + '-' + day
            synopsis = re.findall('<p>(.*?)</p>', item)[0]
            data.append({'url': url, 'title': title, 'synopsis': synopsis, 'create_time': create_time, 'name': '未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '四川政府采购网', 'value': info_data}

class Guizhou(object):
    '''贵州政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-guizhou.gov.cn/article-search.html'

    def get_html(self, keyword, page, proxy):
        if proxy:
            proxy = {'http': 'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        data = {
            'siteId': '1',
            'category.id': '1153418052184995',
            'keywords': keyword,
            'articlePageNo': page,
            'articlePageSize': 15,
        }
        html = requests.post(url=self.url, data=data, proxies=proxy).text
        return self.parse(html)

    def parse(self, html):
        result = re.findall('<li>(.*?)</li>', html)
        data = []
        for item in result:
            url = 'http://www.ccgp-guizhou.gov.cn/' + re.findall('href="(.*?)"', item)[0]
            title = re.findall('black">(.*?)</a>', item)[0]
            create_time = re.findall('<span >(\d{4}\.\d{2}\.\d{2})</span>', item)[0]
            create_time = re.sub('\.', '-', create_time)
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': '未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                try:
                    original_data = data[-1]
                except IndexError:
                    original_data = data
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if original_data in result:
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '贵州省政府采购网', 'value': info_data}

class Yunnan(object):
    '''云南政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-yunnan.gov.cn/bulletin.do'

    def get_html(self, keyword, page, proxy):
        if proxy:
            proxy = {'http': 'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        params = {
            'method': 'moreListQuery',
        }
        data = {
            'current': page,
            'rowCount': 10,
            'query_bulletintitle': keyword,
            'query_sign': 1,
            'query_gglxdm': 'bxlx001',
        }
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
        }
        html = requests.post(url=self.url, params=params, data=data, proxies=proxy, headers=headers).json()
        data = []
        for item in html['rows']:
            url = 'http://www.ccgp-yunnan.gov.cn/newbulletin_zz.do?method=preinsertgomodify&operator_state=1&flag=view&bulletin_id=' + item['bulletin_id']
            title, name, create_time = item['bulletintitle'], item['codeName'], item['finishday']
            data.append({'url': url, 'title': title, 'name': name, 'create_time': create_time, 'synopsis': '未提供简介'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '未搜索到数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '云南政府采购网', 'value': info_data}

class Guangdong(object):
    '''广东省政府采购网'''
    def __init__(self):
        self.url = 'http://www.gdgpo.gov.cn/queryMoreInfoList.do'

    def get_html(self, keyword, page, proxy):
        if proxy:
            proxy = {'http': 'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        data = {
            'pageIndex': page,
            'pageSize': 15,
            'channelCode': '0005',
            'sitewebName': '省直',
            'sitewebId': '4028889705bebb510105bec068b00003',
            'title': keyword,
            'operateDateFrom': (datetime.datetime.now()+datetime.timedelta(days=-90)).strftime('%Y-%m-%d'),
            'operateDateTo': datetime.datetime.now().strftime('%Y-%m-%d'),
        }
        html = requests.post(url=self.url, data=data, proxies=proxy).text
        return self.parse(html)

    def parse(self, html):
        result = re.findall('<li><em>(.*?)</li>', html, re.S)
        data = []
        for item in result:
            url = 'http://www.gdgpo.gov.cn' + re.findall('href="(.*?\.html)"', item)[0]
            title = re.findall('title="(.*?)"', item)[0]
            synopsis = re.findall('">(.*?)\n', item, re.S)[1]
            create_time = re.findall('(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', item)[0]
            data.append({'url': url, 'title': title, 'synopsis': synopsis, 'create_time': create_time})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '广东省政府采购网', 'value': info_data}

class Hainan(object):
    '''海南政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-hainan.gov.cn/cgw/cgw_list.jsp'

    def get_html(self, keyword, page, proxy):
        if proxy:
            proxy = {'http': 'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        params = {
            'title': keyword,
            'bid_type': 101,
            'currentPage': page,
        }
        html = requests.get(url=self.url, proxies=proxy, params=params)

        return self.parse(html=html.text)

    def parse(self, html):
        result = re.findall('<li><span>(.*?)</li>', html, re.S)
        data = []
        for item in result:
            url, title = re.findall('<a href="(/cgw/cgw_show.jsp\?id=\d+)">(.*?)</a>', item)[0]
            url = 'http://www.ccgp-hainan.gov.cn' + url
            create_time = re.findall('(\d{4}-\d{2}-\d{2})', item)[0]
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': '未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '未搜索到数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '海南省政府采购网', 'value': info_data}

class Gansu(object):
    '''甘肃政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-gansu.gov.cn/web/doSearchmxarticle.action'

    def get_html(self, keyword, page, proxy):
        data = {
            'articleSearchInfoVo.releasestarttime': '',
            'articleSearchInfoVo.releaseendtime': '',
            'articleSearchInfoVo.tflag': 1,
            'articleSearchInfoVo.classname': 1280501,
            'articleSearchInfoVo.dtype': '',
            'articleSearchInfoVo.days': '',
            'articleSearchInfoVo.releasestarttimeold': '',
            'articleSearchInfoVo.releaseendtimeold': '',
            'articleSearchInfoVo.title': keyword,
            'articleSearchInfoVo.agentname': '',
            'articleSearchInfoVo.bidcode': '',
            'articleSearchInfoVo.proj_name': '',
            'articleSearchInfoVo.buyername': '',
            'total': 1,
            'limit': 20,
            'current': page,
            'sjm': 7466,
        }
        html = requests.post(url=self.url, data=data, proxies=proxy).text
        return self.parse(html=html)

    def parse(self, html):
        result = re.findall('<li class="li\d+">(.*?)</li>', html, re.S)
        data = []
        for item in result:
            url, title = re.findall('href="(.*?\.html).*?">(.*?)</a>', item)[0]
            url = 'http://www.ccgp-gansu.gov.cn' + url
            create_time = re.findall('发布时间：(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', item)[0]
            name = re.findall('采购人：(\w+) \|', item)[0]
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                try:
                    original_data = data[-1]
                except IndexError:
                    original_data = data
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if original_data in result:
                    break
                elif not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '甘肃政府采购网', 'value': info_data}

class Qinghai(object):
    '''青海政府采购'''
    def __init__(self):
        self.url = 'http://www.ccgp-qinghai.gov.cn/front/search/category'

    def time_conversion(self, time_stamp):
        '''时间戳之间的转换'''
        stime = int(str(time_stamp)[:-3])
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stime))

    def get_jsonData(self, keyword, page, proxy):
        if proxy:
            proxy = {'http':'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        query_data = {
            'pageNo': page,
            'pageSize': 15,
            'categoryCode': 'ZcyAnnouncement2',
            'keyword': keyword,
            'procurementMethodCode': 1,
        }
        headers = {
            'Content-Type': 'application/json',
        }
        jsonData = requests.post(url=self.url, data=json.dumps(query_data), headers=headers, proxies=proxy).json()
        data = []
        for item in jsonData['hits']['hits']:
            url = 'http://www.ccgp-qinghai.gov.cn' + item['_source']['url']
            title = item['_source']['title']
            create_time = self.time_conversion(time_stamp=item['_source']['publishDate'])
            name = item['_source']['districtName']
            data.append({'url': url, 'title': title, 'synopsis':'未提供简介', 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_jsonData(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '青海政府采购网', 'value': info_data}

class Neimeng(object):
    '''内蒙古政府采购网'''
    def __init__(self):
        self.url = 'http://www.nmgp.gov.cn/zfcgwslave/web/index.php'

    def get_html(self, keyword, page, proxy):
        if proxy:
            proxy = {'http':'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        params = {
            'r': 'new-data/anndata'
        }
        data = {
            'type_name': 1,
            'keyword': keyword,
            'annstartdate_S': '',
            'annstartdate_E': '',
            'byf_page': page,
            'fun': 'cggg',
        }
        jsonData = requests.post(url=self.url, params=params, data=data, proxies=proxy).json()
        data = []
        for item in jsonData[0]:
            url = 'http://www.nmgp.gov.cn/category/cggg?tb_id=1&p_id=' + item['wp_mark_id']
            title, name = item['TITLE'], item['ADNAME']
            create_time = re.findall('\d{4}-\d{2}-\d{2}', item['SUBDATE'])[0]
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '内蒙古政府采购网', 'value': info_data}

class Xinjiang(object):
    '''新疆政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-xinjiang.gov.cn/front/search/category'

    def time_conversion(self, time_stamp):
        '''时间戳之间的转换'''
        stime = int(str(time_stamp)[:-3])
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stime))

    def get_html(self, keyword, page, proxy):
        data = {
            'pageNo': page,
            'pageSize': 15,
            'categoryCode': 'ZcyAnnouncement3001',
            'keyword': keyword,
            'procurementMethodCode': '1',
        }
        headers = {
            'Content-Type': 'application/json',
        }
        jsonData = requests.post(url=self.url, data=json.dumps(data), proxies=proxy, headers=headers).json()
        data = []
        for item in jsonData['hits']['hits']:
            url = 'http://www.ccgp-xinjiang.gov.cn' + item['_source']['url']
            title = item['_source']['title']
            create_time = self.time_conversion(item['_source']['publishDate'])
            name = item['_source']['districtName']
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '新疆政府采购网', 'value': info_data}

class Xizang(object):
    '''西藏政府采购网'''
    '''
    该网站下公开招标公告分两种，省级采购公告和市县采购公告
    '''
    def __init__(self):
        self.url = 'http://www.ccgp-xizang.gov.cn/front/cmsArticle/searchArticle.action'

    def get_html(self, keyword, page, categoryId, proxy):
        if proxy:
            proxy = {'http': 'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        data = {
            'categoryId': categoryId,
            'keyWord': keyword,
            'pager.keyword': keyword,
            'pager.pageNumber': page,
        }
        html = requests.post(url=self.url, data=data, proxies=proxy).text
        return self.parse(html=html)

    def parse(self, html):
        result = re.findall('<li>(.*?)</li>', html, re.S)
        data = []
        for item in result:
            url, title = re.findall('href="(.*?)">(.*?)</a>', item)[0]
            url = 'http://www.ccgp-xizang.gov.cn' + url
            title = re.sub('<.*?>', '', title)
            create_time = re.findall('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', item)[0]
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': '未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        '''124 125'''
        info_data = []
        for keyword in keyword_list:
            data = []
            for categoryId in range(124, 126):
                page = 0
                while True:
                    page += 1
                    result = self.get_html(keyword=keyword, page=page, categoryId=categoryId, proxy=proxy)
                    if not len(result):
                        break
                    else:
                        data.extend(result)

            if not len(info_data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})

        return {'name': '西藏政府采购网', 'value': info_data}

class Guangxi(object):
    '''广西政府采购网'''
    def __init__(self):
        self.url = 'http://zfcg.gxzf.gov.cn/front/search/category'

    def time_conversion(self, time_stamp):
        '''时间戳之间的转换'''
        stime = int(str(time_stamp)[:-3])
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stime))

    def get_html(self, keyword, page, proxy):
        if proxy:
            proxy = {'http': 'http://{}'.format(proxy), 'https':'https://{}'.format(proxy)}
        data = {
            'categoryCode': 'ZcyAnnouncement3001',
            'pageSize': '15',
            'pageNo': '%s' % page,
            'keyword': '%s' % keyword,
            'publishDateBegin': '%s' % (datetime.datetime.now()+datetime.timedelta(days=-30*6)).strftime("%Y-%m-%d"),
            'publishDateEnd': '%s' % datetime.datetime.now().strftime('%Y-%m-%d'),
            'procurementMethodCode': '1',
        }
        headers = {'Content-Type': 'application/json',}
        jsonData = requests.post(url=self.url, data=json.dumps(data), proxies=proxy, headers=headers).json()
        data = []
        for item in jsonData['hits']['hits']:
            url = 'http://zfcg.gxzf.gov.cn' + item['_source']['url']
            title = item['_source']['title']
            name = item['_source']['districtName']
            synopsis = item['_source']['gpCatalogName']
            create_time = self.time_conversion(time_stamp=item['_source']['publishDate'])
            data.append({'url': url, 'title': title, 'synopsis': synopsis, 'create_time': create_time, 'name': name})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                page += 1
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '广西政府采购网', 'value': info_data}

class Ningxia(object):
    '''宁夏政府采购网'''
    def __init__(self):
        self.url = 'http://www.ccgp-ningxia.gov.cn/public/NXGPPNEW/dynamic/contents/CGGG/index.jsp'

    def get_html(self, keyword, page, proxy):
        if proxy:
            proxy = {'http': 'http://{}'.format(proxy), 'https': 'https://{}'.format(proxy)}
        params = {
            'cid': 312,
            'sid': 1,
            'type': 101
        }
        data = {
            'keyword': keyword,
            'page': page,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        }
        html = requests.post(url=self.url, params=params, data=data, headers=headers, proxies=proxy).text
        return self.parse(html=html)

    def parse(self, html):
        result = re.findall('<td align="left"(.*?)</th>', html, re.S)
        data = []
        for item in result:
            url = 'http://www.ccgp-ningxia.gov.cn/public/NXGPPNEW/dynamic/' + re.findall('href="(.*?)"', item)[0]
            title = re.findall('title="(.*?)"', item)[0]
            create_time = re.findall('(\d{4}-\d{2}-\d{2})', item)[0]
            data.append({'url': url, 'title': title, 'synopsis': '未提供简介', 'create_time': create_time, 'name': '未提供发布人'})
        return data

    def main(self, keyword_list, proxy=None):
        info_data = []
        for keyword in keyword_list:
            page = 0
            data = []
            while True:
                result = self.get_html(keyword=keyword, page=page, proxy=proxy)
                page += 1
                if not len(result):
                    break
                else:
                    data.extend(result)
            if not len(data):
                info_data.append({'keyword': keyword, 'data': '搜索无数据'})
            else:
                info_data.append({'keyword': keyword, 'data': data})
        return {'name': '宁夏政府采购网', 'value': info_data}


if __name__ == '__main__':
    spider = Ningxia()
    keyword_list = ['雷达', '天气雷达']
    content = spider.main(keyword_list=keyword_list)
    print(content)