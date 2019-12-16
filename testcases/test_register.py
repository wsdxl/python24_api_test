"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/3 20:50
E-mail  : 506615839@qq.com
File    : test_register.py
============================
"""
import os
import random
import requests
import unittest
from library.ddt import ddt, data
from common import read_excel
from common.contans import DataDir
from common.read_conf import conf
from common.my_logger import my_logger
from common.hander_request import HanderRequest
from common.hande_db import HandDB
from common.hander_data import TestData,replace_data

base_url = conf.get('env', 'url')
header = eval(conf.get('env', 'header'))


@ddt
class TestRegister(unittest.TestCase):
    datapath = os.path.join(DataDir, 'cases.xlsx')
    excel = read_excel.ReadExcel(datapath, 'register')
    register_data = excel.read_excel()
    rest = HanderRequest()
    db = HandDB()


    @data(*register_data)
    def test_register(self, case):
        # 判断是否有手机号码需要替换
        if '#phone#' in case['data']:
            phone = self.random_phone()
            setattr(TestData,'phone',phone)
            case['data']=case['data'].replace('#phone#',phone)
        data = eval(case['data'])
        expected = eval(case['expected'])
        case_id = case['case_id']
        url = case['url']
        register_url = base_url + url
        method = case['method']
        response = self.rest.send(url=register_url, method=method, json=data, headers=header)
        res = response.json()
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if case['check_sql']:
                # 去数据库查询当前注册的账号是否存在
                sql=replace_data(case['check_sql'])
                my_logger.info('check_sql:{}'.format(sql))
                # 获取数据库中没有没有该用户的信息
                count = self.db.get_count(sql)
                # 数据库中返回的数据做断言，判断是否有一条数据
                self.assertEqual(count, 1)
        except AssertionError as e:
            self.excel.write_excel(row=case_id + 1, column=8, value='未通过')
            my_logger.info('用例-->{}:执行未通过'.format(case['title']))
            my_logger.error(e)
            print("预期结果：{}".format(expected))
            print("实际结果：{}".format(res))
            raise e
        else:
            self.excel.write_excel(row=case_id + 1, column=8, value='已通过')
            my_logger.info('用例-->{}:执行已通过'.format(case['title']))

    @classmethod
    def random_phone(cls):
        while True:
            phone = '186'
            for i in range(8):
                phone += str(random.randint(0, 9))
            # 去数据库查询号码是否注册过
            sql='select * from futureloan.member where mobile_phone ={}'.format(phone)
            count=cls.db.get_count(sql)
            if count ==0:
                return phone

    @classmethod
    def tearDownClass(cls):
        # 关闭数据的连接和游标对象
        cls.db.close()
