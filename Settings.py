'''项目配置文件'''

'''检索的默认关键字， 可以为多个关键字搜索'''
Default = ['雷达', '天气雷达']

'''
检索模式 SearchType 1为普通关键字检索，2为普通URL检索， 3为URL+关键字检索
注意：如果值为1，则配置Info为“关键字”，默认搜索所有Spider下的所有网站，例如：['天气雷达', '雷达']
     如果值为2，则配置Info为“URL”，默认关键字为上述的Default
     如果值为3，则配置InfoCombination信息为“关键字+URL”，无需配置Info，例如：InfoCombination = {'keyword': ['天气雷达'], 'url': ['http://www.ccgp.gov.cn/']}
'''
SearchType = 3
Info = ['http://www.ccgp-ningxia.gov.cn/']
InfoCombination = {'keyword': '天气雷达', 'url': 'http://www.ccgp.gov.cn/'}

'''
代理设置
如果不使用代理请设置为None，使用的话直接填IP:PORT即可
注意，如果使用代理，请严格控制代理更换频率，建议使用Flask或者Tornado搭建API，保证Proxy值为IP:PORT的形式即可，例如：http://127.0.0.1:5000/get
'''
Proxy = None

'''
excel文件保存路径，例如：在windows下D:\\file\\demo.xlsx 在Linux下/root/demo.xlsx
'''
filename = 'D:\\demo.xlsx'

'''
启动线程数，必须设置整数
'''
MaxWorkThread = 5