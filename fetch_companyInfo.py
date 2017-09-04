# coding:utf-8

import datetime
import logging
import os
import re
import sys
import time
import traceback

from dateutil.parser import parse
from lxml import etree
from pyquery import PyQuery as pq

import config
from db.PyodbcHelper import *
from util import login


class Logger:
    def __init__(self, logName, logFile):
        self._logger = logging.getLogger(logName)
        log_path, filename = os.path.split(logFile)

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        handler = logging.FileHandler(logFile, mode='w', encoding='utf-8')
        formatter = logging.Formatter('%(levelname)s: %(asctime)s  %(message)s')
        handler.setFormatter(formatter)
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(handler)

    def log(self, msg):
        if self._logger is not None:
            self._logger.info(msg)


class Texter:
    def __init__(self, logName, logFile):
        self._logger = logging.getLogger(logName)
        log_path, filename = os.path.split(logFile)

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        handler = logging.FileHandler(logFile, mode='w', encoding='utf-8')
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

    def log(self, msg):
        if self._logger is not None:
            self._logger.info(msg)


class FetchInfo():
    def __init__(self):
        self.localtime = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        self.my_session = self.get_session()
        self.company = Company()
        self._status = 0

    def get_session(self):
        session = login.Login_Session()
        if config.active_login:
            success_session = session.get_login_data()
            return success_session
        else:
            return session

    def fetch_all(self):
        result = self.company.select()
        for com in result:
            self.fetch_company(com)
            self.fetch_info_zbxx(com)
            self.fetch_info_ggxx(com)
            self.fetch_info_xkxx(com)
            self.fetch_info_xzcf(com)
            self.fetch_info_yqqf(com)
            self.fetch_info_bdcdy(com)
            self.fetch_info_dcdy(com)
            self.fetch_info_pwqdy(com)
            self.fetch_info_cfxx(com)
            self.fetch_info_sdq(com)
            self.fetch_info_jyyc(com)
            self.fetch_credit_xybg(com)
            self.fetch_credit_xyls(com)
            self.fetch_risk_fxzs(com)
            self.fetch_risk_fxmx(com)
            

        return self._status

    def format_string(self, v_dict):
        """ 输入字典, 输出格式化的字符串"""
        for key, value in v_dict.items():
            if value == None:
                v_dict[key] = ""

            v_dict[key] = "\""+ str(v_dict[key]) + "\""

        return ",".join(str(x) for x in v_dict.values())

    def parse_list(self, lists):
        if lists:
            return re.sub('\s+', '', lists[0])
        else:
            return None

    def html_parse(self, string):
        string = string.replace("</html>","")
        return string

    def date_parse(self, string):
        string = string.replace("年","-").replace("月","-").replace("日","")
        string = string.replace('/','-')
        return string

    def fetch_company(self, company):
        """企业基本信息"""
        # self.company_info.init_db()
        company_info = OrderedDict()
        url = "http://60.1.100.2/appsearch/doEnEntBaseInfo.do?corpid=%s" % company.CORPID
        fetch_company_info.log('now crawling 企业基本信息 %s : %s' % (company.REGNO, company.NAME))

        try:
            try:
                resp = self.my_session.get(url, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.get(url, timeout=10)
            company_info["smy_dt"] = self.localtime
            company_info["regno"] = company.REGNO  # 注册号
            content = pq(self.html_parse(resp.text))
            company_info["name"] = content("div#tr2>table>tr>td").eq(0).text()
            company_info["leprep"] = content("div#tr2>table>tr>td").eq(1).text()
            company_info["regorg"] = content("div#tr2>table>tr>td").eq(3).text()
            company_info["regloc"] = content("div#tr2>table>tr>td").eq(2).text()
            company_info["type"] = content("div#tr2>table>tr>td").eq(4).text()
            company_info["estdate"] = self.date_parse(content("div#tr2>table>tr>td").eq(5).text())
            company_info["mgrbegin"] = self.date_parse(content("div#tr2>table>tr>td").eq(6).text())
            company_info["mgrend"] = self.date_parse(content("div#tr2>table>tr>td").eq(7).text())
            company_info["mgrscrope"] = content("div#tr2>table>tr>td").eq(8).text()

            # self.company_info.insert(company_info)
            company_info_txt.log(self.format_string(company_info))
            fetch_company_info.log(company_info)
            print(company_info)

            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self._status = -1

    def fetch_info_zbxx(self, company):
        """资本信息"""
        zbxx_info = OrderedDict()
        # self.zbxx_info.init_db()
        url = 'http://60.1.100.2/crreportconinfo/doReadCrReportConInfoListJSON.do'
        fetch_company_info.log('now crawling 资本信息 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'pageNo1': '',
            'pageSize': '',
            'ajaxUrl': '/jsp/server/entappcon/crreportconinfo.jsp',
            'corpid': company.NOCORPID,
            '_t': int(time.time() * 1000)
        }

        try:
            try:
                resp = self.my_session.get(url, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.get(url, timeout=10)
            infos = resp.json().get('dataList')
            if infos:
                for info in infos:
                    # print(info)
                    zbxx_info["smy_dt"] = self.localtime
                    zbxx_info["regno"] = company.REGNO  # 主键
                    zbxx_info["coninforegno"] = info.get("conInfoRegNo")  # 标识号, 主键
                    zbxx_info["coninfoname"] = info.get("conInfoName")  # 股东名称
                    zbxx_info["payconamount"] = info.get('conInfoPayConAmount')  # 认缴金额
                    zbxx_info["paydate"] = info.get('conInfoPayDate')  # 认缴日期
                    zbxx_info["invform"] = info.get('conInfoInvForm')  # 认缴方式
                    zbxx_info["actconamount"] = info.get('conInfoActConAmount')  # 实缴金额
                    zbxx_info["actdate"] = info.get('conInfoActDate')    # 实缴日期
                    zbxx_info["actform"] = info.get('conInfoActForm')  # 实缴方式
                    zbxx_info["percent"] = info.get('conInfoPercent')  # 股权比例
                # self.zbxx_info.insert(zbxx_info)

                    zbxx_info_txt.log(self.format_string(zbxx_info))
                    fetch_company_info.log(zbxx_info)
                    print(zbxx_info)
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self._status = -1

    def fetch_info_ggxx(self, company):
        """高管信息"""
        ggxx_info = OrderedDict()
        # self.ggxx_info.init_db()
        url = 'http://60.1.100.2/crreportconinfo/doReadHzQydsjlryListJSON.do'
        fetch_company_info.log('now crawling 高管信息 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'pageNo1': '',
            'pageSize': 100,
            'ajaxUrl': '/jsp/server/entappcon/hzqydsjlryList.jsp',
            'corpid': company.NOCORPID,
            '_t': int(time.time() * 1000)
        }

        try:
            try:
                resp = self.my_session.post(url, data=data,timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            infos = resp.json().get('dataList')
            if infos:
                for info in infos:
                    ggxx_info["smy_dt"] = self.localtime
                    ggxx_info["regno"] = company.REGNO  # 主键
                    ggxx_info["sfzjhm"] = info.get("sfzjhm")  # 标识号 主键
                    ggxx_info["zwmc"] = info.get("zwmc")  # 职务
                    ggxx_info["xm"] = info.get("xm")  # 姓名
                    # self.ggxx_info.insert(ggxx_info)
                    ggxx_info_txt.log(self.format_string(ggxx_info))
                    fetch_company_info.log(ggxx_info)
                    print(ggxx_info)
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_info_xkxx(self, company):
        """许可信息"""
        xkxx_info = OrderedDict()
        # self.xkxx_info.init_db()
        url = 'http://60.1.100.2/crlicense/doReadPermissionCrLicenseListJSON.do'
        fetch_company_info.log('now crawling 许可信息 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'pageNo2': '',
            'pageSize': 100,
            'ajaxUrl': '/jsp/server/entappcon/crlicenseList.jsp',
            'corpid': company.NOCORPID,
            '_t': int(time.time() * 1000)
        }

        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            infos = resp.json().get('dataList')
            if infos:
                for info in infos:
                    # print(info)
                    xkxx_info["smy_dt"] = self.localtime
                    xkxx_info["regno"] = company.REGNO  # 主键
                    xkxx_info["licDocNo"] = info.get("licDocNo")  # 许可文件编号 ,主键
                    xkxx_info["licDocName"] = info.get("licDocName")  # 许可文件名称
                    xkxx_info["licValidFrom"] = self.date_parse(info.get("licValidFrom"))  # 许可文件有效期自
                    xkxx_info["licValidTo"] = self.date_parse(info.get("licValidTo"))  # 许可文件有效期至
                    xkxx_info["importFrom"] = info.get("importFrom")  # 许可机关
                    xkxx_info["licContent"] = info.get("licContent")  # 许可内容
                    xkxx_info["state"] = info.get("state")  # 是否到期

                # self.xkxx_info.insert(xkxx_info)
                    xkxx_info_txt.log(self.format_string(xkxx_info))
                    fetch_company_info.log(xkxx_info)
                    print(xkxx_info)
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_info_xzcf(self, company):
        """行政处罚信息"""
        # company.NOCORPID = "3306820000106170"
        xzcf_info = OrderedDict()
        # self.xzcf_info.init_db()
        url = 'http://60.1.100.2/crpunish/doReadCrPunishListJSON.do'
        fetch_company_info.log('now crawling 行政处罚信息 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'pageNo3': '',
            'pageSize': 100,
            'ajaxUrl': '/jsp/server/entappcon/crpunishList.jsp',
            'corpid': company.NOCORPID,
            '_t': int(time.time() * 1000)
        }
        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            infos = resp.json().get('dataList')
            if infos:
                for info in infos:
                    # print(info)
                    xzcf_info["smy_dt"] = self.localtime
                    xzcf_info["regno"] = company.REGNO  # 主键
                    xzcf_info["id"] = info.get("id")  # 标识号,主键
                    xzcf_info["punDocno"] = info.get("punDocno")  # 行政处罚文书号
                    xzcf_info["punOrgName"] = info.get("punOrgName")  # 执法部门
                    xzcf_info["punishedName"] = info.get("punishedName")  # 公司名
                    xzcf_info["punRegionName"] = info.get("punRegionName")  # 地区名
                    xzcf_info["punDate"] = self.date_parse(info.get("punDate"))  # 作出行政处罚决定日期
                    xzcf_info["punState"] = info.get("punState")  # 状态
                    xzcf_info["punishedLegRep"] = info.get("punishedLegRep")  # 处罚法人代表
                    # xzcf_info["punAbstract"] = info.get("punAbstract")  # 处罚概要  存在不可解析的html
                    xzcf_info["punCaseName"] = info.get("punCaseName")  # 案件名称
                    xzcf_info["punItemName"] = info.get("punItemName")  # 处罚类型

                    # self.xzcf_info.insert(xzcf_info)
                    xzcf_info_txt.log(self.format_string(xzcf_info))
                    fetch_company_info.log(xzcf_info)
                    print(xzcf_info)
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_info_sfxx(self):
        """司法信息 无权查看"""
        pass

    def fetch_info_gqdj(self):
        """股权冻结,未找到"""
        pass

    def fetch_info_yqqf(self, company):
        """逾期或欠费信息"""
        company.CORPID = "CBC3F2D434091DF5AB61F930F92E1420B08685D23A98ADDAD07DF06B5581D85C"
        company.NOCORPID="3306820000084374"
        yqqf_info = OrderedDict()
        # self.yqqf_info.init_db()
        url = 'http://60.1.100.2/crarrearinfo/doReadCrArrearInfoListJSON.do'
        fetch_company_info.log('now crawling 逾期或欠费信息 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'corpid': company.NOCORPID,
            '_t': int(time.time() * 1000)
        }
        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            infos = resp.json().get('dataList')
            if infos:
                for info in infos:
                    # print(info)
                    fromtable = info.get("fromTable")  # 获取详细信息
                    qf_url = 'http://60.1.100.2/crarrearinfo/doEnAllArrearList.do?corpid=%s&fromtable=%s' % (
                        company.CORPID, fromtable)

                    try:
                        response = self.my_session.get(qf_url, timeout=10)
                    except Exception:
                        print("网络连接中断,尝试重连中...")
                        self.my_session = self.get_session()
                        response = self.my_session.get(qf_url, timeout=10)

                    print(response)
                    print(response.txt)
                    html = etree.HTML(response.text)
                    # print(response.text)
                    items = html.xpath('//*[@class="listbox3"]//tr')
                    for i in range(1, len(items)):
                        yqqf_info["smy_dt"] = self.localtime
                        yqqf_info["regno"] = company.REGNO  # 主键
                        yqqf_info["arrearType"] = info.get("arrearType")  # 逾期类型
                        yqqf_info["importFrom"] = info.get("importFrom")  # 所属机构

                        arrearperiod = html.xpath('//*[@class="listbox3"]//tr[%s]/td[1]/text()' % str(i + 1))
                        print(arrearperiod)

                        arrearperiod = self.parse_list(
                            html.xpath('//*[@class="listbox3"]//tr[%s]/td[3]/text()' % str(i + 1)))
                        print(arrearperiod)
                        print("----")
                        print(yqqf_info.get("arrearperiod"))
                        if yqqf_info.get("arrearperiod") == arrearperiod:
                            continue
                        yqqf_info["arrearperiod"] = arrearperiod   # 欠费所属期 ,主键
                        arrearbalance = self.parse_list(
                            html.xpath('//*[@class="listbox3"]//tr[%s]/td[4]/text()' % str(i + 1)))
                        # print(arrearbalance)
                        yqqf_info["arrearbalance"] = arrearbalance  # 欠费金额（元）

                        fetch_company_info.log(yqqf_info)
                        yqqf_info_txt.log(self.format_string(yqqf_info))
                        print(yqqf_info)
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_info_bdcdy(self, company):
        """不动产抵押信息"""
        # company.NOCORPID = "3300000000012330"
        bdcdy_info = OrderedDict()
        # self.bdcdy_info.init_db()
        url = 'http://60.1.100.2/mortgagereg/doReadHomeMortgageListJSON.do'
        fetch_company_info.log('now crawling 不动产抵押信息 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'pageNo6': '',
            'pageSize': 100,
            'ajaxUrl': '/jsp/server/entappcon/homeMortgageList.jsp',
            'corpid': company.NOCORPID,
            '_t': int(time.time() * 1000)
        }
        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            infos = resp.json().get('dataList')

            if infos:
                for info in infos:
                    bdcdy_info["smy_dt"] = self.localtime
                    bdcdy_info["regno"] = company.REGNO  # 主键
                    bdcdy_info["mortgageCertNo"] = info.get("mortgageCertNo")  # 抵押证编号 ,主键
                    bdcdy_info["mortgageGuarExtent"] = info.get("mortgageGuarExtent")  # 抵押担保范围
                    bdcdy_info["mortgageeName"] = info.get("mortgageeName")  # 抵押权人名称
                    bdcdy_info["guaranteedCreditAmount"] = info.get("guaranteedCreditAmount")  # 被担保主债权数额（万元）
                    bdcdy_info["debtPayFrom"] = self.date_parse(info.get("debtPayFrom"))  # 债务期限起
                    bdcdy_info["debtPayTo"] = self.date_parse(info.get("debtPayTo"))  # 债务期限至
                    bdcdy_info["mortgageReason"] = self.date_parse(info.get("mortgageReason"))  # 申请抵押原因

                    fetch_company_info.log(bdcdy_info)
                    bdcdy_info_txt.log(self.format_string(bdcdy_info))
                    print(bdcdy_info)
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_info_dcdy(self, company):
        """动产抵押信息"""
        # company.NOCORPID = "3300000000012330"
        dcdy_info = OrderedDict()
        # self.dcdy_info.init_db()
        url = 'http://60.1.100.2/crdcdyapplyinfo/doReadCrDcdyApplyinfoListJSON.do'
        data = {
            'corpid': company.NOCORPID,
            '_t': int(time.time() * 1000)
        }
        fetch_company_info.log('now crawling 动产抵押信息 %s : %s' % (company.REGNO, company.NAME))
        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            infos = resp.json().get('dataList')
            if infos:
                for info in infos:
                    dcdy_info["smy_dt"] = self.localtime
                    dcdy_info["regno"] = company.REGNO  # 主键
                    dcdy_info["orderNo"] = info.get("orderNo")  # 抵押证编号 ,主键
                    dcdy_info["department"] = info.get("department")  # 抵押登记机关
                    dcdy_info["guaranteesRange"] = info.get("guaranteesRange")  # 抵押担保范围
                    dcdy_info["mortgageeName"] = info.get("mortgageeName")  # 抵押权人名称
                    dcdy_info["mortgageeCertNo"] = info.get("mortgageeCertNo")  # 	抵押权人证件号
                    dcdy_info["mortgageAmount"] = info.get("mortgageAmount")  # 被担保主债权数额（万元）

                    if info.get("startdate"):
                        dcdy_info["startdate"] = datetime.datetime.strftime(parse(info.get("startdate")),"%Y-%m-%d")  # 债务期限起
                    else:
                        dcdy_info["startdate"] = info.get("startdate")

                    if info.get("enddate"):
                        dcdy_info["enddate"] = datetime.datetime.strftime(parse(info.get("enddate")),"%Y-%m-%d")  # 债务期限至
                    else:
                        dcdy_info["enddate"] = info.get("enddate")

                    fetch_company_info.log(dcdy_info)
                    dcdy_info_txt.log(self.format_string(dcdy_info))
                    print(dcdy_info)
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_info_czxx(self, company):
        """出质信息, 未找到"""
        pass

    def fetch_info_pwqdy(self, company):
        """排污权抵押"""
        # company.NOCORPID = "3306820000082955"
        pwqdy_info = OrderedDict()
        url = "http://60.1.100.2/crmortgagesewagedischargeright/doReadCrMortgageSewageDischargeRightListJSON.do"
        fetch_company_info.log('now crawling 排污权抵押信息 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'corpid': company.NOCORPID,
            '_t': int(time.time() * 1000)
        }

        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            infos = resp.json().get('dataList')
            if infos:
                for info in infos:
                    pwqdy_info["smy_dt"] = self.localtime
                    pwqdy_info["regno"] = company.REGNO  # 主键
                    pwqdy_info["mortgageeName"] = info.get("mortgageeName")  # 抵押权人名称
                    pwqdy_info["guaranty"] = info.get("guaranty")  # 抵押物名称
                    pwqdy_info["mortgageWastewaterAmount"] = info.get("mortgageWastewaterAmount")  # 抵押废水数量（吨/日）
                    pwqdy_info["mortgageSo2Amount"] = info.get("mortgageSo2Amount")  # 抵押二氧化硫数量（吨/年）
                    pwqdy_info["mortgageNoAmount"] = info.get("mortgageNoAmount")  # 抵押氮氧化物数量
                    pwqdy_info["guarantyNo"] = info.get("guarantyNo")  # 抵押物权证编号
                    pwqdy_info["debtPayDate"] = info.get("debtPayDate")  # 债务人履行债务期限
                    pwqdy_info["regOrg"] = info.get("regOrg")  # 登记机关
                    pwqdy_info["regDate"] = info.get("regDate")  # 登记时间

                    print(pwqdy_info)
                    fetch_company_info.log(pwqdy_info)
                    pwqdy_info_txt.log(self.format_string(pwqdy_info))

            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_info_cfxx(self,company):
        """查封信息"""
        # company.NOCORPID = "3306006090166956"
        cfxx_info = OrderedDict()
        # self.cfxx_info.init_db()
        url = 'http://60.1.100.2/crsequestrateall/doReadCrSequestrateAllListJSON.do'
        fetch_company_info.log('now crawling 查封信息 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'pageNo11': '',
            'pageSize': 100,
            'ajaxUrl': '/jsp/server/entappcon/crsequestrateallList.jsp',
            'corpid': company.NOCORPID,
            '_t': int(time.time() * 1000)
        }
        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            infos = resp.json().get('dataList')
            if infos:
                for info in infos:
                    cfxx_info["smy_dt"] = self.localtime
                    cfxx_info["regno"] = company.REGNO  # 主键
                    if info.get("importFrom") == "建设局":
                        cfxx_info["sequestrateType"] = "房产查封"    # 查封类型
                    else:
                        cfxx_info["sequestrateType"] = "土地查封"
                    cfxx_info["sequestrateNo"] = info.get("sequestrateNo")  # 查封文号,主键
                    cfxx_info["sequestrateLoc"] = info.get("sequestrateLoc")  # 查封房屋坐落
                    cfxx_info["sequestrateApplyName"] = info.get("sequestrateApplyName")  # 申请查封单位
                    if info.get("tsaSeizeStartDate"):
                        cfxx_info["tsaSeizeStartDate"] = datetime.datetime.strftime(parse(info.get("tsaSeizeStartDate")),"%Y-%m-%d")  # 查封起始日期
                    else:
                        cfxx_info["tsaSeizeStartDate"] = info.get("tsaSeizeStartDate")

                    if info.get("tsaSeizeEndDate"):
                        cfxx_info["tsaSeizeEndDate"] = datetime.datetime.strftime(parse(info.get("tsaSeizeEndDate")),"%Y-%m-%d")  # 查封截止日期
                    else:
                        cfxx_info["tsaSeizeEndDate"] = info.get("tsaSeizeEndDate")

                    cfxx_info["cancelDate"] = info.get("cancelDate")  # 撤销查封日期
                    cfxx_info["state"] = info.get("state")  # 状态
                    # self.cfxx_info.insert(cfxx_info)
                    cfxx_info_txt.log(self.format_string(cfxx_info))
                    print(cfxx_info)
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_info_sdq(self,company):
        """水电气信息"""
        # company.NOCORPID = "3306820000082955"
        sdq_info = OrderedDict()
        url = 'http://60.1.100.2/appsearch/doReadWaterGasElecResJSON.do'
        fetch_company_info.log('now crawling 水电气信息 %s : %s' % (company.REGNO, company.NAME))
        try:
            for sdq in ['water', 'elec', 'gas']:
                sdq_info.clear()
                data = {
                    'publicSourceType': sdq,
                    'corpid': company.NOCORPID
                }
                try:
                    resp = self.my_session.post(url, data=data, timeout=10)
                except Exception:
                    print("网络连接中断,尝试重连中...")
                    self.my_session = self.get_session()
                    resp = self.my_session.post(url, data=data, timeout=10)

                print(resp.json())
                vals = resp.json().get('dataMap')
                if vals:
                    vals = vals.get('dataList')
                times = resp.json().get('dataMap')
                if times:
                    times = times.get('timeList')
                if vals and times:  # 存在数据
                    infos = zip(vals, times)
                    for vals, times in infos:
                        sdq_info["smy_dt"] = self.localtime
                        sdq_info["regno"] = company.REGNO  # 主键
                        sdq_info["times"] = times
                        sdq_info["vals"] = vals
                        if sdq == "water":
                            sdq_info["type"] = "water"
                        elif sdq == "elec":
                            sdq_info["type"] = "elec"
                        elif sdq == "gas":
                            sdq_info["type"] = "gas"

                        fetch_company_info.log(sdq_info)
                        sdq_info_txt.log(self.format_string(sdq_info))
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self._status = -1

    def fetch_info_jyyc(self, company):
        """经营异常名录"""
        # company.NOCORPID = "3306000090131020"
        jyyc_info = OrderedDict()
        url = "http://60.1.100.2/pubcatalogapply/doReadPubCatalogApplyList.do"
        fetch_company_info.log('now crawling 经营异常名录 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'corpid': company.NOCORPID,
            '_t': int(time.time() * 1000)
        }
        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            infos = resp.json().get('dataList')
            if infos:
                for info in infos:
                    jyyc_info["smy_dt"] = self.localtime
                    jyyc_info["regno"] = company.REGNO  # 主键
                    jyyc_info["appInReaCode"] = info.get("appInReaCode")    # 列入经营异常原因
                    jyyc_info["appInDate"] = info.get("appInDate")       # 列入日期
                    jyyc_info["canOutReaCode"] = info.get("canOutReaCode")  # 移出经营异常名录原因
                    jyyc_info["canOutDate"] = info.get("canOutDate")     # 移出日期
                    jyyc_info["appOrgName"] = info.get("appOrgName")    # 作出决定机关

                    print(jyyc_info)
                    fetch_company_info.log(jyyc_info)
                    jyyc_info_txt.log(self.format_string(jyyc_info))
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_credit_xybg(self, company):
        """信用报告"""
        # company.NOCORPID = "3306820000106178"
        # company.NOCORPID = "3306820000106170"
        # company.CORPID = "BEE872D51346B1E701A3A7505BE690DDB08685D23A98ADDAD07DF06B5581D85C"
        xybg_info = OrderedDict()
        url = 'http://60.1.100.2/crcreditdms/doReadCrCreditDmsByIdJSON.do'
        fetch_company_info.log('now crawling 信用报告信息 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'crCreditDms.corpid':company.NOCORPID
        }
        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            if not resp.json():  # 不存在记录
                return
            xybg_info["smy_dt"] = self.localtime
            xybg_info["regno"] = company.REGNO  # 主键
            xybg_info["dmsScore"] = resp.json().get('dmsScore')  # 当月信用值
            xybg_info["dmsAvgScore"] = resp.json().get('dmsAvgScore')  # 平均信用值

            url2 = 'http://60.1.100.2/crcreditdms/doReadCrCreditDmsListJSON.do'
            try:
                resp = self.my_session.post(url2, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url2, data=data, timeout=10)

            scorelist = resp.json().get('scorelist')
            avgScoreList = resp.json().get('avgScoreList')

            if scorelist:
                xybg_info["zbsl"] = scorelist[0]  # 资本实力
                xybg_info["yynl"] = scorelist[1]  # 运营能力
                xybg_info["ylnl"] = scorelist[2]  # 盈利能力
                xybg_info["cfnl"] = scorelist[3]  # 偿付能力
                xybg_info["fzql"] = scorelist[4]  # 发展潜力
            if xybg_info:
                xybg_info["avgzbsl"]= avgScoreList[0]   # 平均资本实力水平
                xybg_info["avgyynl"]= avgScoreList[1]   # 平均运营能力水平
                xybg_info["avgylnl"]= avgScoreList[2]   # 平均盈利能力水平
                xybg_info["avgcfnl"]= avgScoreList[3]   # 平均偿付能力水平
                xybg_info["avgfzql"] = avgScoreList[4]  # 平均发展潜力水平

            time.sleep(1)

            url3 = "http://60.1.100.2/creditsearch/doEnCreditReport.do?corpid=%s" % company.CORPID
            try:
                resp = self.my_session.get(url3, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url3, timeout=10)

            html = pq(resp.text)

            content = html('.mainlist> .padding5>span')
            xybg_info["pfjd"] = content.eq(1).text()  # 评分解读
            xybg_info["zbsljd"] = content.eq(3).text()  # 资本实力解读
            xybg_info["yynljd"] = content.eq(5).text()  # 运营能力解读
            xybg_info["ylnljd"] = content.eq(7).text()  # 盈利能力解读
            xybg_info["cfnljd"] = content.eq(9).text()  # 偿付能力解读
            xybg_info["fzqljd"] = content.eq(11).text()  # 发展潜力解读

            print(xybg_info)
            fetch_company_info.log(xybg_info)
            xybg_credit_txt.log(self.format_string(xybg_info))

            time.sleep(1)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_credit_xyls(self, company):
        """信用历史"""
        # company.NOCORPID = "3306820000106178"
        xyls_info = OrderedDict()
        url = 'http://60.1.100.2/creditdmshis/doReadCreditResultHisListJSON.do'
        fetch_company_info.log('now crawling 信用历史信息 %s : %s' % (company.REGNO, company.NAME))
        data = {
            'crCreditDms.corpid': company.NOCORPID
        }
        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            scoreList = resp.json().get('scoreList')
            dateList = resp.json().get('dateList')

            if scoreList and dateList:
                info = zip(scoreList, dateList)
                for value, times in info:
                    xyls_info["smy_dt"] = self.localtime
                    xyls_info["regno"] = company.REGNO  # 主键
                    xyls_info["time"] = times  # 时间
                    xyls_info["value"] = value  # 信用评分

                    xyls_credit_txt.log(self.format_string(xyls_info))
                    fetch_company_info.log(xyls_info)
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_risk_fxzs(self, company):
        """风险指数"""
        # company.NOCORPID = "3306820000106178"
        fxzs_info = OrderedDict()
        fetch_company_info.log('now crawling 风险指数 %s : %s' % (company.REGNO, company.NAME))
        url = 'http://60.1.100.2/crristindex/doEnCrRistIndexAnaly.do?corpid=%s' % company.NOCORPID
        try:
            resp = self.my_session.get(url, timeout=10)
        except Exception:
            print("网络连接中断,尝试重连中...")
            self.my_session = self.get_session()
            resp = self.my_session.get(url, timeout=10)

        reg = 'data : {"corpid":corpid,"trade":(\d+)'
        trade_num = re.findall(reg, resp.text)
        data = {
            'corpid': company.NOCORPID,
            'trade': trade_num
        }
        url = 'http://60.1.100.2/crristindex/doReadCrRistIndexAnalyJSON.do'

        try:
            try:
                resp = self.my_session.post(url, data=data, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                resp = self.my_session.post(url, data=data, timeout=10)

            axisList = resp.json().get('axisList')
            dataList = resp.json().get('dataList')

            if axisList and dataList:
                info = zip(axisList, dataList)
                for times, value in info:
                    fxzs_info["smy_dt"] = self.localtime
                    fxzs_info["regno"] = company.REGNO  # 主键
                    fxzs_info["times"] = times     # 日期
                    fxzs_info["value"] = value     # 风险指数
                    fetch_company_info.log(fxzs_info)
                    fxzs_risk_txt.log(self.format_string(fxzs_info))
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            self._status = -1

    def fetch_risk_fxmx(self, company):
        """风险明细"""
        # company.NOCORPID = "3306820000106178"
        fetch_company_info.log('now crawling 风险明细 %s : %s' % (company.REGNO, company.NAME))
        fxmx_info = OrderedDict()
        url = "http://60.1.100.2/crristdetail/doGetRistIndexRecordsListJSON.do?pageSize=100&corpid=%s" % company.NOCORPID
        try:
            try:
                content = self.my_session.get(url, timeout=10)
            except Exception:
                print("网络连接中断,尝试重连中...")
                self.my_session = self.get_session()
                content = self.my_session.get(url, timeout=10)
            resp = pq(content.text)
            totalpage = resp(".hx-table-paging-totPage").text()   # 共有多少页
            if totalpage:  # 存在记录
                for i in range(1, int(totalpage)+1):
                    url = "http://60.1.100.2/crristdetail/doGetRistIndexRecordsListJSON.do?pageNo=%s&corpid=%s"% (i,company.NOCORPID)
                    try:
                        resp = self.my_session.get(url, timeout=10)
                    except Exception:
                        print("网络连接中断,尝试重连中...")
                        self.my_session = self.get_session()
                        resp = self.my_session.get(url, timeout=10)

                    content = pq(resp.text)
                    for i in content(".listbox3>tr").items():
                        fxmx_info["smy_dt"] = self.localtime
                        fxmx_info["regno"] = company.REGNO  # 主键
                        fxmx_info["risk_target"] = i("td").eq(1).text()  # 预警指标
                        fxmx_info["risk_level"] = i("td").eq(2).text()  # 预警级别
                        fxmx_info["risk_update_date"] = i("td").eq(3).text()  # 预警更新日期
                        if fxmx_info["risk_target"]:
                            print(fxmx_info)
                            fetch_company_info.log(fxmx_info)
                            fxmx_risk_txt.log(self.format_string(fxmx_info))
            time.sleep(1)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_company_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self._status = -1


# 日志文件
fetch_company_info = Logger("fetch_company_info", config.company_info_log_path)

# 存储文件
company_info_txt = Texter("company_info_txt", config.company_info_path)
zbxx_info_txt = Texter("zbxx_info_txt", config.zbxx_info_path)
ggxx_info_txt = Texter("ggxx_info_txt", config.ggxx_info_path)
xkxx_info_txt = Texter("xkxx_info_txt", config.xkxx_info_path)
xzcf_info_txt = Texter("xzcf_info_txt", config.xzcf_info_path)
yqqf_info_txt = Texter("yqqf_info_txt", config.yqqf_info_path)
bdcdy_info_txt = Texter("bdcdy_info_txt", config.bdcdy_info_path)
dcdy_info_txt = Texter("dcdy_info_txt", config.dcdy_info_path)
pwqdy_info_txt = Texter("pwqdy_info_txt", config.pwqdy_info_path)
cfxx_info_txt = Texter("cfxx_info_txt", config.cfxx_info_path)
jyyc_info_txt = Texter("jyyc_info_txt", config.jyyc_info_path)
sdq_info_txt = Texter("sdq_info_txt", config.sdq_info_path)
xybg_credit_txt = Texter("xybg_credit_txt", config.xybg_credit_path)
xyls_credit_txt = Texter("xyls_credit_txt", config.xyls_credit_path)
fxzs_risk_txt = Texter("fxzs_risk_txt", config.fxzs_risk_path)
fxmx_risk_txt = Texter("fxmx_risk_txt", config.fxmx_risk_path)

if __name__ == "__main__":
    fetchinfo = FetchInfo()
    fetchinfo.fetch_all()
