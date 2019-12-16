"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/5 21:50
E-mail  : 506615839@qq.com
File    : test_withdraw.py
============================
"""
import os
import unittest
import requests
import jsonpath
from common.read_conf import conf
from common.read_excel import ReadExcel
from common.contans import DataDir
from common.hander_request import HanderRequest
from library.ddt import ddt, data
from common.my_logger import my_logger
from common.hande_db import HandDB
import decimal
from common.hander_data import TestData,replace_data


@ddt
class TestWithDraw(unittest.TestCase):
    datapath = os.path.join(DataDir, 'cases.xlsx')
    excel = ReadExcel(datapath, 'withdraw')
    withdraw_data = excel.read_excel()
    rest = HanderRequest()
    db = HandDB()

    @classmethod
    def setUpClass(cls):
        phone = conf.get('login_data', 'phone')
        setattr(TestData,'phone',phone)
        pwd = conf.get('login_data', 'pwd')
        setattr(TestData, 'pwd', pwd)

    @data(*withdraw_data)
    def test_withdraw(self, case):
        # 准备用例数据
        # 拼接url
        url = conf.get('env', 'url') + case['url']
        method = case['method']
        case['data']=replace_data(case['data'])
        data = eval(case['data'])
        expected = eval(case['expected'])
        row = case['case_id'] + 1
        header = eval(conf.get('env', 'header'))
        if case['interface'] != '登录':
            header['Authorization'] = TestData.token_data

        # 判断是否需要校验
        if case['check_sql']:
            sql = case['check_sql'].format(getattr(TestData,'phone'))
            # 获取充值前的余额
            before_amount = self.db.get_one(sql)[0]

        response = self.rest.send(url=url, method=method, json=data, headers=header)
        res = response.json()

        if case['interface'] == '登录':
            # 获取member_id
            member_id = jsonpath.jsonpath(res, '$..id')[0]
            setattr(TestData,'member_id',str(member_id))
            # 获取token类型
            token_type = jsonpath.jsonpath(res, '$..token_type')[0]
            # 获取token值
            token = jsonpath.jsonpath(res, '$..token')[0]
            token_data = token_type + ' ' + token
            setattr(TestData, 'token_data', token_data)

        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if case['check_sql']:
                sql = case['check_sql'].format(getattr(TestData,'phone'))
                after_amount = self.db.get_one(sql)[0]
                expected_amount = decimal.Decimal(str(data['amount']))
                my_logger.info('提现前余额:{}\n,提现余额:{}\n,提现后余额:{}'.format(before_amount, expected_amount, after_amount))
                self.assertEqual(expected_amount, (before_amount - after_amount))

        except AssertionError as e:
            self.excel.write_excel(row=row, column=8, value='未通过')
            my_logger.info('用例-->{}:执行未通过'.format(case['title']))
            my_logger.error(e)
            print("预期结果：{}".format(expected))
            print("实际结果：{}".format(res))
            raise e
        else:
            self.excel.write_excel(row=row, column=8, value='已通过')
            my_logger.info('用例-->{}:执行已通过'.format(case['title']))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
