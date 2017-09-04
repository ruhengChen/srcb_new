# coding:utf-8

import datetime
import logging
import os
import re
import sys
import time
import traceback
from collections import OrderedDict

from dateutil.parser import parse

import config
from util import login


class Logger:
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
        self.localtime = time.strftime('%Y-%m-%d', time.localtime())
        self.session = login.Login_Session()
        if config.active_login:
            self.session = self.session.get_login_data()

        self._status = 0

    def fetch_all(self):
        self.fetch_risk_fxqyjs_now()
        self.fetch_risk_fxqyjs_ls()
        self.fetch_risk_fxqygz_now()
        self.fetch_risk_fxqygz_ls()
        self.fetch_risk_fxqyts_now()
        self.fetch_risk_fxqyts_ls()

        return self._status
    def format_string(self, v_dict):
        """ 输入字典, 输出格式化的字符串"""

        for key, value in v_dict.items():
            if value == None:
                v_dict[key] = ""

            v_dict[key] = "\"" + str(v_dict[key]) + "\""

        return ",".join(str(x) for x in v_dict.values())

    def fetch_risk_fxqyjs_now(self):
        """风险企业警示类预警提示本月"""
        url = "http://60.1.100.2/crristdetail/doReadWarningListJSON.do"
        fetch_risk_info.log('now crawling 本月风险企业警示类预警提示')
        fxqyjs_now_info = OrderedDict()

        idxSupCodeList = ["A02",  # 企业股东变更
                          "C02",  # 欠税
                          "D02",  # 法定代表人任职资格受限
                          "E06",  # 银行信贷逾期欠息
                          "E09",  # 财产查封
                          ]
        try:
            for idxSupCode in idxSupCodeList:
                data = {
                    "_t": time.time()*1000,
                    "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                    "entName": "",
                    "fixparam_risttype": "2",
                    "idxSupCode": idxSupCode,
                    "pageNo1": "",
                    "pageSize": "100",
                    "theEndTime": "",
                    "theStartTime": "",
                    "timeRange": "1",
                }
                resp = self.session.post(url, data=data)
                content = resp.json().get("paginationHtml")
                reg = re.compile("span class=\"hx-table-paging-totPage\">(\d+)</span>")
                totol_page = re.findall(reg, content)[0]

                if totol_page:
                    for i in range(1, int(totol_page)+1):
                        data = {
                            "_t": time.time() * 1000,
                            "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                            "entName": "",
                            "fixparam_risttype": "2",
                            "idxSupCode": idxSupCode,
                            "pageNo1": i,
                            "pageSize": "100",
                            "theEndTime": "",
                            "theStartTime": "",
                            "timeRange": "1",
                        }
                        resp = self.session.post(url, data=data)
                        infos = resp.json().get("dataList")
                        if infos:
                            for info in infos:
                                fxqyjs_now_info["smy_dt"] = self.localtime
                                fxqyjs_now_info["content"] = info.get("content")  # 风险内容
                                fxqyjs_now_info["entName"] = info.get("entName")  # 风险企业
                                fxqyjs_now_info["name"] = info.get("name")  # 风险类型
                                if info.get("dtCreateDate"):  # 更新日期
                                    fxqyjs_now_info["dtCreateDate"] = datetime.datetime.strftime(parse(info.get("dtCreateDate")), '%Y-%m-%d')
                                else:
                                    fxqyjs_now_info["dtCreateDate"] = None

                                print(fxqyjs_now_info)
                                fetch_risk_info.log(fxqyjs_now_info)
                                risk_fxqyjs_now_txt.log(self.format_string(fxqyjs_now_info))

            time.sleep(1)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_risk_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self._status = -1

    def fetch_risk_fxqyjs_ls(self):
        """风险企业警示类预警提示上月"""
        url = "http://60.1.100.2/crristdetail/doReadWarningListJSON.do"
        fetch_risk_info.log('now crawling 上月风险企业警示类预警提示')
        fxqyjs_ls_info = OrderedDict()

        idxSupCodeList = ["A02",  # 企业股东变更
                          "A03",  # 减资变更
                          "C02",  # 欠税
                          "D02",  # 法定代表人任职资格受限
                          "E06",  # 银行信贷逾期欠息
                          "E09",  # 财产查封
                          ]
        try:
            for idxSupCode in idxSupCodeList:
                data = {
                    "_t": time.time() * 1000,
                    "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                    "entName": "",
                    "fixparam_risttype": "2",
                    "idxSupCode": idxSupCode,
                    "pageNo1": "",
                    "pageSize": "100",
                    "theEndTime": "",
                    "theStartTime": "",
                    "timeRange": "2",
                }
                resp = self.session.post(url, data=data)
                content = resp.json().get("paginationHtml")
                reg = re.compile("span class=\"hx-table-paging-totPage\">(\d+)</span>")
                totol_page = re.findall(reg, content)[0]

                if totol_page:
                    for i in range(1, int(totol_page) + 1):
                        data = {
                            "_t": time.time() * 1000,
                            "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                            "entName": "",
                            "fixparam_risttype": "2",
                            "idxSupCode": idxSupCode,
                            "pageNo1": i,
                            "pageSize": "100",
                            "theEndTime": "",
                            "theStartTime": "",
                            "timeRange": "2",
                        }
                        resp = self.session.post(url, data=data)
                        infos = resp.json().get("dataList")
                        if infos:
                            for info in infos:
                                fxqyjs_ls_info["smy_dt"] = self.localtime
                                fxqyjs_ls_info["content"] = info.get("content")  # 风险内容
                                fxqyjs_ls_info["entName"] = info.get("entName")  # 风险企业
                                fxqyjs_ls_info["name"] = info.get("name")  # 风险类型
                                if info.get("dtCreateDate"):  # 更新日期
                                    fxqyjs_ls_info["dtCreateDate"] = datetime.datetime.strftime(
                                        parse(info.get("dtCreateDate")), '%Y-%m-%d')
                                else:
                                    fxqyjs_ls_info["dtCreateDate"] = None

                                print(fxqyjs_ls_info)
                                fetch_risk_info.log(fxqyjs_ls_info)
                                risk_fxqyjs_ls_txt.log(self.format_string(fxqyjs_ls_info))

            time.sleep(1)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_risk_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self._status = -1

    def fetch_risk_fxqygz_now(self):
        """风险企业关注类预警提示本月"""
        url = "http://60.1.100.2/crristdetail/doReadWarningListJSON.do"
        fetch_risk_info.log('now crawling 本月风险企业关注类预警提示')
        fxqygz_now_info = OrderedDict()

        idxSupCodeList = ["A02",  # 企业股东变更
                          "A03",  # 减资变更
                          "B01",  # 业务下滑风险
                          "C02",  # 工商经营异常名录
                          "C04",  # 其他部门欠费
                          "D01",  # 法定代表人变更
                          "E01",  # 对外担保
                          "E06",  # 银行信贷逾期欠息
                          "E07",  # 质押抵押
                          ]
        try:
            for idxSupCode in idxSupCodeList:
                data = {
                    "_t": time.time() * 1000,
                    "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                    "entName": "",
                    "fixparam_risttype": "3",
                    "idxSupCode": idxSupCode,
                    "pageNo1": "",
                    "pageSize": "100",
                    "theEndTime": "",
                    "theStartTime": "",
                    "timeRange": "1",
                }
                resp = self.session.post(url, data=data)
                content = resp.json().get("paginationHtml")
                reg = re.compile("span class=\"hx-table-paging-totPage\">(\d+)</span>")
                totol_page = re.findall(reg, content)[0]

                if totol_page:
                    for i in range(1, int(totol_page) + 1):
                        data = {
                            "_t": time.time() * 1000,
                            "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                            "entName": "",
                            "fixparam_risttype": "3",
                            "idxSupCode": idxSupCode,
                            "pageNo1": i,
                            "pageSize": "100",
                            "theEndTime": "",
                            "theStartTime": "",
                            "timeRange": "1",
                        }
                        resp = self.session.post(url, data=data)
                        infos = resp.json().get("dataList")
                        if infos:
                            for info in infos:
                                fxqygz_now_info["smy_dt"] = self.localtime
                                fxqygz_now_info["content"] = info.get("content")  # 风险内容
                                fxqygz_now_info["entName"] = info.get("entName")  # 风险企业
                                fxqygz_now_info["name"] = info.get("name")  # 风险类型
                                if info.get("dtCreateDate"):  # 更新日期
                                    fxqygz_now_info["dtCreateDate"] = datetime.datetime.strftime(
                                        parse(info.get("dtCreateDate")), '%Y-%m-%d')
                                else:
                                    fxqygz_now_info["dtCreateDate"] = None

                                print(fxqygz_now_info)
                                fetch_risk_info.log(fxqygz_now_info)
                                risk_fxqygz_now_txt.log(self.format_string(fxqygz_now_info))

            time.sleep(1)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_risk_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self._status = -1

    def fetch_risk_fxqygz_ls(self):
        """风险企业关注类预警提示上月"""
        url = "http://60.1.100.2/crristdetail/doReadWarningListJSON.do"
        fetch_risk_info.log('now crawling 上月风险企业关注类预警提示')
        fxqygz_ls_info = OrderedDict()

        idxSupCodeList = ["A02",  # 企业股东变更
                          "A03",  # 减资变更
                          "B01",  # 业务下滑风险
                          "C02",  # 工商经营异常名录
                          "C04",  # 其他部门欠费
                          "D01",  # 法定代表人变更
                          "E01",  # 对外担保
                          "E06",  # 银行信贷逾期欠息
                          "E07",  # 质押抵押
                          ]
        try:
            for idxSupCode in idxSupCodeList:
                data = {
                    "_t": time.time() * 1000,
                    "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                    "entName": "",
                    "fixparam_risttype": "3",
                    "idxSupCode": idxSupCode,
                    "pageNo1": "",
                    "pageSize": "100",
                    "theEndTime": "",
                    "theStartTime": "",
                    "timeRange": "2",
                }
                resp = self.session.post(url, data=data)
                content = resp.json().get("paginationHtml")
                reg = re.compile("span class=\"hx-table-paging-totPage\">(\d+)</span>")
                totol_page = re.findall(reg, content)[0]

                if totol_page:
                    for i in range(1, int(totol_page) + 1):
                        data = {
                            "_t": time.time() * 1000,
                            "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                            "entName": "",
                            "fixparam_risttype": "3",
                            "idxSupCode": idxSupCode,
                            "pageNo1": i,
                            "pageSize": "100",
                            "theEndTime": "",
                            "theStartTime": "",
                            "timeRange": "2",
                        }
                        resp = self.session.post(url, data=data)
                        infos = resp.json().get("dataList")
                        if infos:
                            for info in infos:
                                fxqygz_ls_info["smy_dt"] = self.localtime
                                fxqygz_ls_info["content"] = info.get("content")  # 风险内容
                                fxqygz_ls_info["entName"] = info.get("entName")  # 风险企业
                                fxqygz_ls_info["name"] = info.get("name")  # 风险类型
                                if info.get("dtCreateDate"):  # 更新日期
                                    fxqygz_ls_info["dtCreateDate"] = datetime.datetime.strftime(
                                        parse(info.get("dtCreateDate")), '%Y-%m-%d')
                                else:
                                    fxqygz_ls_info["dtCreateDate"] = None

                                print(fxqygz_ls_info)
                                fetch_risk_info.log(fxqygz_ls_info)
                                risk_fxqygz_ls_txt.log(self.format_string(fxqygz_ls_info))

            time.sleep(1)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_risk_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self._status = -1

    def fetch_risk_fxqyts_now(self):
        """风险企业提示类预警提示本月"""
        url = "http://60.1.100.2/crristdetail/doReadWarningListJSON.do"
        fetch_risk_info.log('now crawling 本月风险企业提示类预警提示')
        fxqyts_now_info = OrderedDict()

        idxSupCodeList = ["A02",  # 企业股东变更
                          "B02",  # 证照过期
                          "C02",  # 工商经营异常名录
                          "C04",  # 其他部门行政处罚
                          "D01",  # 法定代表人变更
                          "E01",  # 对外担保
                          "E07",  # 质押抵押
                          ]
        try:
            for idxSupCode in idxSupCodeList:
                data = {
                    "_t": time.time() * 1000,
                    "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                    "entName": "",
                    "fixparam_risttype": "1",
                    "idxSupCode": idxSupCode,
                    "pageNo1": "",
                    "pageSize": "100",
                    "theEndTime": "",
                    "theStartTime": "",
                    "timeRange": "1",
                }
                resp = self.session.post(url, data=data)
                content = resp.json().get("paginationHtml")
                reg = re.compile("span class=\"hx-table-paging-totPage\">(\d+)</span>")
                totol_page = re.findall(reg, content)[0]

                if totol_page:
                    for i in range(1, int(totol_page) + 1):
                        data = {
                            "_t": time.time() * 1000,
                            "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                            "entName": "",
                            "fixparam_risttype": "1",
                            "idxSupCode": idxSupCode,
                            "pageNo1": i,
                            "pageSize": "100",
                            "theEndTime": "",
                            "theStartTime": "",
                            "timeRange": "1",
                        }
                        resp = self.session.post(url, data=data)
                        infos = resp.json().get("dataList")
                        if infos:
                            for info in infos:
                                fxqyts_now_info["smy_dt"] = self.localtime
                                fxqyts_now_info["content"] = info.get("content")  # 风险内容
                                fxqyts_now_info["entName"] = info.get("entName")  # 风险企业
                                fxqyts_now_info["name"] = info.get("name")  # 风险类型
                                if info.get("dtCreateDate"):  # 更新日期
                                    fxqyts_now_info["dtCreateDate"] = datetime.datetime.strftime(
                                        parse(info.get("dtCreateDate")), '%Y-%m-%d')
                                else:
                                    fxqyts_now_info["dtCreateDate"] = None

                                print(fxqyts_now_info)
                                fetch_risk_info.log(fxqyts_now_info)
                                risk_fxqyts_now_txt.log(self.format_string(fxqyts_now_info))

            time.sleep(1)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_risk_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self._status = -1

    def fetch_risk_fxqyts_ls(self):
        """风险企业提示类预警提示上月"""
        url = "http://60.1.100.2/crristdetail/doReadWarningListJSON.do"
        fetch_risk_info.log('now crawling 上月风险企业提示类预警提示')
        fxqyts_ls_info = OrderedDict()

        idxSupCodeList = ["A02",  # 企业股东变更
                          "A03",  # 减资变更
                          "B02",  # 证照过期
                          "C02",  # 工商经营异常名录
                          "C04",  # 其他部门行政处罚
                          "D01",  # 法定代表人变更
                          "E01",  # 对外担保
                          "E07",  # 质押抵押
                          ]
        try:
            for idxSupCode in idxSupCodeList:
                data = {
                    "_t": time.time() * 1000,
                    "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                    "entName": "",
                    "fixparam_risttype": "1",
                    "idxSupCode": idxSupCode,
                    "pageNo1": "",
                    "pageSize": "100",
                    "theEndTime": "",
                    "theStartTime": "",
                    "timeRange": "2",
                }
                resp = self.session.post(url, data=data)
                content = resp.json().get("paginationHtml")
                reg = re.compile("span class=\"hx-table-paging-totPage\">(\d+)</span>")
                totol_page = re.findall(reg, content)[0]

                if totol_page:
                    for i in range(1, int(totol_page) + 1):
                        data = {
                            "_t": time.time() * 1000,
                            "ajaxUrl": "/jsp/server/biz/warning/attWarningList.jsp",
                            "entName": "",
                            "fixparam_risttype": "1",
                            "idxSupCode": idxSupCode,
                            "pageNo1": i,
                            "pageSize": "100",
                            "theEndTime": "",
                            "theStartTime": "",
                            "timeRange": "2",
                        }
                        resp = self.session.post(url, data=data)
                        infos = resp.json().get("dataList")
                        if infos:
                            for info in infos:
                                fxqyts_ls_info["smy_dt"] = self.localtime
                                fxqyts_ls_info["content"] = info.get("content")  # 风险内容
                                fxqyts_ls_info["entName"] = info.get("entName")  # 风险企业
                                fxqyts_ls_info["name"] = info.get("name")  # 风险类型
                                if info.get("dtCreateDate"):  # 更新日期
                                    fxqyts_ls_info["dtCreateDate"] = datetime.datetime.strftime(
                                        parse(info.get("dtCreateDate")), '%Y-%m-%d')
                                else:
                                    fxqyts_ls_info["dtCreateDate"] = None

                                print(fxqyts_ls_info)
                                fetch_risk_info.log(fxqyts_ls_info)
                                risk_fxqyts_ls_txt.log(self.format_string(fxqyts_ls_info))

            time.sleep(1)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            fetch_risk_info.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self._status = -1

# 日志文件
fetch_risk_info = Logger("fetch_risk_info", config.risk_info_path)

# 存储文件
risk_fxqyjs_now_txt = Logger("risk_fxqyjs_now_txt", config.risk_fxqyjs_now_path)
risk_fxqyjs_ls_txt = Logger("risk_fxqyjs_ls_txt", config.risk_fxqyjs_ls_path)
risk_fxqygz_now_txt = Logger("risk_fxqygz_now_txt", config.risk_fxqygz_now_path)
risk_fxqygz_ls_txt = Logger("risk_fxqygz_ls_txt", config.risk_fxqygz_ls_path)
risk_fxqyts_now_txt = Logger("risk_fxqyts_now_txt", config.risk_fxqyts_now_path)
risk_fxqyts_ls_txt = Logger("risk_fxqyts_ls_txt", config.risk_fxqyts_ls_path)

if __name__ == "__main__":
    fetch_info = FetchInfo()
    fetch_info.fetch_all()