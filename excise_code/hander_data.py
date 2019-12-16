"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/12 11:32
E-mail  : 506615839@qq.com
File    : hander_data.py
============================
"""
import re
from common.read_conf import conf


# data = '{"mobile_phone": "#phone#", "pwd": "#pwd#"}'
# re1 = r'#(.+?)#'
# res=re.search(re1,data)
# # print(res.group())
# # print(res.group(1))
# if '#phone#' in data:
#     data=data.replace('#phone#',conf.get('login_data','phone'))
#     print(data)
# res=re.search(re1,data)
# # if '#pwd#' in data:
#     data=data.replace('#pwd#',conf.get('login_data','pwd'))
#     print(data)


# -----------------正则-----------------------

# data = '{"mobile_phone": "#phone#", "pwd": "#pwd#"}'
# re1 = r'#(.+?)#'
# res=re.search(re1,data)
# if '#phone#' in data:
#     data=data.replace(res.group(),conf.get('login_data',res.group(1)))
#     print(data)
# res3=re.search(re1,data)
# if '#pwd#' in data:
#     res2=data.replace(res3.group(),conf.get('login_data',res3.group(1)))
#     print(res2)

# data = '{"mobile_phone": "#phone#", "pwd": "#pwd#"}'
# r = r'#(.+?)#'
# res = re.search(r, data)
# if res:
#     res2 = data.replace(res.group(), conf.get('login_data', res.group(1)))
#     print(res2)


class TestData:
    member_id = ""
    pass


def replace_data(data):
    r = r'#(.+?)#'
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
            data = data.replace(item, conf.get('login_data', key))
        except:
            data = data.replace(item, getattr(TestData, key))

    # 返回替换好的数据
    return data


# data='{"mobile_phone":"#phone#","pwd":"#pwd#"}'
# data1=replace_data(data)
# print(data1)
data = '{"member_id":#member_id#,"amount":500}'
data2 = replace_data(data)
print(data2)
