# -*- coding:utf-8 -*-

import random
import os
import datetime
import time
import pyodbc

# 模拟登陆配置

active_login = 1  # 是否需要模拟登陆
LOGIN_NAME = "nsyh_xxb"  # 用户名
LOGIN_PASS = "NSYH123"  # 密码
init_url = "http://60.1.100.2/"  # 网站初始界面
login_url = "http://60.1.100.2/sysuser/doSysUserLoginAction.do"  # 网站登陆界面

active_proxy = 0  # 是否需要代理


# 数据库配置
DB_CONFIG = {

    'DB_CONNECT_TYPE': 'sqlalchemy',  # 'pymongo'sqlalchemy
    # 'DB_CONNECT_STRING':'mongodb://localhost:27017/'
    # 'DB_CONNECT_STRING': 'sqlite:///' + os.path.dirname(__file__) + '/data/proxy.db',
    # 'DB_CONNECT_STRING': 'db2+ibm_db://root:rootroot@localhost:50000/sample',
    'DB_CONNECT_STRING' : 'mysql+pymysql://root:rootroot@localhost/proxy?charset=utf8',
}

# 随机头信息
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


HEADER = {
    'User-Agent': random.choice(USER_AGENTS),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
}

# TEST_URL = 'http://ip.chinaz.com/getip.aspx'
TEST_URL = 'http://ip.chinaz.com/'
TEST_HTTP_HEADER = 'http://httpbin.org/get'
TEST_HTTPS_HEADER = 'https://httpbin.org/get'
# TEST_IP = 'http://httpbin.org/ip'
# TEST_IP = "http://www.jsonip.com/"
# TEST_IP = "http://www.whatismyip.com.tw/"
TEST_IP = "http://ip.chinaz.com/getip.aspx"
TIMEOUT = 7  # socket延时


def get_fetch_range(restart=False):
    FETCH_RANGE_LIST = [
                        [330682000000000, 330682000299999],
                        ]
    if restart:
        return FETCH_RANGE_LIST
    conn = pyodbc.connect(DSN="db2local")
    sql = "select REGNO from company order by REGNO desc"
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchmany(3)  # 获取倒数第三个 因为会出现内外注册号不一致的情况

    last_fetch = int(rows[-1][0])

    for fetch_range in FETCH_RANGE_LIST:
        start_range, end_range = fetch_range

        if end_range > last_fetch > start_range:
            index = FETCH_RANGE_LIST.index(fetch_range)
            while index:
                index -= 1
                FETCH_RANGE_LIST.remove(FETCH_RANGE_LIST[index])
            fetch_range[0] = last_fetch
            FETCH_RANGE_LIST[0] = fetch_range

    return FETCH_RANGE_LIST

# print(eval("[330682000000000, 330682000099999]"))

# 文件路径
date = time.strftime("%Y%m%d", time.localtime())

company_path = "file/" + date + "/company.txt"
company_info_path = "file/" + date + "/company_info.txt"
zbxx_info_path  = "file/" + date + "/zbxx_info.txt"
ggxx_info_path  = "file/" + date + "/ggxx_info.txt"
xkxx_info_path  = "file/" + date + "/xkxx_info.txt"
xzcf_info_path  = "file/" + date + "/xzcf_info.txt"
yqqf_info_path  = "file/" + date + "/yqqf_info.txt"
bdcdy_info_path  = "file/" + date + "/bdcdy_info.txt"
dcdy_info_path  = "file/" + date + "/dcdy_info.txt"
pwqdy_info_path = "file/" + date + "/pwqdy_info.txt"
cfxx_info_path  = "file/" + date + "/cfxx_info.txt"
jyyc_info_path = "file/" + date + "/jyyc_info.txt"
sdq_info_path  = "file/" + date + "/sdq_info.txt"
xybg_credit_path = "file/" + date + "/xybg_credit.txt"
xyls_credit_path = "file/" + date + "/xyls_credit.txt"
fxzs_risk_path = "file/" + date + "/fxzs_risk.txt"
fxmx_risk_path = "file/" + date + "/fxmx_risk.txt"
risk_fxqyjs_now_path = "file/" + date + "/risk_fxqyjs_now.txt"
risk_fxqyjs_ls_path = "file/" + date + "/risk_fxqyjs_ls.txt"
risk_fxqygz_now_path = "file/" + date + "/risk_fxqygz_now.txt"
risk_fxqygz_ls_path = "file/" + date + "/risk_fxqygz_ls.txt"
risk_fxqyts_now_path = "file/" + date + "/risk_fxqyts_now.txt"
risk_fxqyts_ls_path = "file/" + date + "/risk_fxqyts_ls.txt"


# 日志路径
company_log_path = "logs/" + date + "/fetch_company.log"
company_info_log_path = "logs/" + date + "/fetch_company_info.log"
risk_info_path = "logs/" + date + "/risk_info.log"
run_main_log_path = "logs/" + date + "/run_main.log"
error_path = "logs/" + date + "/error.log"


# 握手文件
fetch_company_OK = "file/" + date + "/fetch_company.OK"
fetch_companyInfo_OK = "file/" + date + "/fetch_companyInfo.OK"
fetch_riskInfo_OK = "file/" + date + "/fetch_riskInfo.OK"
