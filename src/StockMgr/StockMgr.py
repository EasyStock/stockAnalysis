'''
Created on Apr 16, 2019

@author: mac
'''
import pandas as pd
from Stock import StockItemDefine
from Stock import StockItem
import os

class CStockMgr(object):
    def __init__(self):
        self._rawStocks = None
        
    def ReadfromHTM(self, fileName):
        dfs = pd.read_html(fileName,encoding='utf-8', header = 0)
        df =dfs[0]
        for index in range(len(df.columns)):
            print(index, df.columns[index])
#         path = fileName[:fileName.rfind('/')+1]
#         fName = fileName[fileName.rfind('/')+1: fileName.rfind('.')]
#         newName = u'%s/%s.csv'%(path,fName)
#         df.to_csv(newName,encoding="utf_8_sig", index=False)
        return df
    
    def SplictToItems(self, df):
        stocks = []
        for _, row in df.iterrows():
            stock = self.FormatToStockItem(row)
            stocks.append(stock)
        
        return stocks
    
    def FormatToStockItem(self, row_item):
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
        item_info[StockItemDefine.stock_XinHao] = row_item[23]
        item_info[StockItemDefine.stock_XinTai] = row_item[24]
        item_info[StockItemDefine.stock_Days] = row_item[25]
        
        item = StockItem.CStockItem()
        item.initWithDict(item_info)
        return item
    
    def SaveToCSV(self,fileName, stocks):
        df = self.FormatResultToDataFrame(stocks)
        df.to_csv(fileName,encoding="utf_8_sig", index=False)
        

    def mergeFiles(self,folder_src,fName, filterName,folder_dest):
        datas = []
        filenames=os.listdir(folder_src)
        for f in filenames:
            fullPath = os.path.join(folder_src, f)
            df = pd.read_csv(fullPath, index_col = 0, encoding='utf_8_sig')
            datas.append(df)
        res = pd.concat(datas, axis=1,join='outer',sort=False)
        res = res.fillna(0)
        fileName = '%s/%s_%s_Result.csv'%(folder_dest, fName,filterName)
        print(fileName)
        res.to_csv(fileName,encoding='utf_8_sig')

    def AnalyzerBanKuaiStocks(self, stocks):
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
    
    def FormatResultToDataFrame(self, stocks):
        stockList = [t.formatToDict() for t in stocks]
        columns = stocks[0].getColunmInfo()
        d = pd.DataFrame(stockList,columns=columns)
        return d
    
    def _Read_Splict_Save(self, fileName, outFileName):
        df = self.ReadfromHTM(fileName)
        stocks = self.SplictToItems(df)
        self.SaveToCSV(outFileName, stocks)
        return stocks
    
    def _Get_BanKuai_Result(self, stocks, fName,filterName, outFolder):
        mapOfResult = self.AnalyzerBanKuaiStocks(stocks)
        
        res = sorted(mapOfResult.items(), key=lambda d:len(d[1]), reverse = True)
        key2 = u'%s' %(fName)
        ret ={
            u'板块':[r[0] for r in res],
            key2:[len(r[1]) for r in res],
        }
        df = pd.DataFrame.from_dict(ret)
        df = df[[u'板块', key2]]
        summaryFolder = u'%s/summary/'%(outFolder)
        if not os.path.exists(summaryFolder):
            os.mkdir(summaryFolder)
        fileName = u'%s/%s.csv'%(summaryFolder,fName)
        print(fileName)
        df.to_csv(fileName,encoding="utf_8_sig", index=False)
        self.mergeFiles(summaryFolder,fName, filterName,outFolder)
    
    def AnalysisOneFileWithFilter(self,fileName, filter_):
        fName = fileName[fileName.rfind('/')+1: fileName.rfind('.')]
        path = fileName[:fileName.rfind('/')+1]
        outFolder = u'%s/../%s/' % (path, filter_.filterName)
        if not os.path.exists(outFolder):
            os.mkdir(outFolder)
        
        DailyFolder = u'%s/DailyFile' %(outFolder)
        csvFileName = u'%s/%s.csv'%(DailyFolder,fName)
        if not os.path.exists(DailyFolder):
            os.mkdir(DailyFolder)
            
        if self._rawStocks == None:
            self._rawStocks = self._Read_Splict_Save(fileName, csvFileName)
            
        print(csvFileName)
        # get filter result
        filterRes = [stock for stock in self._rawStocks if filter_.filterBy(stock)]
        
        # get ban kuai result
        self._Get_BanKuai_Result(filterRes, fName,filter_.filterName,outFolder)
        print('\n\r')
        
    def PrintStockWithKey(self, keyword):
        for stock in self._rawStocks:
            if stock.isKeyIn(keyword):
                print(stock)
    
        
if __name__ == '__main__':
    fileName = u'/Volumes/Data/Downloads/2019-04-17.xls'
    mgr = CStockMgr()
    pd.set_option('display.max_columns', None)
    df = mgr.ReadfromHTM(fileName)
    stocks = mgr.SplictToItems(df)
    print(stocks[5])
    fileName = u'/Volumes/Data/Downloads/aa.csv'
    mgr.SaveToCSV(fileName, stocks)