# coding:utf8
import os
import xlrd
from xlutils.copy import copy


class Reader:
    """
        用来读取Excel文件内容
    """
    def __init__(self):
        # 整个excel工作簿缓存
        self.workbook = None
        # 当前工作sheet
        self.sheet = None
        # 逐行读取时的行数
        self.rows = 0
        # 当前sheet的行数
        self.r = 0

    # 打开excel
    def open_excel(self, srcfile):
        if not os.path.isfile(srcfile):
            print("error：%s not exist!" % (srcfile))
            return

        # 设置读取excel使用utf8编码
        xlrd.Book.encoding = "utf8"
        # 读取excel内容到缓存workbook
        self.workbook = xlrd.open_workbook(filename=srcfile)
        # 选取第一个sheet页面
        self.sheet = self.workbook.sheet_by_index(0)
        # 设置rows为当前sheet的行数
        self.rows = self.sheet.nrows
        # 设置默认读取为第一行
        self.r = 0
        return

    # 切换sheet页面
    def get_sheets(self):
        # 获取所有sheet的名字，并返回
        sheets = self.workbook.sheet_names()
        print(sheets)
        return sheets

    # 切换sheet页面
    def set_sheet(self, name):
        # 通过sheet名字，切换sheet页面
        self.sheet = self.workbook.sheet_by_name(name)
        self.rows = self.sheet.nrows
        self.r = 0
        return

    # 逐行读取
    def readline(self):
        row1 = None

        # 如果当前还没到最后一行，则读取一行
        if self.r < self.rows:
            row = self.sheet.row_values(self.r)
            self.r = self.r + 1
            i = 0
            row1 = row
            # 如果读取的是小数，则判断是不是整数
            for strs in row:
                if type(strs) == float:
                    if strs == int(strs):
                        # 如果是10.0这样的，则取整；如果要输入10.0，请使用在excel里面输入'10.0
                        row1[i] = str(int(strs))
                    else:
                        # 其他数据，转为字符串
                        row1[i] = str(strs)
                else:
                    row1[i] = strs

                i = i + 1
        return row1


class Writer:
    """
        用来复制写入Excel文件
    """
    def __init__(self):
        # 读取需要复制的excel
        self.workbook = None
        # 拷贝的工作空间
        self.wb = None
        # 当前工作的sheet页
        self.sheet = None
        # 记录生成的文件，用来保存
        self.df = None
        # 记录写入的行
        self.row = 0
        # 记录写入的列
        self.clo = 0

    # 复制并打开excel
    def copy_open(self, srcfile, dstfile):
        # 判断要复制的文件是否存在
        if not os.path.isfile(srcfile):
            print(srcfile + " not exist!")
            return

        # 判断要新建的文档是否存在，存在则提示
        if os.path.isfile(dstfile):
            print("warning：" + dstfile + " file already exist!")

        # 记录要保存的文件
        self.df = dstfile
        # 读取excel到缓存
        self.workbook = xlrd.open_workbook(filename=srcfile, formatting_info=True)
        # 拷贝
        self.wb = copy(self.workbook)
        # 默认使用第一个sheet
        # sheet = wb.get_sheet('Sheet1')
        return

    # 切换sheet页面
    def get_sheets(self):
        # 获取所有sheet的名字，并返回
        sheets = self.workbook.sheet_names()
        print(sheets)
        return sheets

    # 切换sheet页面
    def set_sheet(self, name):
        # 通过sheet名字，切换sheet页面
        self.sheet = self.wb.get_sheet(name)
        return

    # 写入指定单元格，保留原格式
    def write(self, r, c, value):
        # 获取要写入的单元格
        def _getCell(sheet, r, c):
            """ HACK: Extract the internal xlwt cell representation. """
            # 获取行
            row = sheet._Worksheet__rows.get(r)
            if not row:
                return None

            # 获取单元格
            cell = row._Row__cells.get(c)
            return cell

        # 获取要写入的单元格
        cell = _getCell(self.sheet, r, c)
        # 写入值
        self.sheet.write(r, c, value)
        if cell:
            # 获取要写入的单元格
            ncell = _getCell(self.sheet, r, c)
            if ncell:
                # 设置写入后格式和写入前一样
                ncell.xf_idx = cell.xf_idx

        return

    # 保存
    def save_close(self):
        # 保存复制后的文件
        self.wb.save(self.df)
        return


# 调试
if __name__ == '__main__':
    reader = Reader()
    reader.open_excel('../lib/cases/HTTP接口用例.xls')
    sheetname = reader.get_sheets()
    for i in range(reader.rows):
        print(reader.readline())

    writer = Writer()
    writer.copy_open('../lib/cases/HTTP接口用例.xls', '../lib/results/results-HTTP接口用例.xls')
    sheetname = writer.get_sheets()
    writer.set_sheet(sheetname[0])
    writer.write(4, 1, 'William')
    writer.set_sheet(sheetname[1])
    writer.write(1, 1, 'William')
    writer.save_close()
