# coding:utf-8

import re
import sys
import time

import requests
from pyquery import PyQuery as pq
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import config
from util import zfyz
from validator.Validator import get_active_proxy


class Login_Session():
    def __init__(self):
        if config.active_proxy:
            self.proxy = get_active_proxy()
            self.session.proxies = self.proxy
        self.session = requests.Session()
        retries = Retry(total=3,
                        backoff_factor=3,
                        status_forcelist=[500, 502, 503, 504]
                        )

        adapter = requests.adapters.HTTPAdapter(max_retries=retries)

        self.session.mount('http://', adapter)

        self.session.headers = config.HEADER

    def get_img(self):
        """获取验证码图片"""
        url = "http://60.1.100.2/kaptcha/doReadKaptcha.do"
        login_img = self.session.get(url)

        with open("kaptcha.jpg", "wb") as f:
            f.write(login_img.content)

    def get_kaptacha(self):
        """破解验证码"""
        login_url = config.login_url

        while True:
            self.get_img()
            kaptacha = zfyz.get_kaptcha()
            reg = re.compile(r'\b\d{4}\b')

            if re.findall(reg, kaptacha):
                break

            time.sleep(1)

        # 登陆请求需要的信息
        post_data = {
            "sysUser.loginName": config.LOGIN_NAME,
            "sysUser.loginPass": config.LOGIN_PASS,
            "sysUser.kaptcha": kaptacha
        }

        post_rsp = self.session.post(login_url, data=post_data)
        return post_rsp

    def get_login_data(self):
        init_url = config.init_url

        while True:
            try:
                login_rsp = self.session.get(init_url, timeout=10)

                if login_rsp:
                    self.session.cookies = login_rsp.cookies
                    break
            except Exception:
                print("连网超时,正在重试,请检查网络连接")

        print("正在破解验证码...")
        post_rsp = self.get_kaptacha()

        while True:
            if post_rsp.status_code == 200:
                authority = pq(post_rsp.text)
                error = authority("#errmsg")
                if error:
                    print("验证码错误,重新登录")
                    time.sleep(2)
                    post_rsp = self.get_kaptacha()
                else:
                    print("login success")
                    return self.session

if __name__ == "__main__":
    login_session = Login_Session()
    success_session = login_session.get_login_data()
    sys.exit()

