# coding:utf-8
import copy
import pyodbc
import random
from collections import OrderedDict

import config


class Proxy():
    params = OrderedDict(
        [('id',{"type":"integer"}),
         ('port',{"type":"VARCHAR"})
         ])

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table test({})".format(','.join(['%s %s' % (key, value["type"])
                                                       for key, value in self.params.items()]))
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self,values):
        pass

    def random_select(self, count=None, conditions=None):
        sql = "select count(1) from PROXYS"
        self.cursor.execute(sql)
        rows = self.cursor.fetchone()[0]
        if rows == 0:
            print("代理数为空...")
        sql = "select * from PROXYS WHERE id = {}".format(round(random.random()*rows))
        self.cursor.execute(sql)
        rows = self.cursor.fetchone()
        return rows


class Company():
    params = OrderedDict([
        ('regno', {"type": "VARCHAR(20)", 'comment':"注册号"}),
        ('name', {"type": "VARCHAR(100)", 'comment':"公司名称"}),
        ('corpid', {"type": "VARCHAR(200)", 'comment': "长的注册号"}),
        ('nocorpid', {"type": "VARCHAR(20)", 'comment':""}),
        ('entUnscId', {"type": "VARCHAR(20)", 'comment':"组织机构号"})
    ])

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table company({})".format(','.join(['%s %s' % (key, value["type"])
                                                       for key, value in self.params.items()]))
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self, values):
        # print(values)
        for key, value in values.items():
            if not value:
                values.pop(key)

        sql = "insert into company({}) values(\'{}\')".format(','.join(values.keys()), '\',\''.join(values.values()))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()

    def select(self, count=None, conditions=None):
        '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
        if conditions:
            sql = "select count(1) from company where {}".format('and '.join(["%s=\'%s\'" %(key,value) for key, value in conditions.items()]))
            print(sql)
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            # print(rows)

            yield rows

        else:
            sql = "select * from company order by regno"
            print(sql)
            self.cursor.execute(sql)
            while 1:
                rows = self.cursor.fetchone()

                if not rows:
                    break

                yield rows

    def update(self,conditions,values):
        sql = "update company set {} where {}"\
            .format(','.join(["%s=\'%s\'" %(key,value) for key, value in values.items()]), 'and '.join(["%s=\'%s\'" %(key,value) for key, value in conditions.items()]))
        sql = sql.replace('\'None\'', 'null')
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()
        return True

    def export(self):
        sql = "select REGNO,NAME,CORPID,NOCORPID,case when ENTUNSCID is null then '' else ENTUNSCID end from company"
        print(sql)
        self.cursor.execute(sql)

        rows = self.cursor.fetchall()

        with open(config.company_path, 'w') as f:
            for i in rows:
                for j in range(0, len(i)):
                    i[j] = "\"" + i[j] + "\""

                f.write(",".join(i)+"\n")



class CompanyInfo():
    params = OrderedDict(
        [('regno', {"type": "VARCHAR(20)", 'comment': "注册号"}),
         ('name', {"type": "VARCHAR(100)", 'comment': "公司名称"}),
         ('leprep', {"type": "VARCHAR(20)", 'comment': "法人代表"}),
         ('regorg', {"type": "VARCHAR(50)", 'comment': "登记机关"}),
         ('regloc', {"type": "VARCHAR(50)", 'comment': "注册地址"}),
         ('type', {"type": "VARCHAR(200)", 'comment': "类型"}),
         ('estdate', {"type": "DATE", 'comment': "成立日期"}),
         ('mgrbegin', {"type": "DATE", 'comment': "营业期限自"}),
         ('mgrend', {"type": "DATE", 'comment': "营业期限至"}),
         ('mgrscrope', {"type": "VARCHAR(1000)", 'comment': "经营范围"}),
         ])
    logic_primary_key = ["regno"]

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table company_info({})".format(','.join(['%s %s' % (key, value["type"])
                                                          for key, value in self.params.items()]))
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self, values, update=True):
        values = {key: str(values[key]) for key in values if values[key]}
        tmp = copy.deepcopy(values)
        if update:
            conditions = {x: tmp.pop(x) for x in self.logic_primary_key}
            sql = "select count(1) from company_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            if rows: ## 已存在记录
                self.update(conditions, tmp)
                return

        sql = "insert into company_info({}) values(\'{}\')".format(','.join(values.keys()), '\',\''.join(values.values()))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()

    def select(self, count=None, conditions=None):
        '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
        if conditions:
            sql = "select count(1) from company_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            return rows
        else:
            sql = "select * from company_info order by regno"
            self.cursor.execute(sql)
            while 1:
                rows = self.cursor.fetchone()

                if not rows:
                    break

                yield rows

    def update(self, conditions, values):
        sql = "update company_info set {} where {}" \
            .format(','.join(["%s=\'%s\'" % (key, value) for key, value in values.items()]),
                    'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()
        return True


class ZbxxInfo():
    params = OrderedDict(
        [('regno', {"type": "VARCHAR(20)", 'comment': "注册号"}),
         ('coninforegno', {"type": "VARCHAR(50)", 'comment': "标识号"}),
         ('coninfoname', {"type": "VARCHAR(20)", 'comment': "股东名称"}),
         ('payconamount', {"type": "VARCHAR(10)", 'comment': "认缴金额（万元）"}),
         ('paydate', {"type": "DATE", 'comment': "认缴日期"}),
         ('invform', {"type": "VARCHAR(50)", 'comment': "认缴方式"}),
         ('actconamount', {"type": "VARCHAR(10)", 'comment': "实缴金额（万元）"}),
         ('actdate', {"type": "DATE", 'comment': "实缴日期"}),
         ('actform', {"type": "VARCHAR(10)", 'comment': "实缴方式"}),
         ('percent', {"type": "VARCHAR(20)", 'comment': "股权比例"}),
         ])
    logic_primary_key = ["regno", "coninforegno"]

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table zbxx_info({})".format(','.join(['%s %s' % (key, value["type"])
                                                          for key, value in self.params.items()]))
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self, values, update=True):
        values = {key: str(values[key]) for key in values if values[key]}
        tmp = copy.deepcopy(values)
        if update:
            conditions = {x: tmp.pop(x) for x in self.logic_primary_key}
            sql = "select count(1) from zbxx_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            if rows: ## 已存在记录
                self.update(conditions, tmp)
                return

        sql = "insert into zbxx_info({}) values(\'{}\')".format(','.join(values.keys()), '\',\''.join(values.values()))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()

    def select(self, count=None, conditions=None):
        '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
        if conditions:
            sql = "select count(1) from zbxx_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            return rows
        else:
            sql = "select * from zbxx_info order by regno"
            self.cursor.execute(sql)
            while 1:
                rows = self.cursor.fetchone()

                if not rows:
                    break

                yield rows

    def update(self, conditions, values):
        sql = "update zbxx_info set {} where {}" \
            .format(','.join(["%s=\'%s\'" % (key, value) for key, value in values.items()]),
                    'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()
        return True


class GgxxInfo():
    params = OrderedDict(
        [('regno', {"type": "VARCHAR(20)", 'comment': "注册号"}),
         ('sfzjhm', {"type": "VARCHAR(100)", 'comment': "标识号"}),
         ('zwmc', {"type": "VARCHAR(20)", 'comment': "职务"}),
         ('xm', {"type": "VARCHAR(10)", 'comment': "姓名"}),
         ])
    logic_primary_key = ["regno", "sfzjhm"]

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table ggxx_info({})".format(','.join(['%s %s' % (key, value["type"])
                                                          for key, value in self.params.items()]))
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self, values, update=True):
        values = {key: str(values[key]) for key in values if values[key]}
        tmp = copy.deepcopy(values)
        if update:
            conditions = {x: tmp.pop(x) for x in self.logic_primary_key}
            sql = "select count(1) from ggxx_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            if rows: ## 已存在记录
                self.update(conditions, tmp)
                return

        sql = "insert into ggxx_info({}) values(\'{}\')".format(','.join(values.keys()), '\',\''.join(values.values()))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()

    def select(self, count=None, conditions=None):
        '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
        if conditions:
            sql = "select count(1) from ggxx_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            return rows
        else:
            sql = "select * from ggxx_info order by regno"
            self.cursor.execute(sql)
            while 1:
                rows = self.cursor.fetchone()

                if not rows:
                    break

                yield rows

    def update(self, conditions, values):
        sql = "update ggxx_info set {} where {}" \
            .format(','.join(["%s=\'%s\'" % (key, value) for key, value in values.items()]),
                    'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()
        return True


class XkxxInfo():
    params = OrderedDict(
        [('regno', {"type": "VARCHAR(20)", 'comment': "注册号"}),
         ('licDocNo', {"type": "VARCHAR(20)", 'comment': "许可文件编号"}),
         ('licDocName', {"type": "VARCHAR(100)", 'comment': "许可文件名称"}),
         ('licValidFrom', {"type": "DATE", 'comment': "许可文件有效期自"}),
         ('licValidTo', {"type": "DATE", 'comment': "许可文件有效期至"}),
         ('importFrom', {"type": "VARCHAR(10)", 'comment': "许可机关"}),
         ('licContent', {"type": "VARCHAR(100)", 'comment': "许可内容"}),
         ('state', {"type": "VARCHAR(5)", 'comment': "是否到期"}),
         ])

    logic_primary_key = ["regno", "licDocNo"]

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table xkxx_info({})".format(','.join(['%s %s' % (key, value["type"])
                                                          for key, value in self.params.items()]))
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self, values, update=True):
        values = {key: str(values[key]) for key in values if values[key]}
        tmp = copy.deepcopy(values)
        if update:
            conditions = {x: tmp.pop(x) for x in self.logic_primary_key}
            sql = "select count(1) from xkxx_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            if rows: ## 已存在记录
                self.update(conditions, tmp)
                return

        sql = "insert into xkxx_info({}) values(\'{}\')".format(','.join(values.keys()), '\',\''.join(values.values()))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()

    def select(self, count=None, conditions=None):
        '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
        if conditions:
            sql = "select count(1) from xkxx_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            return rows
        else:
            sql = "select * from xkxx_info order by regno"
            self.cursor.execute(sql)
            while 1:
                rows = self.cursor.fetchone()

                if not rows:
                    break

                yield rows

    def update(self, conditions, values):
        sql = "update xkxx_info set {} where {}" \
            .format(','.join(["%s=\'%s\'" % (key, value) for key, value in values.items()]),
                    'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()
        return True


class XzcfInfo():
    params = OrderedDict(
        [('regno', {"type": "VARCHAR(20)", 'comment': "注册号"}),
         ('id', {"type": "VARCHAR(50)", 'comment': "标识号"}),
         ('punDocno', {"type": "VARCHAR(50)", 'comment': "行政处罚文书号"}),
         ('punOrgName', {"type": "VARCHAR(50)", 'comment': "执法部门"}),
         ('punishedName', {"type": "VARCHAR(50)", 'comment': "公司名"}),
         ('punRegionName', {"type": "VARCHAR(50)", 'comment': "地区名"}),
         ('punDate', {"type": "DATE", 'comment': "作出行政处罚决定日期"}),
         ('punState', {"type": "VARCHAR(10)", 'comment': "状态"}),
         ('punishedLegRep', {"type": "VARCHAR(10)", 'comment': "处罚法人代表"}),
         ('punAbstract', {"type": "VARCHAR(5000)", 'comment': "处罚概要"}),
         ('punCaseName', {"type": "VARCHAR(100)", 'comment': "案件名称"}),
         ('punItemName', {"type": "VARCHAR(500)", 'comment': "处罚类型"}),
         ])

    logic_primary_key = ["regno", "id"]

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table xzcf_info({})".format(','.join(['%s %s' % (key, value["type"])
                                                          for key, value in self.params.items()]))
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self, values, update=True):
        values = {key: str(values[key]) for key in values if values[key]}
        tmp = copy.deepcopy(values)
        if update:
            conditions = {x: tmp.pop(x) for x in self.logic_primary_key}
            print(conditions)
            sql = "select count(1) from xzcf_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            if rows: ## 已存在记录
                self.update(conditions, tmp)
                return

        sql = "insert into xzcf_info({}) values(\'{}\')".format(','.join(values.keys()), '\',\''.join(values.values()))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()

    def select(self, count=None, conditions=None):
        '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
        if conditions:
            sql = "select count(1) from xzcf_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            return rows
        else:
            sql = "select * from xzcf_info order by regno"
            self.cursor.execute(sql)
            while 1:
                rows = self.cursor.fetchone()

                if not rows:
                    break

                yield rows

    def update(self, conditions, values):
        sql = "update xzcf_info set {} where {}" \
            .format(','.join(["%s=\'%s\'" % (key, value) for key, value in values.items()]),
                    'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()
        return True


class YqqfInfo():
    params = OrderedDict(
        [('regno', {"type": "VARCHAR(20)", 'comment': "注册号"}),
         ('arrearType', {"type": "VARCHAR(10)", 'comment': "逾期类型"}),
         ('importFrom', {"type": "VARCHAR(50)", 'comment': "所属机构"}),
         ('arrearperiod', {"type": "VARCHAR(50)", 'comment': "欠费所属期"}),
         ('arrearbalance', {"type": "VARCHAR(50)", 'comment': "欠费金额（元)"}),
         ])

    logic_primary_key = ["regno", "arrearperiod"]

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table yqqf_info({})".format(','.join(['%s %s' % (key, value["type"])
                                                          for key, value in self.params.items()]))
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self, values, update=True):
        values = {key: str(values[key]) for key in values if values[key]}
        tmp = copy.deepcopy(values)
        if update:
            conditions = {x:tmp.pop(x) for x in self.logic_primary_key}
            sql = "select count(1) from yqqf_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            if rows: ## 已存在记录
                self.update(conditions, tmp)
                return

        sql = "insert into yqqf_info({}) values(\'{}\')".format(','.join(values.keys()), '\',\''.join(values.values()))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()

    def select(self, count=None, conditions=None):
        '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
        if conditions:
            sql = "select count(1) from yqqf_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            return rows
        else:
            sql = "select * from yqqf_info order by regno"
            self.cursor.execute(sql)
            while 1:
                rows = self.cursor.fetchone()

                if not rows:
                    break

                yield rows

    def update(self, conditions, values):
        sql = "update yqqf_info set {} where {}" \
            .format(','.join(["%s=\'%s\'" % (key, value) for key, value in values.items()]),
                    'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()
        return True


class BdcdyInfo():
    params = OrderedDict(
        [('smy_dt', {"type": "DATE", 'comment': "汇总日期"}),
         ('regno', {"type": "VARCHAR(20)", 'comment': "注册号"}),
         ('mortgageCertNo', {"type": "VARCHAR(100)", 'comment': "抵押证编号"}),
         ('mortgageGuarExtent', {"type": "VARCHAR(1000)", 'comment': "抵押担保范围"}),
         ('mortgageeName', {"type": "VARCHAR(100)", 'comment': "抵押权人名称"}),
         ('guaranteedCreditAmount', {"type": "VARCHAR(50)", 'comment': "被担保主债权数额（万元）"}),
         ('debtPayFrom', {"type": "DATE", 'comment': "债务期限起"}),
         ('debtPayTo', {"type": "DATE", 'comment': "债务期限至"}),
         ('mortgageReason', {"type": "VARCHAR(1000)", 'comment': "申请抵押原因"}),
         ])

    # logic_primary_key = ["regno", "mortgageCertNo", 'mortgageeName','debtPayFrom','debtPayTo']

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table bdcdy_info({})".format(','.join(['%s %s' % (key, value["type"])
                                                          for key, value in self.params.items()]))
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self, values, update=True):
        values = {key: str(values[key]) for key in values if values[key]}
        tmp = copy.deepcopy(values)

        if update:
            conditions = {x:tmp.pop(x) for x in self.logic_primary_key}
            sql = "select count(1) from bdcdy_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            if rows: ## 已存在记录
                self.update(conditions, tmp)
                return

        sql = "insert into bdcdy_info({}) values(\'{}\')".format(','.join(values.keys()), '\',\''.join(values.values()))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()

    def select(self, count=None, conditions=None):
        '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
        if conditions:
            sql = "select count(1) from bdcdy_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            return rows
        else:
            sql = "select * from bdcdy_info order by regno"
            self.cursor.execute(sql)
            while 1:
                rows = self.cursor.fetchone()

                if not rows:
                    break

                yield rows

    def update(self, conditions, values):
        sql = "update bdcdy_info set {} where {}" \
            .format(','.join(["%s=\'%s\'" % (key, value) for key, value in values.items()]),
                    'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()
        return True


class DcdyInfo():
    params = OrderedDict(
        [('regno', {"type": "VARCHAR(20)", 'comment': "注册号"}),
         ('orderNo', {"type": "VARCHAR(50)", 'comment': "抵押证编号"}),
         ('department', {"type": "VARCHAR(50)", 'comment': "抵押登记机关"}),
         ('guaranteesRange', {"type": "VARCHAR(100)", 'comment': "抵押担保范围"}),
         ('mortgageeName', {"type": "VARCHAR(100)", 'comment': "抵押权人名称"}),
         ('mortgageeCertNo', {"type": "VARCHAR(50)", 'comment': "抵押权人证件号"}),
         ('mortgageAmount', {"type": "VARCHAR(50)", 'comment': "被担保主债权数额（万元）"}),
         ('startdate', {"type": "DATE", 'comment': "债务期限起"}),
         ('enddate', {"type": "DATE", 'comment': "债务期限至"}),
         ])

    logic_primary_key = ["regno", "orderNo"]

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table dcdy_info({})".format(','.join(['%s %s' % (key, value["type"])
                                                          for key, value in self.params.items()]))
        print(sql)
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self, values, update=True):
        values = {key: str(values[key]) for key in values if values[key]}
        tmp = copy.deepcopy(values)

        if update:
            conditions = {x:tmp.pop(x) for x in self.logic_primary_key}
            sql = "select count(1) from dcdy_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            if rows: ## 已存在记录
                self.update(conditions, tmp)
                return

        sql = "insert into dcdy_info({}) values(\'{}\')".format(','.join(values.keys()), '\',\''.join(values.values()))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()

    def select(self, count=None, conditions=None):
        '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
        if conditions:
            sql = "select count(1) from dcdy_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            return rows
        else:
            sql = "select * from dcdy_info order by regno"
            self.cursor.execute(sql)
            while 1:
                rows = self.cursor.fetchone()

                if not rows:
                    break

                yield rows

    def update(self, conditions, values):
        sql = "update dcdy_info set {} where {}" \
            .format(','.join(["%s=\'%s\'" % (key, value) for key, value in values.items()]),
                    'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()
        return True


class CfxxInfo():
    params = OrderedDict(
        [('regno', {"type": "VARCHAR(20)", 'comment': "注册号"}),
         ('sequestrateNo', {"type": "VARCHAR(100)", 'comment': "查封文号"}),
         ('sequestrateLoc', {"type": "VARCHAR(100)", 'comment': "查封房屋坐落"}),
         ('sequestrateApplyName', {"type": "VARCHAR(100)", 'comment': "申请查封单位"}),
         ('tsaSeizeStartDate', {"type": "DATE", 'comment': "查封起始日期"}),
         ('tsaSeizeEndDate', {"type": "DATE", 'comment': "查封截止日期"}),
         ('cancelDate', {"type": "VARCHAR(50)", 'comment': "撤销查封日期"}),
         ('state', {"type": "VARCHAR(20)", 'comment': "状态"}),
         ])

    logic_primary_key = ["regno", "sequestrateNo"]

    def __init__(self):
        conn = pyodbc.connect(DSN="db2local")
        self.cursor = conn.cursor()

    def init_db(self):
        sql = "create table cfxx_info({})".format(','.join(['%s %s' % (key, value["type"])
                                                          for key, value in self.params.items()]))
        print(sql)
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception:
            print("表已存在")

    def insert(self, values, update=True):
        values = {key: str(values[key]) for key in values if values[key]}
        tmp = copy.deepcopy(values)

        if update:
            conditions = {x:tmp.pop(x) for x in self.logic_primary_key}
            sql = "select count(1) from cfxx_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            if rows: ## 已存在记录
                self.update(conditions, tmp)
                return

        sql = "insert into cfxx_info({}) values(\'{}\')".format(','.join(values.keys()), '\',\''.join(values.values()))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()

    def select(self, count=None, conditions=None):
        '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
        if conditions:
            sql = "select count(1) from cfxx_info where {}".format(
                'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()[0]
            return rows
        else:
            sql = "select * from cfxx_info order by regno"
            self.cursor.execute(sql)
            while 1:
                rows = self.cursor.fetchone()

                if not rows:
                    break

                yield rows

    def update(self, conditions, values):
        sql = "update cfxx_info set {} where {}" \
            .format(','.join(["%s=\'%s\'" % (key, value) for key, value in values.items()]),
                    'and '.join(["%s=\'%s\'" % (key, value) for key, value in conditions.items()]))
        print(sql)
        self.cursor.execute(sql)
        self.cursor.commit()
        return True


if __name__ == "__main__":
    # test = Test()
    # proxy = Proxy()
    # proxy.random_select()
    company = Company()
    row = company.select(conditions={'corpid': '1'})
    for i in row:
        print(i)

    # dcdy = DcdyInfo()

    # company.init_db()
    # com = {'regno': '330682000003872','corpid': '2F0E13AE97FEB178B1FD68253092AA36B08685D23A98ADDAD07DF06B5581D85C',
    #        'name': '万锦商贸有限公司', 'NOCORPID':  '330682000003872'}
    # company.insert(com)
    # company.select(conditions={"NOCORPID": "330682000003872", "regno": "330682000003872",})
    # company.update(conditions={"regno": "330682000003872", "NAME":'万锦商贸有限公司'},values={'NOCORPID': '311',"CORPID":"422"})
    # test.init_db()
    # for i in range(3):
        # print(company.select())
    # for i in company.select():
    #     print(i)
    #     print(i.NOCORPID)
    # Test = {"ip":"192", "port":"80"}
    # test.insert(Test)