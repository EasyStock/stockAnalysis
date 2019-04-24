'''
Created on Apr 22, 2019

@author: mac
'''

from StockMgr.StockMgrBase import CStockMgrBase

class CStockMgr(CStockMgrBase):
    def __init__(self):
        CStockMgrBase.__init__(self)
    
    
    def AnalysisOneFile(self,csvFile, filter_, outFile):
        self.readFromCSV(csvFile)
        res = self.filterBy(self.stocks, filter_)
        self.saveToCSV(outFile, res)