'''
Created on Apr 15, 2019

@author: mac
'''
from StockFilter.StockFilterBase import IStockFilter
from Stock import StockItemDefine

class CStockFilterZhangFu(IStockFilter):

    def __init__(self, params):
        IStockFilter.__init__(self, params)
        self.filterName = u'涨幅%0.1f'%(params)
        self.FilterDescribe = u'涨幅大于%f过滤器'%(params)
        self.threshold = float(params)
        
    
    def filterBy(self, stockInfo):
        info = stockInfo.getStockInfo()
        try:
            price = float(info[StockItemDefine.stock_ZhangDieFu])
            if price > float(self.threshold):
                #print(info)
                return True
            else:
                return False
        except:
            return False
    
        