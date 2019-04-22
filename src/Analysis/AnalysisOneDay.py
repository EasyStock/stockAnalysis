'''
Created on Apr 20, 2019

@author: mac
'''
from StockMgr.StockMgrBanKuai import CStockMgrBanKuai
import os

class CAnalysisOneDay(object):
    def __init__(self):
        pass
    
    
    def AnalysisOneNewDay(self,fileName, filters, exceptBanKuai = ()):
        mgr = CStockMgrBanKuai()
        mgr.stockPreprocess(fileName)
        for flt in filters:
            mgr.AnalysisOneFileWithFilter(fileName, flt, exceptBanKuai)
        
    
    def AnalysisOneOldDay(self, csvFile, filter_):
        mgr = CStockMgrBanKuai()
        mgr.ReadFromCSVAndFilter(csvFile, filter_)
        
    
    def CovertToCSVOnly(self, fileName):
        mgr = CStockMgrBanKuai()
        mgr.stockPreprocess(fileName)
        
    
    
    def AnalysisOneFolder(self, csvFolder, filters,exceptBanKuai = ()):
        mgr = CStockMgrBanKuai()
        filenames=os.listdir(csvFolder)
        for csvFile in filenames:
            if csvFile.find('.csv') == -1:
                continue
            fullPath = os.path.join(csvFolder, csvFile)
            for filter_ in filters:
                mgr.ReadFromCSVAndFilter(fullPath,filter_,exceptBanKuai)
                
    
if __name__ == '__main__':
    fileName = u'/Volumes/Data/StockAssistant/stockAnalysis/data/RawData/2019-04-20.xls'
    
    analy = CAnalysisOneDay()
    analy.CovertToCSVOnly(fileName)
    