"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/5 19:46
E-mail  : 506615839@qq.com
File    : test_recharge.py
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

base_url = conf.get('env', 'url')
header = eval(conf.get('env', 'header'))


@ddt
class TestRecharge(unittest.TestCase):
    datapath = os.path.join(DataDir, 'cases.xlsx')
    excel = ReadExcel(datapath, 'recharge')
    recharge_data = excel.read_excel()
    rest = HanderRequest()


    @classmethod
    def setUpClass(cls):
        # 创建数据库对象
        cls.db = HandDB()
        # 登录，获取用户的id以及鉴权需要用到的token
        login_url = base_url + '/member/login'
        login_data = {"mobile_phone": conf.get('login_data','phone'), "pwd": conf.get('login_data','pwd')}
        expected = {'code': 0, 'msg': 'OK'}
        header = eval(conf.get('env','header'))
        response = requests.post(url=login_url, json=login_data, headers=header)
        res = response.json()
        # 获取用户id
        member_id = jsonpath.jsonpath(res, '$..id')[0]
        setattr(TestData,"member_id",str(member_id))
        # 获取token类型
        token_type = jsonpath.jsonpath(res, '$..token_type')[0]
        # 获取token值
        token = jsonpath.jsonpath(res, '$..token')[0]
        token_data = token_type + ' ' + token
        setattr(TestData, 'token_data', token_data)

    @data(*recharge_data)
    def test_recharge(self, case):
        case['data']=replace_data(case['data'])
        data = eval(case['data'])
        expected = eval(case['expected'])
        row = case['case_id']+1
        url = case['url']
        recharge_url = base_url + url
        method = case['method']
        header = eval(conf.get('env', 'header'))
        header['Authorization'] = getattr(TestData,'token_data')


        # 请求之前数据库看一下当前用户有多少钱
        # 请求后数据库看一下当前用户有多少钱
        # 然后比对增加的钱和用例中的钱
        if case['check_sql']:
            sql = case['check_sql'].format(conf.get('login_data','phone'))
            before_amount = self.db.get_one(sql)[0]

        response = self.rest.send(url=recharge_url, method=method, json=data, headers=header)
        res = response.json()
        leave_amount = jsonpath.jsonpath(res, '$..leave_amount')
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if case['check_sql']:
                sql = case['check_sql'].format(conf.get('login_data', 'phone'))
                after_amount = self.db.get_one(sql)[0]
                expected_amount = eval(case['data'])['amount']
                self.assertEqual(decimal.Decimal(str(expected_amount)), (after_amount - before_amount))
                my_logger.info('充值之前金额为:{}\n,充值金额为:{}\n,充值后金额为:{}'.format(before_amount,expected_amount,after_amount))
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
        # 关闭数据的连接和游标对象
        cls.db.close()
