"""
============================
Author  : XiaoLei.Du
Time    : 2019/11/27 22:10
E-mail  : 506615839@qq.com
File    : my_conf.py
============================
"""
import os
from configparser import ConfigParser
from common.contans import ConfDir
# class MyConf:
#     def __init__(self,filename,encoding='utf8'):
#         self.filename=filename
#         self.encoding=encoding
#         self.conf=ConfigParser()
#         self.conf.read(filename,encoding)
#
#     def get_str(self,section,option):
#         return self.conf.get(section,option)
#
#     def get_int(self,section,option):
#         return self.conf.getint(section,option)
#
#     def get_float(self,section,option):
#         return self.conf.getfloat(section,option)
#
#     def get_bool(self,section,option):
#         return self.conf.getboolean(section,option)
#
#     def write_data(self,section,option,value):
#         self.conf.set(section,option,value)
#         self.conf.write(open(self.filename,'w',encoding=self.encoding))

class ReadConf(ConfigParser):
    def __init__(self,finename,encoding='utf8'):
        super().__init__()
        self.finename=finename
        self.encoding=encoding
        self.read(finename,encoding)

    def writeconf(self,section,option,value):
         self.set(section,option,value)
         self.write(open(self.finename,'w',encoding=self.encoding))

# 获取配置文件的路径
conf_path=os.path.join(ConfDir,'conf.ini')
conf=ReadConf(conf_path)