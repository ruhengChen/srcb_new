# pytesseract.pytesseract.tesseract_cmd = 'E:/Program Files/Tesseract-OCR/tesseract'
#
# im = Image.open("doReadKaptcha.jpg")
# print(im.size)
# print(im.getpixel((99, 49)))
# if 1:
# # if 0:
#     for i in range(100):
#         for j in range(50):
#             r,g,b = im.getpixel((i,j))
#             # if r < 50 and g < 50 and b < 50:
#             #     r=0
#             #     g=0
#             #     b=255
#             if b<200:
#                 r=255
#                 g=255
#                 b=255
#
#
#             # im.putpixel((i,j),(r,g,b))
# # im.show()
# im = im.convert('L')
# # im.show()
# v_code = pytesseract.image_to_string(im, config='-psm 6 digits')
# print(v_code)

# get_active_proxy()
# if 3658 in range(10000):
#     print("ok")
# reg = re.compile( r'\b\d{4}\b')
# print(re.findall(reg,"1335"))

#
# dict1 = {"a":"a","b":"b","c":"c"}
#
# a = ["a", "b"]
#
# b = {i:dict1.pop(i) for i in a}
# print(b)
# print(dict1)
# print(datetime.datetime.strftime(parse(None,default='9999-01-01'),"%Y-%m-%d"))
# print("2016-03-24 00:00:00.0".format("%Y-%m-%d"))
# print(parse("2016-03-24 00:00:00.0"))
#
# a = {"a":None,"b":"b"}
#
# for key, value in a.items():
#     if not value:
#         a[key] = ""
#
# print(",".join(a.values()))
#
# company_info = OrderedDict()
#
# company_info["regno"] = "1"
# company_info["name"] = "2"
# company_info["leprep"] = "3"
# company_info["regorg"] = "4"
# company_info["regloc"] = "5"
# company_info["type"] = "6"
#
# print(",".join(company_info["regno"]))
# def aa(param):
# import sys, traceback
#
# def run_user_code(envdir):
#     source = input(">>> ")
#     try:
#         exec(source, envdir)
#     except Exception:
#         print("Exception in user code:")
#         print("-"*60)
#         traceback.print_exc(file=sys.stdout)
#         print("-"*60)
#
# envdir = {}
# while True:
#     run_user_code(envdir)

# from collections import OrderedDict
#
# a = OrderedDict()
# a["a"] = "a"
# a["b"] = "b"
# a["c"] = "c"
#
# b = {"d":"d"}
# c = a.copy()
# a.update(b)
# a.move_to_end("d", last=False)
#
# print(a)
# print(c)


# import requests
#
# init_url = "http://60.1.100.2/"
# r = requests.get(init_url)
# print(r.cookies)
#
# login_url = "http://60.1.100.2/sysuser/doSysUserLoginAction.do"
# img_url = "http://60.1.100.2/kaptcha/doReadKaptcha.do"
#
# rsp = requests.get(img_url)
# with open("kaptcha.jpg", "wb") as f:
#     f.write(rsp.content)

# with open("1","w",encoding="utf-8") as f:
#     f.write("我发生的发生朵夫所到")


# proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)
#
# static_proxy ={
#     # "https":"https://178.33.4.48:3128",
#     "http":"http://%s:%s@proxy.abuyun.com:9010".format(proxyUser, proxyPass)
#     # 'http': 'http://93.186.253.122:1189'
# }
#
# r = requests.get("http://www.baidu.com",proxies=static_proxy)
# print(r.text)
#
# r= requests.get("http://www.jsonip.com",proxies=static_proxy)
# print(r.text)

# from urllib import request
#
# # 要访问的目标页面
# targetUrl = "http://test.abuyun.com/proxy.php"
# targetUrl = "http://www.jsonip.com"
# #targetUrl = "http://proxy.abuyun.com/switch-ip"
# #targetUrl = "http://proxy.abuyun.com/current-ip"
#
# # 代理服务器
# proxyHost = "proxy.abuyun.com"
# proxyPort = "9010"
#
# # 代理隧道验证信息
#
# proxyUser = "H8PX142BPZXA2V0D"
# proxyPass = "52DE8535C1DEA206"
#
# proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
#     "host" : proxyHost,
#     "port" : proxyPort,
#     "user" : proxyUser,
#     "pass" : proxyPass,
# }
#
# proxy_handler = request.ProxyHandler({
#     "http"  : proxyMeta,
#     # "https" : proxyMeta,
# })
#
# proxy_handler={
#     "http": proxyMeta,
#     "https": proxyMeta,
# }
# print(proxy_handler)
# r= requests.get("http://www.jsonip.com",proxies=proxy_handler)
#auth = request.HTTPBasicAuthHandler()
#opener = request.build_opener(proxy_handler, auth, request.HTTPHandler)

# opener = request.build_opener(proxy_handler)


# opener.addheaders = [("Proxy-Switch-Ip", "yes")]
# request.install_opener(opener)
# resp = request.urlopen(targetUrl).read()

# print (r.text)
#
# proxy_handler = {
#     'http': 'http://218.75.116.58:9999',
#     'https': 'https://218.75.116.58:9999'
# }
# r = requests.get(config.TEST_IP, proxies=proxy_handler, timeout = config.TIMEOUT)
# print(r.text)
#
# list1 = [1,2,3,4,5,6]
# list2 = ["a",'b','c','d']
# for key,value in zip(list1,list2):
#     print(key,value)
# import os
# import time
# print(time.strftime("%Y%m%d",time.localtime()))

# html =  """
#
# """
# from pyquery import PyQuery as pq
# from bs4 import  BeautifulSoup
# # html = BeautifulSoup(html, 'lxml')
# # print(html.contents)
# from lxml import etree
#
# content = pq(html)
# print(content.text())
# reg = re.compile("span class=\"hx-table-paging-totPage\">(\d+)</span>")
# print(re.findall(reg, html)[0])
# import datetime
#
# time1 = 	"2017-06-20T01:03:56"
# print(datetime.datetime.strftime(parse(time1), "%Y-%m-%d"))
# re.findall()

# if "\"fd\"".startswith("\"") and "\"fd\"".endswith("\""):
#     print("ok")


# d = pq(content)
# print(d.html())
# content = d('.mainlist> .padding5>span')
# print(content.eq(1).text()) #评分解读
# print(content.eq(3).text()) #资本实力
# print(content.eq(5).text()) #运营能力
# print(content.eq(7).text()) #盈利能力
# print(content.eq(9).text()) #偿付能力
# print(content.eq(11).text()) #发展潜力


# for i in content.items():
#     if i.attr("style"):
#         print(i.text())
# print(d.filter(lambda i:pq(content).attr('style').text() == "font-size:15px"))
# for i in html(".mainlist> .padding5").items('span'):
#     print(i.eq(0).html())
#     print()
#     print()
    # break
# for i in range(0,1):
#     print(i)

# v_dict = {"a":"a", "b":"b", "c":None, "d":"d"}
#
# for key, value in v_dict.items():
#     if not value:
#         v_dict[key] = ""
#     v_dict[key] = "\"" + v_dict[key] + "\""
#
# print(",".join(str(x) for x in v_dict.values()))

import pyodbc

conn = pyodbc.connect(DSN="db2local")
cursor = conn.cursor()

sql = "select REGNO,NAME,CORPID,NOCORPID,case when ENTUNSCID is null then '' else ENTUNSCID end from company"
cursor.execute(sql)
rows = cursor.fetchall()
for i in rows:
    for j in range(0,len(i)):
        i[j] = "\""+i[j]+"\""
    # print(i)
    # break
#     print(map(lambda x: "\""+x+"\"",i))

    print(",".join(i))