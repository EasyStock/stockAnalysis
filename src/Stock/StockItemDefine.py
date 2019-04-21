'''
Created on Apr 15, 2019

@author: mac
'''
from collections import OrderedDict

stock_ID = u'股票代码'
stock_Name = u'股票简称'
stock_OpenPrice = u'开盘价'
stock_ClosePrice = u'收盘价'
stock_HighPrice = u'最高价'
stock_LowerPrice = u'最低价'
stock_Volumn = u'成交量(股)'
stock_ZhangDieFu = u'涨跌幅(%)'

stock_MA5 = u'5日均线'
stock_MA10 = u'10日均线'
stock_MA20 = u'20日均线'
stock_MA30 = u'30日均线'
stock_MA60 = u'60日均线'

stock_BOLLUp = u'BOLL上轨'
stock_BOLLMid = u'BOLL中轨'
stock_BOLLDown = u'BOLL下轨'
stock_MACD = u'MACD'
stock_K = u'kdj(k值)'
stock_D = u'kdj(d值)'
stock_J = u'kdj(j值)'

stock_GaiNian = u'所属概念'    
stock_ShiZhi = u'a股流通市值'

stock_HangYe = u'所属行业'
stock_Days = u'上市天数'
stock_XinTai = u'技术形态'

    
class CStockItemTemplate(object):
    def __init__(self):
        self.stockInfo = OrderedDict()
        self.stockInfo[stock_ID] = None
        self.stockInfo[stock_Name] = None
        self.stockInfo[stock_OpenPrice] = None
        self.stockInfo[stock_ClosePrice] = None
        self.stockInfo[stock_HighPrice] = None
        self.stockInfo[stock_LowerPrice] = None
        self.stockInfo[stock_Volumn] = None
        self.stockInfo[stock_ZhangDieFu] = None

        self.stockInfo[stock_MA5] = None
        self.stockInfo[stock_MA10] = None
        self.stockInfo[stock_MA20] = None
        self.stockInfo[stock_MA30] = None
        self.stockInfo[stock_MA60] = None
        self.stockInfo[stock_MACD] = None
        
        self.stockInfo[stock_BOLLUp] = None
        self.stockInfo[stock_BOLLMid] = None
        self.stockInfo[stock_BOLLDown] = None

        self.stockInfo[stock_K] = None
        self.stockInfo[stock_D] = None
        self.stockInfo[stock_J] = None
        
        self.stockInfo[stock_ShiZhi] = None
        self.stockInfo[stock_HangYe] = None
        self.stockInfo[stock_GaiNian] = None
        self.stockInfo[stock_Days] = None
        
        self.stockInfo[stock_XinTai] = None
        
    
    def initWithDict(self,dict_):
        for key in dict_:
            self.stockInfo[key] = dict_[key]
    
    def __str__(self, *args, **kwargs):
        return self.stockInfo.__str__()

    def getColunmInfo(self):
        return self.stockInfo.keys()
    
    def formatToDict(self):
        return self.stockInfo
    
    def getStockInfo(self):
        return self.stockInfo
     
    def getBanKuai(self):
        return None
     
    def isKeyIn(self, key):
        return False
     
    def isAllKeysIn(self, keys):
        return False
    
    def isOneKeyIn(self, keys):
        return False
     
    def FilterBy(self, stockFilter):
        return False
    
    
if __name__ == '__main__':
    '''
    开盘价,收盘价,最高价,最低价,成交量,涨跌幅,5日均线, 10日均线,20日均线,30日均线,60日均线,macd, boll(upper)值,boll(mid)值,boll(lower)值,K,D,J,a股流通市值,行业，概念,上市天数,技术形态
    '''
    
    t = CStockItemTemplate()
    print(t)