'''
Created on Apr 16, 2019

@author: mac
'''
import pandas as pd
from Stock import StockItemDefine
from Stock import StockItem
import os
from builtins import staticmethod

class CStockMgr(object): 
    #######################static method########################
    #@staticmethod
    def GetOutDataFolder(self,fileName):
        path = fileName[:fileName.rfind('/')+1]
        outData = u'%s/../OutData' % (path)
        if not os.path.exists(outData):
            os.mkdir(outData)
        return outData
    
    #@staticmethod
    def GetAnalysisDataFolder(self,fileName):
        path = fileName[:fileName.rfind('/')+1]
        analysisData = u'%s/../AnalysisData' % (path)
        if not os.path.exists(analysisData):
            os.mkdir(analysisData)
        return analysisData
    
    #@staticmethod
    def GetAnalysisDataFolderWithFilterName(self,fileName,filterName):
        path = fileName[:fileName.rfind('/')+1]
        analysisData = u'%s/../AnalysisData/%s' % (path,filterName)
        if not os.path.exists(analysisData):
            os.makedirs(analysisData)
        return analysisData
    
    #@staticmethod
    def GetAnalysisBanKuaiFolderWithFilter(self,fileName,filterName):
        path = fileName[:fileName.rfind('/')+1]
        banKuaiFolder = u'%s/../AnalysisData/%s/板块分析/' % (path,filterName)
        if not os.path.exists(banKuaiFolder):
            os.makedirs(banKuaiFolder)
        return banKuaiFolder
    
    #######################private method ##########################
    def __init__(self):
        self.__stocks = None

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
    
    def __formatResultToDataFrame(self, stocks):
        stockList = [t.formatToDict() for t in stocks]
        columns = stocks[0].getColunmInfo()
        d = pd.DataFrame(stockList,columns=columns)
        return d
    
    def __analyzerBanKuaiStocks(self, stocks):
        allKeys = []
        ret = {}
        for stock in stocks:
            allKeys.extend(stock.getBanKuai())
    
        allKeys=list(set(allKeys))
        print('with %d stocks and %d keys' % (len(stocks), len(allKeys)))
        for key in allKeys:
            if key not in ret:
                ret[key] = []
            for stock in stocks:
                if stock.isKeyIn(key):
                    ret[key].append(stock)
        return ret

    def __get_BanKuai_Result(self, stocks, fName, outFolder):
        mapOfResult = self.__analyzerBanKuaiStocks(stocks)
        res = sorted(mapOfResult.items(), key=lambda d:len(d[1]), reverse = True)
        key2 = u'%s' %(fName)
        ret ={
            u'板块':[r[0] for r in res],
            key2:[len(r[1]) for r in res],
        }
        df = pd.DataFrame.from_dict(ret)
        df = df[[u'板块', key2]]
        summaryFolder = u'%s/板块分析/'%(outFolder)
        if not os.path.exists(summaryFolder):
            os.mkdir(summaryFolder)
        fileName = u'%s/%s.csv'%(summaryFolder,fName)
        print(fileName)
        df.to_csv(fileName,encoding="utf_8_sig", index=False)
    
    

    
    def __mergeFiles(self,folder_src,fName, filterName,folder_dest):
        datas = []
        filenames=os.listdir(folder_src)
        for f in filenames:
            if f.find('.csv') == -1:
                continue
            fullPath = os.path.join(folder_src, f)
            df = pd.read_csv(fullPath, index_col = 0, encoding='utf_8_sig')
            datas.append(df)
        res = pd.concat(datas, axis=1,join='outer',sort=False)
        res = res.fillna(0)
        fileName = '%s/merged_%s_%s.csv'%(folder_dest, fName,filterName)
        print(fileName)
        res.to_csv(fileName,encoding='utf_8_sig')

    ########### public method #######################
    def readFromCSV(self, fileName):
        df = pd.read_csv(fileName, index_col = None, encoding='utf_8_sig')
        stocks =  self.__splictToItems(df)
        self.__stocks = stocks
        return stocks
    
    def saveToCSV(self,fileName, stocks):
        df = self.__formatResultToDataFrame(stocks)
        df.to_csv(fileName,encoding="utf_8_sig", index=False)
        
    def stockPreprocess(self, fileName):
        '''
        预处理，将下载的数据存成CSV 格式
        '''
        fName = fileName[fileName.rfind('/')+1: fileName.rfind('.')]
        OutData = self.GetOutDataFolder(fileName)

        outFileName = '%s/%s.csv' %(OutData,fName)
        df = self.__readfromHTM(fileName)
        self.__splictToItems(df)
        self.saveToCSV(outFileName, self.__stocks)
        
    def printStockWithKey(self, **params):
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
    
    def AnalysisOneFileWithFilter(self, fileName, filter_):
        fName = fileName[fileName.rfind('/')+1: fileName.rfind('.')]
        if self.__stocks == None:
            self.stockPreprocess(fileName)
            
        # get filter result
        filterRes = [stock for stock in self.__stocks if filter_.filterBy(stock)]
         
        # get ban kuai result
        outFolder = self.GetAnalysisDataFolderWithFilterName(fileName, filter_.filterName)
        self.__get_BanKuai_Result(filterRes, fName,outFolder)
        
        # merge result
        folder_src = self.GetAnalysisBanKuaiFolderWithFilter(fileName, filter_.filterName)
        self.__mergeFiles(folder_src, fName, filter_.filterName, outFolder)
    
    def ReadFromCSVAndFilter(self, csvFile, filter_):
        fName = csvFile[csvFile.rfind('/')+1: csvFile.rfind('.')]
        self.readFromCSV(csvFile)
        # get filter result
        filterRes = [stock for stock in self.__stocks if filter_.filterBy(stock)]
         
        # get ban kuai result
        outFolder = self.GetAnalysisDataFolderWithFilterName(csvFile, filter_.filterName)
        self.__get_BanKuai_Result(filterRes, fName,outFolder)
        
        # merge result
        folder_src = self.GetAnalysisBanKuaiFolderWithFilter(csvFile, filter_.filterName)
        self.__mergeFiles(folder_src, fName, filter_.filterName, outFolder)
    
    def FilterBy(self, stocks, filter_):
        res = []
        for stock in stocks:
            if filter_.filterBy(stock):
                res.append(stock)
        return res
    
    def GetBanKuaiResult(self, stocks, fName, filterName):
        #get ban kuai result
        outFolder = self.GetAnalysisDataFolderWithFilterName(fileName, filterName)
        self.__get_BanKuai_Result(stocks, fName,filterName,outFolder)
        
    
    def MergeResult(self, fileName, filteName):
        # merge result
        fName = fileName[fileName.rfind('/')+1: fileName.rfind('.')]
        folder_src = self.GetAnalysisBanKuaiFolderWithFilter(fileName, filteName)
        outFolder = self.GetAnalysisDataFolderWithFilterName(fileName, filteName)
        self.__mergeFiles(folder_src, fName, filteName, outFolder)
        
if __name__ == '__main__':
    fileName = u'/Volumes/Data/StockAssistant/stockAnalysis/data/RawData/2019-04-20.xls'
    mgr = CStockMgr()
    mgr.stockPreprocess(fileName)
    #mgr.readFromCSV(outFileName)