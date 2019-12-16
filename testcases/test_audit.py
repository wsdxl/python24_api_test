"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/14 10:37
E-mail  : 506615839@qq.com
File    : test_audit.py
============================
"""
import os
import unittest
import jsonpath
from library.ddt import ddt, data
from common.read_excel import ReadExcel
from common.contans import DataDir
from common.read_conf import conf
from common.hander_request import HanderRequest
from common.hander_data import TestData, replace_data
from common.my_logger import my_logger
from common.hande_db import HandDB

case_path = os.path.join(DataDir, 'cases.xlsx')


@ddt
class TestAudit(unittest.TestCase):
    excel = ReadExcel(case_path, 'audit')
    case_data = excel.read_excel()
    http = HanderRequest()
    db=HandDB()

    @classmethod
    def setUpClass(cls):
        url = conf.get('env', 'url') + '/member/login'
        data = {
            "mobile_phone": conf.get('login_data', 'admin_phone'),
            "pwd": conf.get('login_data', 'admin_pwd')
        }
        headers = eval(conf.get('env', 'header'))

        response = cls.http.send(url=url, method='post', json=data, headers=headers)
        res = response.json()
        # 获取member_id
        admin_member_id = jsonpath.jsonpath(res, '$..id')[0]
        setattr(TestData, 'admin_member_id', str(admin_member_id))
        # 获取token类型
        token_type = jsonpath.jsonpath(res, '$..token_type')[0]
        # 获取token值
        token = jsonpath.jsonpath(res, '$..token')[0]
        token_data = token_type + ' ' + token
        setattr(TestData, 'token_data', token_data)

    def setUp(self):
        url = conf.get('env', 'url') + '/loan/add'
        data = {
            "member_id": getattr(TestData, 'admin_member_id'),
            "title": "借钱实现财富自由",
            "amount": 2000,
            "loan_rate": 12.0,
            "loan_term": 3,
            "loan_date_type": 1,
            "bidding_days": 5
        }
        headers = eval(conf.get('env', 'header'))
        headers['Authorization'] = getattr(TestData, 'token_data')
        response = self.http.send(url=url, method='post', json=data, headers=headers)
        res = response.json()
        # 获取项目id
        loan_id = jsonpath.jsonpath(res, '$..id')[0]
        setattr(TestData, 'loan_id', str(loan_id))

    @data(*case_data)
    def test_audit(self, case):
        pass
        # 准备用例数据
        url = conf.get('env', 'url') + case['url']
        method = case['method']
        case['data'] = replace_data(case['data'])
        data = eval(case['data'])
        expected = eval(case['expected'])
        headers = eval(conf.get('env', 'header'))
        headers['Authorization'] = getattr(TestData, 'token_data')
        row = case['case_id'] + 1
        # 发送请求
        response = self.http.send(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 断言
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if case['check_sql']:
                sql=replace_data(case['check_sql'])
                result_status=self.db.get_one(sql)[0]
                self.assertEqual(expected['status'],result_status)

        except AssertionError as e:
            self.excel.write_excel(row=row, column=8, value='未通过')
            my_logger.info('用例--->{}:执行未通过'.format(case['title']))
            my_logger.error(e)
            print("预期结果：{}".format(expected))
            print("实际结果：{}".format(res))
            raise e
        else:
            self.excel.write_excel(row=row, column=8, value='已通过')
            my_logger.info('用例--->{}:执行已通过'.format(case['title']))
