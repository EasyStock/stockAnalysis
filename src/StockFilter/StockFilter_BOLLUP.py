'''
Created on Apr 15, 2019

@author: mac
'''
from StockFilter.StockFilterBase import IStockFilter
from Stock import StockItemDefine

class CStockFilterBOLLUP(IStockFilter):

    def __init__(self, params):
        IStockFilter.__init__(self, params)
        self.filterName = u'BOLL上轨'
        self.FilterDescribe = u'股价打印BOLL上轨过滤器'
        
    
    def filterBy(self, stockInfo):
        info = stockInfo.getStockInfo()
        try:
            price = float(info[StockItemDefine.stock_ClosePrice])
            BOOLUP = float(info[StockItemDefine.stock_BOLLUp])
            if price >= BOOLUP:
                return True
            else:
                return False
        except:
            return False
    
        