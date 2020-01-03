'''线程池参数一致，方法不一致'''

from concurrent.futures import ThreadPoolExecutor
import time, random

def get_url(number):
    time.sleep(2)
    url = 'http://www.suxin.site/search?page='+ str(number)
    print('成功生产URL：%s' % url)
    return url

def get_html(url):
    time.sleep(3)
    html = '这是%s的数据' % url
    print('%s OK' % url.result())
    return html

if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=3)
    for i in range(20):
        pool.submit(get_url, (random.randint(10, 100))).add_done_callback(get_html)
    pool.shutdown(wait=True)