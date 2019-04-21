'''
Created on Apr 15, 2019

@author: mac
'''

from Stock import StockItemDefine


class CStockItem(StockItemDefine.CStockItemTemplate):
    
    def __init__(self):
        StockItemDefine.CStockItemTemplate.__init__(self)
        self.banKuai = []
        self.__banKuaiExcept = ['沪股通','深股通','融资融券','转融券标的',u'证金持股']
        
    def initWithDict(self, dict_):
        StockItemDefine.CStockItemTemplate.initWithDict(self, dict_)
        gaiNian = self.stockInfo[StockItemDefine.stock_GaiNian]
        self.banKuai = []
        if gaiNian:
            words = gaiNian.split(';')
            for word in words:
                if word not in self.__banKuaiExcept:
                    self.banKuai.append(word)
    
    def isKeyIn(self, key):
        gaiNian = self.stockInfo[StockItemDefine.stock_GaiNian]
        if gaiNian.find(key) != -1:
            return True
        else:
            return False

    def isAllKeysIn(self, keys):
        '''
        only all keys in return True
        '''
        for key in keys:
            if not self.isKeyIn(key):
                return False
            
        return True
    
    def isOneKeyIn(self, keys):
        '''
        if one key in ,return true
        '''
        for key in keys:
            if self.isKeyIn(key):
                return True
        
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
        