# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 14:11:55 2020

@author: aris_
"""
import os
os.getcwd()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class ProcessData:
    def __init__(self,OpenFile,CloseFile,HighFile,LowFile,VolumeFile,MarketCapFile,IndustryFile,SectorFile,AdjacencyMatrixStockSectorFile,AdjacencyMatrixStockIndustryFile): #,OpenInterestFile
        self.OpenFile=OpenFile
        self.CloseFile=CloseFile       
        self.HighFile=HighFile
        self.LowFile=LowFile
        self.VolumeFile=VolumeFile
        #self.OpenInterestFile=OpenInterestFile
        self.MarketCapFile=MarketCapFile
        self.IndustryFile=IndustryFile
        self.SectorFile=SectorFile
        self.AdjacencyMatrixStockSectorFile=AdjacencyMatrixStockSectorFile
        self.AdjacencyMatrixStockIndustryFile=AdjacencyMatrixStockIndustryFile
    def GetData(self):
        self.Open=pd.read_csv(self.OpenFile)
        self.Close=pd.read_csv(self.CloseFile)
        self.High=pd.read_csv(self.HighFile)
        self.Low=pd.read_csv(self.LowFile)
        self.Volume=pd.read_csv(self.VolumeFile)
        #self.OpenInterest=pd.read_csv(self.OpenInterestFile)
        self.MarketCap=pd.read_csv(self.MarketCapFile)
        self.Industry=pd.read_csv(self.IndustryFile)
        self.Sector=pd.read_csv(self.SectorFile)
        #self.Sector=self.Sector.pivot_table(values='sector',index='Date',columns='ticker',aggfunc='first').fillna(0)
        self.AdjacencyMatrixStockSector=pd.read_csv(self.AdjacencyMatrixStockSectorFile)
        self.AdjacencyMatrixStockIndustry=pd.read_csv(self.AdjacencyMatrixStockIndustryFile)
        self.Prices=self.Close.copy()
    def CreatingReturns(self,PeriodOfReturns):        
        CloseLog=self.Close.copy()
        CloseLog.iloc[:,1:].applymap( lambda x:0)
        CloseLog.iloc[:,1:]=self.Close.iloc[:,1:].applymap(np.log)
        CloseLog.replace([np.inf, -np.inf], 0,inplace=True)
        CloseLog.replace(np.nan, 0,inplace=True)
        CloseLog.iloc[:PeriodOfReturns,:]=0
        
        CloseLag=self.Close.shift(PeriodOfReturns)
        CloseLagLog=CloseLag.copy()
        CloseLagLog.iloc[:,1:].applymap( lambda x:0)
        CloseLagLog.iloc[:,1:]=CloseLag.iloc[:,1:].applymap(np.log)
        CloseLagLog.replace([np.inf, -np.inf], 0,inplace=True)
        CloseLagLog.replace(np.nan, 0,inplace=True)
        CloseLagLog.iloc[0,:]=0
        
        Returns=self.Close.copy()
        Returns.iloc[:,1:].applymap( lambda x:0)
        Returns.iloc[:,1:]=CloseLog.iloc[:,1:]-CloseLagLog.iloc[:,1:]
        Returns.replace([np.inf, -np.inf], 0)
        self.Returns=Returns
        return Returns
       
        
class Alpha:
    def __init__(self,ProcessData,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading):
        self.ProcessData=ProcessData
        #self.ProcessData.GetData()
        self.Prices=self.ProcessData.Prices
        self.Open=self.ProcessData.Open
        self.High=self.ProcessData.High
        self.Low=self.ProcessData.Low
        self.Volume=self.ProcessData.Volume
        self.MarketCap=self.ProcessData.MarketCap
        #self.OpenInterest=self.ProcessData.OpenInterest
        self.Close=self.ProcessData.Close
        self.Industry=self.ProcessData.Industry
        self.Sector=self.ProcessData.Sector
        self.AdjacencyMatrixStockSector=self.ProcessData.AdjacencyMatrixStockSector
        self.AdjacencyMatrixStockSector.index=self.AdjacencyMatrixStockSector.iloc[:,0]
        self.AdjacencyMatrixStockSector=self.AdjacencyMatrixStockSector.iloc[:,1:]
        self.AdjacencyMatrixStockIndustry=self.ProcessData.AdjacencyMatrixStockIndustry
        self.AdjacencyMatrixStockIndustry.index=self.AdjacencyMatrixStockIndustry.iloc[:,0]
        self.AdjacencyMatrixStockIndustry=self.AdjacencyMatrixStockIndustry.iloc[:,1:]
        self.NumberOfStocksTrading=NumberOfStocksTrading
        self.TradingFrequency=TradingFrequency
        self.TransactionCosts=TransactionCosts        
        self.TotalAmount=TotalAmount
        self.startDate=startDate
        self.TheAlpha=(self.Prices.copy())
        self.TheAlpha.iloc[:,1:]=0*self.TheAlpha.iloc[:,1:]
        
    def FillingZeros(self):
        for kkk in range(0,self.Close.shape[1]):
            #print(kkk)
            IndexClose=np.where(self.Close.iloc[:,kkk])
            if(len(IndexClose[0])>0):
                IndexCloseFirst=IndexClose[0][0]
                IndexCloseLast=IndexClose[0][-1]
                self.Close.iloc[IndexCloseFirst:IndexCloseLast+1,kkk].replace(0,method='ffill',inplace=True)
            IndexOpen=np.where(self.Open.iloc[:,kkk])
            if(len(IndexOpen[0])>0):
                IndexOpenFirst=IndexOpen[0][0]
                IndexOpenLast=IndexOpen[0][-1]
                self.Open.iloc[IndexOpenFirst:IndexOpenLast+1,kkk].replace(0,method='ffill',inplace=True)
            IndexHigh=np.where(self.High.iloc[:,kkk])
            if(len(IndexHigh[0])>0):
                IndexHighFirst=IndexHigh[0][0]
                IndexHighLast=IndexHigh[0][-1]
                self.High.iloc[IndexHighFirst:IndexHighLast+1,kkk].replace(0,method='ffill',inplace=True)
            IndexLow=np.where(self.Low.iloc[:,kkk])
            if(len(IndexLow[0])>0):
                IndexLowFirst=IndexLow[0][0]
                IndexLowLast=IndexLow[0][-1]
                self.Low.iloc[IndexLowFirst:IndexLowLast+1,kkk].replace(0,method='ffill',inplace=True)
            IndexVolume=np.where(self.Volume.iloc[:,kkk])
            if(len(IndexVolume[0])>0):
                IndexVolumeFirst=IndexVolume[0][0]
                IndexVolumeLast=IndexVolume[0][-1]
                self.Volume.iloc[IndexVolumeFirst:IndexVolumeLast+1,kkk].replace(0,method='ffill',inplace=True)
            if(kkk>=self.MarketCap.shape[1]) :
                pass
            else:
                IndexMarketCap=np.where(self.MarketCap.iloc[:,kkk])            
                if(len(IndexMarketCap[0])>0):
                    IndexMarketCapFirst=IndexMarketCap[0][0]
                    IndexMarketCapLast=IndexMarketCap[0][-1]
                    self.MarketCap.iloc[IndexMarketCapFirst:IndexMarketCapLast+1,kkk].replace(0,method='ffill',inplace=True)

        
    def Rank(self,Row):
        RowMax=Row.abs().max()
        if(RowMax==0):
            return Row
        else:
            Row=(1.0/(2.0*RowMax))*Row
            Kpos=np.where(Row>0)
            Kpos=Kpos[0]
            Kneg=np.where(Row<0)
            Kneg=Kneg[0]
            Row.iloc[Kpos]=(0.5/Row.iloc[Kpos].max())*Row.iloc[Kpos]
            Row.iloc[Kneg]=(0.5/Row.iloc[Kneg].abs().max())*Row.iloc[Kneg]
            Row=Row+0.5
            return Row
    
    def TSRank(self,Data):
        Value=(Data.iloc[-1,:]/(2*Data.abs().max()))+0.5
        return Value
    
    def History(self,Days,Variable):
        self.History0=Variable.iloc[slice(self.dateIndex-Days*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
              
        Value=self.History0.copy()
        return Value
    
    def Correl(self,Value1,Value2,Days):
        HistoryValue1=self.History(Days,Value1)
        HistoryValue2=self.History(Days,Value2)
        Value=0*HistoryValue1.iloc[-1,:].copy()
        
            
        Value= HistoryValue1.corrwith(HistoryValue2,axis=0)
        return Value
    def Covar(self,Value1,Value2,Days):
        HistoryValue1=self.History(Days,Value1)
        HistoryValue2=self.History(Days,Value2)
        Value=0*HistoryValue1.iloc[-1,:].copy()
        for kkk in range(1,HistoryValue1.shape[1]-1):
            Value.iloc[kkk]= HistoryValue1.iloc[:,kkk].cov(HistoryValue2.iloc[:,kkk])
        return Value
    def TSMin(self,Value1,Days):
        HistoryValue1=self.History(Days,Value1)        
        Value=0*HistoryValue1.iloc[-1,:].copy()        
        Value= HistoryValue1.min()
        return Value   
    
    def TSMax(self,Value1,Days):
        HistoryValue1=self.History(Days,Value1)        
        Value=0*HistoryValue1.iloc[-1,:].copy()       
        Value= HistoryValue1.max()
        return Value  
    
    def TSSTD(self,Value1,Days):
        HistoryValue1=self.History(Days,Value1)        
        Value=0*HistoryValue1.iloc[-1,:].copy()      
        Value= HistoryValue1.std()
        return Value  
    
    def TSMean(self,Value1,Days):
        HistoryValue1=self.History(Days,Value1)        
        Value=0*HistoryValue1.iloc[-1,:].copy()      
        Value= HistoryValue1.mean()
        return Value 
    
    def TSArgMin(self,Value1,Days):
        HistoryValue1=self.History(Days,Value1)        
        Value=0*HistoryValue1.iloc[-1,:].copy()
        Value= HistoryValue1.idxmin()
        return Value 
    
    def TSArgMax(self,Value1,Days):
        HistoryValue1=self.History(Days,Value1) 
        print(Days)
        print(HistoryValue1)
        if(HistoryValue1.shape[0]>0):
            Value=0*HistoryValue1.iloc[-1,:].copy()        
            Value= HistoryValue1.idxmax()
        else:
            Value=0*self.ProcessData.Returns.iloc[-1,:].copy()  
        return Value 
    
    def TSSum(self,Value1,Days):
        HistoryValue1=self.History(Days,Value1)        
        Value=0*HistoryValue1.iloc[-1,:].copy()        
        Value= HistoryValue1.sum()
        return Value 
    
    def TSProd(self,Value1,Days):
        HistoryValue1=self.History(Days,Value1)        
        Value=0*HistoryValue1.iloc[-1,:].copy()       
        Value= HistoryValue1.prod()
        return Value 
    
    def Scale(self,Value):
        SumValue=Value.abs().sum()
        return (1.0/SumValue)*Value
    
    def Delta(self,Value,Lag):
        return Value.iloc[self.dateIndex,1:]-Value.iloc[self.dateIndex-Lag,1:]
    
    def Log(self,Value):
        Value=Value.astype('float32').apply(np.log).fillna(0)
        return Value
    
    def Sign(self,Value):
        Value=Value.apply(np.sign)
        return Value
    
        
    def Power(self,Value,power):
        Value=Value.apply(lambda x: np.power(x, power))
        return Value
    
    def TSLinearDecay(self,Value,Days):
        return Value.ewm(span=Days).mean().iloc[-1]
    
    
        
        
    def PrepareAlpha(self,dateIndex, TotalAvailable):
        #Finding the top Market Cap Stocks
        if(self.NumberOfStocksTrading<np.count_nonzero(self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:])):
            self.MarketCapToday=self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:].sort_values(ascending=False).iloc[:self.NumberOfStocksTrading]
            self.Value[self.Value.index.difference(self.MarketCapToday.keys())]=0
        else:
            self.MarketCapToday=self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:].loc[self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:]>0]
            ##print(self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:])
            self.Value.iloc[np.where(self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:]==0)]=0
            
            
        # #print("Top Market Cap Stocks")
        # #print(self.MarketCapToday)
        #Trading only the stocks which fall into the Top Market Cap Range
        #self.Value[self.Value.index.difference(self.MarketCapToday.keys())]=0
        #Excluding short selling
        self.Value.loc[self.Value<0]=0
        #Normalising the Alpha
        if(self.Value.sum()==0):
            pass
        else:
            self.Value=(1.0/self.Value.sum())*self.Value
            self.Value=self.Value*TotalAvailable
        # #print("The Alpha is:")
        # #print(self.Value)
        # #print("That was the Alpha")
    def PrepareAlpha2(self,dateIndex, TotalAvailable):
        #Finding the top Market Cap Stocks        
        if(self.NumberOfStocksTrading<np.count_nonzero(self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:])):
            self.MarketCapToday=self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:].sort_values(ascending=False).iloc[:self.NumberOfStocksTrading]
            self.Value[self.Value.keys().difference(self.MarketCapToday.keys())]=0
        else:
            self.MarketCapToday=self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:].loc[self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:]>0]
            self.Value[self.Value.keys().difference(self.MarketCapToday.keys())]=0

        # #print("Top Market Cap Stocks")
        # #print(self.MarketCapToday)
        #Trading only the stocks which fall into the Top Market Cap Range
        ##s.loc[s.index.intersection(labels)].reindex(labels)
        ##print(self.Value.keys())
        ##print(self.Value.loc[self.Close.columns.difference(self.MarketCapToday.keys())])
        ##print(self.Close.columns.difference(self.MarketCapToday.keys()))
        #self.Value[self.Value.columns.difference(self.MarketCapToday.keys())]=0
        #Excluding short selling
        self.Value.iloc[0][self.Value.iloc[0]<0]=0
        #self.Value.loc[self.Value<0]=0    
        if(self.Value.sum(axis=1)[0]==0):
            pass
        else:
            self.Value=(1.0/self.Value.sum(axis=1)[0])*self.Value
            self.Value=self.Value*TotalAvailable
        # #print("The Alpha is:")
        # #print(self.Value)
        # #print("That was the Alpha")
    
    #Here we allow short-selling
    def PrepareAlphaNeut(self,dateIndex, TotalAvailable):
        #Finding the top Market Cap Stocks
        if(self.NumberOfStocksTrading<np.count_nonzero(self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:])):
            self.MarketCapToday=self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:].sort_values(ascending=False).iloc[:self.NumberOfStocksTrading]
            self.Value[self.Value.index.difference(self.MarketCapToday.keys())]=0
            #Neutralising Alpha
            self.Value[self.MarketCapToday.keys()]=self.Value[self.MarketCapToday.keys()]-self.Value[self.MarketCapToday.keys()].mean()          
            
        else:
            self.MarketCapToday=self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:].loc[self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:]>0]            
            self.Value.iloc[np.where(self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:]==0)]=0   
            #Neutralising Alpha
            self.Value.iloc[np.where(self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:]!=0)]=self.Value.iloc[np.where(self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:]!=0)]-self.Value.iloc[np.where(self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:]!=0)].mean()
        
        
        self.Value.fillna(value=0,inplace=True)
        #Normalising the Alpha
        if(self.Value.abs().sum()==0):
            pass
        else:
            self.Value=(1.0/self.Value.abs().sum())*self.Value
            self.Value=self.Value*TotalAvailable
        # #print("The Alpha is:")
        # #print(self.Value)
        # #print("That was the Alpha")
        
    def PrepareAlpha2Neut(self,dateIndex, TotalAvailable):
        #Finding the top Market Cap Stocks        
        if(self.NumberOfStocksTrading<np.count_nonzero(self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:])):
            self.MarketCapToday=self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:].sort_values(ascending=False).iloc[:self.NumberOfStocksTrading]
            self.Value[self.Value.keys().difference(self.MarketCapToday.keys())]=0
            #Neutralising Alpha
            self.Value[self.MarketCapToday.keys()]=self.Value[self.MarketCapToday.keys()]-self.Value[self.MarketCapToday.keys()].mean()         

        else:
            self.MarketCapToday=self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:].loc[self.MarketCap.iloc[dateIndex-self.TradingFrequency,1:]>0]
            self.Value[self.Value.keys().difference(self.MarketCapToday.keys())]=0
             #Neutralising Alpha
            self.Value[self.MarketCapToday.keys()]=self.Value[self.MarketCapToday.keys()]-self.Value[self.MarketCapToday.keys()].mean()          

        
        
        self.Value.fillna(value=0,inplace=True)
        if(self.Value.abs().sum()==0):
            pass
        else:
            self.Value=(1.0/self.Value.abs().sum())*self.Value
            self.Value=self.Value*TotalAvailable
        # #print("The Alpha is:")
        # #print(self.Value)
        # #print("That was the Alpha")
        
    def IndNeut2(self): 
        self.MarketCapToday=self.MarketCap.iloc[self.dateIndex-self.TradingFrequency,1:].sort_values(ascending=False).iloc[:self.NumberOfStocksTrading]
        self.K=self.AdjacencyMatrixStockIndustry.index.intersection(self.MarketCapToday.index)
        #setting the values of Alpha of stocks not belonging to any industry to 0
        Set0=(self.AdjacencyMatrixStockIndustry.index.symmetric_difference(self.MarketCapToday.index))
        Set00=Set0.intersection(self.MarketCapToday.index)
        self.Value[Set00]=0
        A=self.AdjacencyMatrixStockIndustry.loc[self.K]
        #drop the industries without representation
        A = A.loc[:, (A.sum(axis=0) >0)]
        AA=A.transpose().dot(A)
        AAinv=np.linalg.inv(AA)
        AAinv=pd.DataFrame(AAinv)
        AAinv.index=AA.index
        AAinv.columns=AA.columns
        V=(self.Value[self.K]).transpose()
        V=V-((A.dot(AAinv)).dot(A.transpose())).dot(V)
        VT=V.transpose()
        self.Value[self.K]=VT
        
    def IndSector2(self):  
        self.MarketCapToday=self.MarketCap.iloc[self.dateIndex-self.TradingFrequency,1:].sort_values(ascending=False).iloc[:self.NumberOfStocksTrading]
        self.K=self.AdjacencyMatrixStockSector.index.intersection(self.MarketCapToday.index)
        #setting the values of Alpha of stocks not belonging to any industry to 0
        Set0=(self.AdjacencyMatrixStockSector.index.symmetric_difference(self.MarketCapToday.index))
        Set00=Set0.intersection(self.MarketCapToday.index)
        self.Value[Set00]=0
        A=self.AdjacencyMatrixStockSector.loc[self.K]
        #drop the industries without representation
        A = A.loc[:, (A.sum(axis=0) >0)]
        AA=A.transpose().dot(A)
        AAinv=np.linalg.inv(AA)
        AAinv=pd.DataFrame(AAinv)
        AAinv.index=AA.index
        AAinv.columns=AA.columns
        V=(self.Value[self.K]).transpose()
        V=V-((A.dot(AAinv)).dot(A.transpose())).dot(V)
        VT=V.transpose()
        self.Value[self.K]=VT     
        
    def PCANeut2(self,NumberOfDays,NumberOfPCA):
        self.MarketCapToday=self.MarketCap.iloc[self.dateIndex-self.TradingFrequency,1:].sort_values(ascending=False).iloc[:self.NumberOfStocksTrading]
        self.K=self.MarketCapToday.index
        if(self.dateIndex>=NumberOfDays*self.TradingFrequency):
            SelectedReturns=self.TheAlphaReturns.loc[slice(self.dateIndex-NumberOfDays*self.TradingFrequency,self.dateIndex,self.TradingFrequency),self.K]
            Correlation=SelectedReturns.corr()
            from sklearn.decomposition import PCA
            pca_corr = PCA(n_components=3) 
            Correlation.fillna(value=0,inplace=True) 
            A=pca_corr.fit_transform(Correlation) 
            A=pd.DataFrame(A)  
            A.index=self.K
            AA=A.transpose().dot(A)
            AAinv=np.linalg.inv(AA)
            AAinv=pd.DataFrame(AAinv)
            AAinv.index=AA.index
            AAinv.columns=AA.columns
            V=(self.Value[self.K]).transpose()
            V=V-((A.dot(AAinv)).dot(A.transpose())).dot(V)
            VT=V.transpose()
            self.Value[self.K]=VT     
        else:
            pass
        
        
        
        
    
    def SetAlphaParameters(self):
        pass
    def GenerateAlpha(self):
        self.Value=0
    def __add__(self,other):
        return self.Value+other.Value
    def __sub__(self,other):
        return self.Value-other.Value
    def __mul__(self,other):
        return self.Value*other.Value
    def __pow__(self,other):
        return self.Value**other.Value
    

