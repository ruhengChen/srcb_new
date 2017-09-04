# coding: utf-8

import logging
import os

import config
import fetch_company
import fetch_companyInfo
import fetch_riskInfo


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


if __name__ == "__main__":
    # 日志文件
    run_main_log = Logger("run_main_log", config.run_main_log_path)

    # 获取企业名单
    company_status = fetch_company.search_code()
    run_main_log.log("fetch_company finish!")
    if company_status != 0:
        with open(config.error_path, 'a') as f:
            f.write("Warning ! fetch_company exists error message!!!")

    f = open(config.fetch_company_OK, 'w')
    f.close()

    # 获取企业信息
    fetch_companyInfo = fetch_companyInfo.FetchInfo()
    company_info_status = fetch_companyInfo.fetch_all()
    run_main_log.log("fetch_companyInfo finish!")
    if company_info_status != 0:
        with open(config.error_path, 'a') as f:
            f.write("Warning ! fetch_companyInfo exists error message!!!")

    f = open(config.fetch_companyInfo_OK, 'w')
    f.close()

    # 获取风险信息
    fetch_riskInfo = fetch_riskInfo.FetchInfo()
    risk_info_status = fetch_riskInfo.fetch_all()
    run_main_log.log("fetch_riskInfo finish!")
    if risk_info_status != 0:
        with open(config.error_path, 'a') as f:
            f.write("Warning ! fetch_riskInfo exists error message!!!")

    f = open(config.fetch_riskInfo_OK, 'w')
    f.close()


