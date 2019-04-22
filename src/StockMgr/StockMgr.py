'''
Created on Apr 16, 2019

@author: mac
'''
import pandas as pd
from Stock import StockItemDefine
import os
from StockMgr.StockMgrBase import CStockMgrBase

class CStockMgr(CStockMgrBase): 
    #######################static method########################
    def GetOutDataFolder(self,fileName):
        path = fileName[:fileName.rfind('/')+1]
        outData = u'%s/../OutData' % (path)
        if not os.path.exists(outData):
            os.mkdir(outData)
        return outData
    
    def GetAnalysisDataFolder(self,fileName):
        path = fileName[:fileName.rfind('/')+1]
        analysisData = u'%s/../AnalysisData' % (path)
        if not os.path.exists(analysisData):
            os.mkdir(analysisData)
        return analysisData
    
    def GetAnalysisDataFolderWithFilterName(self,fileName,filterName):
        path = fileName[:fileName.rfind('/')+1]
        analysisData = u'%s/../AnalysisData/%s' % (path,filterName)
        if not os.path.exists(analysisData):
            os.makedirs(analysisData)
        return analysisData
    
    def GetAnalysisBanKuaiFolderWithFilter(self,fileName,filterName):
        path = fileName[:fileName.rfind('/')+1]
        banKuaiFolder = u'%s/../AnalysisData/%s/板块分析/' % (path,filterName)
        if not os.path.exists(banKuaiFolder):
            os.makedirs(banKuaiFolder)
        return banKuaiFolder
    
    #######################private method ##########################
    def __init__(self):
        CStockMgrBase.__init__(self)
    
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
        
    def __getStocksWithExceptBanKuai(self,stocks, exceptBanKuai):
        if exceptBanKuai == None or len(exceptBanKuai) == 0:
            return stocks
        
        res = []
        for stock in stocks:
            if not stock.isOneKeyIn(exceptBanKuai) :
                res.append(stock)
            else:
                print(stock.stockInfo[StockItemDefine.stock_ID],stock.stockInfo[StockItemDefine.stock_GaiNian])
        return res
                

    ########### public method #######################
    
    def AnalysisOneFileWithFilter(self, fileName, filter_, exceptBanKuai = ()):
        fName = fileName[fileName.rfind('/')+1: fileName.rfind('.')]
        if self.__stocks == None:
            self.stockPreprocess(fileName)
        
        #Except Ban Kuai Data
        stocksWithExcept = self.__getStocksWithExceptBanKuai(self.stocks, exceptBanKuai)
        
        # get ban kuai statics
        outFolder = self.GetAnalysisDataFolderWithFilterName(fileName, filter_.filterName)
        self.__get_BanKuai_Result(stocksWithExcept, '板块统计',outFolder)
        
        # get filter result
        filterRes = [stock for stock in stocksWithExcept if filter_.filterBy(stock)]
         
        # get ban kuai result
        outFolder = self.GetAnalysisDataFolderWithFilterName(fileName, filter_.filterName)
        self.__get_BanKuai_Result(filterRes, fName,outFolder)
        
        # merge result
        folder_src = self.GetAnalysisBanKuaiFolderWithFilter(fileName, filter_.filterName)
        self.__mergeFiles(folder_src, fName, filter_.filterName, outFolder)
    
    def ReadFromCSVAndFilter(self, csvFile, filter_, exceptBanKuai = ()):
        fName = csvFile[csvFile.rfind('/')+1: csvFile.rfind('.')]
        self.readFromCSV(csvFile)
        
        #Except Ban Kuai Data
        stocksWithExcept = self.__getStocksWithExceptBanKuai(self.stocks, exceptBanKuai)
        
        # get ban kuai statics
        outFolder = self.GetAnalysisDataFolderWithFilterName(csvFile, filter_.filterName)
        self.__get_BanKuai_Result(stocksWithExcept, '板块统计',outFolder)
        
        # get filter result
        filterRes = [stock for stock in stocksWithExcept if filter_.filterBy(stock)]
         
        # get ban kuai result
        outFolder = self.GetAnalysisDataFolderWithFilterName(csvFile, filter_.filterName)
        self.__get_BanKuai_Result(filterRes, fName,outFolder)
        
        # merge result
        folder_src = self.GetAnalysisBanKuaiFolderWithFilter(csvFile, filter_.filterName)
        self.__mergeFiles(folder_src, fName, filter_.filterName, outFolder)
        
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
        
    def GetStocksWithExceptBanKuai(self, fileName, exceptBanKuai):
        self.readFromCSV(fileName)
        self.__getStocksWithExceptBanKuai(self.__stocks, exceptBanKuai)
        
if __name__ == '__main__':
    fileName = u'/Volumes/Data/StockAssistant/stockAnalysis/data/OutData/2019-04-19.csv'
    mgr = CStockMgr()
    #mgr.stockPreprocess(fileName)
    #mgr.readFromCSV(fileName)
    mgr.GetStocksWithExceptBanKuai(fileName, ('车联网',))
    #mgr.readFromCSV(outFileName)