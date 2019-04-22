'''
Created on Apr 15, 2019

@author: mac
'''
from StockFilter.StockFilterBase import IStockFilter
from Stock import StockItemDefine

class CStockFilterBOLL_DOWN1(IStockFilter):

    def __init__(self, params):
        IStockFilter.__init__(self, params)
        self.filterName = u'BOLL下轨分析1'
        self.FilterDescribe = u'最低点摸过BOLL下轨，收盘价在下轨之上'
        
    
    def filterBy(self, stockInfo):
        info = stockInfo.getStockInfo()
        try:
            price = float(info[StockItemDefine.stock_ClosePrice])
            BOLLDOWN = float(info[StockItemDefine.stock_BOLLDown])
            lowest = float(info[StockItemDefine.stock_LowerPrice])
            if price > BOLLDOWN and lowest <= BOLLDOWN:
                return True
            else:
                return False
        except:
            return False
    