"""
============================
Author  : XiaoLei.Du
Time    : 2019/12/10 10:18
E-mail  : 506615839@qq.com
File    : 20191210正则.py
============================
"""
import re

# 单字符表示规则

# . 表示除了\n之外的其他任何一个字符
re1 = r'.'
res1 = re.findall(re1, 'sddvdftdfdc')
# print(res1)

# []:表示举例一个字符
re2 = r'[abc]'
res2 = re.findall(re2, 'ffssfacvbdsfbbdfccdefrgyjuab')
# print(res2)

# \d:表示任何一个数字
re3 = r'\d'
res3 = re.findall(re3, 'ydgtygg124bvf876v455')
# print(res3)

# \D:表示任何一个非数字
re4 = r'\D'
res4 = re.findall(re4, 'ydgtygg124bvf876v455')
# print(res4)

# \s:表示一个空白键
re5 = r'\s'
res5 = re.findall(re5, 'sdfggf 3tgffg 7fno dg  dgh')
# print(res5)

# \S:表示非空白键
re6 = r'\S'
res6 = re.findall(re6, 'sdfggf 3tgffg 7fno dg  dgh')
# print(res6)

# \w：表示一个单词字符(数字、字母、下划线)
re7 = r'\w'
res7 = re.findall(re7, 'dg#%^dkgl345%76_$23df')
# print(res7)

# \W:表示一个非单词字符
re8 = r'\W'
res8 = re.findall(re8, 'dg#%^dkgl345%76_$23df')
# print(res8)

# 二、多个字符的匹配规则
re21 = r'abc'
res21 = re.findall(re21, 'abrtyy45667abcohkkcba234abc')
# print(res21)

# 同时定义多个规则
re22 = r'13641878150|13812345678|18621842068'
res22 = re.findall(re22, 'sdf13641878150gfg13812345678hjmnn1862184206812')
# print(res22)

# 匹配手机号码：11位
# {m}:表示匹配一个字符m次

re23 = r'1[3,4,5,6,7,9]\d{9}'
res23 = re.findall(re23, '321364188875412yuu1478652225555514788078544576')
# print(res23)
# {m,}:表示匹配一个字符不小于m次

re24 = r'\d{7,}'
res24 = re.findall(re24, '321364188875412yuu1478652225555514788078544576')
# print(res24)

# {m,n}表示匹配一个字符出现m次到n次
# 贪婪模式：如果给定一个范围，它会尽可能的去匹配更多的
re25=r'\d{3,5}'
res25=re.findall(re25,'aaaaa123456ghj333yyy77iii88jj909768876')
# print(res25)

# 关闭贪婪模式，表达式后加个问号（匹配尽可能少的）
re26=r'\d{3,5}?'
res26=re.findall(re26,'aaaaa123456ghj333yyy77iii88jj909768876')
# print(res26)

# * :表示一个字符出现0次以上（包括0次）
re27=r'\d*'
res27=re.findall(re27,'343aa1112df345g1h6699')
# print(res27)

# +:表示一个字符出现1次以上（包括1次）
re28=r'\d+'
res28=re.findall(re28,'343aa1112df345g1h6699')
# print(res28)

# ？：表示0次或者1次
re29=r'\d?'
res29=re.findall(re29,'343aa1112df345g1h6699')
# print(res29)

# 三、边界匹配

# ^:匹配字符串的开头
re31=r"^python"
res31 = re.findall(re31,"python999python")
# print(res31)

# $:匹配字符串的结尾
re32=r"python$"
res32 = re.findall(re32,"python999python")
# print(res32)

# \b:匹配单词的边界
# re33=r"\bpython"
# res33 = re.findall(re33,"python999python")
# print('res33:',res33)

# \B:匹配非单词的边界
# re33=r"\Bpython"
# res33 = re.findall(re33,"1python999 python")
# print(res33)

# ()：匹配分组:在匹配的数据中提取数据
# re34=r'aa(\d{3})bb'
# res34 = re.findall(re34,"gg21111h2222hj333klg444hj555klghjkaa123bbhhjhjjaa345bb")
# print(res34)

re35=r"aa(\d{2,})bb(\d{2,})cc"
res35 = re.findall(re35,"aa123bb345cc7890ghjkl78aa22bb33cc")
print(res35)
