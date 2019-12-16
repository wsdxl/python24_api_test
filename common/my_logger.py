"""
============================
Author  : XiaoLei.Du
Time    : 2019/11/23 17:53
E-mail  : 506615839@qq.com
File    : log_func.py
============================
"""
import os
import logging
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler
from common.contans import LogDir
from common.read_conf import conf
level=conf.get('logging','level')
f_level=conf.get('logging','f_level')
s_level=conf.get('logging','s_level')
filename=conf.get('logging','filename')


class MyLogger(object):
    @staticmethod
    def create_logger():
        # 一、自定义一个名为python24的日志收集器
        test_log = logging.getLogger(filename)
        # 二、定义日志收集器等级
        test_log.setLevel(level)
        # 三、添加输出渠道
        # 1、创建一个输出到控制台的输出渠道
        sh = logging.StreamHandler()
        # 2、设置输出等级(输出到控制台)
        sh.setLevel(s_level)
        # 3、将输出渠道绑定到日志收集器上
        test_log.addHandler(sh)
        # 四、输出到文件
        log_path=os.path.join(LogDir,'log.log')
        # fh = logging.FileHandler(log_path, 'a', 'utf8')
        # 按文件大小进行轮转
        fh=RotatingFileHandler(filename=log_path,maxBytes=1024*1024,backupCount=3,encoding='utf8')
        fh.setLevel(f_level)
        test_log.addHandler(fh)
        test_log.addHandler(sh)

        # 五、设置日志输出的格式
        # 创建一个日志输出格式
        formatter = logging.Formatter("'%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'")
        # 将输出格式和输出渠道绑定
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)
        return test_log


my_logger=MyLogger.create_logger()