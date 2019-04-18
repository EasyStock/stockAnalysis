'''
Created on Apr 15, 2019

@author: mac
'''

from Stock import StockItemDefine


class CStockItem(StockItemDefine.CStockItemTemplate):
    
    def __init__(self):
        StockItemDefine.CStockItemTemplate.__init__(self)
        self.banKuai = []
        
    def initWithDict(self, dict_):
        StockItemDefine.CStockItemTemplate.initWithDict(self, dict_)
        gaiNian = self.stockInfo[StockItemDefine.stock_GaiNian]
        self.banKuai = []
        if gaiNian:
            words = gaiNian.split(';')
            if words and len(words) >0:
                self.banKuai = words
    
    def isKeyIn(self, key):
        gaiNian = self.stockInfo[StockItemDefine.stock_GaiNian]
        if gaiNian.find(key) != -1:
            return True
        else:
            return False

    def isKeysIn(self, keys):
        res = [False for key in keys if not self.isKeyIn(key)]
        if not res:
            return True
        else:
            return False
        
    def getBanKuai(self):
        return self.banKuai
    
    
    def FilterBy(self, stockFilter):
        if stockFilter:
            return stockFilter.FilterBy(self)
        else:
            return False

    
if __name__ == '__main__':
    t = CStockItem()
    print(t)
        