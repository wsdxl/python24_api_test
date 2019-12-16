"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/12 20:41
E-mail  : 506615839@qq.com
File    : hander_data.py
============================
"""
import re
from common.read_conf import conf

class TestData:
    # member_id = ""
    pass


def replace_data(data):
    r = r"#(.+?)#"
    # 判断是否有需要替换的数据
    while re.search(r, data):
        # 匹配第一个要替换的数据
        res = re.search(r, data)
        # 提取待替换的内容
        item = res.group()
        # 获取替换内容的数据项
        key = res.group(1)
        try:
            # 根据替换内容中的数据项去配置文件中找到对应的内容，进行替换
            data = data.replace(item, conf.get("login_data", key))
        except:
            data = data.replace(item, getattr(TestData, key))

    # 返回替换好的数据
    return data