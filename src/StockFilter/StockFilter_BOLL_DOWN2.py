'''
Created on Apr 15, 2019

@author: mac
'''
from StockFilter.StockFilterBase import IStockFilter
from Stock import StockItemDefine

class CStockFilterBOLL_DOWN2(IStockFilter):

    def __init__(self, params):
        IStockFilter.__init__(self, params)
        self.filterName = u'BOLL下轨分析2'
        self.FilterDescribe = u'收盘价在下轨之下'
        
    
    def filterBy(self, stockInfo):
        info = stockInfo.getStockInfo()
        try:
            price = float(info[StockItemDefine.stock_ClosePrice])
            BOLL_DOWN = float(info[StockItemDefine.stock_BOLLDown])
            if price < BOLL_DOWN:
                return True
            else:
                return False
        except:
            return False
    