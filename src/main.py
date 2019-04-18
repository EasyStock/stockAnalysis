'''
Created on Apr 17, 2019

@author: mac
'''
from StockMgr.StockMgr import CStockMgr
from StockFilter.StockFilter_ZhangFu import CStockFilterZhangFu
from StockFilter.StockFilter_MA5 import CStockFilterMA5
from StockFilter.StockFilter_BOLLUP import CStockFilterBOLLUP

def AnalysisOneDay(fileName):
    mgr = CStockMgr()
#     df = mgr.ReadfromHTM(fileName)
#     stocks = mgr.SplictToItems(df)
#     print(stocks[5])
#     fileName = u'/Volumes/Data/Downloads/aa.csv'
#     mgr.SaveToCSV(fileName, stocks)
    zhangDiefu3 = CStockFilterZhangFu(3)
    zhangDiefu7 = CStockFilterZhangFu(7)
    MA5Filter = CStockFilterMA5(None)
    BOLLUpFilter = CStockFilterBOLLUP(None)
    filters = [zhangDiefu3,zhangDiefu7,MA5Filter,BOLLUpFilter]
    for filter_ in filters:
        mgr.AnalysisOneFileWithFilter(fileName, filter_)
    
    y = input('是否要分析板块？Y or N')
    if y != 'Y':
        return
    times = 10
    while(times):
        keyword = input('输入板块')
        mgr.PrintStockWithKey(keyword)
        times = times -1
        
        
if __name__ == '__main__':
    fileName = u'/Volumes/Data/StockAnalysisData/TTTT/rawData/2019-04-18.xls'
    AnalysisOneDay(fileName)

    