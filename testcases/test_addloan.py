"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/8 19:30
E-mail  : 506615839@qq.com
File    : test_addloan.py
============================
"""
import os
import unittest
import jsonpath
import pymysql
from common.hande_db import HandDB
from library.ddt import ddt, data
from common.read_excel import ReadExcel
from common.contans import DataDir
from common.hander_request import HanderRequest
from common.read_conf import conf
from common.my_logger import my_logger
from common.hander_data import replace_data,TestData

datapath = os.path.join(DataDir, 'cases.xlsx')


@ddt
class TestAddLoan(unittest.TestCase):
    excel = ReadExcel(datapath, 'add_loan')
    addloan_data = excel.read_excel()
    http = HanderRequest()


    @classmethod
    def setUpClass(cls):
        cls.db = HandDB()
        # admin_phone=conf.get('login_data','admin_phone')
        # setattr(TestData,'admin_phone',admin_phone)
        # admin_pwd=conf.get('login_data','admin_pwd')
        # setattr(TestData, 'admin_pwd', admin_pwd)
        pass

    @data(*addloan_data)
    def test_addloan(self, case):
        # 准备用例数据
        # 拼接完整的接口地址
        url = conf.get('env', 'url') + case['url']
        case['data']=replace_data(case['data'])
        data = eval(case['data'])
        expected = eval(case['expected'])
        row = case['case_id']+1
        header = eval(conf.get('env', 'header'))
        if case['interface'] != '登录':
            header['Authorization'] = getattr(TestData,'token_data')
        method = case['method']

        if case['check_sql']:
            sql = case['check_sql'].format(getattr(TestData, 'member_id'))
            before_count = self.db.get_count(sql)
        # 发送请求
        response = self.http.send(url=url, method=method, json=data, headers=header)
        res = response.json()

        if case['interface']=='登录':
            # 获取用户id
            member_id=jsonpath.jsonpath(res,'$..id')[0]
            setattr(TestData,'member_id',str(member_id))
            # 获取token类型
            token_type=jsonpath.jsonpath(res,'$..token_type')[0]
            # 获取token值
            token=jsonpath.jsonpath(res,'$..token')[0]
            token_data=token_type+' '+token
            setattr(TestData,'token_data',token_data)

        # 断言
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if case['check_sql']:
                sql = case['check_sql'].format(getattr(TestData,'member_id'))
                after_count = self.db.get_count(sql)
                self.assertEqual(1,after_count-before_count)

        except AssertionError as e:
            self.excel.write_excel(row=row, column=8, value='未通过')
            my_logger.info("用例：{}--->执行未通过".format(case["title"]))
            my_logger.error(e)
            print("预取结果：{}".format(expected))
            print("实际结果：{}".format(res))
            raise e
        else:
            self.excel.write_excel(row=row, column=8, value='已通过')
            my_logger.info("用例：{}--->执行已通过".format(case["title"]))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()