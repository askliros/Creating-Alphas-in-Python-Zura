# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:34:38 2020

@author: aris_
"""
import os
os.getcwd()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
os.chdir('.\\SHARADARStockPrices10Years')
df=pd.read_csv('SHARADARStockPrices10Years.csv')
df['ticker']=df['ticker'].str.upper()
# CCCL=df[df['ticker']=='CCCL']
# CCCL.loc[CCCL['date']=='2010-01-11']
# CCCL.loc[CCCL['date']=='2010-12-01']
# CCC=CCCL.loc[CCCL['date'].sort_values().iloc[:10].index]
# CCC.loc[CCC['date']=='2010-01-12']

path = os.chdir('..\\GICSFundamentals')
pathstr='.\\GICSFundamentals\\'
files = os.listdir(path)
dataFundamentals= pd.read_csv(pathstr+files[0])
Classification=dataFundamentals[["ticker","sector","industry"]]
Classification.dropna(inplace=True)



dfClass=df.join(Classification.set_index('ticker'), on='ticker')

# CCCL=dfClass[dfClass['ticker']=='CCCL']
# CCCL.loc[CCCL['date']=='2010-01-11']
# CCCL.loc[CCCL['date']=='2010-12-01']
# CCC=CCCL.loc[CCCL['date'].sort_values().iloc[:10].index]
# CCC.loc[CCC['date']=='2010-01-12']


#dfClass[['Open','ticker','industry','sector']].tail(10)
dfClass.drop_duplicates(inplace=True)


# CCCL=dfClass[dfClass['ticker']=='CCCL']
# CCCL.loc[CCCL['date']=='2010-01-11']
# CCCL.loc[CCCL['date']=='2010-12-01']
# CCC=CCCL.loc[CCCL['date'].sort_values().iloc[:10].index]
# CCC.loc[CCC['date']=='2010-01-12']

os.chdir('..\\DailyFundamentals')
OtherFundamentals=pd.read_csv('DailyFundamentals.csv')


OF=OtherFundamentals[['ticker', 'date','marketcap']]

# OFCCCL=OF[OF['ticker']=='CCCL']
# OFCCCL.loc[OFCCCL['date']=='2010-01-10']

OFWanted=OF.loc[OF['date']>='2010-01-04']

#dfClassFinal=dfClass.join(OFWanted.set_index('ticker'), on='ticker')

dfClassFinal=dfClass.merge(OFWanted,how='left',on=['ticker', 'date'])
#dfClassFinal=dfClass.merge(OFWanted,on=['ticker'])
dfClassFinal.fillna(method='ffill',inplace=True)


# CCCL=dfClassFinal[dfClassFinal['ticker']=='CCCL']
# CCCL.loc[CCCL['date']=='2010-01-11']
# CCCL.loc[CCCL['date']=='2010-12-01']
# CCC=CCCL.loc[CCCL['date'].sort_values().iloc[:10].index]
# CCC.loc[CCC['date']=='2010-01-12']

os.chdir('..')

OpenStock=dfClassFinal[["ticker","date","open"]]
OpenStock=OpenStock.pivot_table(values='open',index='date',columns='ticker').fillna(0)
CloseStock=dfClassFinal[["ticker","date","close"]]
CloseStock=CloseStock.pivot_table(values='close',index='date',columns='ticker').fillna(0)
HighStock=dfClassFinal[["ticker","date","high"]]
HighStock=HighStock.pivot_table(values='high',index='date',columns='ticker').fillna(0)
LowStock=dfClassFinal[["ticker","date","low"]]
LowStock=LowStock.pivot_table(values='low',index='date',columns='ticker').fillna(0)
VolumeStock=dfClassFinal[["ticker","date","volume"]]
VolumeStock=VolumeStock.pivot_table(values='volume',index='date',columns='ticker').fillna(0)
# OpenInterestStock=dfClassFinal[["ticker","date","OpenInt"]]
# OpenInterestStock=OpenInterestStock.pivot_table(values='OpenInt',index='date',columns='ticker').fillna(0)
MarketCapStock=dfClassFinal[["ticker","date","marketcap"]]
MarketCapStock=MarketCapStock.pivot_table(values='marketcap',index='date',columns='ticker').fillna(0)
IndustryStock=dfClassFinal[["ticker","date","industry"]]
IndustryStock=IndustryStock.pivot_table(values='industry',index='date',columns='ticker',aggfunc='first').fillna(0)
SectorStock=dfClassFinal[["ticker","date","sector"]]
SectorStock=SectorStock.pivot_table(values='sector',index='date',columns='ticker',aggfunc='first').fillna(0)

#os.chdir('C:\\Users\\aris_\\AlphaDevelopment')

OpenStock.to_csv("OpenStock2.csv")
CloseStock.to_csv("CloseStock2.csv")
HighStock.to_csv("HighStock2.csv")
LowStock.to_csv("LowStock2.csv")
VolumeStock.to_csv("VolumeStock2.csv")
MarketCapStock.to_csv("MarketCapStock2.csv")
IndustryStock.to_csv("IndustryStock2.csv")
#IndustryStock.apply(lambda x: pd.unique(x).tolist().remove(0))
SectorStock.to_csv("SectorStock2.csv")
#SectorStock.apply(lambda x: pd.unique(x).tolist().remove(0))

#IndustryStock['AA'].unique().tolist().remove(0)

class PandasProcessing:
    def __init__(self,df):
        self.df=df        
    def GetUnique(self,col):
        theUnique=self.df.iloc[:,col].unique().tolist()
        if(0 in theUnique)  :
            theUnique.remove(0)
        return theUnique[0]
    def ReturnUniqueValues(self):
        self.UniqueDictionary={}
        for col in range(0,self.df.shape[1]):
            self.UniqueDictionary[self.df.columns[col]]=self.GetUnique(col)
    

PP=PandasProcessing(SectorStock)
PP.GetUnique(4)
PP.ReturnUniqueValues()
StockSectorDictionary=PP.UniqueDictionary
column_namesSector = set(StockSectorDictionary.values())
AdjacencyMatrixStockSector=pd.DataFrame(np.zeros((len(StockSectorDictionary.keys()),len(column_namesSector))))
AdjacencyMatrixStockSector.columns=column_namesSector
AdjacencyMatrixStockSector.index=StockSectorDictionary.keys()
for  kkk in StockSectorDictionary.keys():    
    AdjacencyMatrixStockSector.loc[kkk,StockSectorDictionary[kkk]]=1
AdjacencyMatrixStockSector.to_csv("AdjacencyMatrixStockSector.csv")    

PP2=PandasProcessing(IndustryStock)
PP2.GetUnique(4)
PP2.ReturnUniqueValues()
StockIndustryDictionary=PP2.UniqueDictionary
column_namesIndustry = set(StockIndustryDictionary.values())
AdjacencyMatrixStockIndustry=pd.DataFrame(np.zeros((len(StockIndustryDictionary.keys()),len(column_namesIndustry))))
AdjacencyMatrixStockIndustry.columns=column_namesIndustry
AdjacencyMatrixStockIndustry.index=StockIndustryDictionary.keys()
for  kkk in StockIndustryDictionary.keys():    
    AdjacencyMatrixStockIndustry.loc[kkk,StockIndustryDictionary[kkk]]=1
AdjacencyMatrixStockIndustry.to_csv("AdjacencyMatrixStockIndustry.csv")    





