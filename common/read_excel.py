"""
============================
Author  : XiaoLei.Du
Time    : 2019/11/21 8:26
E-mail  : 506615839@qq.com
Software: PyCharm
============================
"""
import os
from common.contans import DataDir
import openpyxl

class CaseData:
    pass

class ReadExcel(object):

    def __init__(self,filename,sheetname):
        self.filename=filename
        self.sheetname=sheetname

    def open(self):
        self.workbook = openpyxl.load_workbook(self.filename)
        self.sheet = self.workbook[self.sheetname]

    def save(self):
        self.workbook.save(self.filename)

    def close(self):
        self.workbook.close()

    def read_excel(self):
        self.open()
        row = list(self.sheet.rows)
        title = []
        for r in row[0]:
            title.append(r.value)
        # print(title)
        cases = []
        for i in row[1:]:
            case = []
            for v in i:
                case.append(v.value)
            # print(case)
            data = dict(zip(title, case))
            cases.append(data)
        self.close()
        return (cases)

    def read_excel_obj(self):
        self.open()
        row = list(self.sheet.rows)
        title = []
        for r in row[0]:
            title.append(r.value)
        # print(title)
        cases = []
        for i in row[1:]:
            case = []
            for v in i:
                case.append(v.value)
            # print(case)
            data = list(zip(title, case))
            casedata = CaseData()
            for m,n in data:
                setattr(casedata,m,n)
            cases.append(casedata)
        self.close()
        return (cases)

    def write_excel(self,row,column,value):
        self.open()
        self.sheet.cell(row=row,column=column,value=value)
        self.save()
        self.close()





if __name__ == '__main__':
    import jsonpath
    datapath=os.path.join(DataDir,'cases.xlsx')
    read=ReadExcel(datapath,'recharge')
    res=read.read_excel()
    print(eval(res[0]['data']))



