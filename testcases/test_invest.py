"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/15 15:35
E-mail  : 506615839@qq.com
File    : test_invest.py
============================
"""
import os
import jsonpath
import unittest
from library.ddt import ddt, data
from common.read_excel import ReadExcel
from common.contans import DataDir
from common.hander_request import HanderRequest
from common.read_conf import conf
from common.hander_data import TestData, replace_data
from common.my_logger import my_logger

data_path = os.path.join(DataDir, 'cases.xlsx')


@ddt
class TestInvest(unittest.TestCase):
    excel = ReadExcel(data_path, 'invest')
    invest_datas = excel.read_excel()
    http = HanderRequest()

    @data(*invest_datas)
    def test_invest(self, case):
        # 1、准备用例数据
        url = conf.get('env', 'url') + case['url']
        method = case['method']
        case['data'] = replace_data(case['data'])
        data = eval(case['data'])
        headers = eval(conf.get('env', 'header'))
        if case['interface'] != 'login':
            headers['Authorization'] = getattr(TestData, 'token_data')
        expected = eval(case['expected'])
        row = case['case_id'] + 1

        # 2、发送请求
        response = self.http.send(url=url, method=method, json=data, headers=headers)
        res = response.json()

        if case['interface'] == 'login':
            # 提取member_id和token
            member_id = jsonpath.jsonpath(res, '$..id')[0]
            setattr(TestData,'member_id',str(member_id))

            token_type = jsonpath.jsonpath(res, '$..token_type')[0]
            token = jsonpath.jsonpath(res, '$..token')[0]
            token_data = token_type + ' ' + token
            setattr(TestData, 'token_data', token_data)

        elif case['interface'] == 'add':
            loan_id = jsonpath.jsonpath(res, '$..id')[0]
            setattr(TestData, 'loan_id', str(loan_id))

        # 3、断言
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            self.excel.write_excel(row=row, column=8, value='未通过')
            my_logger.info('用例：{}--->执行未通过'.format(case['title']))
            my_logger.error(e)
            print("预取结果：{}".format(expected))
            print("实际结果：{}".format(res))
            raise e
        else:
            self.excel.write_excel(row=row, column=8, value='已通过')
            my_logger.info('用例：{}--->执行已通过'.format(case['title']))
