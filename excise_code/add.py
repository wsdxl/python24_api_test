"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/12 22:10
E-mail  : 506615839@qq.com
File    : add.py
============================
"""
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

datapath = os.path.join(DataDir, 'cases.xlsx')


@ddt
class TestAddLoan(unittest.TestCase):
    excel = ReadExcel(datapath, 'add_loan')
    addloan_data = excel.read_excel()
    http = HanderRequest()


    @classmethod
    def setUpClass(cls):
        cls.db = HandDB()
        cls.admin_phone=conf.get('login_data','admin_phone')
        cls.admin_pwd=conf.get('login_data','admin_pwd')

    @data(*addloan_data)
    def test_addloan(self, case):
        # 准备用例数据
        # 拼接完整的接口地址
        url = conf.get('env', 'url') + case['url']
        if '#member_id#' in case['data']:
            case['data'] = case['data'].replace('#member_id#', str(self.member_id))
        if '#admin_phone#' in case['data']:
            case['data'] = case['data'].replace('#admin_phone#', str(self.admin_phone))
        if '#admin_pwd#' in case['data']:
            case['data'] = case['data'].replace('#admin_pwd#', str(self.admin_pwd))
        data = eval(case['data'])
        expected = eval(case['expected'])
        row = case['case_id']+1
        header = eval(conf.get('env', 'header'))
        if case['interface'] != '登录':
            header['Authorization'] = self.token_data
        method = case['method']
        # 发送请求
        response = self.http.send(url=url, method=method, json=data, headers=header)
        res = response.json()

        if case['interface']=='登录':
            # 获取用户id
            TestAddLoan.member_id=jsonpath.jsonpath(res,'$..id')[0]
            # 获取token类型
            token_type=jsonpath.jsonpath(res,'$..token_type')[0]
            # 获取token值
            token=jsonpath.jsonpath(res,'$..token')[0]
            TestAddLoan.token_data=token_type+' '+token

        # 断言
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if res['msg'] == 'ok':
                sql = 'select * from futureloan.loan WHERE member_id={}'.format(self.member_id)
                count = self.db.get_count(sql)
                self.assertEqual(count, 1)
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