'''
Created on Apr 17, 2019

@author: mac
'''
from StockMgr.StockMgr import CStockMgr
from StockFilter.StockFilter_ZhangFu import CStockFilterZhangFu
from StockFilter.StockFilter_MA5 import CStockFilterMA5
from StockFilter.StockFilter_BOLLUP import CStockFilterBOLLUP
from Analysis.AnalysisOneDay import CAnalysisOneDay


def GetFilters():
    zhangDiefu3 = CStockFilterZhangFu(3)
    zhangDiefu7 = CStockFilterZhangFu(7)
    MA5Filter = CStockFilterMA5(None)
    BOLLUpFilter = CStockFilterBOLLUP(None)
    filters = [zhangDiefu3,zhangDiefu7,MA5Filter,BOLLUpFilter]
    return filters

def AnalysisOneDay(fileName):
    mgr = CStockMgr()
    
    filters = GetFilters()
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
        
def ReadAndSaveToFile(fileName):
    mgr = CStockMgr()
    mgr.stockPreprocess(fileName)
    

def Test():
    fileName = u'/Volumes/Data/StockAssistant/stockAnalysis/data/RawData/2019-04-20.xls'
    csvFile = u'/Volumes/Data/StockAssistant/stockAnalysis/data/OutData/2019-04-19.csv'
    csvFolder = u'/Volumes/Data/StockAssistant/stockAnalysis/data/OutData'
    analy = CAnalysisOneDay()
    #analy.CovertToCSVOnly(fileName)
    filters = GetFilters()
    #analy.AnalysisOneOldDay(csvFile, zhangDiefu7)
    analy.AnalysisOneFolder(csvFolder, filters)
    #analy.AnalysisOneNewDay(fileName, (zhangDiefu7,))
    
    
if __name__ == '__main__':
    Test()

    