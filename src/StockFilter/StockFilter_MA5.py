'''
Created on Apr 15, 2019

@author: mac
'''
from StockFilter.StockFilterBase import IStockFilter
from Stock import StockItemDefine

class CStockFilterMA5(IStockFilter):

    def __init__(self, params):
        IStockFilter.__init__(self, params)
        self.filterName = u'5日均线'
        self.FilterDescribe = u'股价大于5日均线过滤器'
        
    
    def filterBy(self, stockInfo):
        info = stockInfo.getStockInfo()
        try:
            ma5 = float(info[StockItemDefine.stock_MA5])
            price = float(info[StockItemDefine.stock_ClosePrice])
            if price > ma5:
                return True
            else:
                return False
        except:
            return False
    
        