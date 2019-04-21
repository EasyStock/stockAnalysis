'''
Created on Apr 20, 2019

@author: mac
'''
from StockMgr.StockMgr import CStockMgr
import os

class CAnalysisOneDay(object):
    def __init__(self):
        pass
    
    
    def AnalysisOneNewDay(self,fileName, filters, exceptBanKuai = ()):
        mgr = CStockMgr()
        mgr.stockPreprocess(fileName)
        for flt in filters:
            mgr.AnalysisOneFileWithFilter(fileName, flt, exceptBanKuai)
        
    
    def AnalysisOneOldDay(self, csvFile, filter_):
        mgr = CStockMgr()
        mgr.ReadFromCSVAndFilter(csvFile, filter_)
        
    
    def CovertToCSVOnly(self, fileName):
        mgr = CStockMgr()
        mgr.stockPreprocess(fileName)
        
    
    
    def AnalysisOneFolder(self, csvFolder, filters,exceptBanKuai = ()):
        mgr = CStockMgr()
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
    