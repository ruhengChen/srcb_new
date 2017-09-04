# coding:utf-8
import json
import time

import gevent
import requests
from gevent import monkey

from db.PyodbcHelper import *
from util.exception import Test_URL_Fail

monkey.patch_all()

def process_start(tasks, myip, queue2):
    spawns = []
    for task in tasks:
        spawns.append(gevent.spawn(detect_proxy, myip, task, queue2))
    gevent.joinall(spawns)


def detect_proxy(selfip, proxy, queue2=None):
    '''
    :param proxy: ip字典
    :return:
    '''
    ip = proxy['ip']
    port = proxy['port']
    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}
    protocol, types, speed = checkProxy(selfip, proxies)
    if protocol > 0:
        proxy['protocol'] = protocol
        proxy['type'] = types
        proxy['speed'] = speed
    else:
        proxy = None
    if queue2:
        queue2.put(proxy)
    return proxy


def checkProxy(selfip, proxies):
    '''
    用来检测代理的类型，突然发现，免费网站写的信息不靠谱，还是要自己检测代理的类型
    :param
    :return:
    '''
    protocol = -1
    types = -1
    speed = -1
    http, http_types, http_speed = _checkHttpProxy(selfip, proxies)
    https, https_types, https_speed = _checkHttpProxy(selfip, proxies, False)
    if http and https:
        protocol = 2
        types = http_types
        speed = http_speed
    elif http:
        types = http_types
        protocol = 0
        speed = http_speed
    elif https:
        types = https_types
        protocol = 1
        speed = https_speed
    else:
        types = -1
        protocol = -1
        speed = -1
    return protocol, types, speed


def _checkHttpProxy(selfip, proxies, isHttp=True):
    types = -1
    speed = -1
    if isHttp:
        test_url = config.TEST_HTTP_HEADER
    else:
        test_url = config.TEST_HTTPS_HEADER
    try:
        start = time.time()
        r = requests.get(url=test_url, headers=config.HEADER, timeout=config.TIMEOUT, proxies=proxies)
        if r.ok:
            speed = round(time.time() - start, 2)
            content = json.loads(r.text)
            headers = content['headers']
            ip = content['origin']
            x_forwarded_for = headers.get('X-Forwarded-For', None)
            x_real_ip = headers.get('X-Real-Ip', None)
            if selfip in ip or ',' in ip:
                return False, types, speed
            elif x_forwarded_for is None and x_real_ip is None:
                types = 0
            elif selfip not in x_forwarded_for and selfip not in x_real_ip:
                types = 1
            else:
                types = 2
            return True, types, speed
        else:
            return False, types, speed
    except Exception as e:
        return False, types, speed


def getMyIP():
    try:
        r = requests.get(url=config.TEST_IP, headers=config.HEADER, timeout=config.TIMEOUT)
        ip = json.loads(r.text)
        return ip['origin']
    except Exception as e:
        raise Test_URL_Fail

# 获取可用的ip代理
static_proxy ={
    "https":"https://144.217.207.178:3128",
    # 'http': 'http://165.138.124.4:8080'
}
# static_proxy ={
#     'http': 'http://H8PX142BPZXA2V0D:52DE8535C1DEA206@proxy.abuyun.com:9010',
#     'https': 'http://H8PX142BPZXA2V0D:52DE8535C1DEA206@proxy.abuyun.com:9010'
# }
def get_active_proxy():
    proxysqlhelper  = Proxy()

    # print(proxysqlhelper.random_select())
    result_dict = {}
    proxy = {}
    result =  proxysqlhelper.random_select()

    result_dict.clear()
    if result.PROTOCOL == 1:
        result_dict["http"] = "http://%s:%s" %(result.IP,result.PORT)
    else:
        result_dict["https"] = "https://%s:%s" % (result.IP,result.PORT)
    proxy["ip"] = result.IP
    proxy["port"] = result.PORT
    proxy["protocol"] = result.PROTOCOL

    if static_proxy:
        r = requests.get(url=config.TEST_IP, headers=config.HEADER, proxies=static_proxy)
        print(r.text)
        return static_proxy
        # result_dict = static_proxy
    try:
        # print("正在使用ip:%s" % (proxy["ip"]))
        r = requests.get(url=config.TEST_IP, headers=config.HEADER, timeout=config.TIMEOUT, proxies=result_dict)
        print(r.text)


        # print(r.text)
        return result_dict
    except Exception as e:
        return_str = "代理IP:%s无效,正在尝试下一个ip" % proxy["ip"]
        print(return_str)
        get_active_proxy()



if __name__ == '__main__':
    # getMyIP()
    get_active_proxy()

    # str="{ip:'61.150.43.121',address:'陕西省西安市 西安电子科技大学'}"
    # j = json.dumps(str)
    # str = j['ip']
    # print str