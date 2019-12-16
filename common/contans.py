"""
============================
Author  : XiaoLei.Du
Time    : 2019/11/27 22:12
E-mail  : 506615839@qq.com
File    : contans.py
============================
"""
import os
# dir=os.path.dirname(__file__)
# print(dir)
BASEDIR=os.path.dirname(os.path.dirname(__file__))
# log目录路径
LogDir=os.path.join(BASEDIR,'log')
# data目录路径
DataDir=os.path.join(BASEDIR,'data')
# 报告目录路径
ReportDir=os.path.join(BASEDIR,'reports')
# 用例目录lujing
CaseDir=os.path.join(BASEDIR,'testcases')
# 配置目录的路径
ConfDir=os.path.join(BASEDIR,'conf')
