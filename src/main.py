'''
Created on Apr 17, 2019

@author: mac
'''
from StockMgr.StockMgrBanKuai import CStockMgrBanKuai
from StockFilter.StockFilter_ZhangFu import CStockFilterZhangFu
from StockFilter.StockFilter_MA5 import CStockFilterMA5
from StockFilter.StockFilter_BOLLUP import CStockFilterBOLLUP
from Analysis.AnalysisOneDay import CAnalysisOneDay
from StockFilter.StockFilter_BOLL_DOWN1 import CStockFilterBOLL_DOWN1
from StockFilter.StockFilter_BOLL_DOWN2 import CStockFilterBOLL_DOWN2


def GetFilters():
    zhangDiefu3 = CStockFilterZhangFu(3)
    zhangDiefu7 = CStockFilterZhangFu(7)
    MA5Filter = CStockFilterMA5(None)
    BOLLUpFilter = CStockFilterBOLLUP(None)
    BOLLDown1 = CStockFilterBOLL_DOWN1(None)
    BOLLDown2 = CStockFilterBOLL_DOWN2(None)
    #filters = [zhangDiefu3,zhangDiefu7,MA5Filter,BOLLUpFilter,BOLLDown1,BOLLDown2]
    filters = [BOLLDown1,BOLLDown2]
    return filters

def AnalysisOneDay(fileName):
    mgr = CStockMgrBanKuai()
    
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
    mgr = CStockMgrBanKuai()
    mgr.stockPreprocess(fileName)
    

def Test():
    fileName = u'/Volumes/Data/StockAssistant/stockAnalysis/data/RawData/2019-04-19.xls'
    csvFile = u'/Volumes/Data/StockAssistant/stockAnalysis/data/OutData/2019-04-19.csv'
    csvFolder = u'/Volumes/Data/StockAssistant/stockAnalysis/data/OutData'
    analy = CAnalysisOneDay()
    #analy.CovertToCSVOnly(fileName)
    filters = GetFilters()
    #analy.AnalysisOneOldDay(csvFile, filters)
    analy.AnalysisOneFolder(csvFolder, filters, ('石墨烯',))
    #analy.AnalysisOneNewDay(fileName, filters, ('石墨烯',))

def AnalysisNewOneDay():
    fileName = u'/Volumes/Data/StockAssistant/stockAnalysis/data/RawData/2019-04-22.xls'
    analy = CAnalysisOneDay()
    filters = GetFilters()
    exceptBanKuais = []
    analy.AnalysisOneNewDay(fileName, filters, exceptBanKuais)
    
def PrintKeyIn():
    csvFile = u'/Volumes/Data/StockAssistant/stockAnalysis/data/OutData/2019-04-19.csv'
    mgr = CStockMgrBanKuai()
    mgr.readFromCSV(csvFile)
    while(1):
        keyword = input('输入板块')
        mgr.printStockWithKey(keyword)
        
def PrintOneKeyIn():
    csvFile = u'/Volumes/Data/StockAssistant/stockAnalysis/data/OutData/2019-04-19.csv'
    mgr = CStockMgrBanKuai()
    mgr.readFromCSV(csvFile)
    keys = []
    mgr.printStockWithKey(keys)
    
def PrintAllKeyIn():
    csvFile = u'/Volumes/Data/StockAssistant/stockAnalysis/data/OutData/2019-04-19.csv'
    mgr = CStockMgrBanKuai()
    mgr.readFromCSV(csvFile)
    keys = ()
    mgr.printStockWithKey(keys)
    

def AnalysisOneFolder():
    csvFolder = u'/Volumes/Data/StockAssistant/stockAnalysis/data/OutData'
    analy = CAnalysisOneDay()
    filters = GetFilters()
    exceptBanKuais = []
    analy.AnalysisOneFolder(csvFolder, filters, exceptBanKuais)

if __name__ == '__main__':
    #Test()
    AnalysisOneFolder()


    