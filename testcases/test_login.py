"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/2 19:42
E-mail  : 506615839@qq.com
File    : futureloan.py
============================
"""
import os
import unittest
from library.ddt import ddt,data
from common import read_excel
from common.contans import DataDir
from common.read_conf import conf
from common.my_logger import my_logger
from common.hander_request import HanderRequest
base_url=conf.get('env','url')
header =eval(conf.get('env','header'))
@ddt
class TestLogin(unittest.TestCase):
    datapath=os.path.join(DataDir,'cases.xlsx')
    excel=read_excel.ReadExcel(datapath,'login')
    login_data=excel.read_excel()
    rest=HanderRequest()

    @data(*login_data)
    def test_login(self,case):
        login_data=eval(case['data'])
        expected=eval(case['expected'])
        case_id=case['case_id']
        url=case['url']
        login_url=base_url+url
        method=case['method']
        response=self.rest.send(url=login_url,method=method,json=login_data,headers=header)
        res=response.json()
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            self.excel.write_excel(row=case_id+1,column=8,value='未通过')
            my_logger.info('用例-->{}:执行未通过'.format(case['title']))
            my_logger.error(e)
            print("预期结果：{}".format(expected))
            print("实际结果：{}".format(res))
            raise e
        else:
            self.excel.write_excel(row=case_id+1,column=8,value='已通过')
            my_logger.info('用例-->{}:执行已通过'.format(case['title']))


