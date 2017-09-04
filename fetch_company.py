# coding:utf-8

import datetime
import logging
import os
import re
import sys
import time
import traceback

from db.PyodbcHelper import *
from util import login

PATTERN = re.compile('var\s+corpid\s+=\s+"(\d{16})";\s+')
local_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")


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


def get_session():
    session = login.Login_Session()
    if config.active_login:
        success_session = session.get_login_data()
        return success_session
    else:
        return session


def format_string(v_dict):
    """ 输入字典, 输出格式化的字符串"""

    for key, value in v_dict.items():
        if value is None:
            v_dict[key] = ""

        v_dict[key] = "\"" + str(v_dict[key]) + "\""

    return ",".join(str(x) for x in v_dict.values())


def search_code():
    print("crawing company ...")
    company = Company()
    company.init_db()
    company_dict = OrderedDict()
    mysession = get_session()
    url = "http://60.1.100.2/appsearch/doGetAutoCompleteJson.do"

    status = 0

    fetch_list = config.get_fetch_range()
    print(fetch_list)
    for fetch_range in fetch_list:
        for no in range(fetch_range[0], fetch_range[1]):
            data = {'searchParam':no}
            try:
                resp = mysession.post(url, headers=config.HEADER, data=data, timeout=config.TIMEOUT)
                print(resp.json()["list"])

            except Exception:
                mysession = get_session()
                resp = mysession.post(url, headers=config.HEADER, data=data, timeout=config.TIMEOUT)

            company_dict["corpid"] = resp.json()["list"][0]["corpid"]
            company_dict["name"] = resp.json()["list"][0]["name"]
            company_dict["regno"] = resp.json()["list"][0]["regno"]

            if len(company_dict["corpid"]) > 10:
                company_dict["nocorpid"] = fetch_nocorpid(company_dict["corpid"], mysession)
                company_dict["entUnscId"] = fetch_entUnscId(company_dict["nocorpid"], mysession)

                print(company_dict)

                new_company_dict = company_dict.copy()
                new_company_dict.update({"smy_dt":local_time})
                new_company_dict.move_to_end("smy_dt", last=False)
                # company_txt.log(format_string(new_company_dict))

                result = company.select(conditions={"corpid": company_dict.get("corpid")})

                for i in result:
                    result = i

                try:
                    fetch_company_log.log("%s : %s" % (no, str(company_dict)))
                    if result == 0:
                        company.insert(company_dict)
                        print("insert")
                    else:
                        print("update")
                        company.update({"corpid": company_dict.pop("corpid")}, company_dict)
                except Exception:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    fetch_company_log.log(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
                    status = -1
            time.sleep(1)

    if status != 0:
        print("程序执行有误,请检查")
    else:
        print("程序执行无误,导出company表")
        company.export()
    return status


def fetch_nocorpid(corpid, mysession):
    url = 'http://60.1.100.2/appsearch/doEnEntBaseInfo.do?corpid=%s' % corpid
    resp = mysession.get(url)
    nocorpid = PATTERN.findall(resp.text)
    if nocorpid:
        return nocorpid[0]


def  fetch_entUnscId(nocorpid, mysession):
    """获取组织机构代码"""
    url = "http://60.1.100.2/crreportconinfo/doReadCrReportConInfoListJSON.do"
    data = {
        "_t" : time.time()*1000,
        "ajaxUrl": "/jsp/server/entappcon/crreportconinfo.jsp",
        "corpid": nocorpid,
        "pageNo1": "",
        "pageSize": ""
    }
    resp = mysession.post(url, data=data)
    infos = resp.json()
    if infos:
        if infos.get("crEntBaseInfo"):
            return infos.get("crEntBaseInfo").get("entUnscId")
        else:
            return None
    return None


fetch_company_log = Logger("fetch_company_log", config.company_log_path)


if __name__ == "__main__":
    search_code()
