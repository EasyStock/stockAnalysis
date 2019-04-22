'''
Created on Apr 22, 2019

@author: mac
'''

import pandas as pd
from Stock import StockItemDefine
from Stock import StockItem


class CStockMgrBase(object):
    
    def __init__(self):
        self.stocks = None
    
    def __readfromHTM(self, fileName):
        dfs = pd.read_html(fileName,encoding='utf-8', header = 0)
        df =dfs[0]
        for index in range(len(df.columns)):
            print(index, df.columns[index])
        return df

    def __splictToItems(self, df):
        '''
        格式统一化,
        '''
        stocks = []
        for _, row in df.iterrows():
            stock = self.__formatToStockItem(row)
            stocks.append(stock)
        self.__stocks = stocks
        return stocks

    def __formatResultToDataFrame(self, stocks):
        stockList = [t.formatToDict() for t in stocks]
        columns = stocks[0].getColunmInfo()
        d = pd.DataFrame(stockList,columns=columns)
        return d

    def __formatToStockItem(self, row_item):
        '''
        格式统一化
        '''
        item_info = {}
        item_info[StockItemDefine.stock_ID] = row_item[0]
        item_info[StockItemDefine.stock_Name] = row_item[1]
        
        item_info[StockItemDefine.stock_OpenPrice] = row_item[2]
        item_info[StockItemDefine.stock_ClosePrice] = row_item[3]
        item_info[StockItemDefine.stock_HighPrice] = row_item[4]
        item_info[StockItemDefine.stock_LowerPrice] = row_item[5]
        item_info[StockItemDefine.stock_Volumn] = row_item[6]
        item_info[StockItemDefine.stock_ZhangDieFu] = row_item[7]
        
        item_info[StockItemDefine.stock_MA5] = row_item[8]
        item_info[StockItemDefine.stock_MA10] = row_item[9]
        item_info[StockItemDefine.stock_MA20] = row_item[10]
        item_info[StockItemDefine.stock_MA30] = row_item[11]
        item_info[StockItemDefine.stock_MA60] = row_item[12]
        
        item_info[StockItemDefine.stock_MACD] = row_item[13]
        
        item_info[StockItemDefine.stock_BOLLUp] = row_item[14]
        item_info[StockItemDefine.stock_BOLLMid] = row_item[15]
        item_info[StockItemDefine.stock_BOLLDown] = row_item[16]
        
        item_info[StockItemDefine.stock_K] = row_item[17]
        item_info[StockItemDefine.stock_D] = row_item[18]
        item_info[StockItemDefine.stock_J] = row_item[19]
        
        item_info[StockItemDefine.stock_ShiZhi] = row_item[20]
        item_info[StockItemDefine.stock_HangYe] = row_item[21]
        item_info[StockItemDefine.stock_GaiNian] = row_item[22]
        item_info[StockItemDefine.stock_Days] = row_item[23]
        item_info[StockItemDefine.stock_XinTai] = row_item[24]
        
        item = StockItem.CStockItem()
        item.initWithDict(item_info)
        return item
    
    def readFromCSV(self, fileName):
        df = pd.read_csv(fileName, index_col = None, encoding='utf_8_sig')
        stocks =  self.__splictToItems(df)
        self.stocks = stocks
        return stocks
    
    def saveToCSV(self,fileName, stocks):
        df = self.__formatResultToDataFrame(stocks)
        df.to_csv(fileName,encoding="utf_8_sig", index=False)

    def printStockWithKey(self, params):
        '''
        根据传入类型过滤数据
        '''
        if isinstance(params, tuple):
            for stock in self.__stocks:
                if stock.isAllKeysIn(params):
                    print(stock)
        elif isinstance(params, list):
            for stock in self.__stocks:
                if stock.isOneKeyIn(params):
                    print(stock)
        else:
            for stock in self.__stocks:
                if stock.isKeyIn(params):
                    print(stock)

    def stockPreprocess(self, fileName):
        '''
        预处理，将下载的数据存成CSV 格式
        '''
        fName = fileName[fileName.rfind('/')+1: fileName.rfind('.')]
        OutData = self.GetOutDataFolder(fileName)

        outFileName = '%s/%s.csv' %(OutData,fName)
        df = self.__readfromHTM(fileName)
        self.__splictToItems(df)
        self.saveToCSV(outFileName, self.stocks)

    def filterBy(self, stocks, filter_):
        res = []
        for stock in stocks:
            if filter_.filterBy(stock):
                res.append(stock)
        return res